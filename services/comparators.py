import pandas as pd
import difflib
from deepdiff import DeepDiff
import jsondiff
import xmltodict  # To convert XML to Python dict for comparison


def compare_json(json_v1, json_v2):
    """Compares two JSON objects."""
    print("Comparing JSON objects...")
    return jsondiff.diff(json_v1, json_v2)


def compare_dict(dict_v1, dict_v2):
    """Compares two dictionaries."""
    print("Comparing dictionaries...")
    return DeepDiff(dict_v1, dict_v2)


def compare_strings(str_v1, str_v2):
    """Compares two strings."""
    print("Comparing strings...")
    diff = difflib.unified_diff(str_v1.splitlines(), str_v2.splitlines())
    return "\n".join(diff)


def compare_csv(csv_v1_path, csv_v2_path):
    """Compares two CSV files."""
    print("Comparing CSV files...")
    df_v1 = pd.read_csv(csv_v1_path)
    df_v2 = pd.read_csv(csv_v2_path)
    return df_v1.compare(df_v2)


def compare_xml(xml_v1, xml_v2):
    """Compares two XML documents."""
    print("Comparing XML documents...")
    dict_v1 = xmltodict.parse(xml_v1)
    dict_v2 = xmltodict.parse(xml_v2)
    return DeepDiff(dict_v1, dict_v2)


# Example usage
if __name__ == "__main__":
    # Compare JSON objects
    json_v1 = {'name': 'Test'}
    json_v2 = {'name': 'Test', 'age': 30}
    result = compare_json(json_v1, json_v2)
    print("JSON Comparison Result:", result)

    # Compare dictionary objects
    dict_v1 = {'name': 'Test'}
    dict_v2 = {'name': 'Test', 'age': 30}
    result = compare_dict(dict_v1, dict_v2)
    print("Dict Comparison Result:", result)

    # Compare CSV files (Assuming csv_v1.csv and csv_v2.csv
