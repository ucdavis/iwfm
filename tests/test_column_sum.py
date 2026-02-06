# test_column_sum.py
# Unit tests for the column_sum function in the iwfm package
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

import iwfm


class TestColumnSumFunctionExists:
    """Test that the column_sum function exists and is callable."""

    def test_column_sum_exists(self):
        """Test that column_sum function exists in the iwfm module."""
        assert hasattr(iwfm, 'column_sum')
        assert callable(getattr(iwfm, 'column_sum'))


class TestColumnSumBasicFunctionality:
    """Test basic functionality of column_sum."""

    def test_single_column(self):
        """Test summing a single column."""
        lst = [
            [1],
            [2],
            [3]
        ]
        result = iwfm.column_sum(lst)
        assert result == [6]

    def test_two_columns(self):
        """Test summing two columns."""
        lst = [
            [1, 10],
            [2, 20],
            [3, 30]
        ]
        result = iwfm.column_sum(lst)
        assert result == [6, 60]

    def test_three_columns(self):
        """Test summing three columns."""
        lst = [
            [1, 10, 100],
            [2, 20, 200],
            [3, 30, 300]
        ]
        result = iwfm.column_sum(lst)
        assert result == [6, 60, 600]

    def test_single_row(self):
        """Test with a single row."""
        lst = [[1, 2, 3, 4, 5]]
        result = iwfm.column_sum(lst)
        assert result == [1, 2, 3, 4, 5]

    def test_two_rows(self):
        """Test with two rows."""
        lst = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        result = iwfm.column_sum(lst)
        assert result == [5, 7, 9]


class TestColumnSumReturnType:
    """Test the return type of column_sum."""

    def test_returns_list(self):
        """Test that column_sum returns a list."""
        lst = [[1, 2], [3, 4]]
        result = iwfm.column_sum(lst)
        assert isinstance(result, list)

    def test_return_length_matches_columns(self):
        """Test that return list length matches number of columns."""
        lst = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10]
        ]
        result = iwfm.column_sum(lst)
        assert len(result) == 5


class TestColumnSumWithIntegers:
    """Test column_sum with integer values."""

    def test_positive_integers(self):
        """Test with positive integers."""
        lst = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        result = iwfm.column_sum(lst)
        assert result == [12, 15, 18]

    def test_negative_integers(self):
        """Test with negative integers."""
        lst = [
            [-1, -2, -3],
            [-4, -5, -6]
        ]
        result = iwfm.column_sum(lst)
        assert result == [-5, -7, -9]

    def test_mixed_positive_negative_integers(self):
        """Test with mixed positive and negative integers."""
        lst = [
            [10, -20, 30],
            [-10, 20, -30]
        ]
        result = iwfm.column_sum(lst)
        assert result == [0, 0, 0]

    def test_zeros(self):
        """Test with all zeros."""
        lst = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        result = iwfm.column_sum(lst)
        assert result == [0, 0, 0]


class TestColumnSumWithFloats:
    """Test column_sum with floating point values."""

    def test_positive_floats(self):
        """Test with positive floats."""
        lst = [
            [1.5, 2.5],
            [3.5, 4.5]
        ]
        result = iwfm.column_sum(lst)
        assert result == [5.0, 7.0]

    def test_negative_floats(self):
        """Test with negative floats."""
        lst = [
            [-1.1, -2.2],
            [-3.3, -4.4]
        ]
        result = iwfm.column_sum(lst)
        assert abs(result[0] - (-4.4)) < 0.001
        assert abs(result[1] - (-6.6)) < 0.001

    def test_mixed_int_float(self):
        """Test with mixed integers and floats."""
        lst = [
            [1, 2.5, 3],
            [4.5, 5, 6.5]
        ]
        result = iwfm.column_sum(lst)
        assert result[0] == 5.5
        assert result[1] == 7.5
        assert result[2] == 9.5

    def test_small_decimals(self):
        """Test with small decimal values."""
        lst = [
            [0.001, 0.002],
            [0.003, 0.004],
            [0.005, 0.006]
        ]
        result = iwfm.column_sum(lst)
        assert abs(result[0] - 0.009) < 0.0001
        assert abs(result[1] - 0.012) < 0.0001

    def test_large_floats(self):
        """Test with large floating point values."""
        lst = [
            [1000000.5, 2000000.5],
            [3000000.5, 4000000.5]
        ]
        result = iwfm.column_sum(lst)
        assert result[0] == 4000001.0
        assert result[1] == 6000001.0


class TestColumnSumEdgeCases:
    """Test edge cases for column_sum."""

    def test_empty_list(self):
        """Test with empty list."""
        lst = []
        result = iwfm.column_sum(lst)
        assert result == []

    def test_many_rows(self):
        """Test with many rows."""
        lst = [[i] for i in range(100)]
        result = iwfm.column_sum(lst)
        # Sum of 0 to 99 = 99*100/2 = 4950
        assert result == [4950]

    def test_many_columns(self):
        """Test with many columns."""
        lst = [
            list(range(50)),
            list(range(50))
        ]
        result = iwfm.column_sum(lst)
        assert len(result) == 50
        # Each column sums two identical values
        for i in range(50):
            assert result[i] == i * 2


class TestColumnSumRealWorldScenarios:
    """Test column_sum with realistic data scenarios."""

    def test_budget_data_columns(self):
        """Test summing budget-like data columns."""
        # Simulate budget data: [inflow, outflow, storage]
        lst = [
            [1000.0, 800.0, 200.0],   # Period 1
            [1200.0, 900.0, 500.0],   # Period 2
            [1100.0, 850.0, 750.0],   # Period 3
            [1300.0, 1000.0, 1050.0]  # Period 4
        ]
        result = iwfm.column_sum(lst)
        assert result[0] == 4600.0  # Total inflow
        assert result[1] == 3550.0  # Total outflow
        assert result[2] == 2500.0  # Total storage change

    def test_coordinate_data(self):
        """Test summing coordinate-like data."""
        # Simulate summing x, y offsets
        lst = [
            [10.0, 20.0],
            [5.0, -10.0],
            [-3.0, 15.0]
        ]
        result = iwfm.column_sum(lst)
        assert result[0] == 12.0  # Sum of x offsets
        assert result[1] == 25.0  # Sum of y offsets

    def test_time_series_data(self):
        """Test summing time series data columns."""
        # Simulate monthly values for different locations
        lst = [
            [100, 200, 300],  # Jan
            [110, 210, 310],  # Feb
            [120, 220, 320],  # Mar
            [130, 230, 330],  # Apr
        ]
        result = iwfm.column_sum(lst)
        assert result[0] == 460   # Location 1 total
        assert result[1] == 860   # Location 2 total
        assert result[2] == 1260  # Location 3 total

    def test_square_matrix(self):
        """Test summing a square matrix."""
        lst = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        result = iwfm.column_sum(lst)
        assert result == [12, 15, 18]


class TestColumnSumSpecialValues:
    """Test column_sum with special numeric values."""

    def test_very_large_values(self):
        """Test with very large values."""
        lst = [
            [1e10, 1e10],
            [1e10, 1e10]
        ]
        result = iwfm.column_sum(lst)
        assert result[0] == 2e10
        assert result[1] == 2e10

    def test_very_small_values(self):
        """Test with very small values."""
        lst = [
            [1e-10, 1e-10],
            [1e-10, 1e-10]
        ]
        result = iwfm.column_sum(lst)
        assert abs(result[0] - 2e-10) < 1e-15
        assert abs(result[1] - 2e-10) < 1e-15


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
