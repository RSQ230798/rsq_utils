from typing import Dict, List, Union, Any

JsonType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

def camel_to_snake(text: str) -> str:
    """Convert CamelCase to snake_case.
    
    Args:
        text: The CamelCase string to convert.
        
    Returns:
        The string converted to snake_case.
        
    Examples:
        >>> camel_to_snake("camelCase")
        'camel_case'
        >>> camel_to_snake("ThisIsATest")
        'this_is_a_test'
    """
    if not text:
        return text
        
    output = text[0].lower()
    for i, letter in enumerate(text[1:], 1):
        # Add underscore when current letter is uppercase and either:
        # 1. Next letter is lowercase (if not last letter)
        # 2. Previous letter is lowercase
        if letter.isupper() and (
            (i < len(text) - 1 and text[i + 1].islower()) or
            text[i - 1].islower()
        ):
            output += "_" + letter.lower()
        else:
            output += letter.lower()
    
    return output

def convert_keys_to_snake_case(data: JsonType) -> JsonType:
    """Recursively convert all dictionary keys from camelCase to snake_case.
    
    Args:
        data: The data structure to convert. Can be a dictionary, list, or primitive type.
        
    Returns:
        The data structure with all dictionary keys converted to snake_case.
        
    Examples:
        >>> convert_keys_to_snake_case({"firstName": "John", "lastName": "Doe"})
        {'first_name': 'John', 'last_name': 'Doe'}
        >>> convert_keys_to_snake_case([{"userId": 1}, {"userId": 2}])
        [{'user_id': 1}, {'user_id': 2}]
    """
    if isinstance(data, dict):
        return {
            camel_to_snake(str(key)): convert_keys_to_snake_case(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    else:
        return data
