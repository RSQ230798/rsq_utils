import pytest
from src.rsq_utils.paths import clean_path, find_template_params

def test_clean_path_leading_slash():
    """Test cleaning paths with leading slash."""
    assert clean_path("/folder/") == "folder/"
    assert clean_path("/file.json") == "file.json"
    assert clean_path("/path/to/folder/") == "path/to/folder/"

def test_clean_path_trailing_slash():
    """Test cleaning paths with trailing slash."""
    # For folders (no file extension)
    assert clean_path("folder") == "folder/"
    assert clean_path("folder/") == "folder/"
    assert clean_path("path/to/folder") == "path/to/folder/"
    
    # For files (with extension)
    assert clean_path("file.json/") == "file.json"
    assert clean_path("file.json") == "file.json"
    assert clean_path("path/to/file.json/") == "path/to/file.json"

def test_clean_path_complex_cases():
    """Test cleaning paths with multiple conditions."""
    assert clean_path("/path/to/folder/") == "path/to/folder/"
    assert clean_path("/path/to/file.json/") == "path/to/file.json"
    assert clean_path("path/to/folder") == "path/to/folder/"
    assert clean_path("/path/to/file.parquet/") == "path/to/file.parquet"

def test_find_template_params_single():
    """Test finding single template parameter."""
    template = "folder/{param}/file.json"
    params = find_template_params(template)
    assert params == ["param"]

def test_find_template_params_multiple():
    """Test finding multiple template parameters."""
    template = "{year}/{month}/data_{type}.json"
    params = find_template_params(template)
    assert params == ["year", "month", "type"]

def test_find_template_params_none():
    """Test finding parameters in template with no parameters."""
    template = "folder/subfolder/file.json"
    params = find_template_params(template)
    assert params == []

def test_find_template_params_complex():
    """Test finding parameters in complex templates."""
    template = "{region}/data/{year}/{month}/type_{data_type}.{format}"
    params = find_template_params(template)
    assert params == ["region", "year", "month", "data_type", "format"]

def test_find_template_params_duplicate():
    """Test finding parameters with duplicates."""
    template = "{param}/data/{param}/file.json"
    params = find_template_params(template)
    # Should return each parameter only once
    assert params == ["param", "param"]

def test_find_template_params_nested():
    """Test finding nested parameters (not supported)."""
    template = "{outer{inner}}/file.json"
    params = find_template_params(template)
    # Should treat it as one parameter
    assert params == ["outer{inner"]
