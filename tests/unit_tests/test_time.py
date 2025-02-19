"""Tests for time utilities."""
from datetime import datetime, timedelta
import time
import pytest
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

def test_timer_basic():
    """Test basic Timer functionality."""
    timer = Timer()
    timer.start(10)
    time.sleep(1)
    time_remaining = timer.get_time_remaining()
    assert time_remaining >= 8

def test_timer_not_started():
    """Test Timer error when not started."""
    timer = Timer()
    with pytest.raises(ValueError, match="Timer not started"):
        timer.get_time_remaining()

def test_stopwatch():
    """Test BatchTimer functionality."""
    stopwatch = Stopwatch()
    stopwatch.start()
    time.sleep(1)
    stopwatch.stop()
    
    assert stopwatch.time_elapsed >= 1

def test_stopwatch_error():
    """Test BatchTimer error states."""
    stopwatch = Stopwatch()
    with pytest.raises(ValueError):
        stopwatch.stop()  # Not started or stopped

def test_date_range_2_dates():
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
    assert date_range.date_range == expected

def test_date_range_with_number_of_days():
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
    assert date_range.date_range == expected

    date_range.generate_date_range(end_date=end_date, number_of_days=number_of_days)
    assert date_range.date_range == expected

def test_date_range_with_step():
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
    assert date_range.date_range == expected_forward

    date_range.generate_date_range(start_date=start_date, number_of_days=number_of_days, step=step, include_edge_dates=True)
    assert date_range.date_range == expected_forward + ["2024-01-04"]

    date_range.generate_date_range(end_date=end_date, number_of_days=number_of_days, step=step, include_edge_dates=False)
    assert date_range.date_range == expected_backward

    date_range.generate_date_range(end_date=end_date, number_of_days=number_of_days, step=step, include_edge_dates=True)
    assert date_range.date_range == ["2024-01-01"] + expected_backward

def test_date_range_pair_dates():
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
    assert pairs == expected

def test_transform_date_functions():
    """Test date transformation functions."""
    date_str = "2024-01-01"
    date_obj = datetime(2024, 1, 1)
    
    assert transform_date_to_string(date_str) == date_str
    assert transform_date_to_string(date_obj) == date_str
    assert transform_date_to_datetime(date_str) == date_obj
    assert transform_date_to_datetime(date_obj) == date_obj
    
    with pytest.raises(ValueError):
        transform_date_to_string(123)
    with pytest.raises(ValueError):
        transform_date_to_datetime(123)

def test_days_between_dates():
    """Test days_between_dates function."""
    assert days_between_dates("2024-01-01", "2024-01-05") == 4
    assert days_between_dates("2024-01-05", "2024-01-01") == 4  # Absolute value
    assert days_between_dates(
        datetime(2024, 1, 1),
        datetime(2024, 1, 5)
    ) == 4

def test_today_yesterday():
    """Test today and yesterday functions."""
    today_date = datetime.now()
    yesterday_date = today_date - timedelta(days=1)
    
    assert today() == today_date.strftime("%Y-%m-%d")
    assert yesterday() == yesterday_date.strftime("%Y-%m-%d")

def test_is_date_file():
    """Test is_date_file function."""
    assert is_date_file("2024-01-01.txt") is True
    assert is_date_file("not-a-date.txt") is False
    assert is_date_file("2024-13-01.txt") is False  # Invalid month

def test_sort_dates_descending():
    """Test sort_dates_descending function."""
    dates = ["2024-01-01", "2024-01-03", "2024-01-02"]
    expected = ["2024-01-03", "2024-01-02", "2024-01-01"]
    assert sort_dates_descending(dates) == expected

def test_find_last_update_file():
    """Test find_last_update_file function."""
    files = [
        "2024-01-01.txt",
        "2024-01-03.txt",
        "2024-01-02.txt",
        "not-a-date.txt"
    ]
    assert find_last_update_file(files) == "2024-01-03.txt"
    
    with pytest.raises(IndexError):
        find_last_update_file(["not-a-date.txt"])
