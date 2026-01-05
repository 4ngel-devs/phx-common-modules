"""Tests for DateUtils class."""

from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest

from sucrim.utils.date_utils import DateUtils, MEXICO_TIMEZONE


class TestDateUtils:
    """Test cases for DateUtils."""

    def test_now_returns_datetime_with_mexico_timezone(self):
        """Test that now() returns a datetime with Mexico timezone."""
        result = DateUtils.now()

        assert isinstance(result, datetime)
        assert result.tzinfo == MEXICO_TIMEZONE
        assert result.tzinfo is not None

    def test_today_returns_date(self):
        """Test that today() returns a date object."""
        result = DateUtils.today()

        assert isinstance(result, date)
        assert result == datetime.now(MEXICO_TIMEZONE).date()

    def test_now_and_today_are_consistent(self):
        """Test that now() and today() return consistent values."""
        now = DateUtils.now()
        today = DateUtils.today()

        assert now.date() == today

    def test_to_mexico_timezone_with_naive_datetime(self):
        """Test converting naive datetime to Mexico timezone."""
        naive_dt = datetime(2024, 1, 15, 12, 30, 0)
        result = DateUtils.to_mexico_timezone(naive_dt)

        assert result.tzinfo == MEXICO_TIMEZONE
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_to_mexico_timezone_with_utc_datetime(self):
        """Test converting UTC datetime to Mexico timezone."""
        utc_dt = datetime(2024, 1, 15, 18, 0, 0, tzinfo=ZoneInfo("UTC"))
        result = DateUtils.to_mexico_timezone(utc_dt)

        assert result.tzinfo == MEXICO_TIMEZONE
        # Mexico is UTC-6, so 18:00 UTC should be 12:00 Mexico time
        assert result.hour == 12

    def test_to_mexico_timezone_with_mexico_datetime(self):
        """Test converting datetime already in Mexico timezone."""
        mexico_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=MEXICO_TIMEZONE)
        result = DateUtils.to_mexico_timezone(mexico_dt)

        assert result.tzinfo == MEXICO_TIMEZONE
        assert result == mexico_dt

    def test_from_mexico_timezone_to_utc(self):
        """Test converting from Mexico timezone to UTC."""
        mexico_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=MEXICO_TIMEZONE)
        result = DateUtils.from_mexico_timezone(mexico_dt, ZoneInfo("UTC"))

        assert result.tzinfo == ZoneInfo("UTC")
        # Mexico is UTC-6, so 12:00 Mexico should be 18:00 UTC
        assert result.hour == 18

    def test_from_mexico_timezone_with_naive_datetime(self):
        """Test converting naive datetime assumed to be in Mexico timezone."""
        naive_dt = datetime(2024, 1, 15, 12, 0, 0)
        result = DateUtils.from_mexico_timezone(naive_dt, ZoneInfo("UTC"))

        assert result.tzinfo == ZoneInfo("UTC")
        assert result.hour == 18

    def test_from_mexico_timezone_with_string_timezone(self):
        """Test converting with string timezone identifier."""
        mexico_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=MEXICO_TIMEZONE)
        result = DateUtils.from_mexico_timezone(mexico_dt, "UTC")

        assert result.tzinfo == ZoneInfo("UTC")
        assert result.hour == 18

    def test_timezone_consistency(self):
        """Test that converting to and from Mexico timezone is consistent."""
        original = datetime(2024, 1, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC"))

        # Convert to Mexico
        mexico_dt = DateUtils.to_mexico_timezone(original)

        # Convert back to UTC
        back_to_utc = DateUtils.from_mexico_timezone(mexico_dt, ZoneInfo("UTC"))

        # Should be the same (within the same day)
        assert back_to_utc.date() == original.date()
        # The hour difference should be consistent (UTC-6 for Mexico)
        assert abs((back_to_utc - original).total_seconds()) < 3600  # Within 1 hour

