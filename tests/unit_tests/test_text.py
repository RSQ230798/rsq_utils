"""Tests for text utilities."""
import pytest
from src.rsq_utils.text import (
    camel_to_snake, 
    convert_keys_to_snake_case
)

def test_camel_to_snake_basic():
    """Test basic camel case to snake case conversion."""
    assert camel_to_snake("camelCase") == "camel_case"
    assert camel_to_snake("ThisIsATest") == "this_is_a_test"
    assert camel_to_snake("ABC") == "abc"
    assert camel_to_snake("AbC") == "ab_c"
    assert camel_to_snake("simpletext") == "simpletext"

def test_camel_to_snake_edge_cases():
    """Test edge cases for camel case conversion."""
    assert camel_to_snake("") == ""
    assert camel_to_snake("A") == "a"
    assert camel_to_snake("AAA") == "aaa"
    assert camel_to_snake("AaA") == "aa_a"
    assert camel_to_snake("aaa") == "aaa"
    assert camel_to_snake("ATestWithALongName") == "a_test_with_a_long_name"

def test_convert_keys_to_snake_case_dict():
    """Test dictionary key conversion."""
    input_dict = {
        "firstName": "John",
        "lastName": "Doe",
        "phoneNumber": "123-456-7890"
    }
    expected = {
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "123-456-7890"
    }
    assert convert_keys_to_snake_case(input_dict) == expected

def test_convert_keys_to_snake_case_nested():
    """Test nested dictionary conversion."""
    input_dict = {
        "userData": {
            "firstName": "John",
            "lastName": "Doe",
            "contactInfo": {
                "phoneNumber": "123-456-7890",
                "emailAddress": "john@example.com"
            }
        }
    }
    expected = {
        "user_data": {
            "first_name": "John",
            "last_name": "Doe",
            "contact_info": {
                "phone_number": "123-456-7890",
                "email_address": "john@example.com"
            }
        }
    }
    assert convert_keys_to_snake_case(input_dict) == expected

def test_convert_keys_to_snake_case_list():
    """Test list of dictionaries conversion."""
    input_list = [
        {"firstName": "John"},
        {"lastName": "Doe"}
    ]
    expected = [
        {"first_name": "John"},
        {"last_name": "Doe"}
    ]
    assert convert_keys_to_snake_case(input_list) == expected

def test_convert_keys_to_snake_case_mixed():
    """Test mixed data structure conversion."""
    input_data = {
        "userData": [
            {"firstName": "John"},
            {"lastName": "Doe"}
        ],
        "otherData": {
            "someKey": "value",
            "nestedList": [
                {"itemId": 1},
                {"itemId": 2}
            ]
        }
    }
    expected = {
        "user_data": [
            {"first_name": "John"},
            {"last_name": "Doe"}
        ],
        "other_data": {
            "some_key": "value",
            "nested_list": [
                {"item_id": 1},
                {"item_id": 2}
            ]
        }
    }
    assert convert_keys_to_snake_case(input_data) == expected

def test_convert_keys_to_snake_case_primitives():
    """Test primitive value handling."""
    assert convert_keys_to_snake_case("string") == "string"
    assert convert_keys_to_snake_case(123) == 123
    assert convert_keys_to_snake_case(True) is True
    assert convert_keys_to_snake_case(None) is None
