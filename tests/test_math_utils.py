# test_math_utils.py
# unit test for math methods in the iwfm package
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
"""Tests for mathematical utility functions in the iwfm package."""

import math
import pytest
import iwfm


class TestLogTrans:
    """Test the logtrans function."""
    
    def test_logtrans_positive_values(self):
        """Test log transformation of positive values."""
        assert iwfm.logtrans(1.0) == 0.0  # log10(1) = 0
        assert iwfm.logtrans(10.0) == 1.0  # log10(10) = 1
        assert iwfm.logtrans(100.0) == 2.0  # log10(100) = 2
        assert iwfm.logtrans(0.1) == -1.0  # log10(0.1) = -1
    
    def test_logtrans_zero_value(self):
        """Test log transformation of zero returns zero_offset."""
        result = iwfm.logtrans(0.0)
        assert result == -2.0  # default zero_offset
        
        # Test custom zero_offset
        result = iwfm.logtrans(0.0, zero_offset=-5.0)
        assert result == -5.0
    
    def test_logtrans_negative_values(self):
        """Test log transformation of negative values returns neg_val."""
        result = iwfm.logtrans(-1.0)
        assert result == 1e-9  # default neg_val
        
        result = iwfm.logtrans(-100.0)
        assert result == 1e-9  # default neg_val
        
        # Test custom neg_val
        result = iwfm.logtrans(-1.0, neg_val=1e-6)
        assert result == 1e-6
    
    def test_logtrans_rounding(self):
        """Test rounding behavior."""
        # Test default rounding (4 decimal places)
        result = iwfm.logtrans(math.pi)
        expected = round(math.log10(math.pi), 4)
        assert result == expected
        
        # Test custom rounding
        result = iwfm.logtrans(math.pi, roundoff=2)
        expected = round(math.log10(math.pi), 2)
        assert result == expected
    
    def test_logtrans_string_input(self):
        """Test that string inputs are converted to float."""
        result = iwfm.logtrans("10.0")
        assert result == 1.0


class TestRound:
    """Test the round function."""
    
    def test_round_zero_decimals(self):
        """Test rounding to integer."""
        assert iwfm.round(3.7, 0) == 3
        assert iwfm.round(3.2, 0) == 3
        assert iwfm.round(3.9, 0) == 3
        assert type(iwfm.round(3.7, 0)) == int
    
    def test_round_positive_decimals(self):
        """Test rounding to positive decimal places."""
        assert iwfm.round(3.14159, 2) == 3.14
        assert iwfm.round(3.14159, 3) == 3.141
        assert iwfm.round(3.14159, 4) == 3.1415
        
        # Test rounding behavior
        assert iwfm.round(1.235, 2) == 1.23  # truncation, not proper rounding
        assert iwfm.round(1.999, 2) == 1.99
    
    def test_round_large_numbers(self):
        """Test rounding large numbers."""
        assert iwfm.round(123456.789, 1) == 123456.7
        assert iwfm.round(123456.789, 0) == 123456
    
    def test_round_negative_numbers(self):
        """Test rounding negative numbers."""
        assert iwfm.round(-3.14159, 2) == -3.14
        assert iwfm.round(-3.7, 0) == -3
    
    def test_round_negative_decimals_raises_error(self):
        """Test that negative decimal places cause system exit."""
        with pytest.raises(SystemExit):
            iwfm.round(3.14, -1)


class TestColumnSum:
    """Test the column_sum function."""
    
    def test_column_sum_basic(self):
        """Test basic column sum functionality."""
        data = [[1, 2, 3], [4, 5, 6]]
        result = iwfm.column_sum(data)
        assert result == [5, 7, 9]  # [1+4, 2+5, 3+6]
    
    def test_column_sum_single_row(self):
        """Test column sum with single row."""
        data = [[1, 2, 3]]
        result = iwfm.column_sum(data)
        assert result == [1, 2, 3]
    
    def test_column_sum_single_column(self):
        """Test column sum with single column."""
        data = [[1], [2], [3]]
        result = iwfm.column_sum(data)
        assert result == [6]
    
    def test_column_sum_empty_lists(self):
        """Test column sum with empty data."""
        data = []
        result = iwfm.column_sum(data)
        assert result == []
    
    def test_column_sum_mixed_numbers(self):
        """Test column sum with mixed integer and float types."""
        data = [[1.5, 2], [3, 4.5]]
        result = iwfm.column_sum(data)
        assert result == [4.5, 6.5]
    
    def test_column_sum_negative_numbers(self):
        """Test column sum with negative numbers."""
        data = [[1, -2, 3], [-4, 5, -6]]
        result = iwfm.column_sum(data)
        assert result == [-3, 3, -3]
    
    def test_column_sum_zeros(self):
        """Test column sum with zeros."""
        data = [[0, 1, 0], [2, 0, 3]]
        result = iwfm.column_sum(data)
        assert result == [2, 1, 3]