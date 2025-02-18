"""Tests for time utilities."""
from datetime import datetime, timedelta
import time
import unittest
from src.rsq_utils.time import (
    Timer,
    Stopwatch,
    DateRange,
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
        timer.start(10)
        time.sleep(1)
        time_remaining = timer.get_time_remaining()
        self.assertGreaterEqual(time_remaining, 8)

    def test_timer_not_started(self):
        """Test Timer error when not started."""
        timer = Timer()
        with self.assertRaisesRegex(ValueError, "Timer not started"):
            timer.get_time_remaining()

    def test_stopwatch(self):
        """Test BatchTimer functionality."""
        stopwatch = Stopwatch()
        stopwatch.start()
        time.sleep(1)
        stopwatch.stop()
        
        self.assertGreaterEqual(stopwatch.time_elapsed, 1)

    def test_stopwatch_error(self):
        """Test BatchTimer error states."""
        stopwatch = Stopwatch()
        with self.assertRaises(ValueError):
            stopwatch.stop()  # Not started or stopped

    def test_date_range_2_dates(self):
        """Test basic DateRange functionality."""
        date_range = DateRange()
        date_range.generate_date_range(start_date="2024-01-01", end_date="2024-01-05", step=1)
        expected = [
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
            "2024-01-04",
            "2024-01-05"
        ]
        self.assertEqual(date_range.date_range, expected)

    def test_date_range_with_number_of_days(self):
        start_date = "2024-01-01"
        number_of_days = 3
        date_range = DateRange()
        end_date = "2024-01-04"

        expected = [
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
            "2024-01-04"
        ]

        date_range.generate_date_range(start_date=start_date, number_of_days=number_of_days)
        self.assertEqual(date_range.date_range, expected)

        date_range.generate_date_range(end_date=end_date, number_of_days=number_of_days)
        self.assertEqual(date_range.date_range, expected)

    def test_date_range_with_step(self):
        start_date = "2024-01-01"
        number_of_days = 3
        date_range = DateRange()
        end_date = "2024-01-04"
        step = 2

        expected_forward = [
            "2024-01-01",
            "2024-01-03"
        ]

        expected_backward = [
            "2024-01-02",
            "2024-01-04"
        ]

        date_range.generate_date_range(start_date=start_date, number_of_days=number_of_days, step=step, include_edge_dates=False)
        self.assertEqual(date_range.date_range, expected_forward)

        date_range.generate_date_range(start_date=start_date, number_of_days=number_of_days, step=step, include_edge_dates=True)
        self.assertEqual(date_range.date_range, expected_forward + ["2024-01-04"])

        date_range.generate_date_range(end_date=end_date, number_of_days=number_of_days, step=step, include_edge_dates=False)
        self.assertEqual(date_range.date_range, expected_backward)

        date_range.generate_date_range(end_date=end_date, number_of_days=number_of_days, step=step, include_edge_dates=True)
        self.assertEqual(date_range.date_range,  ["2024-01-01"] + expected_backward)

    def test_date_range_pair_dates(self):
        """Test DateRange pair_dates method."""
        start_date = "2024-01-01"
        number_of_days = 2
        date_range = DateRange()

        date_range.generate_date_range(start_date=start_date, number_of_days=number_of_days)
        pairs = date_range.pair_dates()
        expected = [
            ("2024-01-01", "2024-01-02"),
            ("2024-01-02", "2024-01-03")
        ]
        self.assertEqual(pairs, expected)

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
