# test_secs_between.py
# unit tests for secs_between function
# Copyright (C) 2026 University of California
# -----------------------------------------------------------------------------
# This information is free; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This work is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# -----------------------------------------------------------------------------
from datetime import datetime


import iwfm


class TestSecsBetween:
    """Tests for the secs_between function."""

    def test_one_second(self):
        """Test difference of one second."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 0, 0, 1)

        result = iwfm.secs_between(start, end)

        assert result == 1.0

    def test_one_minute(self):
        """Test difference of one minute (60 seconds)."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 0, 1, 0)

        result = iwfm.secs_between(start, end)

        assert result == 60.0

    def test_one_hour(self):
        """Test difference of one hour (3600 seconds)."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 1, 0, 0)

        result = iwfm.secs_between(start, end)

        assert result == 3600.0

    def test_combined_hours_minutes_seconds(self):
        """Test combined hours, minutes, and seconds."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 2, 30, 45)

        result = iwfm.secs_between(start, end)

        # 2 hours = 7200, 30 minutes = 1800, 45 seconds = 45
        expected = 2 * 3600 + 30 * 60 + 45
        assert result == expected

    def test_zero_difference(self):
        """Test same start and end time (zero seconds)."""
        start = datetime(2000, 1, 1, 12, 30, 45)
        end = datetime(2000, 1, 1, 12, 30, 45)

        result = iwfm.secs_between(start, end)

        assert result == 0.0

    def test_returns_float(self):
        """Test that function returns a float."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 0, 0, 30)

        result = iwfm.secs_between(start, end)

        assert isinstance(result, float)

    def test_fractional_seconds(self):
        """Test difference with fractional seconds (microseconds)."""
        start = datetime(2000, 1, 1, 0, 0, 0, 0)
        end = datetime(2000, 1, 1, 0, 0, 1, 500000)  # 1.5 seconds

        result = iwfm.secs_between(start, end)

        # Result is rounded to 1 decimal place
        assert abs(result - 1.5) < 0.1

    def test_multiple_hours(self):
        """Test difference of multiple hours."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 5, 0, 0)

        result = iwfm.secs_between(start, end)

        assert result == 5 * 3600

    def test_across_midnight(self):
        """Test difference across midnight (within same calculation)."""
        start = datetime(2000, 1, 1, 23, 0, 0)
        end = datetime(2000, 1, 2, 1, 0, 0)

        result = iwfm.secs_between(start, end)

        # 2 hours = 7200 seconds
        assert result == 7200.0

    def test_one_day(self):
        """Test difference of exactly one day."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 2, 0, 0, 0)

        result = iwfm.secs_between(start, end)

        # 24 hours = 86400 seconds
        assert result == 86400.0

    def test_multiple_days(self):
        """Test difference of multiple days."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 4, 0, 0, 0)

        result = iwfm.secs_between(start, end)

        # 3 days = 72 hours = 259200 seconds
        assert result == 3 * 24 * 3600

    def test_30_seconds(self):
        """Test difference of 30 seconds."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 0, 0, 30)

        result = iwfm.secs_between(start, end)

        assert result == 30.0

    def test_90_seconds(self):
        """Test difference of 90 seconds (1 min 30 sec)."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 0, 1, 30)

        result = iwfm.secs_between(start, end)

        assert result == 90.0

    def test_specific_times(self):
        """Test with specific datetime values."""
        start = datetime(2020, 6, 15, 10, 30, 0)
        end = datetime(2020, 6, 15, 12, 45, 30)

        result = iwfm.secs_between(start, end)

        # 2 hours 15 minutes 30 seconds
        expected = 2 * 3600 + 15 * 60 + 30
        assert result == expected

    def test_year_boundary(self):
        """Test difference across year boundary."""
        start = datetime(2000, 12, 31, 23, 59, 0)
        end = datetime(2001, 1, 1, 0, 1, 0)

        result = iwfm.secs_between(start, end)

        # 2 minutes = 120 seconds
        assert result == 120.0

    def test_leap_year(self):
        """Test during leap year."""
        start = datetime(2000, 2, 28, 0, 0, 0)
        end = datetime(2000, 2, 29, 0, 0, 0)

        result = iwfm.secs_between(start, end)

        # 1 day = 86400 seconds
        assert result == 86400.0

    def test_small_difference(self):
        """Test very small time difference."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 0, 0, 0, 100000)  # 0.1 seconds

        result = iwfm.secs_between(start, end)

        assert abs(result - 0.1) < 0.1

    def test_12_hour_difference(self):
        """Test 12 hour difference."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 1, 12, 0, 0)

        result = iwfm.secs_between(start, end)

        assert result == 12 * 3600

    def test_week_difference(self):
        """Test one week difference."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 8, 0, 0, 0)

        result = iwfm.secs_between(start, end)

        # 7 days = 604800 seconds
        assert result == 7 * 24 * 3600


class TestSecsBetweenEdgeCases:
    """Edge case tests for secs_between function."""

    def test_datetime_with_microseconds(self):
        """Test datetime objects with microseconds."""
        start = datetime(2000, 1, 1, 0, 0, 0, 0)
        end = datetime(2000, 1, 1, 0, 0, 2, 300000)  # 2.3 seconds

        result = iwfm.secs_between(start, end)

        # Should be approximately 2.3, rounded to 1 decimal
        assert abs(result - 2.3) < 0.1

    def test_end_of_month(self):
        """Test across end of month."""
        start = datetime(2000, 1, 31, 12, 0, 0)
        end = datetime(2000, 2, 1, 12, 0, 0)

        result = iwfm.secs_between(start, end)

        # 1 day = 86400 seconds
        assert result == 86400.0

    def test_different_years(self):
        """Test dates in different years."""
        start = datetime(1999, 12, 31, 0, 0, 0)
        end = datetime(2000, 1, 1, 0, 0, 0)

        result = iwfm.secs_between(start, end)

        # 1 day = 86400 seconds
        assert result == 86400.0

    def test_same_day_different_times(self):
        """Test same day with different times."""
        start = datetime(2020, 5, 15, 8, 30, 0)
        end = datetime(2020, 5, 15, 17, 45, 30)

        result = iwfm.secs_between(start, end)

        # 9 hours 15 minutes 30 seconds
        expected = 9 * 3600 + 15 * 60 + 30
        assert result == expected

    def test_long_duration(self):
        """Test longer duration (30 days)."""
        start = datetime(2000, 1, 1, 0, 0, 0)
        end = datetime(2000, 1, 31, 0, 0, 0)

        result = iwfm.secs_between(start, end)

        # 30 days
        expected = 30 * 24 * 3600
        assert result == expected
