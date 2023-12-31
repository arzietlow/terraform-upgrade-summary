import sys
import json
import pyfiglet
import argparse
from tabulate import tabulate
from semantic_version import Version
from upgrade_summary.utils import (
    parse_version,
    is_version_within_range,
    get_minor_versions_in_range,
    print_terraform_updates
)
from upgrade_summary.changelog import (
    parse_minor_versions_from_root_changelog_markdown,
    gather_markdown_sections_by_version,
    parse_section,
    parse_section_verbose
)

def main():
    ROOT_CHANGELOG_URL = "https://raw.githubusercontent.com/hashicorp/terraform/main/CHANGELOG.md"
    MINOR_VERSION_CHANGELOG_URL_TEMPLATE = "https://raw.githubusercontent.com/hashicorp/terraform/v{}/CHANGELOG.md"

    # Set up arguments
    parser = argparse.ArgumentParser(description='Terraform upgrade summarizer')
    parser.add_argument('lower_version', help='Beginning version')
    parser.add_argument('higher_version', help='Ending version')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    args = parser.parse_args()
    parse_fn = parse_section_verbose if args.verbose else parse_section

    if not len(sys.argv) >= 3:
        print("Usage: python3 summarize_upgrade.py <lower_version> <higher_version>")
        return
    try:
        lower_version = parse_version(sys.argv[1])
        higher_version = parse_version(sys.argv[2])
    except ValueError as e:
        print(f'Error with input version(s): {e}')
        sys.exit(1)

    published_minor_versions = parse_minor_versions_from_root_changelog_markdown(ROOT_CHANGELOG_URL)
    minor_versions_to_scan = get_minor_versions_in_range(lower_version, higher_version, published_minor_versions)

    # print("SCANNING THE FOLLOWING MINOR VERSIONS: ", minor_versions_to_scan)
    
    # Consolidate all update details into single upgrade
    all_changes = {}
    release_versions = []
    for minor_version in minor_versions_to_scan:
        all_changes[minor_version] = {}
        changelog_url = MINOR_VERSION_CHANGELOG_URL_TEMPLATE.format(minor_version)
        all_releases_for_version = gather_markdown_sections_by_version(changelog_url)
        for release in all_releases_for_version:
            if is_version_within_range(release, lower_version, higher_version):
                release_versions.append(release)
                all_changes[minor_version][release] = parse_fn(all_releases_for_version[release]) # Calls either parse_section or parse_section_verbose

    # print(all_changes)

    upgrade_aspects = {
        'breaking_changes': [],
        'upgrade_notes': [],
        'security_notes': [],
        'bug_fixes': [],
        'new_features': [],
        'enhancements': [],
        'notes': [],
        'experiments': []
    }

    # Organize upgrade details
    organized_upgrade = {}
    for aspect in upgrade_aspects:
        header = aspect.upper().replace('_', ' ')
        organized_upgrade[header] = {}
        for release in release_versions:
            minor_version = '.'.join(release.split('.')[:2])
            content = all_changes[minor_version][release][aspect]
            if minor_version not in organized_upgrade[header]: 
                if content: organized_upgrade[header][minor_version] = {}
            if content: 
                organized_upgrade[header][minor_version][release] = '\n'.join(f"* - {bulletpoint}" if not bulletpoint.startswith('* ') else bulletpoint for bulletpoint in content)
                for bulletpoint in content:
                    if '* ' in bulletpoint:
                        upgrade_aspects[aspect].extend(bulletpoint.split('* '))
                    else: upgrade_aspects[aspect].append(bulletpoint)

    formatted_data = json.dumps(organized_upgrade)
    formatted_data = formatted_data.replace('{}', '"NONE FOUND"')
    header = pyfiglet.figlet_format("TERRAFORM UPGRADE SUMMARY", font='big')
    sub_header = f"(for versions {lower_version} -> {higher_version})\n"

    # PRINT OUTPUT 
    print(header, sub_header)
    summary_table_headers = ['UPGRADE ASPECT', 'COUNT']
    summary_table = []
    for aspect in upgrade_aspects:
        summary_table.append([aspect.replace('_', ' ').upper(), len(upgrade_aspects[aspect]) if len(upgrade_aspects[aspect]) != 0 else "NONE"])
    print(tabulate(summary_table, summary_table_headers, tablefmt="simple"), '\n')
    print("This upgrade spans a total of {} releases".format(len(release_versions)), '\n')
    print_terraform_updates(formatted_data)

if __name__ == "__main__":
    main()