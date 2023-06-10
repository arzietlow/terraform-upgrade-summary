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

    pattern = r'^(v)?(\d+)\.(\d+)(\.\d+)?$'

    # Check for the full version pattern
    match = re.match(pattern, version_str, re.IGNORECASE)

    if match:
        return Version(f'{match.group(2)}.{match.group(3)}.{match.group(4)[1:] if match.group(4) else "0"}')

    raise ValueError(f'Invalid version format: {version_str}')