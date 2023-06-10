import sys
from semantic_version import Version
from utils import (
    parse_version,
    is_version_within_range,
    get_minor_versions_in_range
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

    print("SCANNING THE FOLLOWING MINOR VERSIONS: ", minor_versions_to_scan)
    
    # Consolidate all update details into single upgrade
    all_changes = {}
    for version in minor_versions_to_scan:
        all_changes[version] = {}
        changelog_url = MINOR_VERSION_CHANGELOG_URL_TEMPLATE.format(version)
        all_releases_for_version = gather_markdown_sections_by_version(changelog_url)
        for release in all_releases_for_version:
            if is_version_within_range(release, lower_version, higher_version):
                all_changes[version][release] = parse_section(all_releases_for_version[release])

    total_upgrade = {
        'bug_fixes': [],
        'enhancements': [],
        'upgrade_notes': [],
        'new_features': [],
        'security_notes': [],
        'notes': [],
        'experiments': [],
        'breaking_changes': []
    }
    releases = 0
    for minor_version in all_changes:
        for release in all_changes[minor_version]:
            releases += 1
            for update_aspect in all_changes[minor_version][release]:
                if all_changes[minor_version][release][update_aspect]:
                    total_upgrade[update_aspect].extend(all_changes[minor_version][release][update_aspect])

    # Print quick summary table
    for aspect in total_upgrade:
        print(aspect, len(total_upgrade[aspect]))
    
    # Print all upgrade details
    for aspect in total_upgrade:
        header_text = aspect.replace('_', ' ').upper() + ': '
        print(header_text)
        for info in total_upgrade[aspect]:
            print(info)

    print("THIS UPGRADE SPANS A TOTAL OF {} releases".format(releases))

if __name__ == "__main__":
    main()