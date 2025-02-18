"""Tests for variables utilities."""
import types
import unittest
import pandas as pd
from src.rsq_utils.variables import Variables

class TestVariables(unittest.TestCase):
    """Test cases for variables utilities."""

    def test_variables_initialization(self):
        """Test Variables initialization."""
        # Empty initialization
        vars_empty = Variables()
        self.assertEqual(len(vars_empty), 0)
        
        # Initialize with dictionary
        initial_vars = {"a": 1, "b": "test"}
        vars_with_data = Variables(initial_vars)
        self.assertEqual(vars_with_data["a"], 1)
        self.assertEqual(vars_with_data["b"], "test")

    def test_variables_deepcopy(self):
        """Test deep copying of variables."""
        # Test with nested dictionary
        nested_dict = {"outer": {"inner": [1, 2, 3]}}
        vars_nested = Variables(nested_dict)
        
        # Modify original dictionary
        nested_dict["outer"]["inner"].append(4)
        
        # Verify Variables instance wasn't affected
        self.assertEqual(vars_nested["outer"]["inner"], [1, 2, 3])

    def test_variables_module_handling(self):
        """Test handling of module objects."""
        # Create a Variables instance with a module
        vars_with_module = Variables({"pd": pd, "data": [1, 2, 3]})

        # Verify module is preserved
        self.assertIsInstance(vars_with_module["pd"], types.ModuleType)
        self.assertIs(vars_with_module["pd"], pd)

    def test_variables_update(self):
        """Test update method."""
        vars_obj = Variables({"a": 1})
        
        # Update with new values
        vars_obj.update_variables({"b": 2, "c": {"nested": True}})
        
        self.assertEqual(vars_obj["a"], 1)
        self.assertEqual(vars_obj["b"], 2)
        self.assertTrue(vars_obj["c"]["nested"])
        
        # Verify deep copy on update
        update_dict = {"d": [1, 2, 3]}
        vars_obj.update_variables(update_dict)
        update_dict["d"].append(4)
        self.assertEqual(vars_obj["d"], [1, 2, 3])

    def test_variables_copy(self):
        """Test copy method."""
        original = Variables({"a": [1, 2, 3], "b": {"nested": True}})
        copied = original.copy_variables()
        
        # Modify original
        original["a"].append(4)
        original["b"]["new_key"] = False
        
        # Verify copy wasn't affected
        self.assertEqual(copied["a"], [1, 2, 3])
        self.assertEqual(copied["b"], {"nested": True})

    def test_variables_summary(self):
        """Test get_summary method."""
        # Create test data
        df = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": ["a", "b", "c"]
        })
        
        test_data = {
            "number": 42,
            "string": "test",
            "list": [1, 2, 3],
            "dict": {"key": "value"},
            "dataframe": df
        }
        
        vars_obj = Variables(test_data)
        summary = vars_obj.get_summary()
        
        # Check summary structure
        self.assertIsInstance(summary, dict)
        for key in test_data.keys():
            self.assertIn(key, summary)
        
        # Check specific summaries
        self.assertEqual(summary["number"]["type"], "int")
        self.assertEqual(summary["string"]["type"], "str")
        self.assertEqual(summary["list"]["type"], "list")
        self.assertEqual(summary["list"]["length"], 3)
        self.assertEqual(summary["dict"]["type"], "dict")
        self.assertEqual(summary["dataframe"]["type"], "pandas.DataFrame")
        self.assertEqual(summary["dataframe"]["shape"], str(df.shape))

    def test_variables_dataframe_summary(self):
        """Test DataFrame summarization."""
        df = pd.DataFrame({
            "numbers": [1, 2, 3],
            "strings": ["a", "b", "c"]
        })
        
        vars_obj = Variables({"df": df})
        summary = vars_obj.get_summary()["df"]
        
        self.assertEqual(summary["type"], "pandas.DataFrame")
        self.assertEqual(summary["shape"], str(df.shape))
        self.assertIsInstance(summary["columns"], list)
        self.assertIsInstance(summary["data_types"], dict)
        self.assertIsInstance(summary["data_examples"], dict)
        self.assertIsInstance(summary["number_of_unique_values"], dict)
        self.assertIsInstance(summary["memory_usage"], (int, float))

    def test_variables_nested_summary(self):
        """Test summarization of nested structures."""
        nested_data = {
            "level1": {
                "level2": {
                    "level3": [1, 2, 3]
                }
            },
            "level21": [1, 2, 3],
            "level31": Variables({"a": 1, "b": 2, "c": {"nested": True, "list": [1, 2, 3]}})
        }
        
        vars_obj = Variables(nested_data)
        summary = vars_obj.get_summary()
        
        self.assertEqual(summary["level1"]["type"], "dict")
        self.assertEqual(summary["level1"]["summary"]["level2"]["type"], "dict")
        self.assertEqual(summary["level1"]["summary"]["level2"]["summary"]["level3"]["type"], "list")
        self.assertEqual(summary["level1"]["summary"]["level2"]["summary"]["level3"]["length"], 3)

        self.assertEqual(summary["level21"]["type"], "list")
        self.assertEqual(summary["level21"]["length"], 3)

        self.assertEqual(summary["level31"]["type"], "dict")
        self.assertEqual(summary["level31"]["summary"], nested_data["level31"].get_summary())

if __name__ == '__main__':
    unittest.main()
