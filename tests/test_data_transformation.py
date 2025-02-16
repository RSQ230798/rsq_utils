"""Tests for data transformation utilities."""
import unittest
from src.data_transformation import list_batch_split

class TestDataTransformation(unittest.TestCase):
    """Test cases for data transformation utilities."""

    def test_list_batch_split_valid(self):
        """Test list_batch_split with valid inputs."""
        # Test with default batch size
        input_list = list(range(250))
        result = list_batch_split(input_list)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0]), 100)
        self.assertEqual(len(result[1]), 100)
        self.assertEqual(len(result[2]), 50)
        
        # Test with custom batch size
        result = list_batch_split(input_list, batch_size=50)
        self.assertEqual(len(result), 5)
        for batch in result:
            self.assertEqual(len(batch), 50)
        
    def test_list_batch_split_empty(self):
        """Test list_batch_split with empty list."""
        result = list_batch_split([])
        self.assertEqual(result, [])

    def test_list_batch_split_single_batch(self):
        """Test list_batch_split when input is smaller than batch size."""
        input_list = list(range(50))
        result = list_batch_split(input_list, batch_size=100)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], input_list)

    def test_list_batch_split_invalid_input(self):
        """Test list_batch_split with invalid inputs."""
        # Test with non-list input
        with self.assertRaisesRegex(ValueError, "Input must be a list"):
            list_batch_split("not a list")
        
        # Test with invalid batch size
        with self.assertRaisesRegex(ValueError, "Batch size must be at least 1"):
            list_batch_split([1, 2, 3], batch_size=0)

if __name__ == '__main__':
    unittest.main()
