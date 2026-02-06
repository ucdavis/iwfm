# test_calib_bias_calc.py
# Unit tests for calib/bias_calc.py - Calculate bias between two lists
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
import numpy as np


class TestBiasCalc:
    """Tests for bias_calc function"""

    def test_returns_float(self):
        """Test that function returns a float."""
        from iwfm.calib.bias_calc import bias_calc

        predictions = [100.0, 110.0, 120.0]
        targets = [95.0, 105.0, 115.0]

        result = bias_calc(predictions, targets)

        assert isinstance(result, (float, np.floating))

    def test_positive_bias(self):
        """Test positive bias (predictions > targets)."""
        from iwfm.calib.bias_calc import bias_calc

        predictions = [100.0, 110.0, 120.0]
        targets = [90.0, 100.0, 110.0]  # All 10 less

        result = bias_calc(predictions, targets)

        assert result > 0
        assert np.isclose(result, 10.0)

    def test_negative_bias(self):
        """Test negative bias (predictions < targets)."""
        from iwfm.calib.bias_calc import bias_calc

        predictions = [90.0, 100.0, 110.0]
        targets = [100.0, 110.0, 120.0]  # All 10 more

        result = bias_calc(predictions, targets)

        assert result < 0
        assert np.isclose(result, -10.0)

    def test_zero_bias(self):
        """Test zero bias (perfect match)."""
        from iwfm.calib.bias_calc import bias_calc

        predictions = [100.0, 110.0, 120.0]
        targets = [100.0, 110.0, 120.0]

        result = bias_calc(predictions, targets)

        assert np.isclose(result, 0.0)

    def test_mixed_differences(self):
        """Test with mixed positive and negative differences."""
        from iwfm.calib.bias_calc import bias_calc

        predictions = [100.0, 110.0, 120.0]
        targets = [105.0, 105.0, 120.0]  # -5, +5, 0

        result = bias_calc(predictions, targets)

        assert np.isclose(result, 0.0)

    def test_single_value(self):
        """Test with single value."""
        from iwfm.calib.bias_calc import bias_calc

        predictions = [100.0]
        targets = [95.0]

        result = bias_calc(predictions, targets)

        assert np.isclose(result, 5.0)

    def test_large_values(self):
        """Test with large values."""
        from iwfm.calib.bias_calc import bias_calc

        predictions = [1e6, 2e6, 3e6]
        targets = [1e6 - 100, 2e6 - 100, 3e6 - 100]

        result = bias_calc(predictions, targets)

        assert np.isclose(result, 100.0)

    def test_accepts_numpy_arrays(self):
        """Test that function accepts numpy arrays."""
        from iwfm.calib.bias_calc import bias_calc

        predictions = np.array([100.0, 110.0, 120.0])
        targets = np.array([95.0, 105.0, 115.0])

        result = bias_calc(predictions, targets)

        assert np.isclose(result, 5.0)


class TestBiasCalcImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import bias_calc
        assert callable(bias_calc)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.bias_calc import bias_calc
        assert callable(bias_calc)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.bias_calc import bias_calc
        
        assert bias_calc.__doc__ is not None
        assert 'bias' in bias_calc.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
