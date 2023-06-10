import requests
import re

def parse_minor_versions_from_root_changelog_markdown(url):
    response = requests.get(url)
    content = response.text
    
    pattern = r'\[v(\d+\.\d+)\]'
    minor_versions = re.findall(pattern, content)
    
    return minor_versions

def get_minor_versions_in_range(start_version, end_version, minor_versions):
    start_major, start_minor, _ = map(int, start_version.split('.'))
    end_major, end_minor, _ = map(int, end_version.split('.'))
    
    spanned_versions = []
    
    for version in minor_versions:
        major, minor = map(int, version.split('.'))
        
        if (start_major == major):
            if (start_minor <= minor):
                spanned_versions.append(version)
        elif (start_major < major < end_major) or (start_major == major and start_minor <= minor) or (end_major == major and minor <= end_minor):
            spanned_versions.append(version)
    
    return spanned_versions

def gather_markdown_sections_by_version(url):
    """
    Parses out all sections from a single markdown file retrieved from a URL and returns them as a dictionary.

    Args:
        url (str): The URL of the markdown file.

    Returns:
        Dict[str, str]: A dictionary where the keys are version numbers (string) and
        the values are corresponding section contents (string) (markdown).
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        markdown_text = response.text

        # Remove the "(Unreleased)" section at the top
        markdown_text = re.sub(r'## \d+\.\d+\.\d+ \(Unreleased\)\s+', '', markdown_text)

        # Remove the "## Previous Releases" section
        markdown_text = re.sub(r'## Previous Releases[\s\S]*', '', markdown_text)

        # Use regex to find each header2 section
        pattern = r'## (\d+\.\d+\.\d+) \((.+?)\)\s+([\s\S]+?)(?=\n## \d+\.\d+\.\d+|$)'
        sections = re.findall(pattern, markdown_text)

        # Create a dictionary to store the sections
        sections_dict = {}
        for version, _, content in sections:
            sections_dict[version] = content.strip()

        return sections_dict

    except requests.exceptions.RequestException as e:
        print("Error occurred during the HTTP request:", e)
        return None
    
def parse_section(markdown_text):
    '''
        Parses a SECTION's Markdown text (corresponding to 1 released version of Terraform) and extracts different sections and bullet points from it.

        Args:
        markdown_text (str): The Markdown text to parse.

        Returns:
        dict: The parsed result containing different sections and their corresponding bullet points.
    '''

    result = {
        'bug_fixes': [],
        'enhancements': [],
        'upgrade_notes': [],
        'new_features': [],
        'security_notes': [],
        'notes': [],
        'experiments': [],
        'breaking_changes': []
    }

    headers = [
        'ENHANCEMENTS',
        'BUG FIXES',
        'UPGRADE NOTES',
        'NEW FEATURES',
        'SECURITY NOTES',
        'NOTES',
        'EXPERIMENTS',
        'BREAKING CHANGES'
    ]

    # Extract headers using regex
    pattern = r'(' + '|'.join(headers) + r')(.*?)(?=(?:' + '|'.join(headers) + r')|$)'
    sections = re.findall(pattern, markdown_text, re.DOTALL)

    # # Use regex to extract bugfixes and enhancements
    # pattern = r'(ENHANCEMENTS|BUG FIXES)(.*?)(?=(?:ENHANCEMENTS|BUG FIXES)|$)'
    # sections = re.findall(pattern, markdown_text, re.DOTALL)

    # Extract bullet points from each section
    for section in sections:
        section_name = section[0].strip()
        bullet_points = re.findall(r'\*\s+(.*)', section[1])
        if bullet_points:
            result_field = section_name.lower().replace(' ', '_')
            result[result_field] = bullet_points

    return result