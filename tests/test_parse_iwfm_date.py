# test_parse_iwfm_date.py
# unit tests for parse_iwfm_date function
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


class TestParseIwfmDate:
    """Tests for the parse_iwfm_date function."""

    def test_standard_date_with_24_00(self):
        """Test parsing date with 24:00 (end of day)."""
        result = iwfm.parse_iwfm_date('10/31/1973_24:00')
        # 24:00 on 10/31 becomes 00:00 on 11/01
        assert result == datetime(1973, 11, 1, 0, 0)

    def test_standard_date_with_regular_time(self):
        """Test parsing date with regular time."""
        result = iwfm.parse_iwfm_date('10/31/1973_12:00')
        assert result == datetime(1973, 10, 31, 12, 0)

    def test_midnight_time(self):
        """Test parsing date with 00:00 (start of day)."""
        result = iwfm.parse_iwfm_date('01/15/2000_00:00')
        assert result == datetime(2000, 1, 15, 0, 0)

    def test_end_of_year_with_24_00(self):
        """Test 24:00 on Dec 31 rolls over to Jan 1 of next year."""
        result = iwfm.parse_iwfm_date('12/31/1999_24:00')
        assert result == datetime(2000, 1, 1, 0, 0)

    def test_end_of_february_leap_year(self):
        """Test 24:00 on Feb 28 in leap year."""
        result = iwfm.parse_iwfm_date('02/28/2000_24:00')
        # 2000 is a leap year, so Feb 29 exists
        assert result == datetime(2000, 2, 29, 0, 0)

    def test_end_of_february_non_leap_year(self):
        """Test 24:00 on Feb 28 in non-leap year."""
        result = iwfm.parse_iwfm_date('02/28/2001_24:00')
        # 2001 is not a leap year, so rolls to March 1
        assert result == datetime(2001, 3, 1, 0, 0)

    def test_various_times(self):
        """Test parsing various times throughout the day."""
        test_cases = [
            ('05/15/2010_06:00', datetime(2010, 5, 15, 6, 0)),
            ('05/15/2010_12:30', datetime(2010, 5, 15, 12, 30)),
            ('05/15/2010_18:45', datetime(2010, 5, 15, 18, 45)),
            ('05/15/2010_23:59', datetime(2010, 5, 15, 23, 59)),
        ]
        for date_str, expected in test_cases:
            result = iwfm.parse_iwfm_date(date_str)
            assert result == expected, f"Failed for {date_str}"

    def test_single_digit_month_with_leading_zero(self):
        """Test parsing date with single digit month (with leading zero)."""
        result = iwfm.parse_iwfm_date('01/05/1990_12:00')
        assert result == datetime(1990, 1, 5, 12, 0)

    def test_single_digit_day_with_leading_zero(self):
        """Test parsing date with single digit day (with leading zero)."""
        result = iwfm.parse_iwfm_date('12/01/1990_12:00')
        assert result == datetime(1990, 12, 1, 12, 0)

    def test_invalid_date_returns_none(self):
        """Test that invalid date format returns None."""
        result = iwfm.parse_iwfm_date('invalid_date')
        assert result is None

    def test_missing_time_returns_none(self):
        """Test that date without time returns None."""
        result = iwfm.parse_iwfm_date('10/31/1973')
        assert result is None

    def test_missing_underscore_returns_none(self):
        """Test that date without underscore separator returns None."""
        result = iwfm.parse_iwfm_date('10/31/1973 24:00')
        assert result is None

    def test_empty_string_returns_none(self):
        """Test that empty string returns None."""
        result = iwfm.parse_iwfm_date('')
        assert result is None

    def test_none_input_returns_none(self):
        """Test that None input returns None."""
        result = iwfm.parse_iwfm_date(None)
        assert result is None

    def test_malformed_date_returns_none(self):
        """Test that malformed date returns None."""
        result = iwfm.parse_iwfm_date('13/31/1973_24:00')  # Invalid month
        assert result is None

    def test_malformed_time_returns_none(self):
        """Test that malformed time returns None."""
        result = iwfm.parse_iwfm_date('10/31/1973_25:00')  # Invalid hour (not 24:00)
        assert result is None

    def test_typical_iwfm_water_year_dates(self):
        """Test typical IWFM water year end dates."""
        # Water year typically ends at end of September
        result = iwfm.parse_iwfm_date('09/30/1974_24:00')
        assert result == datetime(1974, 10, 1, 0, 0)

        result = iwfm.parse_iwfm_date('09/30/2020_24:00')
        assert result == datetime(2020, 10, 1, 0, 0)

    def test_first_of_month(self):
        """Test parsing first of month dates."""
        result = iwfm.parse_iwfm_date('01/01/2000_00:00')
        assert result == datetime(2000, 1, 1, 0, 0)

    def test_last_of_month_various(self):
        """Test parsing last day of various months with 24:00."""
        test_cases = [
            ('01/31/2000_24:00', datetime(2000, 2, 1, 0, 0)),   # Jan -> Feb
            ('03/31/2000_24:00', datetime(2000, 4, 1, 0, 0)),   # Mar -> Apr
            ('04/30/2000_24:00', datetime(2000, 5, 1, 0, 0)),   # Apr -> May
            ('06/30/2000_24:00', datetime(2000, 7, 1, 0, 0)),   # Jun -> Jul
            ('11/30/2000_24:00', datetime(2000, 12, 1, 0, 0)),  # Nov -> Dec
        ]
        for date_str, expected in test_cases:
            result = iwfm.parse_iwfm_date(date_str)
            assert result == expected, f"Failed for {date_str}"

    def test_century_boundaries(self):
        """Test dates around century boundaries."""
        # Year 1999
        result = iwfm.parse_iwfm_date('06/15/1999_12:00')
        assert result == datetime(1999, 6, 15, 12, 0)

        # Year 2000
        result = iwfm.parse_iwfm_date('06/15/2000_12:00')
        assert result == datetime(2000, 6, 15, 12, 0)

        # Year 2001
        result = iwfm.parse_iwfm_date('06/15/2001_12:00')
        assert result == datetime(2001, 6, 15, 12, 0)

    def test_return_type_is_datetime(self):
        """Test that return type is datetime object."""
        result = iwfm.parse_iwfm_date('10/31/1973_24:00')
        assert isinstance(result, datetime)

    def test_minutes_preserved(self):
        """Test that minutes are correctly preserved."""
        result = iwfm.parse_iwfm_date('05/15/2010_14:30')
        assert result.minute == 30

        result = iwfm.parse_iwfm_date('05/15/2010_14:45')
        assert result.minute == 45

    def test_hour_preserved(self):
        """Test that hour is correctly preserved."""
        for hour in range(0, 24):
            date_str = f'05/15/2010_{hour:02d}:00'
            result = iwfm.parse_iwfm_date(date_str)
            assert result.hour == hour, f"Failed for hour {hour}"
