import re
from semantic_version import Version

def is_version_within_range(current, start_version, end_version):
    current_version = Version(current)
    if start_version < current_version <= end_version: return True
    return False

def get_minor_versions_in_range(start_version, end_version, minor_versions):

    spanned_versions = []

    for version in minor_versions:
        current = Version(version + '.0')

        if (start_version <= current <= end_version) or (start_version.major == current.major and start_version.minor == current.minor and current <= end_version):
            spanned_versions.append(version)

    return spanned_versions

def parse_version(version_str):
    # Pattern to match "<at_least_one_digit>.<at_least_one_digit>.<at_least_one_digit>"
    pattern_full = r'^(\d+)\.(\d+)\.(\d+)$'

    # Pattern to match "v<at_least_one_digit>.<at_least_one_digit>.<at_least_one_digit>"
    pattern_v_full = r'^v(\d+)\.(\d+)\.(\d+)$'

    # Pattern to match "<at_least_one_digit>.<at_least_one_digit>"
    pattern_minor = r'^(\d+)\.(\d+)$'

    # Pattern to match "v<at_least_one_digit>.<at_least_one_digit>"
    pattern_v_minor = r'^v(\d+)\.(\d+)$'

    # Check for the full version pattern
    match_full = re.match(pattern_full, version_str)
    match_v_full = re.match(pattern_v_full, version_str)

    if match_full:
        return Version(version_str)
    elif match_v_full:
        return Version(match_v_full.group(1, 2, 3))

    # Check for the minor version pattern
    match_minor = re.match(pattern_minor, version_str)
    match_v_minor = re.match(pattern_v_minor, version_str)

    if match_minor:
        return Version(f'{version_str}.0')
    elif match_v_minor:
        return Version(f'v{match_v_minor.group(1)}.{match_v_minor.group(2)}.0')

    raise ValueError(f'Invalid version format: {version_str}')