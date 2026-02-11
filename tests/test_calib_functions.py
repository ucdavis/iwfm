# test_calib_functions.py
# unit tests for calibration utility functions in the iwfm package
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

import numpy as np
from datetime import datetime
import iwfm.calib as calib
from iwfm.calib.compare import compare


class TestBiasCalc:
    """Test the bias_calc function."""
    
    def test_bias_calc_positive_bias(self):
        """Test bias calculation with positive bias (predictions > targets)."""
        predictions = [10.0, 20.0, 30.0, 40.0]
        targets = [8.0, 18.0, 28.0, 38.0]
        
        result = calib.bias_calc(predictions, targets)
        expected = 2.0  # (10-8 + 20-18 + 30-28 + 40-38) / 4 = 8/4 = 2.0
        
        assert abs(result - expected) < 1e-10
    
    def test_bias_calc_negative_bias(self):
        """Test bias calculation with negative bias (predictions < targets)."""
        predictions = [5.0, 15.0, 25.0]
        targets = [10.0, 20.0, 30.0]
        
        result = calib.bias_calc(predictions, targets)
        expected = -5.0  # (5-10 + 15-20 + 25-30) / 3 = -15/3 = -5.0
        
        assert abs(result - expected) < 1e-10
    
    def test_bias_calc_zero_bias(self):
        """Test bias calculation with zero bias (perfect predictions)."""
        predictions = [1.0, 2.0, 3.0, 4.0, 5.0]
        targets = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        result = calib.bias_calc(predictions, targets)
        expected = 0.0
        
        assert abs(result - expected) < 1e-10
    
    def test_bias_calc_single_values(self):
        """Test bias calculation with single values."""
        predictions = [15.5]
        targets = [12.3]
        
        result = calib.bias_calc(predictions, targets)
        expected = 3.2
        
        assert abs(result - expected) < 1e-10
    
    def test_bias_calc_mixed_values(self):
        """Test bias calculation with mixed positive and negative differences."""
        predictions = [10.0, 5.0, 15.0, 8.0]
        targets = [8.0, 7.0, 12.0, 11.0]
        # Differences: [2.0, -2.0, 3.0, -3.0] = 0.0 / 4 = 0.0
        
        result = calib.bias_calc(predictions, targets)
        expected = 0.0
        
        assert abs(result - expected) < 1e-10


class TestRmseCalc:
    """Test the rmse_calc function."""
    
    def test_rmse_calc_perfect_predictions(self):
        """Test RMSE calculation with perfect predictions."""
        predictions = [1.0, 2.0, 3.0, 4.0]
        targets = [1.0, 2.0, 3.0, 4.0]
        
        result = calib.rmse_calc(predictions, targets)
        expected = 0.0
        
        assert abs(result - expected) < 1e-10
    
    def test_rmse_calc_basic(self):
        """Test RMSE calculation with known values."""
        predictions = [2.0, 4.0, 6.0]
        targets = [1.0, 3.0, 5.0]
        # Squared differences: [1.0, 1.0, 1.0]
        # Mean: 1.0, RMSE: sqrt(1.0) = 1.0
        
        result = calib.rmse_calc(predictions, targets)
        expected = 1.0
        
        assert abs(result - expected) < 1e-10
    
    def test_rmse_calc_larger_differences(self):
        """Test RMSE with larger differences."""
        predictions = [10.0, 20.0]
        targets = [7.0, 16.0]
        # Squared differences: [9.0, 16.0]
        # Mean: 12.5, RMSE: sqrt(12.5) ≈ 3.536
        
        result = calib.rmse_calc(predictions, targets)
        expected = np.sqrt(12.5)
        
        assert abs(result - expected) < 1e-10
    
    def test_rmse_calc_single_value(self):
        """Test RMSE calculation with single value."""
        predictions = [5.0]
        targets = [2.0]
        # Squared difference: 9.0, RMSE: 3.0
        
        result = calib.rmse_calc(predictions, targets)
        expected = 3.0
        
        assert abs(result - expected) < 1e-10
    
    def test_rmse_calc_negative_values(self):
        """Test RMSE with negative values."""
        predictions = [-2.0, -4.0, -1.0]
        targets = [-1.0, -3.0, -3.0]
        # Squared differences: [1.0, 1.0, 4.0]
        # Mean: 2.0, RMSE: sqrt(2.0) ≈ 1.414
        
        result = calib.rmse_calc(predictions, targets)
        expected = np.sqrt(2.0)
        
        assert abs(result - expected) < 1e-10


class TestFindNearestIndex:
    """Test the find_nearest_index function."""
    
    def test_find_nearest_index_exact_match(self):
        """Test finding exact match in array."""
        array = np.array([[1.0, 10], [2.0, 20], [3.0, 30], [4.0, 40]])
        value = 3.0
        
        result = calib.find_nearest_index(array, value)
        expected = 2  # Index of row with 3.0 in first column
        
        assert result == expected
    
    def test_find_nearest_index_closest_value(self):
        """Test finding closest value when no exact match."""
        array = np.array([[1.0, 10], [3.0, 30], [5.0, 50]])
        value = 2.1
        
        result = calib.find_nearest_index(array, value)
        expected = 1  # Index of 3.0 (closest to 2.1: |3.0-2.1|=0.9 < |1.0-2.1|=1.1)
        
        assert result == expected
    
    def test_find_nearest_index_closest_higher(self):
        """Test finding closest value when target is between values."""
        array = np.array([[1.0, 10], [3.0, 30], [5.0, 50]])
        value = 3.8
        
        result = calib.find_nearest_index(array, value)
        expected = 1  # Index of 3.0 (3.8 is closer to 3.0 than 5.0)
        
        assert result == expected
    
    def test_find_nearest_index_single_row(self):
        """Test with single row array."""
        array = np.array([[42.5, 100]])
        value = 50.0
        
        result = calib.find_nearest_index(array, value)
        expected = 0
        
        assert result == expected
    
    def test_find_nearest_index_negative_values(self):
        """Test with negative values in array."""
        array = np.array([[-5.0, 10], [-2.0, 20], [1.0, 30], [4.0, 40]])
        value = -3.0
        
        result = calib.find_nearest_index(array, value)
        expected = 1  # Index of -2.0 (closest to -3.0)
        
        assert result == expected
    
    def test_find_nearest_index_large_array(self):
        """Test with larger array."""
        array = np.array([[i*0.5, i*10] for i in range(10)])
        # array first column: [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
        value = 2.3
        
        result = calib.find_nearest_index(array, value)
        expected = 5  # Index of 2.5 (closest to 2.3)
        
        assert result == expected


class TestInterpVal:
    """Test the interp_val function."""
    
    def test_interp_val_exact_early_date(self):
        """Test interpolation when obs_date equals early_date."""
        obs_date = datetime(2020, 1, 1)
        early_date = datetime(2020, 1, 1)
        early_val = 10.0
        late_date = datetime(2020, 1, 11)
        late_val = 20.0
        
        result = calib.interp_val(obs_date, early_date, early_val, late_date, late_val)
        expected = 10.0
        
        assert result == expected
    
    def test_interp_val_exact_late_date(self):
        """Test interpolation when obs_date equals late_date."""
        obs_date = datetime(2020, 1, 11)
        early_date = datetime(2020, 1, 1)
        early_val = 10.0
        late_date = datetime(2020, 1, 11)
        late_val = 20.0
        
        result = calib.interp_val(obs_date, early_date, early_val, late_date, late_val)
        expected = 20.0
        
        assert result == expected
    
    def test_interp_val_midpoint(self):
        """Test interpolation at midpoint between dates."""
        obs_date = datetime(2020, 1, 6)  # Midpoint
        early_date = datetime(2020, 1, 1)
        early_val = 10.0
        late_date = datetime(2020, 1, 11)  # 10 days span
        late_val = 20.0
        
        # obs_date is 5 days after early_date, halfway through 10-day span
        # Should return midpoint value: 10.0 + (20.0 - 10.0) * 0.5 = 15.0
        result = calib.interp_val(obs_date, early_date, early_val, late_date, late_val)
        expected = 15.0
        
        assert abs(result - expected) < 1e-10
    
    def test_interp_val_quarter_point(self):
        """Test interpolation at quarter point."""
        obs_date = datetime(2020, 1, 3)  # 2 days after start
        early_date = datetime(2020, 1, 1)
        early_val = 0.0
        late_date = datetime(2020, 1, 9)  # 8 days span
        late_val = 80.0
        
        # obs_date is 2 days after early_date, 2/8 = 0.25 through span
        # Should return: 0.0 + (80.0 - 0.0) * 0.25 = 20.0
        result = calib.interp_val(obs_date, early_date, early_val, late_date, late_val)
        expected = 20.0
        
        assert abs(result - expected) < 1e-10
    
    def test_interp_val_decreasing_values(self):
        """Test interpolation with decreasing values."""
        obs_date = datetime(2020, 6, 15)  # Midpoint
        early_date = datetime(2020, 6, 10)
        early_val = 100.0
        late_date = datetime(2020, 6, 20)  # 10 days span
        late_val = 50.0
        
        # obs_date is 5 days after early_date, halfway through 10-day span
        # Should return: 100.0 + (50.0 - 100.0) * 0.5 = 75.0
        result = calib.interp_val(obs_date, early_date, early_val, late_date, late_val)
        expected = 75.0
        
        assert abs(result - expected) < 1e-10
    
    def test_interp_val_negative_values(self):
        """Test interpolation with negative values."""
        obs_date = datetime(2020, 3, 5)
        early_date = datetime(2020, 3, 1)  # 4 days before obs
        early_val = -10.0
        late_date = datetime(2020, 3, 13)  # 12 days span total, 8 days after obs
        late_val = -30.0
        
        # obs_date is 4 days after early_date, 4/12 = 1/3 through span
        # Should return: -10.0 + (-30.0 - (-10.0)) * (1/3) = -10.0 + (-20.0) * (1/3) = -16.67
        result = calib.interp_val(obs_date, early_date, early_val, late_date, late_val)
        expected = -10.0 + (-20.0) * (4/12)
        
        assert abs(result - expected) < 1e-10


class TestSimEquiv:
    """Test the sim_equiv function."""
    
    def test_sim_equiv_basic(self):
        """Test basic sim_equiv functionality."""
        # Create test simulated hydrograph data
        # Format: [[date, value1, value2], ...]
        simhyd = np.array([
            [datetime(2020, 1, 1), 10.0, 100.0],
            [datetime(2020, 1, 11), 20.0, 200.0],
            [datetime(2020, 1, 21), 30.0, 300.0]
        ], dtype=object)
        
        # Test interpolation at midpoint
        date = datetime(2020, 1, 6)  # 5 days after first date
        simhyd_col = 1  # Use second column (value1)
        
        result = calib.sim_equiv(simhyd, date, simhyd_col, round_val=2)
        
        # Should interpolate between 10.0 and 20.0 at 50% point = 15.0
        expected = 15.0
        
        assert abs(result - expected) < 1e-10
    
    def test_sim_equiv_different_column(self):
        """Test sim_equiv with different column."""
        simhyd = np.array([
            [datetime(2020, 1, 1), 10.0, 100.0],
            [datetime(2020, 1, 11), 20.0, 200.0],
            [datetime(2020, 1, 21), 30.0, 300.0]
        ], dtype=object)
        
        date = datetime(2020, 1, 6)  # Midpoint
        simhyd_col = 2  # Use third column (value2)
        
        result = calib.sim_equiv(simhyd, date, simhyd_col, round_val=2)
        
        # Should interpolate between 100.0 and 200.0 at 50% point = 150.0
        expected = 150.0
        
        assert abs(result - expected) < 1e-10
    
    def test_sim_equiv_rounding(self):
        """Test sim_equiv rounding functionality."""
        simhyd = np.array([
            [datetime(2020, 1, 1), 10.0, 100.0],
            [datetime(2020, 1, 4), 13.333, 133.333]
        ], dtype=object)
        
        date = datetime(2020, 1, 2)  # 1/3 of the way through
        simhyd_col = 1
        
        # Test different rounding values
        result_2 = calib.sim_equiv(simhyd, date, simhyd_col, round_val=2)
        result_4 = calib.sim_equiv(simhyd, date, simhyd_col, round_val=4)
        
        # Should be approximately 11.111 (10 + 3.333/3)
        assert isinstance(result_2, float)
        assert isinstance(result_4, float)
        assert abs(result_2 - round(11.111, 2)) < 1e-10
        assert abs(result_4 - round(11.111, 4)) < 1e-10
    
    def test_sim_equiv_edge_dates(self):
        """Test sim_equiv with date near the boundary."""
        simhyd = np.array([
            [datetime(2020, 1, 1), 5.0, 50.0],
            [datetime(2020, 1, 10), 15.0, 150.0]
        ], dtype=object)
        
        # Test date very close to first date
        date = datetime(2020, 1, 2)  # 1 day after, 1/9 through span
        simhyd_col = 1
        
        result = calib.sim_equiv(simhyd, date, simhyd_col, round_val=3)
        
        # Should be approximately 5 + (15-5) * (1/9) = 5 + 10/9 ≈ 6.111
        expected = round(5.0 + 10.0 * (1/9), 3)
        
        assert abs(result - expected) < 1e-10


class TestCalibMathFunctions:
    """Test mathematical utility functions in calib module."""
    
    def test_bias_and_rmse_consistency(self):
        """Test that bias_calc and rmse_calc work together consistently."""
        predictions = [10.0, 15.0, 20.0, 25.0]
        targets = [12.0, 13.0, 22.0, 23.0]
        
        bias = calib.bias_calc(predictions, targets)
        rmse = calib.rmse_calc(predictions, targets)
        
        # Both should be valid numbers
        assert isinstance(bias, (int, float, np.number))
        assert isinstance(rmse, (int, float, np.number))
        assert not np.isnan(bias)
        assert not np.isnan(rmse)
        assert rmse >= 0  # RMSE should always be non-negative
    
    def test_empty_lists_behavior(self):
        """Test behavior with empty input lists."""
        bias = calib.bias_calc([], [])
        rmse = calib.rmse_calc([], [])
        
        # Functions return NaN for empty lists rather than raising errors
        assert np.isnan(bias)
        assert np.isnan(rmse)
    
    def test_mismatched_length_behavior(self):
        """Test behavior with mismatched input lengths."""
        predictions = [1.0, 2.0, 3.0]
        targets = [1.0, 2.0]  # Shorter list
        
        # Should either handle gracefully or raise appropriate error
        try:
            bias = calib.bias_calc(predictions, targets)
            rmse = calib.rmse_calc(predictions, targets)
            # If no error, both should be valid numbers
            assert isinstance(bias, (int, float, np.number))
            assert isinstance(rmse, (int, float, np.number))
        except (ValueError, IndexError):
            # This is also acceptable behavior
            pass


def test_compare():
    """Test the compare function in iwfm.calib.

    compare(list1, list2) returns (missing, in_both) where:
    - missing: items in list1 that are NOT in list2
    - in_both: items in list1 that ARE in list2
    """
    list1 = ["a", "b", "c"]
    list2 = ["b", "c", "d"]

    expected_missing = ["a"]
    expected_in_both = ["b", "c"]

    missing, in_both = compare(list1, list2)

    assert missing == expected_missing, f"Expected missing {expected_missing}, but got {missing}"
    assert in_both == expected_in_both, f"Expected in_both {expected_in_both}, but got {in_both}"