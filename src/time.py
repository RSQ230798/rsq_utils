from datetime import datetime, timedelta
import time
from typing import List, Optional, Tuple, Union

DateType = Union[str, datetime]
DateRangeType = List[DateType]

# Objects
class Stopwatch:
    """
    Simple stopwatch for measuring elapsed time.
    """
    def __init__(self) -> None:
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.time_elapsed: Optional[float] = None

    def start(self) -> None:
        self.start_time = time.time()
        self.end_time = None
        self.time_elapsed = None

    def stop(self) -> None:
        if self.start_time:
            self.end_time = time.time()
            self.time_elapsed = self.end_time - self.start_time
        else:
            raise ValueError("Stopwatch not started")
    
    def get_time_elapsed(self) -> float:
        if self.start_time:
            current_time = time.time()
            self.time_elapsed = current_time - self.start_time
            return self.time_elapsed
        
        else:
            raise ValueError("Stopwatch not started")

class Timer:
    """Simple timer for measuring elapsed time."""
    
    def __init__(self) -> None:
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start(self, length: int) -> None:
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=length)
        
    def get_time_remaining(self) -> int:
        if self.start_time and self.end_time:
            time_remaining = (self.end_time - datetime.now()).seconds
            return max(time_remaining, 0)
        else:
            raise ValueError("Timer not started")

class DateRange:
    """
    Factory that generates DateRange objects. 
    """
    def __init__(self) -> None:
        self.date_range: DateRangeType = []
        self.start_date: DateType = None
        self.end_date: DateType = None
        self.number_of_days: int = None
        self.begining_point: str = "start_date"
        self.step: int = 1
        self.include_edge_dates: bool = True

    def generate_date_range(self, 
                            start_date: DateType= None, 
                            end_date: DateType = None, 
                            number_of_days: int = None,
                            step: int = 1, 
                            include_edge_dates: bool = True
                            ) -> None:
        """
        Generate a range of dates based on:
        1) start date and an end date
        2) start date and a number of days
        3) end date and a number of days
        """
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_days = number_of_days
        self.step = step
        self.include_edge_dates = include_edge_dates
        self.begining_point = None

        self._validate_inputs()
        self._clean_inputs()
        self._generate_date_range()
        self._include_edge_dates()

    
    def _validate_inputs(self) -> None:
        if not self.start_date and not self.end_date:
            raise ValueError("At least one of start_date, end_date, must be provided")
        
        elif self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValueError("start_date must be before end_date")

        else:
            if not self.number_of_days:
                raise ValueError("number_of_days must be provided if only one date is given")
            else:
                if self.number_of_days < 0:
                    raise ValueError("number_of_days must be a positive integer")        

        if self.step < 1 or not isinstance(self.step, int):
            raise ValueError("step must be a positive integer")

    def _clean_inputs(self) -> None:
        if self.start_date and self.number_of_days:
            self.begining_point = "start_date"
            self.start_date = transform_date_to_datetime(self.start_date)
            self.end_date = self.start_date + timedelta(days=self.number_of_days)

        elif self.end_date and self.number_of_days:
            self.begining_point = "end_date"
            self.end_date = transform_date_to_datetime(self.end_date)
            self.start_date = self.end_date - timedelta(days=self.number_of_days)
        
        elif self.start_date and self.end_date:
            self.begining_point = "start_date"
            self.start_date = transform_date_to_datetime(self.start_date)
            self.end_date = transform_date_to_datetime(self.end_date)
            self.number_of_days = days_between_dates(self.start_date, self.end_date)

    def _generate_date_range(self) -> DateRangeType:
        if self.begining_point == "start_date":    
            date_range = [transform_date_to_string(self.start_date + timedelta(days=d)) for d in range(0, days_between_dates(self.start_date, self.end_date) + 1, self.step)]
            self.date_range = sort_dates_ascending(date_range)

        elif self.begining_point == "end_date":
            date_range = [transform_date_to_string(self.end_date - timedelta(days=d)) for d in range(0, days_between_dates(self.start_date, self.end_date) + 1, self.step)]
            self.date_range = sort_dates_ascending(date_range)

    def _include_edge_dates(self) -> None:
        if self.include_edge_dates:
            end_date = transform_date_to_string(self.end_date)
            start_date = transform_date_to_string(self.start_date)

            if self.date_range[-1] != end_date:
                self.date_range.append(end_date)

            if self.date_range[0] != start_date:
                self.date_range.insert(0, start_date)

    def pair_dates(self) -> List[Tuple[str, str]]:
        if self.date_range:
            return list(zip(self.date_range[:-1], self.date_range[1:]))
        else:
            raise ValueError("Date range not generated")
    
# Helper Functions
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

def sort_dates_descending(dates: DateRangeType) -> DateRangeType:
    """Sort dates in descending order.
    
    Args:
        dates: List of date strings.
        
    Returns:
        Sorted list of dates.
    """
    return sorted(dates, reverse=True)

def sort_dates_ascending(dates: DateRangeType) -> DateRangeType:
    """Sort dates in ascending order.
    
    Args:
        dates: List of date strings.
        
    Returns:
        Sorted list of dates.
    """
    return sorted(dates)

def find_last_update_file(list_of_file_names: List[str]) -> str:
    """Find most recent date-formatted filename.
    
    Args:
        list_of_file_names: List of filenames to check.
        
    Returns:
        Most recent date filename.
        
    Raises:
        IndexError: If no date files found.
    """
    date_files: DateRangeType = list(filter(is_date_file, list_of_file_names))
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
    """
    Get today's date in YYYY-MM-DD format.
    """
    return datetime.now().strftime("%Y-%m-%d")

def yesterday() -> str:
    """
    Get yesterday's date in YYYY-MM-DD
    """
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
