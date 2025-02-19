"""Tests for environment variable utilities."""
import os
import pytest
from pathlib import Path
import tempfile
from src.rsq_utils.env import load_dotenv
import shutil

@pytest.fixture
def env_setup():
    """Set up test environment."""
    # Store original environment
    original_env = dict(os.environ)
    original_dir = os.getcwd()
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    yield temp_dir
    
    # Cleanup
    os.environ.clear()
    os.environ.update(original_env)
    os.chdir(original_dir)
    shutil.rmtree(temp_dir)

def test_load_dotenv_default_path(env_setup):
    """Test load_dotenv with default path."""
    temp_dir = env_setup
    # Create a temporary .env file
    env_file = Path(temp_dir) / ".env"
    env_file.write_text("TEST_VAR=test_value")
    
    # Change to temp directory and load env
    os.chdir(temp_dir)
    assert load_dotenv() is True
    assert os.getenv("TEST_VAR") == "test_value"

def test_load_dotenv_custom_path(env_setup):
    """Test load_dotenv with custom path."""
    temp_dir = env_setup
    # Create a temporary .env file
    env_file = Path(temp_dir) / "custom.env"
    env_file.write_text("CUSTOM_VAR=custom_value")
    
    assert load_dotenv(env_file) is True
    assert os.getenv("CUSTOM_VAR") == "custom_value"

def test_load_dotenv_nonexistent_file():
    """Test load_dotenv with nonexistent file."""
    with pytest.raises(ValueError):
        load_dotenv("nonexistent.env")

def test_load_dotenv_invalid_path_type():
    """Test load_dotenv with invalid path type."""
    with pytest.raises(TypeError):
        load_dotenv(123)  # type: ignore
