"""Memory management utilities for monitoring system and process memory usage."""
from typing import Dict, List, Optional
import psutil

MemoryData = Dict[str, float]

class Memory:
    """Memory manager for tracking system and process memory usage over time.
    
    This class provides utilities to monitor memory usage of both the system and the current
    process. It can track memory usage over time by maintaining a history of measurements.
    
    Attributes:
        start_memory: Initial memory snapshot taken at instantiation
        memory_history: List of memory snapshots taken over time
        current_memory: Most recent memory snapshot (None until get_current_memory is called)
    """
    
    def __init__(self) -> None:
        """Initialize the memory manager with an initial memory snapshot."""
        self.start_memory: MemoryData = self.__get_memory_data()
        self.memory_history: List[MemoryData] = [self.start_memory]
        self.current_memory: Optional[MemoryData] = None
        
    def __get_memory_data(self) -> MemoryData:
        """Get current memory usage data for both system and process.
        
        Returns:
            Dictionary containing memory usage metrics in gigabytes and percentages.
            
        Raises:
            psutil.Error: If unable to access system or process memory information.
        """
        try:
            system_memory = psutil.virtual_memory()
            process_memory = psutil.Process()

            return {
                "system_memory_total_gb": system_memory.total / (1024 ** 3),
                "system_memory_used_gb": system_memory.used / (1024 ** 3),
                "system_memory_available_gb": system_memory.available / (1024 ** 3),
                "system_memory_used_%": system_memory.used / system_memory.total * 100,
                "process_memory_used_gb": process_memory.memory_info().rss / (1024 ** 3)
            }
        except psutil.Error as e:
            raise RuntimeError(f"Failed to get memory data: {str(e)}") from e

    def append_memory_history(self) -> None:
        """Add current memory snapshot to history."""
        self.memory_history.append(self.__get_memory_data())
    
    def reset_memory_data(self) -> None:
        """Reset memory history to initial state.
        
        Clears all memory history except the initial snapshot and resets current_memory.
        """
        self.memory_history = [self.start_memory]
        self.current_memory = None

    def get_current_memory(self) -> MemoryData:
        """Get current memory usage snapshot.
        
        Returns:
            Dictionary containing current memory usage metrics.
        """
        self.current_memory = self.__get_memory_data()
        return self.current_memory
