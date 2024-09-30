import logging
import pandas as pd
import difflib
from deepdiff import DeepDiff
import jsondiff
from abc import ABC, abstractmethod
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Abstract Comparator
class Comparator(ABC):
    """
    Abstract base class for comparison strategies.
    All concrete comparators must implement the `compare` method.
    """
    
    @abstractmethod
    def compare(self, result_v1: Any, result_v2: Any):
        """
        Compare two results and return the differences.
        :param result_v1: First result for comparison.
        :param result_v2: Second result for comparison.
        :return: The differences between the two results.
        """
        pass


# JSON Comparator
class JSONComparator(Comparator):
    """
    Compares two JSON objects and returns the differences using jsondiff.
    """
    
    def compare(self, result_v1: Dict, result_v2: Dict):
        if not isinstance(result_v1, dict) or not isinstance(result_v2, dict):
            logger.error("Invalid input: Both inputs must be dictionaries (JSON objects).")
            raise ValueError("Both inputs must be dictionaries (JSON objects).")
        
        logger.info("Comparing JSON objects...")
        return jsondiff.diff(result_v1, result_v2)


# Dictionary Comparator (can use deepdiff)
class DictComparator(Comparator):
    """
    Compares two dictionary objects and returns the differences using DeepDiff.
    """
    
    def compare(self, result_v1: Dict, result_v2: Dict):
        if not isinstance(result_v1, dict) or not isinstance(result_v2, dict):
            logger.error("Invalid input: Both inputs must be dictionaries.")
            raise ValueError("Both inputs must be dictionaries.")
        
        logger.info("Comparing dictionaries...")
        return DeepDiff(result_v1, result_v2)


# String Comparator (can use difflib)
class StringComparator(Comparator):
    """
    Compares two strings and returns a diff using difflib.
    """
    
    def compare(self, result_v1: str, result_v2: str):
        if not isinstance(result_v1, str) or not isinstance(result_v2, str):
            logger.error("Invalid input: Both inputs must be strings.")
            raise ValueError("Both inputs must be strings.")
        
        logger.info("Comparing strings...")
        diff = difflib.unified_diff(result_v1.splitlines(), result_v2.splitlines())
        return "\n".join(diff)


# CSV Comparator (using pandas)
class CSVComparator(Comparator):
    """
    Compares two CSV files and returns the differences using pandas DataFrames.
    """
    
    def compare(self, result_v1: str, result_v2: str):
        try:
            df_v1 = pd.read_csv(result_v1)
            df_v2 = pd.read_csv(result_v2)
            
            logger.info("Comparing CSV files...")
            return df_v1.compare(df_v2)
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise FileNotFoundError(f"File not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred during CSV comparison: {e}")
            raise Exception(f"An error occurred during CSV comparison: {e}")


# Context for comparison
class ComparisonContext:
    """
    Context for performing comparisons using different comparator strategies.
    The context selects the appropriate comparator for the given data format.
    """
    
    def __init__(self, comparator: Comparator):
        self.comparator = comparator
    
    def set_comparator(self, comparator: Comparator):
        """
        Sets the comparator strategy to be used in comparisons.
        :param comparator: A concrete instance of Comparator.
        """
        self.comparator = comparator
    
    def compare(self, result_v1: Any, result_v2: Any):
        """
        Performs comparison using the set comparator.
        :param result_v1: First result for comparison.
        :param result_v2: Second result for comparison.
        :return: The differences between the two results.
        """
        return self.comparator.compare(result_v1, result_v2)


# Example usage
if __name__ == "__main__":
    # Compare two JSON objects
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
    # Assuming 'result_v1.csv' and 'result_v2.csv' are paths to actual CSV files
    # result = context.compare('result_v1.csv', 'result_v2.csv')
    # print("CSV Comparison Result:\n", result)
    
    # Compare two strings
    string_comparator = StringComparator()
    context.set_comparator(string_comparator)
    result = context.compare("Version 1 output\nAnother line", "Version 2 output\nDifferent line")
    print("String Comparison Result:\n", result)
