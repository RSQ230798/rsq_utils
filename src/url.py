"""URL utilities for parameter encoding and combination generation."""
from typing import Dict, List, Any, Union
from urllib.parse import urljoin, urlencode, urlparse
from itertools import product

ParamValue = Union[str, int, float, bool]
ParamDict = Dict[str, List[ParamValue]]

# helper functions
def is_valid_url(url: str) -> bool:
    """Check if a URL is valid.
    
    Args:
        url: URL to validate.
        
    Returns:
        True if URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def sanitize_params(params: Dict[str, Any]) -> Dict[str, str]:
    """Convert parameter values to strings and remove None values.
    
    Args:
        params: Dictionary of parameters to sanitize.
        
    Returns:
        Dictionary with sanitized parameter values.
    """
    return {
        str(key): str(value)
        for key, value in params.items()
        if value is not None
    }

def url_encode(base_url: str, params: Dict[str, Any]) -> str:
    """Encode parameters and append them to a base URL.
    
    Args:
        base_url: Base URL to append parameters to.
        params: Dictionary of parameters to encode.
        
    Returns:
        Complete URL with encoded parameters.
        
    Raises:
        ValueError: If base_url is not a valid URL.
    """
    if not is_valid_url(base_url):
        raise ValueError(f"Invalid base URL: {base_url}")
        
    sanitized_params = sanitize_params(params)
    return urljoin(base_url, f"?{urlencode(sanitized_params)}")

def generate_parameter_combos(parameters: ParamDict) -> List[Dict[str, ParamValue]]:
    """Generate all possible combinations of parameter values.
    
    Takes a dictionary of parameters and their possible values and returns a list
    of dictionaries containing all possible combinations of the parameters and
    their values.
    
    Args:
        parameters: Dictionary where each key is a parameter name and each value
                   is a list of possible values for that parameter.
                   
    Returns:
        List of dictionaries, each containing one possible combination of parameter values.
        
    Examples:
        >>> params = {
        ...     "type": ["A", "B"],
        ...     "status": [1, 2]
        ... }
        >>> generate_parameter_combos(params)
        [
            {"type": "A", "status": 1},
            {"type": "A", "status": 2},
            {"type": "B", "status": 1},
            {"type": "B", "status": 2}
        ]
    """
    if not parameters:
        return []
        
    if not all(isinstance(values, list) for values in parameters.values()):
        raise ValueError("All parameter values must be lists")
        
    keys = parameters.keys()
    values_lists = parameters.values()

    return [
        {key: value for key, value in zip(keys, values_combo)}
        for values_combo in product(*values_lists)
    ]
