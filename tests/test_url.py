"""Tests for URL utilities."""
import unittest
from src.url import (
    url_encode, 
    generate_parameter_combos, 
    is_valid_url, 
    sanitize_params
)

class TestUrl(unittest.TestCase):
    """Test cases for URL utilities."""

    def test_is_valid_url(self):
        """Test URL validation."""
        self.assertTrue(is_valid_url("https://example.com"))
        self.assertTrue(is_valid_url("http://localhost:8000"))
        self.assertTrue(is_valid_url("ftp://files.example.com"))
        
        self.assertFalse(is_valid_url("not-a-url"))
        self.assertFalse(is_valid_url("http://"))
        self.assertFalse(is_valid_url("https://"))
        self.assertFalse(is_valid_url(""))

    def test_sanitize_params(self):
        """Test parameter sanitization."""
        params = {
            "str": "value",
            "int": 123,
            "float": 3.14,
            "bool": True,
            "none": None,
        }
        
        result = sanitize_params(params)
        expected = {
            "str": "value",
            "int": "123",
            "float": "3.14",
            "bool": "True"
        }
        self.assertEqual(result, expected)
        self.assertNotIn("none", result)

    def test_url_encode_valid(self):
        """Test URL encoding with valid inputs."""
        base_url = "https://api.example.com"
        params = {
            "key": "value",
            "number": 123,
            "flag": True
        }
        
        result = url_encode(base_url, params)
        self.assertTrue(result.startswith(base_url + "?"))
        self.assertIn("key=value", result)
        self.assertIn("number=123", result)
        self.assertIn("flag=True", result)

    def test_url_encode_invalid(self):
        """Test URL encoding with invalid inputs."""
        with self.assertRaisesRegex(ValueError, "Invalid base URL"):
            url_encode("not-a-url", {"key": "value"})

    def test_generate_parameter_combos_valid(self):
        """Test parameter combination generation with valid inputs."""
        params = {
            "type": ["A", "B"],
            "status": [1, 2]
        }
        
        result = generate_parameter_combos(params)
        self.assertEqual(len(result), 4)
        self.assertIn({"type": "A", "status": 1}, result)
        self.assertIn({"type": "A", "status": 2}, result)
        self.assertIn({"type": "B", "status": 1}, result)
        self.assertIn({"type": "B", "status": 2}, result)

    def test_generate_parameter_combos_empty(self):
        """Test parameter combination generation with empty input."""
        self.assertEqual(generate_parameter_combos({}), [])

    def test_generate_parameter_combos_single(self):
        """Test parameter combination generation with single parameter."""
        params = {"type": ["A", "B"]}
        result = generate_parameter_combos(params)
        self.assertEqual(len(result), 2)
        self.assertIn({"type": "A"}, result)
        self.assertIn({"type": "B"}, result)

    def test_generate_parameter_combos_invalid(self):
        """Test parameter combination generation with invalid inputs."""
        # Test with non-list values
        with self.assertRaisesRegex(ValueError, "All parameter values must be lists"):
            generate_parameter_combos({"key": "not a list"})

if __name__ == '__main__':
    unittest.main()
