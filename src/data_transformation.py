from typing import List, TypeVar

T = TypeVar('T')

def list_batch_split(lst: List[T], batch_size: int = 100) -> List[List[T]]:
    """Split a list into batches of a specified size.
    
    Args:
        lst: The input list to be split into batches.
        batch_size: The maximum size of each batch. Defaults to 100.
    
    Returns:
        A list of lists, where each inner list is a batch of the original list.
    
    Raises:
        ValueError: If the input is not a list.
        ValueError: If batch_size is less than 1.
    """
    if not isinstance(lst, list):
        raise ValueError("Input must be a list")
    if batch_size < 1:
        raise ValueError("Batch size must be at least 1")
        
    return [lst[i:i + batch_size] for i in range(0, len(lst), batch_size)]
