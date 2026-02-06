# test_calib_interp_val.py
# Unit tests for calib/interp_val.py - Interpolate simulated value to observation date
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
from datetime import date, datetime
import numpy as np


class TestInterpVal:
    """Tests for interp_val function"""

    def test_returns_early_val_when_obs_equals_early(self):
        """Test that early_val is returned when obs_date equals early_date."""
        from iwfm.calib.interp_val import interp_val

        obs_date = date(2020, 1, 15)
        early_date = date(2020, 1, 15)
        early_val = 100.0
        late_date = date(2020, 1, 31)
        late_val = 200.0

        result = interp_val(obs_date, early_date, early_val, late_date, late_val)

        assert result == early_val

    def test_returns_late_val_when_obs_equals_late(self):
        """Test that late_val is returned when obs_date equals late_date."""
        from iwfm.calib.interp_val import interp_val

        obs_date = date(2020, 1, 31)
        early_date = date(2020, 1, 15)
        early_val = 100.0
        late_date = date(2020, 1, 31)
        late_val = 200.0

        result = interp_val(obs_date, early_date, early_val, late_date, late_val)

        assert result == late_val

    def test_interpolates_midpoint(self):
        """Test interpolation at midpoint between dates."""
        from iwfm.calib.interp_val import interp_val

        early_date = date(2020, 1, 1)
        early_val = 100.0
        late_date = date(2020, 1, 11)  # 10 days later
        late_val = 200.0
        obs_date = date(2020, 1, 6)    # 5 days in (midpoint)

        result = interp_val(obs_date, early_date, early_val, late_date, late_val)

        # Midpoint should be average of values
        assert np.isclose(result, 150.0)

    def test_interpolates_quarter_point(self):
        """Test interpolation at 1/4 point between dates."""
        from iwfm.calib.interp_val import interp_val

        early_date = date(2020, 1, 1)
        early_val = 100.0
        late_date = date(2020, 1, 21)  # 20 days later
        late_val = 200.0
        obs_date = date(2020, 1, 6)    # 5 days in (1/4 point)

        result = interp_val(obs_date, early_date, early_val, late_date, late_val)

        # 1/4 of range: 100 + 0.25 * (200-100) = 125
        assert np.isclose(result, 125.0)

    def test_interpolates_three_quarter_point(self):
        """Test interpolation at 3/4 point between dates."""
        from iwfm.calib.interp_val import interp_val

        early_date = date(2020, 1, 1)
        early_val = 100.0
        late_date = date(2020, 1, 21)  # 20 days later
        late_val = 200.0
        obs_date = date(2020, 1, 16)   # 15 days in (3/4 point)

        result = interp_val(obs_date, early_date, early_val, late_date, late_val)

        # 3/4 of range: 100 + 0.75 * (200-100) = 175
        assert np.isclose(result, 175.0)

    def test_decreasing_values(self):
        """Test interpolation with decreasing values."""
        from iwfm.calib.interp_val import interp_val

        early_date = date(2020, 1, 1)
        early_val = 200.0
        late_date = date(2020, 1, 11)
        late_val = 100.0
        obs_date = date(2020, 1, 6)  # midpoint

        result = interp_val(obs_date, early_date, early_val, late_date, late_val)

        # Midpoint of decreasing values
        assert np.isclose(result, 150.0)

    def test_negative_values(self):
        """Test interpolation with negative values."""
        from iwfm.calib.interp_val import interp_val

        early_date = date(2020, 1, 1)
        early_val = -100.0
        late_date = date(2020, 1, 11)
        late_val = -50.0
        obs_date = date(2020, 1, 6)  # midpoint

        result = interp_val(obs_date, early_date, early_val, late_date, late_val)

        assert np.isclose(result, -75.0)

    def test_works_with_datetime_objects(self):
        """Test that function works with datetime objects."""
        from iwfm.calib.interp_val import interp_val

        early_date = datetime(2020, 1, 1, 0, 0, 0)
        early_val = 100.0
        late_date = datetime(2020, 1, 11, 0, 0, 0)
        late_val = 200.0
        obs_date = datetime(2020, 1, 6, 0, 0, 0)

        result = interp_val(obs_date, early_date, early_val, late_date, late_val)

        assert np.isclose(result, 150.0)

    def test_single_day_interval(self):
        """Test with single day interval."""
        from iwfm.calib.interp_val import interp_val

        early_date = date(2020, 1, 1)
        early_val = 100.0
        late_date = date(2020, 1, 2)
        late_val = 200.0
        obs_date = date(2020, 1, 1)

        result = interp_val(obs_date, early_date, early_val, late_date, late_val)

        assert result == early_val


class TestInterpValImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import interp_val
        assert callable(interp_val)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.interp_val import interp_val
        assert callable(interp_val)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.interp_val import interp_val
        
        assert interp_val.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
