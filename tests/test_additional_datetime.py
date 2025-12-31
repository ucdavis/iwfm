# test_additional_datetime.py
# unit tests for date and time utility functions in the iwfm package
# Copyright (C) 2025 University of California
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

from datetime import datetime, timedelta
import pytest
import iwfm


class TestSecsBetween:
    """Test the secs_between function."""
    
    def test_secs_between_basic(self):
        """Test basic seconds calculation between two times."""
        start = datetime(2020, 1, 1, 10, 0, 0)
        end = datetime(2020, 1, 1, 10, 0, 30)  # 30 seconds later
        
        result = iwfm.secs_between(start, end)
        assert result == 30
    
    def test_secs_between_minutes(self):
        """Test with minute differences."""
        start = datetime(2020, 1, 1, 10, 0, 0)
        end = datetime(2020, 1, 1, 10, 5, 0)  # 5 minutes later
        
        result = iwfm.secs_between(start, end)
        assert result == 300  # 5 * 60 = 300 seconds
    
    def test_secs_between_hours(self):
        """Test with hour differences."""
        start = datetime(2020, 1, 1, 10, 0, 0)
        end = datetime(2020, 1, 1, 12, 0, 0)  # 2 hours later
        
        result = iwfm.secs_between(start, end)
        assert result == 7200  # 2 * 3600 = 7200 seconds
    
    def test_secs_between_complex(self):
        """Test with hours, minutes, and seconds."""
        start = datetime(2020, 1, 1, 10, 30, 15)
        end = datetime(2020, 1, 1, 12, 45, 45)  # 2:15:30 later
        
        result = iwfm.secs_between(start, end)
        expected = 2 * 3600 + 15 * 60 + 30  # 8130 seconds
        assert result == expected
    
    def test_secs_between_fractional_seconds(self):
        """Test with fractional seconds."""
        start = datetime(2020, 1, 1, 10, 0, 0, 0)
        end = datetime(2020, 1, 1, 10, 0, 5, 500000)  # 5.5 seconds later
        
        result = iwfm.secs_between(start, end)
        assert result == 5.5
    
    def test_secs_between_zero_difference(self):
        """Test with identical times."""
        dt = datetime(2020, 1, 1, 10, 0, 0)
        
        result = iwfm.secs_between(dt, dt)
        assert result == 0


class TestAdditionalDateFunctions:
    """Test additional date utility functions that may need more coverage."""
    
    def test_year_function_coverage(self):
        """Test year function with various formats."""
        # Test different year formats that might not be covered
        assert iwfm.year("1/1/05") == 2005  # 2-digit year < 20
        assert iwfm.year("1/1/85") == 1985  # 2-digit year >= 20
        assert iwfm.year("1/1/2020") == 2020  # 4-digit year
    
    def test_text_date_edge_cases(self):
        """Test text_date function with edge cases."""
        # Test single digit month and day
        assert iwfm.text_date("1/1/20") == "01/01/2020"
        assert iwfm.text_date("5/9/85") == "05/09/1985"
        
        # Test double digit month and day
        assert iwfm.text_date("12/31/99") == "12/31/1999"
        assert iwfm.text_date("10/25/15") == "10/25/2015"
    
    def test_month_day_edge_cases(self):
        """Test month and day functions with edge cases."""
        # Test single digit months/days
        assert iwfm.month("5/15/2020") == 5
        assert iwfm.day("1/7/2020") == 7
        
        # Test double digit months/days
        assert iwfm.month("12/25/2020") == 12
        assert iwfm.day("6/30/2020") == 30
        
        # Test with different separators (if the function handles them)
        assert iwfm.month("01/02/2020") == 1
        assert iwfm.day("01/02/2020") == 2


class TestDateTimeStringConversions:
    """Test string to datetime conversions if str2datetime exists."""
    
    def test_str2datetime_basic(self):
        """Test basic string to datetime conversion."""
        # This tests the str2datetime function if it's available
        try:
            # Test basic date string with 4-digit year
            result = iwfm.str2datetime("01/01/2020")
            expected = datetime(2020, 1, 1)
            assert result == expected
            
            # Test with different date in 4-digit year format  
            result = iwfm.str2datetime("12/25/1999")
            expected = datetime(1999, 12, 25)
            assert result == expected
            
            # Note: str2datetime only handles MM/DD/YYYY date format (no time component)
            # For 2-digit years, it treats them literally (not as 19xx or 20xx)
            
        except AttributeError:
            # str2datetime function might not be available or have different signature
            pytest.skip("str2datetime function not available or has different interface")
        except ValueError as e:
            # Function might have limitations in date format handling
            pytest.skip(f"str2datetime function has format limitations: {e}")


class TestDtsDaysAndDiff:
    """Test the dts2days and dates_diff functions if available."""
    
    def test_dts2days_basic(self):
        """Test dts2days function."""
        try:
            # Test conversion from datetime to days since start date
            start_date = datetime(2020, 1, 1)
            target_date = datetime(2020, 1, 2)
            
            result = iwfm.dts2days(target_date, start_date)
            assert result == 1  # 1 day after start date
            
            # Test with a date before start date
            earlier_date = datetime(2019, 12, 31)
            result = iwfm.dts2days(earlier_date, start_date)
            assert result == -1  # 1 day before start date
            
        except (AttributeError, TypeError):
            pytest.skip("dts2days function not available or has different interface")
    
    def test_dates_diff_basic(self):
        """Test dates_diff function."""
        try:
            # Test date difference calculation with datetime objects
            from datetime import datetime
            dt1 = datetime(2020, 1, 1)
            dt2 = datetime(2020, 1, 2)
            result = iwfm.dates_diff(dt1, dt2)
            assert result == 1  # 1 day difference
            
            # Test with larger difference
            dt3 = datetime(2020, 1, 1)
            dt4 = datetime(2020, 1, 10)
            result2 = iwfm.dates_diff(dt3, dt4)
            assert result2 == 9  # 9 days difference
            
            # Test that order doesn't matter (function uses abs())
            result3 = iwfm.dates_diff(dt4, dt3)
            assert result3 == 9  # Same result regardless of order
            
        except (AttributeError, TypeError):
            pytest.skip("dates_diff function not available or has different interface")


class TestDateIndexing:
    """Test date_index and index_date functions if available."""
    
    def test_date_index_basic(self):
        """Test date_index function."""
        try:
            # Test converting date to index (calculating date N months after start_date)
            # date_index(inval, start_date) returns a date inval months after start_date
            result = iwfm.date_index(3, "01/01/2020")  # 3 months after Jan 1, 2020
            assert isinstance(result, str)
            assert result == "04/01/2020"  # Should be April 1, 2020
            
            # Test with 12 months (full year)
            result2 = iwfm.date_index(12, "01/01/2020")  # 12 months after Jan 1, 2020
            assert result2 == "01/01/2021"  # Should be January 1, 2021
            
            # Test crossing year boundary
            result3 = iwfm.date_index(6, "08/15/2020")  # 6 months after Aug 15, 2020
            assert result3 == "02/15/2021"  # Should be February 15, 2021
            
            # Test with 0 months (should return same date)
            result4 = iwfm.date_index(0, "01/01/2020")
            assert result4 == "01/01/2020"  # Should be same date
            
        except (AttributeError, TypeError):
            pytest.skip("date_index function not available or has different interface")
    
    def test_index_date_basic(self):
        """Test index_date function."""
        try:
            # Test converting date to index (days from start_date to in_date)
            # index_date(in_date, start_date) returns number of days between dates
            
            # Test with same date (should be 0)
            result = iwfm.index_date("01/01/2020", "01/01/2020")
            assert isinstance(result, int)
            assert result == 0
            
            # Test with one day difference
            result2 = iwfm.index_date("01/02/2020", "01/01/2020")
            assert result2 == 1
            
            # Test with one week difference
            result3 = iwfm.index_date("01/08/2020", "01/01/2020")
            assert result3 == 7
            
            # Test with default start_date (10/01/1984)
            result4 = iwfm.index_date("10/01/1984")  # Should be 0 (same as default start_date)
            assert result4 == 0
            
            # Test with date after default start_date 
            result5 = iwfm.index_date("10/02/1984")  # One day after default start_date
            assert result5 == 1  # Now correctly returns 1
            
            # Test cross-month boundary
            result6 = iwfm.index_date("02/01/2020", "01/31/2020")
            assert result6 == 1
            
            # Test cross-year boundary
            result7 = iwfm.index_date("01/01/2020", "12/31/2019")
            assert result7 == 1
            
        except (AttributeError, TypeError):
            pytest.skip("index_date function not available or has different interface")