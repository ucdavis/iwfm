# test_generate_timesteps.py
# Unit tests for the generate_timesteps function in the iwfm package
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
import re

import iwfm


class TestGenerateTimestepsFunctionExists:
    """Test that the generate_timesteps function exists and is callable."""

    def test_generate_timesteps_exists(self):
        """Test that generate_timesteps function exists in the iwfm module."""
        assert hasattr(iwfm, 'generate_timesteps')
        assert callable(getattr(iwfm, 'generate_timesteps'))


class TestGenerateTimestepsReturnType:
    """Test the return type of generate_timesteps."""

    def test_returns_list(self):
        """Test that generate_timesteps returns a list."""
        result = iwfm.generate_timesteps(
            "10/31/1973_24:00", 5, 1.0, "1MON"
        )
        assert isinstance(result, list)

    def test_returns_correct_length(self):
        """Test that returned list has correct number of elements."""
        n_steps = 12
        result = iwfm.generate_timesteps(
            "10/31/1973_24:00", n_steps, 1.0, "1MON"
        )
        assert len(result) == n_steps

    def test_returns_strings(self):
        """Test that returned list contains strings."""
        result = iwfm.generate_timesteps(
            "10/31/1973_24:00", 3, 1.0, "1MON"
        )
        for item in result:
            assert isinstance(item, str)


class TestGenerateTimestepsDateFormat:
    """Test the date format of generated timesteps."""

    def test_iwfm_date_format(self):
        """Test that dates are in IWFM format (MM/DD/YYYY_24:00)."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 1.0, "1MON"
        )

        # Check format pattern: MM/DD/YYYY_24:00
        pattern = r'^\d{2}/\d{2}/\d{4}_24:00$'
        for date_str in result:
            assert re.match(pattern, date_str), f"Date '{date_str}' doesn't match IWFM format"

    def test_dates_end_with_2400(self):
        """Test that all dates end with _24:00."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 5, 1.0, "1MON"
        )

        for date_str in result:
            assert date_str.endswith('_24:00')

    def test_valid_month_values(self):
        """Test that months are valid (01-12)."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 12, 1.0, "1MON"
        )

        for date_str in result:
            month = int(date_str.split('/')[0])
            assert 1 <= month <= 12

    def test_valid_day_values(self):
        """Test that days are valid (01-31)."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 12, 1.0, "1MON"
        )

        for date_str in result:
            day = int(date_str.split('/')[1])
            assert 1 <= day <= 31


class TestGenerateTimestepsMonthly:
    """Test generate_timesteps with monthly time steps."""

    def test_monthly_time_steps(self):
        """Test monthly time step generation."""
        result = iwfm.generate_timesteps(
            "10/31/1973_24:00", 3, 1.0, "1MON"
        )

        assert len(result) == 3
        # All should be strings in IWFM format
        for date_str in result:
            assert '_24:00' in date_str

    def test_monthly_with_1MON_unit(self):
        """Test monthly with '1MON' time unit."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 12, 1.0, "1MON"
        )
        assert len(result) == 12

    def test_monthly_with_MON_unit(self):
        """Test monthly with 'MON' time unit."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 6, 1.0, "MON"
        )
        assert len(result) == 6

    def test_monthly_generates_end_of_month(self):
        """Test that monthly generates end-of-month dates."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 1.0, "1MON"
        )

        # Check specific end-of-month days
        # January has 31 days, February 2000 has 29 (leap year), March has 31
        days = [int(d.split('/')[1]) for d in result]
        assert days[0] == 31  # January
        assert days[1] == 29  # February (leap year 2000)
        assert days[2] == 31  # March

    def test_monthly_year_rollover(self):
        """Test that monthly generation handles year rollover correctly."""
        result = iwfm.generate_timesteps(
            "10/01/2000_00:00", 5, 1.0, "1MON"
        )

        # Extract years from dates
        years = [int(d.split('/')[2].split('_')[0]) for d in result]
        assert 2000 in years
        assert 2001 in years

    def test_monthly_february_leap_year(self):
        """Test February in a leap year (2000)."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 2, 1.0, "1MON"
        )

        # February 2000 should be 29th
        feb_date = result[1]
        assert '02/29/2000' in feb_date

    def test_monthly_february_non_leap_year(self):
        """Test February in a non-leap year (2001)."""
        result = iwfm.generate_timesteps(
            "01/01/2001_00:00", 2, 1.0, "1MON"
        )

        # February 2001 should be 28th
        feb_date = result[1]
        assert '02/28/2001' in feb_date


class TestGenerateTimestepsDaily:
    """Test generate_timesteps with non-monthly time steps."""

    def test_daily_time_steps(self):
        """Test daily time step generation."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 5, 1.0, "1DAY"
        )

        assert len(result) == 5
        for date_str in result:
            assert isinstance(date_str, str)
            assert '_24:00' in date_str

    def test_non_monthly_returns_strings(self):
        """Test that non-monthly time units return formatted strings."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 1.0, "1DAY"
        )

        for item in result:
            assert isinstance(item, str)
            assert '/' in item  # Date separator


class TestGenerateTimestepsNSteps:
    """Test generate_timesteps with different n_steps values."""

    def test_single_step(self):
        """Test with a single time step."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 1, 1.0, "1MON"
        )
        assert len(result) == 1

    def test_many_steps(self):
        """Test with many time steps (10 years monthly)."""
        n_steps = 120
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", n_steps, 1.0, "1MON"
        )
        assert len(result) == n_steps

    def test_zero_steps(self):
        """Test with zero time steps."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 0, 1.0, "1MON"
        )
        assert len(result) == 0
        assert result == []


class TestGenerateTimestepsFallback:
    """Test generate_timesteps fallback behavior for invalid dates."""

    def test_invalid_date_returns_step_strings(self):
        """Test that invalid date format returns 'Step N' fallback."""
        result = iwfm.generate_timesteps(
            "invalid_date", 3, 1.0, "1MON"
        )

        assert len(result) == 3
        assert result[0] == "Step 1"
        assert result[1] == "Step 2"
        assert result[2] == "Step 3"

    def test_malformed_date_returns_step_strings(self):
        """Test that malformed date returns 'Step N' fallback."""
        result = iwfm.generate_timesteps(
            "2000-01-01", 3, 1.0, "1MON"  # Wrong format (ISO instead of IWFM)
        )

        assert len(result) == 3
        for i, item in enumerate(result):
            assert item == f"Step {i+1}"

    def test_empty_date_returns_step_strings(self):
        """Test that empty date string returns 'Step N' fallback."""
        result = iwfm.generate_timesteps(
            "", 3, 1.0, "1MON"
        )

        assert len(result) == 3
        for item in result:
            assert "Step" in item


class TestGenerateTimestepsTimeUnits:
    """Test generate_timesteps with various time unit strings."""

    def test_1MON_uppercase(self):
        """Test with '1MON' uppercase."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 1.0, "1MON"
        )
        assert len(result) == 3
        # Should be end-of-month dates
        for date_str in result:
            assert '_24:00' in date_str

    def test_MON_only(self):
        """Test with 'MON' only (without number prefix)."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 1.0, "MON"
        )
        assert len(result) == 3

    def test_1DAY_time_unit(self):
        """Test with '1DAY' time unit."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 1.0, "1DAY"
        )
        assert len(result) == 3

    def test_other_time_unit(self):
        """Test with other time unit (not monthly)."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 1.0, "1HOUR"
        )
        assert len(result) == 3


class TestGenerateTimestepsRealWorldScenarios:
    """Test generate_timesteps with realistic IWFM scenarios."""

    def test_water_year_start(self):
        """Test generating timesteps starting at water year (October)."""
        result = iwfm.generate_timesteps(
            "09/30/1973_24:00", 12, 1.0, "1MON"
        )

        assert len(result) == 12
        # First should be October
        assert result[0].startswith('10/')

    def test_c2vsimcg_simulation_period(self):
        """Test timesteps for a typical C2VSimCG simulation period."""
        # 42 years of monthly data
        n_years = 42
        n_months = n_years * 12
        result = iwfm.generate_timesteps(
            "09/30/1973_24:00", n_months, 1.0, "1MON"
        )

        assert len(result) == n_months

        # First date should be in 1973
        assert '1973' in result[0]

        # Last date should be around 2015
        assert '2015' in result[-1] or '2014' in result[-1] or '2016' in result[-1]

    def test_budget_output_period(self):
        """Test generating timesteps for budget output."""
        # 504 months (42 years)
        result = iwfm.generate_timesteps(
            "10/31/1973_24:00", 504, 1.0, "1MON"
        )

        assert len(result) == 504

    def test_short_simulation(self):
        """Test timesteps for a short simulation period."""
        result = iwfm.generate_timesteps(
            "01/31/2020_24:00", 6, 1.0, "1MON"
        )

        assert len(result) == 6
        # All should be in 2020
        for date_str in result:
            assert '2020' in date_str


class TestGenerateTimestepsDeltaT:
    """Test generate_timesteps with different delta_t values."""

    def test_delta_t_one(self):
        """Test with delta_t = 1.0."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 1.0, "1DAY"
        )
        assert len(result) == 3

    def test_delta_t_fractional(self):
        """Test with fractional delta_t."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 0.5, "1DAY"
        )
        assert len(result) == 3

    def test_delta_t_larger(self):
        """Test with delta_t > 1."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 3, 2.0, "1DAY"
        )
        assert len(result) == 3


class TestGenerateTimestepsEdgeCases:
    """Test edge cases for generate_timesteps."""

    def test_december_to_january(self):
        """Test transition from December to January."""
        result = iwfm.generate_timesteps(
            "12/01/2000_00:00", 3, 1.0, "1MON"
        )

        assert len(result) == 3
        # Should include December 2000, January 2001, February 2001
        months = [d.split('/')[0] for d in result]
        assert '12' in months  # December
        assert '01' in months  # January

    def test_year_boundary(self):
        """Test year boundary handling."""
        result = iwfm.generate_timesteps(
            "11/30/2020_24:00", 4, 1.0, "1MON"
        )

        # Extract years
        years = set()
        for d in result:
            year = d.split('/')[2].split('_')[0]
            years.add(year)

        # Should span 2020 and 2021
        assert '2020' in years or '2021' in years

    def test_all_months_in_year(self):
        """Test generating all 12 months of a year."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 12, 1.0, "1MON"
        )

        # Extract unique months
        months = set(d.split('/')[0] for d in result)
        # Should have all 12 months
        assert len(months) == 12

    def test_consistent_format_across_steps(self):
        """Test that all generated dates have consistent format."""
        result = iwfm.generate_timesteps(
            "01/01/2000_00:00", 24, 1.0, "1MON"
        )

        pattern = r'^\d{2}/\d{2}/\d{4}_24:00$'
        for date_str in result:
            assert re.match(pattern, date_str), \
                f"Inconsistent format: {date_str}"


class TestGenerateTimestepsComparisonWithDatetimeObjects:
    """Test generate_timesteps produces dates consistent with generate_datetime_objects."""

    def test_same_number_of_results(self):
        """Test that both functions return same number of items."""
        n_steps = 12
        start_date = "01/01/2000_00:00"

        timesteps = iwfm.generate_timesteps(start_date, n_steps, 1.0, "1MON")
        datetimes = iwfm.generate_datetime_objects(start_date, n_steps, 1.0, "1MON")

        assert len(timesteps) == len(datetimes)

    def test_monthly_dates_match(self):
        """Test that monthly dates from both functions align."""
        n_steps = 6
        start_date = "01/01/2000_00:00"

        timesteps = iwfm.generate_timesteps(start_date, n_steps, 1.0, "1MON")
        datetimes = iwfm.generate_datetime_objects(start_date, n_steps, 1.0, "1MON")

        for i in range(n_steps):
            # Extract month/day/year from timestep string
            ts_parts = timesteps[i].split('_')[0].split('/')
            ts_month = int(ts_parts[0])
            ts_day = int(ts_parts[1])
            ts_year = int(ts_parts[2])

            # Compare with datetime object
            dt = datetimes[i]
            assert ts_month == dt.month
            assert ts_day == dt.day
            assert ts_year == dt.year


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
