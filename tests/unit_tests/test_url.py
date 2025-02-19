"""Tests for URL utilities."""
import pytest
from src.rsq_utils.url import (
    url_encode, 
    generate_parameter_combos, 
    is_valid_url, 
    sanitize_params
)

def test_is_valid_url():
    """Test URL validation."""
    assert is_valid_url("https://example.com") is True
    assert is_valid_url("http://localhost:8000") is True
    assert is_valid_url("ftp://files.example.com") is True
    
    assert is_valid_url("not-a-url") is False
    assert is_valid_url("http://") is False
    assert is_valid_url("https://") is False
    assert is_valid_url("") is False

def test_sanitize_params():
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
    assert result == expected
    assert "none" not in result

def test_url_encode_valid():
    """Test URL encoding with valid inputs."""
    base_url = "https://api.example.com"
    params = {
        "key": "value",
        "number": 123,
        "flag": True
    }
    
    result = url_encode(base_url, params)
    assert result.startswith(base_url + "?")
    assert "key=value" in result
    assert "number=123" in result
    assert "flag=True" in result

def test_url_encode_invalid():
    """Test URL encoding with invalid inputs."""
    with pytest.raises(ValueError, match="Invalid base URL"):
        url_encode("not-a-url", {"key": "value"})

def test_generate_parameter_combos_valid():
    """Test parameter combination generation with valid inputs."""
    params = {
        "type": ["A", "B"],
        "status": [1, 2]
    }
    
    result = generate_parameter_combos(params)
    assert len(result) == 4
    assert {"type": "A", "status": 1} in result
    assert {"type": "A", "status": 2} in result
    assert {"type": "B", "status": 1} in result
    assert {"type": "B", "status": 2} in result

def test_generate_parameter_combos_empty():
    """Test parameter combination generation with empty input."""
    assert generate_parameter_combos({}) == []

def test_generate_parameter_combos_single():
    """Test parameter combination generation with single parameter."""
    params = {"type": ["A", "B"]}
    result = generate_parameter_combos(params)
    assert len(result) == 2
    assert {"type": "A"} in result
    assert {"type": "B"} in result

def test_generate_parameter_combos_invalid():
    """Test parameter combination generation with invalid inputs."""
    # Test with non-list values
    with pytest.raises(ValueError, match="All parameter values must be lists"):
        generate_parameter_combos({"key": "not a list"})
