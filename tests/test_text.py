"""Tests for text utilities."""
import unittest
from src.rsq_utils.text import (
    camel_to_snake, 
    convert_keys_to_snake_case
)

class TestText(unittest.TestCase):
    """Test cases for text utilities."""

    def test_camel_to_snake_basic(self):
        """Test basic camel case to snake case conversion."""
        self.assertEqual(camel_to_snake("camelCase"), "camel_case")
        self.assertEqual(camel_to_snake("ThisIsATest"), "this_is_a_test")
        self.assertEqual(camel_to_snake("ABC"), "abc")
        self.assertEqual(camel_to_snake("AbC"), "ab_c")
        self.assertEqual(camel_to_snake("simpletext"), "simpletext")

    def test_camel_to_snake_edge_cases(self):
        """Test edge cases for camel case conversion."""
        self.assertEqual(camel_to_snake(""), "")
        self.assertEqual(camel_to_snake("A"), "a")
        self.assertEqual(camel_to_snake("AAA"), "aaa")
        self.assertEqual(camel_to_snake("AaA"), "aa_a")
        self.assertEqual(camel_to_snake("aaa"), "aaa")
        self.assertEqual(camel_to_snake("ATestWithALongName"), "a_test_with_a_long_name")

    def test_convert_keys_to_snake_case_dict(self):
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
        self.assertEqual(convert_keys_to_snake_case(input_dict), expected)

    def test_convert_keys_to_snake_case_nested(self):
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
        self.assertEqual(convert_keys_to_snake_case(input_dict), expected)

    def test_convert_keys_to_snake_case_list(self):
        """Test list of dictionaries conversion."""
        input_list = [
            {"firstName": "John"},
            {"lastName": "Doe"}
        ]
        expected = [
            {"first_name": "John"},
            {"last_name": "Doe"}
        ]
        self.assertEqual(convert_keys_to_snake_case(input_list), expected)

    def test_convert_keys_to_snake_case_mixed(self):
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
        self.assertEqual(convert_keys_to_snake_case(input_data), expected)

    def test_convert_keys_to_snake_case_primitives(self):
        """Test primitive value handling."""
        self.assertEqual(convert_keys_to_snake_case("string"), "string")
        self.assertEqual(convert_keys_to_snake_case(123), 123)
        self.assertTrue(convert_keys_to_snake_case(True))
        self.assertIsNone(convert_keys_to_snake_case(None))

if __name__ == '__main__':
    unittest.main()
