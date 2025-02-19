"""Tests for memory utilities."""
import pytest
from src.rsq_utils.memory import Memory

def test_memory_initialization():
    """Test Memory class initialization."""
    memory = Memory()
    assert memory.start_memory is not None
    assert len(memory.memory_history) == 1
    assert memory.current_memory is None

def test_memory_data_format():
    """Test memory data structure format."""
    memory = Memory()
    data = memory.get_current_memory()
    
    expected_keys = {
        "system_memory_total_gb",
        "system_memory_used_gb",
        "system_memory_available_gb",
        "system_memory_used_%",
        "process_memory_used_gb"
    }
    
    assert set(data.keys()) == expected_keys
    for value in data.values():
        assert isinstance(value, float)
    assert data["system_memory_used_%"] >= 0
    assert data["system_memory_used_%"] <= 100

def test_memory_history():
    """Test memory history tracking."""
    memory = Memory()
    initial_snapshot = memory.memory_history[0]
    
    # Add new snapshots
    memory.append_memory_history()
    memory.append_memory_history()
    
    assert len(memory.memory_history) == 3
    assert memory.memory_history[0] == initial_snapshot
    for snapshot in memory.memory_history:
        assert isinstance(snapshot, dict)

def test_memory_reset():
    """Test memory reset functionality."""
    memory = Memory()
    initial_snapshot = memory.memory_history[0]
    
    # Add snapshots and get current memory
    memory.append_memory_history()
    memory.get_current_memory()
    
    # Reset
    memory.reset_memory_data()
    
    assert len(memory.memory_history) == 1
    assert memory.memory_history[0] == initial_snapshot
    assert memory.current_memory is None

def test_get_current_memory():
    """Test current memory retrieval."""
    memory = Memory()
    
    # First call
    data1 = memory.get_current_memory()
    assert memory.current_memory == data1
    
    # Second call should update current_memory
    data2 = memory.get_current_memory()
    assert memory.current_memory == data2

def test_memory_error_handling():
    """Test error handling in memory operations."""
    memory = Memory()
    
    # Verify no exceptions are raised for normal operations
    memory.get_current_memory()
    memory.append_memory_history()
    memory.reset_memory_data()
