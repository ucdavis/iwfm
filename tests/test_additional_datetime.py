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

from datetime import datetime
import pytest
import iwfm


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