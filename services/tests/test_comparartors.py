import unittest
from deepdiff import DeepDiff
import jsondiff

# Assuming the comparison functions are in a module named `comparison`
from comparison_service import compare_json, compare_dict, compare_strings, compare_csv, compare_xml


class TestComparisons(unittest.TestCase):

    def test_compare_json(self):
        """Test the compare_json function."""
        result_v1 = {'name': 'Test'}
        result_v2 = {'name': 'Test', 'age': 30}
        expected_diff = {'age': 30}
        self.assertEqual(compare_json(result_v1, result_v2), expected_diff)

    def test_compare_dict(self):
        """Test the compare_dict function."""
        result_v1 = {'name': 'Test'}
        result_v2 = {'name': 'Test', 'age': 30}
        expected_diff = DeepDiff(result_v1, result_v2)
        self.assertEqual(compare_dict(result_v1, result_v2), expected_diff)

    def test_compare_strings(self):
        """Test the compare_strings function."""
        result_v1 = "Version 1 output\nAnother line"
        result_v2 = "Version 2 output\nDifferent line"
        expected_diff = '\n'.join([
            "--- ",
            "+++ ",
            "@@ -1,2 +1,2 @@",
            "-Version 1 output",
            "+Version 2 output",
            "-Another line",
            "+Different line"
        ])
        self.assertEqual(compare_strings(result_v1, result_v2), expected_diff)

    def test_compare_csv(self):
        """Test the compare_csv function."""
        result_v1_path = 'test_data/result_v1.csv'
        result_v2_path = 'test_data/result_v2.csv'

        # Create test CSV files
        with open(result_v1_path, 'w') as f1, open(result_v2_path, 'w') as f2:
            f1.write("Name,Age\nJohn,25\nAlice,30")
            f2.write("Name,Age\nJohn,25\nAlice,31")

        df_diff = compare_csv(result_v1_path, result_v2_path)

        # Validate that the age difference is caught
        self.assertFalse(df_diff.empty)

    def test_compare_xml(self):
        """Test the compare_xml function."""
        xml_v1 = '''<person><name>John</name><age>30</age></person>'''
        xml_v2 = '''<person><name>John</name><age>31</age></person>'''

        expected_diff = DeepDiff({'person': {'name': 'John', 'age': '30'}}, {'person': {'name': 'John', 'age': '31'}})
        self.assertEqual(compare_xml(xml_v1, xml_v2), expected_diff)


if __name__ == "__main__":
    unittest.main()
