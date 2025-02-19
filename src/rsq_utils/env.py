"""Environment variable utilities."""
from typing import Optional, Union
from pathlib import Path
from dotenv import load_dotenv as _load_dotenv

def load_dotenv(dotenv_path: Optional[Union[str, Path]] = None) -> bool:
    """Load environment variables from a .env file.
    
    Args:
        dotenv_path: Path to the .env file. If not provided, defaults to '.env' in the current directory.
    
    Returns:
        bool: True if the .env file was loaded successfully, False otherwise.
        
    Raises:
        ValueError: If the provided path does not exist.
    """
    if dotenv_path is None:
        dotenv_path = '.env'
        
    path = Path(dotenv_path)
    if not path.is_file():
        raise ValueError(f"Environment file not found at: {path}")
        
    return _load_dotenv(path)
