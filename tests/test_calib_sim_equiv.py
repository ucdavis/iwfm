# test_calib_sim_equiv.py
# Unit tests for calib/sim_equiv.py - Calculate simulated equivalent for a date
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
from datetime import date


class TestSimEquiv:
    """Tests for sim_equiv function"""

    def test_returns_float(self):
        """Test that function returns a float."""
        from iwfm.calib.sim_equiv import sim_equiv

        # Create simulated hydrograph array
        # Format: [date_as_days, value1, value2, ...]
        simhyd = np.array([
            [date(2020, 1, 1), 100.0, 200.0],
            [date(2020, 1, 11), 110.0, 210.0],
            [date(2020, 1, 21), 120.0, 220.0],
        ], dtype=object)

        result = sim_equiv(simhyd, date(2020, 1, 6), simhyd_col=1)

        assert isinstance(result, float)

    def test_interpolates_value(self):
        """Test that value is interpolated between dates."""
        from iwfm.calib.sim_equiv import sim_equiv

        simhyd = np.array([
            [date(2020, 1, 1), 100.0],
            [date(2020, 1, 11), 200.0],
        ], dtype=object)

        # Date at midpoint should give midpoint value
        result = sim_equiv(simhyd, date(2020, 1, 6), simhyd_col=1)

        # Should be around 150 (midpoint)
        assert 100.0 <= result <= 200.0

    def test_rounds_to_specified_decimals(self):
        """Test that result is rounded to specified decimal places."""
        from iwfm.calib.sim_equiv import sim_equiv

        simhyd = np.array([
            [date(2020, 1, 1), 100.0],
            [date(2020, 1, 11), 200.0],
        ], dtype=object)

        result = sim_equiv(simhyd, date(2020, 1, 6), simhyd_col=1, round_val=0)

        # Should be rounded to integer
        assert result == round(result, 0)

    def test_uses_correct_column(self):
        """Test that correct column is used for interpolation."""
        from iwfm.calib.sim_equiv import sim_equiv

        simhyd = np.array([
            [date(2020, 1, 1), 100.0, 1000.0],
            [date(2020, 1, 11), 200.0, 2000.0],
        ], dtype=object)

        result1 = sim_equiv(simhyd, date(2020, 1, 6), simhyd_col=1)
        result2 = sim_equiv(simhyd, date(2020, 1, 6), simhyd_col=2)

        # Column 2 values are 10x column 1
        assert result2 > result1


class TestSimEquivImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import sim_equiv
        assert callable(sim_equiv)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.sim_equiv import sim_equiv
        assert callable(sim_equiv)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.sim_equiv import sim_equiv
        
        assert sim_equiv.__doc__ is not None
        assert 'simulated' in sim_equiv.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
