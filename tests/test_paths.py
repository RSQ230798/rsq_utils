import unittest
from src.rsq_utils.paths import clean_path, find_template_params

class TestFunctions(unittest.TestCase):
    """Test suite for utility functions."""

    def test_clean_path_leading_slash(self):
        """Test cleaning paths with leading slash."""
        self.assertEqual(clean_path("/folder/"), "folder/")
        self.assertEqual(clean_path("/file.json"), "file.json")
        self.assertEqual(clean_path("/path/to/folder/"), "path/to/folder/")

    def test_clean_path_trailing_slash(self):
        """Test cleaning paths with trailing slash."""
        # For folders (no file extension)
        self.assertEqual(clean_path("folder"), "folder/")
        self.assertEqual(clean_path("folder/"), "folder/")
        self.assertEqual(clean_path("path/to/folder"), "path/to/folder/")
        
        # For files (with extension)
        self.assertEqual(clean_path("file.json/"), "file.json")
        self.assertEqual(clean_path("file.json"), "file.json")
        self.assertEqual(clean_path("path/to/file.json/"), "path/to/file.json")

    def test_clean_path_complex_cases(self):
        """Test cleaning paths with multiple conditions."""
        self.assertEqual(clean_path("/path/to/folder/"), "path/to/folder/")
        self.assertEqual(clean_path("/path/to/file.json/"), "path/to/file.json")
        self.assertEqual(clean_path("path/to/folder"), "path/to/folder/")
        self.assertEqual(clean_path("/path/to/file.parquet/"), "path/to/file.parquet")

    def test_find_template_params_single(self):
        """Test finding single template parameter."""
        template = "folder/{param}/file.json"
        params = find_template_params(template)
        self.assertEqual(params, ["param"])

    def test_find_template_params_multiple(self):
        """Test finding multiple template parameters."""
        template = "{year}/{month}/data_{type}.json"
        params = find_template_params(template)
        self.assertEqual(params, ["year", "month", "type"])

    def test_find_template_params_none(self):
        """Test finding parameters in template with no parameters."""
        template = "folder/subfolder/file.json"
        params = find_template_params(template)
        self.assertEqual(params, [])

    def test_find_template_params_complex(self):
        """Test finding parameters in complex templates."""
        template = "{region}/data/{year}/{month}/type_{data_type}.{format}"
        params = find_template_params(template)
        self.assertEqual(
            params, 
            ["region", "year", "month", "data_type", "format"]
        )

    def test_find_template_params_duplicate(self):
        """Test finding parameters with duplicates."""
        template = "{param}/data/{param}/file.json"
        params = find_template_params(template)
        # Should return each parameter only once
        self.assertEqual(params, ["param", "param"])

    def test_find_template_params_nested(self):
        """Test finding nested parameters (not supported)."""
        template = "{outer{inner}}/file.json"
        params = find_template_params(template)
        # Should treat it as one parameter
        self.assertEqual(params, ["outer{inner"])


if __name__ == '__main__':
    unittest.main()
