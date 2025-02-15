"""Tests for environment variable utilities."""
import os
import unittest
from pathlib import Path
import tempfile
from src.env import load_dotenv
import shutil

class TestEnv(unittest.TestCase):
    """Test cases for environment variable utilities."""
    
    def setUp(self):
        """Set up test environment."""
        # Store original environment
        self.original_env = dict(os.environ)
        self.original_dir = os.getcwd()
        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)
        # Restore original directory
        os.chdir(self.original_dir)
        # Clean up temp files
        shutil.rmtree(self.temp_dir)

    def test_load_dotenv_default_path(self):
        """Test load_dotenv with default path."""
        # Create a temporary .env file
        env_file = Path(self.temp_dir) / ".env"
        env_file.write_text("TEST_VAR=test_value")
        
        # Change to temp directory and load env
        os.chdir(self.temp_dir)
        self.assertTrue(load_dotenv())
        self.assertEqual(os.getenv("TEST_VAR"), "test_value")

    def test_load_dotenv_custom_path(self):
        """Test load_dotenv with custom path."""
        # Create a temporary .env file
        env_file = Path(self.temp_dir) / "custom.env"
        env_file.write_text("CUSTOM_VAR=custom_value")
        
        self.assertTrue(load_dotenv(env_file))
        self.assertEqual(os.getenv("CUSTOM_VAR"), "custom_value")

    def test_load_dotenv_nonexistent_file(self):
        """Test load_dotenv with nonexistent file."""
        with self.assertRaises(ValueError):
            load_dotenv("nonexistent.env")

    def test_load_dotenv_invalid_path_type(self):
        """Test load_dotenv with invalid path type."""
        with self.assertRaises(TypeError):
            load_dotenv(123)  # type: ignore

if __name__ == '__main__':
    unittest.main()
