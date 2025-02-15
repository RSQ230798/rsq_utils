"""Tests for memory utilities."""
import unittest
from src.memory import Memory

class TestMemory(unittest.TestCase):
    """Test cases for memory utilities."""

    def test_memory_initialization(self):
        """Test Memory class initialization."""
        memory = Memory()
        self.assertIsNotNone(memory.start_memory)
        self.assertEqual(len(memory.memory_history), 1)
        self.assertIsNone(memory.current_memory)

    def test_memory_data_format(self):
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
        
        self.assertEqual(set(data.keys()), expected_keys)
        for value in data.values():
            self.assertIsInstance(value, float)
        self.assertGreaterEqual(data["system_memory_used_%"], 0)
        self.assertLessEqual(data["system_memory_used_%"], 100)

    def test_memory_history(self):
        """Test memory history tracking."""
        memory = Memory()
        initial_snapshot = memory.memory_history[0]
        
        # Add new snapshots
        memory.append_memory_history()
        memory.append_memory_history()
        
        self.assertEqual(len(memory.memory_history), 3)
        self.assertEqual(memory.memory_history[0], initial_snapshot)
        for snapshot in memory.memory_history:
            self.assertIsInstance(snapshot, dict)

    def test_memory_reset(self):
        """Test memory reset functionality."""
        memory = Memory()
        initial_snapshot = memory.memory_history[0]
        
        # Add snapshots and get current memory
        memory.append_memory_history()
        memory.get_current_memory()
        
        # Reset
        memory.reset_memory_data()
        
        self.assertEqual(len(memory.memory_history), 1)
        self.assertEqual(memory.memory_history[0], initial_snapshot)
        self.assertIsNone(memory.current_memory)

    def test_get_current_memory(self):
        """Test current memory retrieval."""
        memory = Memory()
        
        # First call
        data1 = memory.get_current_memory()
        self.assertEqual(memory.current_memory, data1)
        
        # Second call should update current_memory
        data2 = memory.get_current_memory()
        self.assertEqual(memory.current_memory, data2)

    def test_memory_error_handling(self):
        """Test error handling in memory operations."""
        memory = Memory()
        
        # Verify no exceptions are raised for normal operations
        try:
            memory.get_current_memory()
            memory.append_memory_history()
            memory.reset_memory_data()
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")

if __name__ == '__main__':
    unittest.main()
