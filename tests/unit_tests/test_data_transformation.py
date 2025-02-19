"""Tests for data transformation utilities."""
import pytest
from src.rsq_utils.data_transformation import list_batch_split

def test_list_batch_split_valid():
    """Test list_batch_split with valid inputs."""
    # Test with default batch size
    input_list = list(range(250))
    result = list_batch_split(input_list)
    assert len(result) == 3
    assert len(result[0]) == 100
    assert len(result[1]) == 100
    assert len(result[2]) == 50
    
    # Test with custom batch size
    result = list_batch_split(input_list, batch_size=50)
    assert len(result) == 5
    for batch in result:
        assert len(batch) == 50

def test_list_batch_split_empty():
    """Test list_batch_split with empty list."""
    result = list_batch_split([])
    assert result == []

def test_list_batch_split_single_batch():
    """Test list_batch_split when input is smaller than batch size."""
    input_list = list(range(50))
    result = list_batch_split(input_list, batch_size=100)
    assert len(result) == 1
    assert result[0] == input_list

def test_list_batch_split_invalid_input():
    """Test list_batch_split with invalid inputs."""
    # Test with non-list input
    with pytest.raises(ValueError, match="Input must be a list"):
        list_batch_split("not a list")
    
    # Test with invalid batch size
    with pytest.raises(ValueError, match="Batch size must be at least 1"):
        list_batch_split([1, 2, 3], batch_size=0)
