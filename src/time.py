"""Time utilities for date manipulation and timing operations."""
from datetime import datetime, timedelta
import time
from typing import List, Optional, Tuple, Union

DateType = Union[str, datetime]

class HistoricalDates:
    """Generate historical date sequences."""
    
    def generate_historic_dates(self, number_of_previous_days: int) -> List[str]:
        """Generate a list of dates from today going back a specified number of days.
        
        Args:
            number_of_previous_days: Number of days to go back.
            
        Returns:
            List of dates in YYYY-MM-DD format.
        """
        return [transform_date_to_string(datetime.now() - timedelta(days=i)) 
                for i in range(number_of_previous_days)]

    def generate_dates_from_previous_date(self, previous_date: DateType) -> List[str]:
        """Generate a list of dates from a previous date up to today.
        
        Args:
            previous_date: Starting date.
            
        Returns:
            List of dates in YYYY-MM-DD format.
        """
        previous_date = transform_date_to_datetime(previous_date)
        current_date = datetime.now()
        delta = current_date - previous_date
        return [transform_date_to_string(current_date - timedelta(days=i)) 
                for i in range(delta.days)]

class Timer:
    """Simple timer for measuring elapsed time."""
    
    def __init__(self) -> None:
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.time_elapsed: Optional[int] = None

    def start(self) -> None:
        """Start the timer."""
        self.start_time = datetime.now()

    def stop(self) -> None:
        """Stop the timer and calculate elapsed time.
        
        Raises:
            ValueError: If timer was not started.
        """
        if self.start_time:
            self.end_time = datetime.now()
            self.time_elapsed = (self.end_time - self.start_time).seconds
        else:
            raise ValueError("Timer not started")
        
class BatchTimer(Timer):
    """Timer with batch processing delay capabilities."""
    
    def __init__(self, time_between_batches: int) -> None:
        """Initialize with specified delay between batches.
        
        Args:
            time_between_batches: Seconds to wait between batches.
        """
        self.time_between_batches = time_between_batches
        super().__init__()

    def wait(self) -> None:
        """Wait remaining time if less than batch interval has passed.
        
        Raises:
            ValueError: If timer was not started or stopped.
        """
        if self.start_time is not None and self.end_time is not None and self.time_elapsed is not None:
            if self.time_elapsed <= self.time_between_batches:
                time.sleep(self.time_between_batches - self.time_elapsed)
        else:
            raise ValueError("Timer either not started or ended")

def is_date_file(file_name: str) -> bool:
    """Check if a filename represents a date (YYYY-MM-DD format).
    
    Args:
        file_name: Name of file to check.
        
    Returns:
        True if filename is a valid date, False otherwise.
    """
    try:
        datetime.strptime(file_name.split(".")[0], "%Y-%m-%d")
        return True
    except ValueError:
        return False

def sort_dates_descending(dates: List[str]) -> List[str]:
    """Sort dates in descending order.
    
    Args:
        dates: List of date strings.
        
    Returns:
        Sorted list of dates.
    """
    return sorted(dates, reverse=True)

def find_last_update_file(list_of_file_names: List[str]) -> str:
    """Find most recent date-formatted filename.
    
    Args:
        list_of_file_names: List of filenames to check.
        
    Returns:
        Most recent date filename.
        
    Raises:
        IndexError: If no date files found.
    """
    date_files = list(filter(is_date_file, list_of_file_names))
    if not date_files:
        raise IndexError("No date files found")
    date_files = sort_dates_descending(date_files)
    return date_files[0]

def transform_date_to_string(date: DateType) -> str:
    """Convert a date to string format (YYYY-MM-DD).
    
    Args:
        date: Date to convert.
        
    Returns:
        Date string in YYYY-MM-DD format.
        
    Raises:
        ValueError: If date is not str or datetime.
    """
    if isinstance(date, str):
        return date
    elif isinstance(date, datetime):
        return date.strftime("%Y-%m-%d")
    else:
        raise ValueError("Invalid date format: must be either string or datetime object")

def transform_date_to_datetime(date: DateType) -> datetime:
    """Convert a date to datetime object.
    
    Args:
        date: Date to convert.
        
    Returns:
        Datetime object.
        
    Raises:
        ValueError: If date is not str or datetime.
    """
    if isinstance(date, datetime):
        return date
    elif isinstance(date, str):
        return datetime.strptime(date, "%Y-%m-%d")
    else:
        raise ValueError("Invalid date format: must be either string or datetime object")

def days_between_dates(date1: DateType, date2: DateType) -> int:
    """Calculate number of days between two dates.
    
    Args:
        date1: First date.
        date2: Second date.
        
    Returns:
        Number of days between dates.
    """
    date1 = transform_date_to_datetime(date1)
    date2 = transform_date_to_datetime(date2)
    return abs((date2 - date1).days)

def today() -> str:
    """Get today's date in YYYY-MM-DD format.
    
    Returns:
        Today's date string.
    """
    return datetime.now().strftime("%Y-%m-%d")

def yesterday() -> str:
    """Get yesterday's date in YYYY-MM-DD format.
    
    Returns:
        Yesterday's date string.
    """
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

class DateRange:
    """Generate sequences of dates within a range."""
    
    def __init__(self, start_date: DateType, end_date: DateType, step: int = 1) -> None:
        """Initialize with date range parameters.
        
        Args:
            start_date: Starting date.
            end_date: Ending date.
            step: Days between each date in sequence.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.step = step
        self.date_range = self.__generate_date_range()

    def __generate_date_range(self) -> List[str]:
        """Generate list of dates in the range.
        
        Returns:
            List of dates in YYYY-MM-DD format.
        """
        start_date = transform_date_to_datetime(self.start_date)
        end_date = transform_date_to_datetime(self.end_date)
        
        date_range = [
            transform_date_to_string(start_date + timedelta(days=i))
            for i in range(0, days_between_dates(start_date, end_date) + 1, self.step)
        ]

        if date_range[-1] != transform_date_to_string(end_date):
            date_range.append(transform_date_to_string(end_date))

        return date_range
    
    def pair_dates(self) -> List[Tuple[str, str]]:
        """Create pairs of consecutive dates from the range.
        
        Returns:
            List of date pairs.
        """
        return list(zip(self.date_range[:-1], self.date_range[1:]))
