# test_calib_rmse_calc.py
# Unit tests for calib/rmse_calc.py - Calculate RMSE between two lists
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


class TestRmseCalc:
    """Tests for rmse_calc function"""

    def test_returns_float(self):
        """Test that function returns a float."""
        from iwfm.calib.rmse_calc import rmse_calc

        predictions = [100.0, 110.0, 120.0]
        targets = [95.0, 105.0, 115.0]

        result = rmse_calc(predictions, targets)

        assert isinstance(result, (float, np.floating))

    def test_zero_rmse(self):
        """Test zero RMSE (perfect match)."""
        from iwfm.calib.rmse_calc import rmse_calc

        predictions = [100.0, 110.0, 120.0]
        targets = [100.0, 110.0, 120.0]

        result = rmse_calc(predictions, targets)

        assert np.isclose(result, 0.0)

    def test_known_rmse(self):
        """Test with known RMSE calculation."""
        from iwfm.calib.rmse_calc import rmse_calc

        # Differences: 3, 4 -> squared: 9, 16 -> mean: 12.5 -> sqrt: 3.536
        predictions = [103.0, 104.0]
        targets = [100.0, 100.0]

        result = rmse_calc(predictions, targets)

        expected = np.sqrt((9 + 16) / 2)
        assert np.isclose(result, expected)

    def test_rmse_always_positive(self):
        """Test that RMSE is always positive."""
        from iwfm.calib.rmse_calc import rmse_calc

        # Negative differences
        predictions = [90.0, 95.0, 100.0]
        targets = [100.0, 105.0, 110.0]

        result = rmse_calc(predictions, targets)

        assert result >= 0

    def test_uniform_error(self):
        """Test with uniform error."""
        from iwfm.calib.rmse_calc import rmse_calc

        # All differences are 5
        predictions = [105.0, 115.0, 125.0]
        targets = [100.0, 110.0, 120.0]

        result = rmse_calc(predictions, targets)

        assert np.isclose(result, 5.0)

    def test_single_value(self):
        """Test with single value."""
        from iwfm.calib.rmse_calc import rmse_calc

        predictions = [100.0]
        targets = [97.0]

        result = rmse_calc(predictions, targets)

        assert np.isclose(result, 3.0)

    def test_large_values(self):
        """Test with large values."""
        from iwfm.calib.rmse_calc import rmse_calc

        predictions = [1e6, 2e6, 3e6]
        targets = [1e6 + 10, 2e6 + 10, 3e6 + 10]

        result = rmse_calc(predictions, targets)

        assert np.isclose(result, 10.0)

    def test_accepts_numpy_arrays(self):
        """Test that function accepts numpy arrays."""
        from iwfm.calib.rmse_calc import rmse_calc

        predictions = np.array([100.0, 110.0, 120.0])
        targets = np.array([100.0, 110.0, 120.0])

        result = rmse_calc(predictions, targets)

        assert np.isclose(result, 0.0)

    def test_rmse_vs_bias(self):
        """Test that RMSE >= |bias| (always true by definition)."""
        from iwfm.calib.rmse_calc import rmse_calc
        from iwfm.calib.bias_calc import bias_calc

        predictions = [100.0, 120.0, 90.0]
        targets = [110.0, 110.0, 110.0]

        rmse = rmse_calc(predictions, targets)
        bias = bias_calc(predictions, targets)

        assert rmse >= abs(bias)


class TestRmseCalcImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import rmse_calc
        assert callable(rmse_calc)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.rmse_calc import rmse_calc
        assert callable(rmse_calc)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.rmse_calc import rmse_calc
        
        assert rmse_calc.__doc__ is not None
        assert 'rmse' in rmse_calc.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
