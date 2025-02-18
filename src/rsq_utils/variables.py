"""Variable management utilities for handling and summarizing Python variables."""
import types
import copy
from typing import Any, Dict, List, Optional, TypeVar
import pandas as pd

T = TypeVar('T')
VariableDict = Dict[str, Any]
SummaryDict = Dict[str, Any]

class Variables(dict):
    """Variables container with isolation and summarization capabilities.
    
    A dictionary-like object that provides deep copying of variables and
    comprehensive summaries of their contents. Handles special cases like
    pandas DataFrames and maintains module references.

    ** Useful for cache management, storing local variables, storing global variables, etc.
    
    Args:
        variables: Initial dictionary of variables to store. Defaults to None.
    """
    
    def __init__(self, variables: Optional[VariableDict] = None) -> None:
        deep_copy = self.__deepcopy(variables or {})
        super().__init__(deep_copy)

    def __deepcopy(self, variables: VariableDict) -> VariableDict:
        """Create a deep copy of variables while preserving module references.
        
        Args:
            variables: Dictionary of variables to copy.
            
        Returns:
            Deep copy of variables with module references preserved.
        """
        modules = {k: v for k, v in variables.items() if isinstance(v, types.ModuleType)}
        non_modules = {k: v for k, v in variables.items() if not isinstance(v, types.ModuleType)}
        
        non_modules_copy = copy.deepcopy(non_modules)
        non_modules_copy.update(modules)
        
        return non_modules_copy

    def update_variables(self, new_variables: VariableDict) -> None:
        """Update variables with new values, maintaining isolation.
        
        Args:
            new_variables: Dictionary of new variables to add/update.
        """
        super().update(self.__deepcopy(new_variables))

    def copy_variables(self) -> 'Variables':
        """Create a new Variables instance with copied data.
        
        Returns:
            New Variables instance with copied data.
        """
        return Variables(self.__deepcopy(self))
    
    def get_summary(self) -> SummaryDict:
        """Get a comprehensive summary of all variables.
        
        Returns:
            Dictionary containing summaries of all variables.
        """
        return {key: self.__summarize_variable(value) for key, value in self.items()}
        
    def __summarize_variable(self, value: Any) -> SummaryDict:
        """Generate a summary for a single variable.
        
        Args:
            value: Variable to summarize.
            
        Returns:
            Summary dictionary appropriate for the variable type.
        """
        if isinstance(value, pd.DataFrame):
            return self.__dataframe_summary(value)
        elif isinstance(value, dict):
            return self.__dict_summary(value)
        elif isinstance(value, list):
            return self.__list_summary(value)
        else:
            return self.__other_variables_summary(value)
    
    def __dataframe_summary(self, df: pd.DataFrame) -> SummaryDict:
        """Generate a summary for a pandas DataFrame.
        
        Args:
            df: DataFrame to summarize.
            
        Returns:
            Summary of DataFrame's structure and content.
        """
        return {
            "type": "pandas.DataFrame",
            "shape": str(df.shape),
            "columns": list(df.columns),
            "data_types": df.dtypes.to_dict(),
            "data_examples": df.head(10).to_dict(),
            "number_of_unique_values": df.nunique().to_dict(),
            "memory_usage": float(df.memory_usage(deep=True).sum()),
        }
    
    def __dict_summary(self, value: Dict[Any, Any]) -> SummaryDict:
        """Generate a summary for a dictionary.
        
        Args:
            value: Dictionary to summarize.
            
        Returns:
            Summary of dictionary structure and content.
        """
        return {
            "type": "dict",
            "keys": list(value.keys())[:10],
            "summary": {k: self.__summarize_variable(v) for k, v in list(value.items())[:10]}
        }
    
    def __list_summary(self, value: List[Any]) -> SummaryDict:
        """Generate a summary for a list.
        
        Args:
            value: List to summarize.
            
        Returns:
            Summary of list length and content.
        """
        return {
            "type": "list",
            "length": len(value),
            "first_elements": [self.__summarize_variable(v) for v in value[:10]]
        }

    def __other_variables_summary(self, value: Any) -> SummaryDict:
        """Generate a summary for any other type of variable.
        
        Args:
            value: Variable to summarize.
            
        Returns:
            Basic summary with type and string representation.
        """
        try:
            return {
                "type": type(value).__name__,
                "summary": value.get_summary(),
            }
        except:
            return {
                "type": type(value).__name__,
                "value": str(value)[:100],
            }

class LocalVariables(Variables):
    """
    Local variables container with isolation and summarization capabilities.
    """
    pass

class GlobalVariables(Variables):
    """
    Global variables container with isolation and summarization capabilities.
    """
    pass

class Cache(Variables):
    """
    Cache container with isolation and summarization capabilities.
    """
    pass

