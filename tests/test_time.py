"""Tests for time utilities."""
from datetime import datetime, timedelta
import time
import unittest
from src.time import (
    Timer,
    BatchTimer,
    DateRange,
    HistoricalDates,
    transform_date_to_string,
    transform_date_to_datetime,
    days_between_dates,
    today,
    yesterday,
    is_date_file,
    sort_dates_descending,
    find_last_update_file
)

class TestTime(unittest.TestCase):
    """Test cases for time utilities."""

    def test_timer_basic(self):
        """Test basic Timer functionality."""
        timer = Timer()
        timer.start()
        time.sleep(1)
        timer.stop()
        self.assertGreaterEqual(timer.time_elapsed, 1)

    def test_timer_not_started(self):
        """Test Timer error when not started."""
        timer = Timer()
        with self.assertRaisesRegex(ValueError, "Timer not started"):
            timer.stop()

    def test_batch_timer(self):
        """Test BatchTimer functionality."""
        timer = BatchTimer(2)
        timer.start()
        time.sleep(1)
        timer.stop()
        
        start_time = time.time()
        timer.wait()
        elapsed = time.time() - start_time
        self.assertGreaterEqual(elapsed, 1)  # Should wait remaining 1 second

    def test_batch_timer_error(self):
        """Test BatchTimer error states."""
        timer = BatchTimer(2)
        with self.assertRaises(ValueError):
            timer.wait()  # Not started or stopped

    def test_date_range_basic(self):
        """Test basic DateRange functionality."""
        date_range = DateRange("2024-01-01", "2024-01-05")
        expected = [
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
            "2024-01-04",
            "2024-01-05"
        ]
        self.assertEqual(date_range.date_range, expected)

    def test_date_range_with_step(self):
        """Test DateRange with custom step."""
        date_range = DateRange("2024-01-01", "2024-01-05", step=2)
        expected = [
            "2024-01-01",
            "2024-01-03",
            "2024-01-05"
        ]
        self.assertEqual(date_range.date_range, expected)

    def test_date_range_pair_dates(self):
        """Test DateRange pair_dates method."""
        date_range = DateRange("2024-01-01", "2024-01-03")
        pairs = date_range.pair_dates()
        expected = [
            ("2024-01-01", "2024-01-02"),
            ("2024-01-02", "2024-01-03")
        ]
        self.assertEqual(pairs, expected)

    def test_historical_dates(self):
        """Test HistoricalDates functionality."""
        historical = HistoricalDates()
        dates = historical.generate_historic_dates(3)
        self.assertEqual(len(dates), 3)
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        two_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        
        self.assertEqual(dates, [today_str, yesterday_str, two_days_ago])

    def test_transform_date_functions(self):
        """Test date transformation functions."""
        date_str = "2024-01-01"
        date_obj = datetime(2024, 1, 1)
        
        self.assertEqual(transform_date_to_string(date_str), date_str)
        self.assertEqual(transform_date_to_string(date_obj), date_str)
        self.assertEqual(transform_date_to_datetime(date_str), date_obj)
        self.assertEqual(transform_date_to_datetime(date_obj), date_obj)
        
        with self.assertRaises(ValueError):
            transform_date_to_string(123)
        with self.assertRaises(ValueError):
            transform_date_to_datetime(123)

    def test_days_between_dates(self):
        """Test days_between_dates function."""
        self.assertEqual(days_between_dates("2024-01-01", "2024-01-05"), 4)
        self.assertEqual(days_between_dates("2024-01-05", "2024-01-01"), 4)  # Absolute value
        self.assertEqual(
            days_between_dates(
                datetime(2024, 1, 1),
                datetime(2024, 1, 5)
            ),
            4
        )

    def test_today_yesterday(self):
        """Test today and yesterday functions."""
        today_date = datetime.now()
        yesterday_date = today_date - timedelta(days=1)
        
        self.assertEqual(today(), today_date.strftime("%Y-%m-%d"))
        self.assertEqual(yesterday(), yesterday_date.strftime("%Y-%m-%d"))

    def test_is_date_file(self):
        """Test is_date_file function."""
        self.assertTrue(is_date_file("2024-01-01.txt"))
        self.assertFalse(is_date_file("not-a-date.txt"))
        self.assertFalse(is_date_file("2024-13-01.txt"))  # Invalid month

    def test_sort_dates_descending(self):
        """Test sort_dates_descending function."""
        dates = ["2024-01-01", "2024-01-03", "2024-01-02"]
        expected = ["2024-01-03", "2024-01-02", "2024-01-01"]
        self.assertEqual(sort_dates_descending(dates), expected)

    def test_find_last_update_file(self):
        """Test find_last_update_file function."""
        files = [
            "2024-01-01.txt",
            "2024-01-03.txt",
            "2024-01-02.txt",
            "not-a-date.txt"
        ]
        self.assertEqual(find_last_update_file(files), "2024-01-03.txt")
        
        with self.assertRaises(IndexError):
            find_last_update_file(["not-a-date.txt"])

if __name__ == '__main__':
    unittest.main()
