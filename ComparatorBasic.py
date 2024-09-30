from abc import ABC, abstractmethod
from deepdiff import DeepDiff
import difflib
import pandas as pd
import jsondiff

# Abstract Comparator
class Comparator(ABC):
    @abstractmethod
    def compare(self, result_v1, result_v2):
        pass

# JSON Comparator
class JSONComparator(Comparator):
    def compare(self, result_v1, result_v2):
        return jsondiff.diff(result_v1, result_v2)

# Dictionary Comparator (can use deepdiff)
class DictComparator(Comparator):
    def compare(self, result_v1, result_v2):
        return DeepDiff(result_v1, result_v2)

# String Comparator (can use difflib)
class StringComparator(Comparator):
    def compare(self, result_v1, result_v2):
        diff = difflib.unified_diff(result_v1, result_v2)
        return "\n".join(diff)

# CSV Comparator (using pandas)
class CSVComparator(Comparator):
    def compare(self, result_v1, result_v2):
        df_v1 = pd.read_csv(result_v1)
        df_v2 = pd.read_csv(result_v2)
        return df_v1.compare(df_v2)

# Context for comparison
class ComparisonContext:
    def __init__(self, comparator: Comparator):
        self.comparator = comparator

    def set_comparator(self, comparator: Comparator):
        self.comparator = comparator

    def compare(self, result_v1, result_v2):
        return self.comparator.compare(result_v1, result_v2)

# Example usage
if __name__ == "__main__":
    # Compare two JSON files
    json_comparator = JSONComparator()
    context = ComparisonContext(json_comparator)
    result = context.compare({'name': 'Test'}, {'name': 'Test', 'age': 30})
    print("JSON Comparison Result:", result)
    
    # Compare two dictionary results
    dict_comparator = DictComparator()
    context.set_comparator(dict_comparator)
    result = context.compare({'name': 'Test'}, {'name': 'Test', 'age': 30})
    print("Dict Comparison Result:", result)
    
    # Compare two CSV files
    csv_comparator = CSVComparator()
    context.set_comparator(csv_comparator)
    result = context.compare('result_v1.csv', 'result_v2.csv')
    print("CSV Comparison Result:\n", result)

    # Compare two strings
    string_comparator = StringComparator()
    context.set_comparator(string_comparator)
    result = context.compare('Version 1 output', 'Version 2 output')
    print("String Comparison Result:\n", result)
