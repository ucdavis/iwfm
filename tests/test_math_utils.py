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


