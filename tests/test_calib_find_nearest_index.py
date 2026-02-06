# test_calib_find_nearest_index.py
# Unit tests for calib/find_nearest_index.py - Find index of nearest value in array
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


class TestFindNearestIndex:
    """Tests for find_nearest_index function"""

    def test_exact_match(self):
        """Test finding exact match in array."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [10.0, 1.0],
            [20.0, 2.0],
            [30.0, 3.0],
        ])
        
        idx = find_nearest_index(array, 20.0)
        
        assert idx == 1

    def test_nearest_value_below(self):
        """Test finding nearest when value is between two points (closer to lower)."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [10.0, 1.0],
            [20.0, 2.0],
            [30.0, 3.0],
        ])
        
        # 14 is closer to 10 than to 20
        idx = find_nearest_index(array, 14.0)
        
        assert idx == 0

    def test_nearest_value_above(self):
        """Test finding nearest when value is between two points (closer to upper)."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [10.0, 1.0],
            [20.0, 2.0],
            [30.0, 3.0],
        ])
        
        # 17 is closer to 20 than to 10
        idx = find_nearest_index(array, 17.0)
        
        assert idx == 1

    def test_value_below_range(self):
        """Test when value is below all array values."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [10.0, 1.0],
            [20.0, 2.0],
            [30.0, 3.0],
        ])
        
        # -100 is closest to 10 (first element)
        idx = find_nearest_index(array, -100.0)
        
        assert idx == 0

    def test_value_above_range(self):
        """Test when value is above all array values."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [10.0, 1.0],
            [20.0, 2.0],
            [30.0, 3.0],
        ])
        
        # 1000 is closest to 30 (last element)
        idx = find_nearest_index(array, 1000.0)
        
        assert idx == 2

    def test_midpoint_between_values(self):
        """Test when value is exactly midway between two array values."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [10.0, 1.0],
            [20.0, 2.0],
        ])
        
        # 15 is exactly midway - argmin returns first occurrence
        idx = find_nearest_index(array, 15.0)
        
        # Should return either 0 or 1 (both are equally close)
        assert idx in [0, 1]

    def test_single_row(self):
        """Test with single row array."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([[50.0, 100.0]])
        
        idx = find_nearest_index(array, 999.0)
        
        assert idx == 0

    def test_first_column_only(self):
        """Test that only first column is used for matching."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        # Second column has value 25, but should not be matched
        array = np.array([
            [10.0, 25.0],
            [20.0, 50.0],
            [30.0, 75.0],
        ])
        
        idx = find_nearest_index(array, 25.0)
        
        # Should match closest in first column (20 or 30), not second column
        assert idx == 1 or idx == 2  # 25 is between 20 and 30

    def test_negative_values(self):
        """Test with negative values in array."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [-30.0, 1.0],
            [-20.0, 2.0],
            [-10.0, 3.0],
        ])
        
        idx = find_nearest_index(array, -25.0)
        
        # -25 is between -30 and -20, closer to -30? No, equally close
        # Actually: |-25 - (-30)| = 5, |-25 - (-20)| = 5, so first one
        assert idx in [0, 1]

    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative values."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [-10.0, 1.0],
            [0.0, 2.0],
            [10.0, 3.0],
        ])
        
        idx = find_nearest_index(array, -3.0)
        
        # -3 is closest to 0
        assert idx == 1

    def test_float_precision(self):
        """Test with floating point values requiring precision."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [1.001, 1.0],
            [1.002, 2.0],
            [1.003, 3.0],
        ])
        
        idx = find_nearest_index(array, 1.0021)
        
        # 1.0021 is closest to 1.002
        assert idx == 1

    def test_large_array(self):
        """Test with large array."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        # Create array with 1000 rows
        first_col = np.arange(0, 1000, 1).reshape(-1, 1)
        second_col = np.zeros((1000, 1))
        array = np.hstack([first_col, second_col])
        
        idx = find_nearest_index(array, 500.5)
        
        # Should find index 500 or 501
        assert idx in [500, 501]

    def test_unsorted_array(self):
        """Test with unsorted first column."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [30.0, 1.0],
            [10.0, 2.0],
            [20.0, 3.0],
        ])
        
        idx = find_nearest_index(array, 15.0)
        
        # 15 is closest to 10 (at index 1) or 20 (at index 2)
        # |15-30|=15, |15-10|=5, |15-20|=5
        assert idx in [1, 2]

    def test_duplicate_values(self):
        """Test with duplicate values in first column."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [10.0, 1.0],
            [20.0, 2.0],
            [20.0, 3.0],
            [30.0, 4.0],
        ])
        
        idx = find_nearest_index(array, 20.0)
        
        # Should return first occurrence
        assert idx == 1

    def test_many_columns(self):
        """Test with array having many columns."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [10.0, 1.0, 2.0, 3.0, 4.0, 5.0],
            [20.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            [30.0, 11.0, 12.0, 13.0, 14.0, 15.0],
        ])
        
        idx = find_nearest_index(array, 25.0)
        
        # 25 is between 20 and 30, closer to... |25-20|=5, |25-30|=5
        assert idx in [1, 2]

    def test_return_type(self):
        """Test that return type is integer."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [10.0, 1.0],
            [20.0, 2.0],
        ])
        
        idx = find_nearest_index(array, 15.0)
        
        # numpy argmin returns numpy.int64, which is integer-like
        assert isinstance(idx, (int, np.integer))

    def test_zero_value(self):
        """Test finding zero value."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [-10.0, 1.0],
            [0.0, 2.0],
            [10.0, 3.0],
        ])
        
        idx = find_nearest_index(array, 0.0)
        
        assert idx == 1

    def test_very_large_values(self):
        """Test with very large values."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [1e10, 1.0],
            [2e10, 2.0],
            [3e10, 3.0],
        ])
        
        idx = find_nearest_index(array, 2.5e10)
        
        # 2.5e10 is between 2e10 and 3e10
        assert idx in [1, 2]

    def test_very_small_values(self):
        """Test with very small values."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        array = np.array([
            [1e-10, 1.0],
            [2e-10, 2.0],
            [3e-10, 3.0],
        ])
        
        idx = find_nearest_index(array, 2.5e-10)
        
        assert idx in [1, 2]


class TestFindNearestIndexImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import find_nearest_index
        assert callable(find_nearest_index)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.find_nearest_index import find_nearest_index
        assert callable(find_nearest_index)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.find_nearest_index import find_nearest_index
        
        assert find_nearest_index.__doc__ is not None
        assert 'index' in find_nearest_index.__doc__.lower()


class TestFindNearestIndexTypicalUseCases:
    """Tests for typical use cases in calibration context."""

    def test_time_series_lookup(self):
        """Test finding nearest time index in time series data."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        # Simulate time series: column 0 = days, column 1 = values
        array = np.array([
            [0.0, 100.0],
            [30.0, 110.0],
            [60.0, 120.0],
            [90.0, 130.0],
            [120.0, 140.0],
        ])
        
        # Find index for day 45
        idx = find_nearest_index(array, 45.0)
        
        # 45 is between 30 and 60, closer to 30? |45-30|=15, |45-60|=15
        # Equally close, so either 1 or 2
        assert idx in [1, 2]

    def test_elevation_lookup(self):
        """Test finding nearest elevation index."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        # Simulate elevation data: column 0 = elevation, column 1 = parameter
        array = np.array([
            [100.0, 0.1],
            [150.0, 0.2],
            [200.0, 0.3],
            [250.0, 0.4],
        ])
        
        # Find index for elevation 175
        idx = find_nearest_index(array, 175.0)
        
        # 175 is between 150 and 200, equally close
        assert idx in [1, 2]

    def test_observation_matching(self):
        """Test matching observation times to simulation times."""
        from iwfm.calib.find_nearest_index import find_nearest_index

        # Simulation output times (days since start)
        sim_times = np.array([
            [0.0, 10.5],
            [1.0, 10.6],
            [2.0, 10.7],
            [3.0, 10.8],
            [4.0, 10.9],
            [5.0, 11.0],
        ])
        
        # Find simulation time closest to observation at day 2.3
        idx = find_nearest_index(sim_times, 2.3)
        
        # 2.3 is closest to 2.0 (index 2)
        assert idx == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
