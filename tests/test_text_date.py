# test_text_date.py
# unit tests for text_date function
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

import iwfm


class TestTextDateBasic:
    """Basic tests for text_date function."""

    def test_already_formatted_date(self):
        """Test date already in MM/DD/YYYY format."""
        result = iwfm.text_date("01/15/2000")

        assert result == "01/15/2000"

    def test_returns_string(self):
        """Test that function returns a string."""
        result = iwfm.text_date("1/1/2000")

        assert isinstance(result, str)

    def test_output_format(self):
        """Test that output follows MM/DD/YYYY format."""
        result = iwfm.text_date("1/1/2000")

        parts = result.split("/")
        assert len(parts) == 3
        assert len(parts[0]) == 2  # MM
        assert len(parts[1]) == 2  # DD
        assert len(parts[2]) == 4  # YYYY


class TestTextDateSingleDigitMonth:
    """Tests for single-digit month padding."""

    def test_single_digit_month_january(self):
        """Test January (month 1) gets padded to 01."""
        result = iwfm.text_date("1/15/2000")

        assert result.startswith("01/")

    def test_single_digit_month_september(self):
        """Test September (month 9) gets padded to 09."""
        result = iwfm.text_date("9/15/2000")

        assert result.startswith("09/")

    def test_double_digit_month_october(self):
        """Test October (month 10) stays as 10."""
        result = iwfm.text_date("10/15/2000")

        assert result.startswith("10/")

    def test_double_digit_month_december(self):
        """Test December (month 12) stays as 12."""
        result = iwfm.text_date("12/15/2000")

        assert result.startswith("12/")

    def test_all_single_digit_months(self):
        """Test all single-digit months get padded."""
        for month in range(1, 10):
            result = iwfm.text_date(f"{month}/15/2000")
            expected_month = f"0{month}"
            assert result.startswith(f"{expected_month}/"), f"Month {month} not padded correctly"


class TestTextDateSingleDigitDay:
    """Tests for single-digit day padding."""

    def test_single_digit_day_first(self):
        """Test day 1 gets padded to 01."""
        result = iwfm.text_date("01/1/2000")

        assert "/01/" in result

    def test_single_digit_day_ninth(self):
        """Test day 9 gets padded to 09."""
        result = iwfm.text_date("01/9/2000")

        assert "/09/" in result

    def test_double_digit_day_tenth(self):
        """Test day 10 stays as 10."""
        result = iwfm.text_date("01/10/2000")

        assert "/10/" in result

    def test_double_digit_day_thirty_first(self):
        """Test day 31 stays as 31."""
        result = iwfm.text_date("01/31/2000")

        assert "/31/" in result

    def test_all_single_digit_days(self):
        """Test all single-digit days get padded."""
        for day in range(1, 10):
            result = iwfm.text_date(f"01/{day}/2000")
            expected_day = f"0{day}"
            assert f"/{expected_day}/" in result, f"Day {day} not padded correctly"


class TestTextDateBothSingleDigit:
    """Tests for both single-digit month and day."""

    def test_both_single_digit(self):
        """Test both month and day are single digits."""
        result = iwfm.text_date("1/1/2000")

        assert result == "01/01/2000"

    def test_single_month_double_day(self):
        """Test single-digit month with double-digit day."""
        result = iwfm.text_date("5/15/2000")

        assert result == "05/15/2000"

    def test_double_month_single_day(self):
        """Test double-digit month with single-digit day."""
        result = iwfm.text_date("10/5/2000")

        assert result == "10/05/2000"

    def test_both_double_digit(self):
        """Test both month and day are double digits."""
        result = iwfm.text_date("11/25/2000")

        assert result == "11/25/2000"


class TestTextDateTwoDigitYear:
    """Tests for two-digit year conversion."""

    def test_two_digit_year_2000s(self):
        """Test two-digit year in 2000s (00-20 -> 2000-2020)."""
        result = iwfm.text_date("1/15/00")

        assert result == "01/15/2000"

    def test_two_digit_year_10(self):
        """Test year 10 becomes 2010."""
        result = iwfm.text_date("1/15/10")

        assert result == "01/15/2010"

    def test_two_digit_year_20(self):
        """Test year 20 becomes 2020."""
        result = iwfm.text_date("1/15/20")

        assert result == "01/15/2020"

    def test_two_digit_year_1900s(self):
        """Test two-digit year in 1900s (21-99 -> 1921-1999)."""
        result = iwfm.text_date("1/15/99")

        assert result == "01/15/1999"

    def test_two_digit_year_21(self):
        """Test year 21 becomes 1921."""
        result = iwfm.text_date("1/15/21")

        assert result == "01/15/1921"

    def test_two_digit_year_50(self):
        """Test year 50 becomes 1950."""
        result = iwfm.text_date("1/15/50")

        assert result == "01/15/1950"

    def test_two_digit_year_73(self):
        """Test year 73 becomes 1973 (common in IWFM files)."""
        result = iwfm.text_date("9/30/73")

        assert result == "09/30/1973"


class TestTextDateFourDigitYear:
    """Tests for four-digit year passthrough."""

    def test_four_digit_year_2000(self):
        """Test four-digit year 2000 stays as is."""
        result = iwfm.text_date("1/15/2000")

        assert result.endswith("/2000")

    def test_four_digit_year_1973(self):
        """Test four-digit year 1973 stays as is."""
        result = iwfm.text_date("9/30/1973")

        assert result.endswith("/1973")

    def test_four_digit_year_2025(self):
        """Test four-digit year 2025 stays as is."""
        result = iwfm.text_date("1/15/2025")

        assert result.endswith("/2025")

    def test_four_digit_year_1950(self):
        """Test four-digit year 1950 stays as is."""
        result = iwfm.text_date("6/1/1950")

        assert result.endswith("/1950")


class TestTextDateSpecialDates:
    """Tests for special dates."""

    def test_new_years_day(self):
        """Test New Year's Day."""
        result = iwfm.text_date("1/1/2000")

        assert result == "01/01/2000"

    def test_leap_year_day(self):
        """Test leap year February 29."""
        result = iwfm.text_date("2/29/2000")

        assert result == "02/29/2000"

    def test_end_of_year(self):
        """Test December 31."""
        result = iwfm.text_date("12/31/2000")

        assert result == "12/31/2000"

    def test_common_iwfm_start_date(self):
        """Test common IWFM simulation start date."""
        result = iwfm.text_date("9/30/73")

        assert result == "09/30/1973"

    def test_end_of_month_dates(self):
        """Test various end of month dates."""
        # 30-day months
        assert iwfm.text_date("4/30/2000") == "04/30/2000"
        assert iwfm.text_date("6/30/2000") == "06/30/2000"
        assert iwfm.text_date("9/30/2000") == "09/30/2000"
        assert iwfm.text_date("11/30/2000") == "11/30/2000"

        # 31-day months
        assert iwfm.text_date("1/31/2000") == "01/31/2000"
        assert iwfm.text_date("3/31/2000") == "03/31/2000"
        assert iwfm.text_date("5/31/2000") == "05/31/2000"
        assert iwfm.text_date("7/31/2000") == "07/31/2000"
        assert iwfm.text_date("8/31/2000") == "08/31/2000"
        assert iwfm.text_date("10/31/2000") == "10/31/2000"
        assert iwfm.text_date("12/31/2000") == "12/31/2000"


class TestTextDateEdgeCases:
    """Edge case tests."""

    def test_minimum_date_components(self):
        """Test minimum values (1/1/00)."""
        result = iwfm.text_date("1/1/00")

        assert result == "01/01/2000"

    def test_maximum_month_day(self):
        """Test maximum month and day values."""
        result = iwfm.text_date("12/31/99")

        assert result == "12/31/1999"

    def test_already_zero_padded(self):
        """Test input that's already zero-padded."""
        result = iwfm.text_date("01/01/2000")

        assert result == "01/01/2000"

    def test_mixed_padding_month_padded(self):
        """Test mixed: month padded, day not."""
        result = iwfm.text_date("01/5/2000")

        assert result == "01/05/2000"

    def test_mixed_padding_day_padded(self):
        """Test mixed: day padded, month not."""
        result = iwfm.text_date("5/01/2000")

        assert result == "05/01/2000"


class TestTextDateConsistency:
    """Tests for consistent output across various inputs."""

    def test_same_date_different_formats(self):
        """Test that different input formats produce same output."""
        formats = [
            "1/1/00",
            "01/1/00",
            "1/01/00",
            "01/01/00",
            "1/1/2000",
            "01/1/2000",
            "1/01/2000",
            "01/01/2000",
        ]

        results = [iwfm.text_date(f) for f in formats]

        # All should produce the same result
        assert all(r == "01/01/2000" for r in results)

    def test_different_dates_different_results(self):
        """Test that different dates produce different results."""
        date1 = iwfm.text_date("1/1/2000")
        date2 = iwfm.text_date("1/2/2000")
        date3 = iwfm.text_date("2/1/2000")

        assert date1 != date2
        assert date1 != date3
        assert date2 != date3
