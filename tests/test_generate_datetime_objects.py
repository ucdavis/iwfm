# test_generate_datetime_objects.py
# Unit tests for the generate_datetime_objects function in the iwfm package
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

import pytest
from datetime import datetime, timedelta

import iwfm


class TestGenerateDatetimeObjectsFunctionExists:
    """Test that the generate_datetime_objects function exists and is callable."""

    def test_generate_datetime_objects_exists(self):
        """Test that generate_datetime_objects function exists in the iwfm module."""
        assert hasattr(iwfm, 'generate_datetime_objects')
        assert callable(getattr(iwfm, 'generate_datetime_objects'))


class TestGenerateDatetimeObjectsReturnType:
    """Test the return type of generate_datetime_objects."""

    def test_returns_list(self):
        """Test that generate_datetime_objects returns a list."""
        result = iwfm.generate_datetime_objects(
            "10/31/1973_24:00", 5, 1.0, "1MON"
        )
        assert isinstance(result, list)

    def test_returns_correct_length(self):
        """Test that returned list has correct number of elements."""
        n_steps = 12
        result = iwfm.generate_datetime_objects(
            "10/31/1973_24:00", n_steps, 1.0, "1MON"
        )
        assert len(result) == n_steps

    def test_returns_datetime_objects_monthly(self):
        """Test that returned list contains datetime objects for monthly."""
        result = iwfm.generate_datetime_objects(
            "10/31/1973_24:00", 3, 1.0, "1MON"
        )
        for item in result:
            assert isinstance(item, datetime)


class TestGenerateDatetimeObjectsMonthly:
    """Test generate_datetime_objects with monthly time steps."""

    def test_monthly_time_steps(self):
        """Test monthly time step generation."""
        # Start date: 10/31/1973_24:00 = November 1, 1973
        result = iwfm.generate_datetime_objects(
            "10/31/1973_24:00", 3, 1.0, "1MON"
        )

        # Should generate last days of months starting from November
        assert len(result) == 3
        # All should be datetime objects
        for dt in result:
            assert isinstance(dt, datetime)

    def test_monthly_with_1MON_unit(self):
        """Test monthly with '1MON' time unit."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 12, 1.0, "1MON"
        )
        assert len(result) == 12

    def test_monthly_with_MON_unit(self):
        """Test monthly with 'MON' time unit."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 6, 1.0, "MON"
        )
        assert len(result) == 6

    def test_monthly_year_rollover(self):
        """Test that monthly generation handles year rollover correctly."""
        # Start in October, generate 5 months to cross into next year
        result = iwfm.generate_datetime_objects(
            "10/01/2000_00:00", 5, 1.0, "1MON"
        )

        assert len(result) == 5
        # Should include dates from 2000 and 2001
        years = [dt.year for dt in result]
        assert 2000 in years
        assert 2001 in years

    def test_monthly_generates_end_of_month(self):
        """Test that monthly generates end-of-month dates."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 3, 1.0, "1MON"
        )

        # Check that dates are last days of months
        for dt in result:
            # Last day of month: next day is first of next month
            next_day = dt + timedelta(days=1)
            assert next_day.day == 1

    def test_monthly_february_non_leap_year(self):
        """Test February end date in non-leap year."""
        # Start in January 2001 (not leap year)
        result = iwfm.generate_datetime_objects(
            "01/01/2001_00:00", 2, 1.0, "1MON"
        )

        # Second month should be February 28
        feb_date = result[1]
        assert feb_date.month == 2
        assert feb_date.day == 28

    def test_monthly_february_leap_year(self):
        """Test February end date in leap year."""
        # Start in January 2000 (leap year)
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 2, 1.0, "1MON"
        )

        # Second month should be February 29
        feb_date = result[1]
        assert feb_date.month == 2
        assert feb_date.day == 29


class TestGenerateDatetimeObjectsDaily:
    """Test generate_datetime_objects with non-monthly time steps."""

    def test_daily_time_steps(self):
        """Test daily time step generation."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 5, 1.0, "1DAY"
        )

        assert len(result) == 5
        for dt in result:
            assert isinstance(dt, datetime)

    def test_non_monthly_returns_datetimes(self):
        """Test that non-monthly time units return datetime objects."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 3, 1.0, "1DAY"
        )

        for item in result:
            assert isinstance(item, datetime)


class TestGenerateDatetimeObjectsDateFormats:
    """Test generate_datetime_objects with different IWFM date formats."""

    def test_standard_iwfm_date_format(self):
        """Test with standard MM/DD/YYYY_HH:MM format."""
        result = iwfm.generate_datetime_objects(
            "09/30/1973_24:00", 3, 1.0, "1MON"
        )
        assert len(result) == 3

    def test_midnight_format(self):
        """Test with 24:00 midnight format."""
        result = iwfm.generate_datetime_objects(
            "12/31/1999_24:00", 3, 1.0, "1MON"
        )
        assert len(result) == 3

    def test_regular_time_format(self):
        """Test with regular HH:MM format (not 24:00)."""
        result = iwfm.generate_datetime_objects(
            "01/15/2000_12:00", 3, 1.0, "1MON"
        )
        assert len(result) == 3


class TestGenerateDatetimeObjectsNSteps:
    """Test generate_datetime_objects with different n_steps values."""

    def test_single_step(self):
        """Test with a single time step."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 1, 1.0, "1MON"
        )
        assert len(result) == 1

    def test_many_steps(self):
        """Test with many time steps."""
        n_steps = 120  # 10 years of monthly data
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", n_steps, 1.0, "1MON"
        )
        assert len(result) == n_steps

    def test_zero_steps(self):
        """Test with zero time steps."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 0, 1.0, "1MON"
        )
        assert len(result) == 0


class TestGenerateDatetimeObjectsFallback:
    """Test generate_datetime_objects fallback behavior."""

    def test_invalid_date_returns_strings(self):
        """Test that invalid date format returns string fallback."""
        result = iwfm.generate_datetime_objects(
            "invalid_date", 3, 1.0, "1MON"
        )

        assert len(result) == 3
        # Fallback should return strings like "Step 1", "Step 2", etc.
        assert result[0] == "Step 1"
        assert result[1] == "Step 2"
        assert result[2] == "Step 3"

    def test_malformed_date_returns_strings(self):
        """Test that malformed date returns string fallback."""
        result = iwfm.generate_datetime_objects(
            "2000-01-01", 3, 1.0, "1MON"  # Wrong format
        )

        assert len(result) == 3
        # Should return string fallback
        for item in result:
            assert isinstance(item, str)
            assert "Step" in item

    def test_empty_date_returns_strings(self):
        """Test that empty date string returns string fallback."""
        result = iwfm.generate_datetime_objects(
            "", 3, 1.0, "1MON"
        )

        assert len(result) == 3
        for item in result:
            assert isinstance(item, str)


class TestGenerateDatetimeObjectsTimeUnits:
    """Test generate_datetime_objects with various time unit strings."""

    def test_1MON_uppercase(self):
        """Test with '1MON' uppercase."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 3, 1.0, "1MON"
        )
        assert len(result) == 3

    def test_MON_only(self):
        """Test with 'MON' only."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 3, 1.0, "MON"
        )
        assert len(result) == 3

    def test_1DAY(self):
        """Test with '1DAY' time unit."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 3, 1.0, "1DAY"
        )
        assert len(result) == 3

    def test_other_time_unit(self):
        """Test with other time unit (not monthly)."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 3, 1.0, "1HOUR"
        )
        assert len(result) == 3


class TestGenerateDatetimeObjectsRealWorldScenarios:
    """Test generate_datetime_objects with realistic IWFM scenarios."""

    def test_water_year_monthly_data(self):
        """Test generating monthly data for a water year (Oct-Sep)."""
        # Start at end of September (beginning of water year)
        result = iwfm.generate_datetime_objects(
            "09/30/1973_24:00", 12, 1.0, "1MON"
        )

        assert len(result) == 12
        # All should be datetime objects
        for dt in result:
            assert isinstance(dt, datetime)

    def test_multi_year_simulation(self):
        """Test generating dates for a multi-year simulation."""
        # 42 years of monthly data (like C2VSimCG)
        n_years = 42
        n_months = n_years * 12
        result = iwfm.generate_datetime_objects(
            "09/30/1973_24:00", n_months, 1.0, "1MON"
        )

        assert len(result) == n_months

        # First date should be in 1973
        assert result[0].year == 1973

        # Last date should be around 2015
        last_year = result[-1].year
        assert last_year >= 2014 and last_year <= 2016

    def test_budget_output_dates(self):
        """Test date generation for budget output files."""
        # Typical budget period
        result = iwfm.generate_datetime_objects(
            "10/31/1973_24:00", 504, 1.0, "1MON"  # 42 years
        )

        assert len(result) == 504

    def test_short_simulation(self):
        """Test date generation for a short simulation period."""
        # Just a few months
        result = iwfm.generate_datetime_objects(
            "01/31/2020_24:00", 6, 1.0, "1MON"
        )

        assert len(result) == 6
        # First date should be in 2020
        assert result[0].year == 2020


class TestGenerateDatetimeObjectsDeltaT:
    """Test generate_datetime_objects with different delta_t values."""

    def test_delta_t_one(self):
        """Test with delta_t = 1.0."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 3, 1.0, "1DAY"
        )
        assert len(result) == 3

    def test_delta_t_fractional(self):
        """Test with fractional delta_t."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 3, 0.5, "1DAY"
        )
        assert len(result) == 3

    def test_delta_t_larger(self):
        """Test with delta_t > 1."""
        result = iwfm.generate_datetime_objects(
            "01/01/2000_00:00", 3, 2.0, "1DAY"
        )
        assert len(result) == 3


class TestGenerateDatetimeObjectsEdgeCases:
    """Test edge cases for generate_datetime_objects."""

    def test_december_to_january(self):
        """Test transition from December to January."""
        # Start in December
        result = iwfm.generate_datetime_objects(
            "12/01/2000_00:00", 3, 1.0, "1MON"
        )

        assert len(result) == 3
        # Should have December 2000, January 2001, February 2001
        months = [dt.month for dt in result]
        years = [dt.year for dt in result]

        assert 12 in months  # December
        assert 1 in months   # January
        assert 2001 in years  # Next year

    def test_end_of_year_boundary(self):
        """Test year boundary handling."""
        result = iwfm.generate_datetime_objects(
            "11/30/2020_24:00", 3, 1.0, "1MON"
        )

        # Should cross into 2021
        years = set(dt.year for dt in result)
        assert len(years) == 2  # Both 2020 and 2021

    def test_early_month_start(self):
        """Test with start date early in a month."""
        result = iwfm.generate_datetime_objects(
            "01/05/2000_12:00", 3, 1.0, "1MON"
        )

        assert len(result) == 3
        for dt in result:
            assert isinstance(dt, datetime)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
