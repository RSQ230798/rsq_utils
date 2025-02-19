"""Tests for variables utilities."""
import types
import pytest
import pandas as pd
from src.rsq_utils.variables import Variables

def test_variables_initialization():
    """Test Variables initialization."""
    # Empty initialization
    vars_empty = Variables()
    assert len(vars_empty) == 0
    
    # Initialize with dictionary
    initial_vars = {"a": 1, "b": "test"}
    vars_with_data = Variables(initial_vars)
    assert vars_with_data["a"] == 1
    assert vars_with_data["b"] == "test"

def test_variables_deepcopy():
    """Test deep copying of variables."""
    # Test with nested dictionary
    nested_dict = {"outer": {"inner": [1, 2, 3]}}
    vars_nested = Variables(nested_dict)
    
    # Modify original dictionary
    nested_dict["outer"]["inner"].append(4)
    
    # Verify Variables instance wasn't affected
    assert vars_nested["outer"]["inner"] == [1, 2, 3]

def test_variables_module_handling():
    """Test handling of module objects."""
    # Create a Variables instance with a module
    vars_with_module = Variables({"pd": pd, "data": [1, 2, 3]})

    # Verify module is preserved
    assert isinstance(vars_with_module["pd"], types.ModuleType)
    assert vars_with_module["pd"] is pd

def test_variables_update():
    """Test update method."""
    vars_obj = Variables({"a": 1})
    
    # Update with new values
    vars_obj.update_variables({"b": 2, "c": {"nested": True}})
    
    assert vars_obj["a"] == 1
    assert vars_obj["b"] == 2
    assert vars_obj["c"]["nested"] is True
    
    # Verify deep copy on update
    update_dict = {"d": [1, 2, 3]}
    vars_obj.update_variables(update_dict)
    update_dict["d"].append(4)
    assert vars_obj["d"] == [1, 2, 3]

def test_variables_copy():
    """Test copy method."""
    original = Variables({"a": [1, 2, 3], "b": {"nested": True}})
    copied = original.copy_variables()
    
    # Modify original
    original["a"].append(4)
    original["b"]["new_key"] = False
    
    # Verify copy wasn't affected
    assert copied["a"] == [1, 2, 3]
    assert copied["b"] == {"nested": True}

def test_variables_summary():
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
    assert isinstance(summary, dict)
    for key in test_data.keys():
        assert key in summary
    
    # Check specific summaries
    assert summary["number"]["type"] == "int"
    assert summary["string"]["type"] == "str"
    assert summary["list"]["type"] == "list"
    assert summary["list"]["length"] == 3
    assert summary["dict"]["type"] == "dict"
    assert summary["dataframe"]["type"] == "pandas.DataFrame"
    assert summary["dataframe"]["shape"] == str(df.shape)

def test_variables_dataframe_summary():
    """Test DataFrame summarization."""
    df = pd.DataFrame({
        "numbers": [1, 2, 3],
        "strings": ["a", "b", "c"]
    })
    
    vars_obj = Variables({"df": df})
    summary = vars_obj.get_summary()["df"]
    
    assert summary["type"] == "pandas.DataFrame"
    assert summary["shape"] == str(df.shape)
    assert isinstance(summary["columns"], list)
    assert isinstance(summary["data_types"], dict)
    assert isinstance(summary["data_examples"], dict)
    assert isinstance(summary["number_of_unique_values"], dict)
    assert isinstance(summary["memory_usage"], (int, float))

def test_variables_nested_summary():
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
    
    assert summary["level1"]["type"] == "dict"
    assert summary["level1"]["summary"]["level2"]["type"] == "dict"
    assert summary["level1"]["summary"]["level2"]["summary"]["level3"]["type"] == "list"
    assert summary["level1"]["summary"]["level2"]["summary"]["level3"]["length"] == 3

    assert summary["level21"]["type"] == "list"
    assert summary["level21"]["length"] == 3

    assert summary["level31"]["type"] == "dict"
    assert summary["level31"]["summary"] == nested_data["level31"].get_summary()
