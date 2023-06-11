import unittest
import json
from upgrade_summary.changelog import parse_section

class TestParseSection(unittest.TestCase):
    def test_parse_section(self):
        self.maxDiff = None
        markdown_text = '''
            ENHANCEMENTS:
            * Added support for feature X.
            * Improved performance.

            BUG FIXES:
            * Fixed issue with component Y.
            * Addressed security vulnerability.

            UPGRADE NOTES:
            * Please note the breaking changes in version 2.0.

            NEW FEATURES:
            * Introducing feature Z.
            * Added support for module ABC.

            SECURITY NOTES:
            * Improved authentication mechanisms.

            NOTES:
            * Some additional notes.

            EXPERIMENTS:
            * Experimental feature A is now available.

            BREAKING CHANGES:
            * Updated API endpoints.
            * Modified configuration format.

            UPGRADE NOTES AND BREAKING CHANGES:
            * Breaking change: Removed deprecated function B.
            * Breaking change: Updated library C to version 1.0.
            * Upgrade note: Please update your credentials.

            OTHER SECTION:
            * Some other bullet points.
        '''

        expected_result = {
            "bug_fixes": ["Fixed issue with component Y.\n            * Addressed security vulnerability."],
            "enhancements": ["Added support for feature X.\n            * Improved performance."],
            "upgrade_notes": ["Please note the breaking changes in version 2.0."],
            "new_features": ["Introducing feature Z.\n            * Added support for module ABC."],
            "security_notes": ["Improved authentication mechanisms."],
            "notes": ["Some additional notes."],
            "experiments": ["Experimental feature A is now available."],
            "breaking_changes": ["Breaking change: Removed deprecated function B.\n            * Breaking change: Updated library C to version 1.0.\n            * Upgrade note: Please update your credentials."]
        }

        result = parse_section(markdown_text)
        print("RESULT: ", result)
        for key in expected_result:
            self.assertEqual(result[key], expected_result[key])

if __name__ == '__main__':
    unittest.main()
