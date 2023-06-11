import sys
import json
import pyfiglet
from semantic_version import Version
from utils import (
    parse_version,
    is_version_within_range,
    get_minor_versions_in_range,
    print_terraform_updates
)
from changelog import (
    parse_minor_versions_from_root_changelog_markdown,
    gather_markdown_sections_by_version,
    parse_section
)

def main():

    ROOT_CHANGELOG_URL = "https://raw.githubusercontent.com/hashicorp/terraform/main/CHANGELOG.md"
    MINOR_VERSION_CHANGELOG_URL_TEMPLATE = "https://raw.githubusercontent.com/hashicorp/terraform/v{}/CHANGELOG.md"

    if len(sys.argv) != 3:
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
                all_changes[minor_version][release] = parse_section(all_releases_for_version[release])

    # print(all_changes)

    upgrade_aspects = [
        'breaking_changes',
        'upgrade_notes',
        'security_notes',
        'bug_fixes',
        'new_features',
        'enhancements',
        'notes',
        'experiments'
    ]

    # for minor_version in all_changes:
    #     for release in all_changes[minor_version]:
    #         for update_aspect in all_changes[minor_version][release]:
    #             if all_changes[minor_version][release][update_aspect]:
    #                 total_upgrade[update_aspect].extend(all_changes[minor_version][release][update_aspect])

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
                organized_upgrade[header][minor_version][release] = '\n'.join(f"* - {bulletpoint}" for bulletpoint in content)

    formatted_data = json.dumps(organized_upgrade)
    formatted_data = formatted_data.replace('{}', '"NONE FOUND"')
    # # formatted_data = formatted_data.replace('{\n', '').replace('\n}', '').replace('\\n', '\n').replace('\\"', '"').replace("{}", "NONE FOUND")
    header = pyfiglet.figlet_format("TERRAFORM UPGRADE SUMMARY", font='big')
    sub_header = f"(for versions {lower_version} -> {higher_version})\n"
    print(header, sub_header)
    print_terraform_updates(formatted_data)

    print("THIS UPGRADE SPANS A TOTAL OF {} releases".format(release_versions))

if __name__ == "__main__":
    main()