# test_iwfm_read_param_table_floats.py
# Tests for iwfm_read_param_table_floats function
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

"""
Tests for iwfm.iwfm_read_param_table_floats function.

The iwfm_read_param_table_floats function reads a table of float parameters
from file lines and returns a numpy array.

Two modes of operation:
1. If first value is 0: One set of values for all elements (returns 1D array)
2. If first value is not 0: Multiple rows of values (returns 2D array)

The function skips the first column (element/line ID) and returns only the
float values from columns 2+.
"""

import os
import sys
import inspect
import numpy as np

# Add the iwfm directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from iwfm.iwfm_read_param_table_floats import iwfm_read_param_table_floats


class TestIwfmReadParamTableFloatsFunctionExists:
    """Test that iwfm_read_param_table_floats function exists and has correct signature."""

    def test_function_exists(self):
        """Test that iwfm_read_param_table_floats function is importable."""
        assert iwfm_read_param_table_floats is not None

    def test_function_is_callable(self):
        """Test that iwfm_read_param_table_floats is callable."""
        assert callable(iwfm_read_param_table_floats)

    def test_function_has_docstring(self):
        """Test that iwfm_read_param_table_floats has a docstring."""
        assert iwfm_read_param_table_floats.__doc__ is not None
        assert len(iwfm_read_param_table_floats.__doc__) > 0

    def test_function_signature(self):
        """Test that iwfm_read_param_table_floats has the expected parameters."""
        sig = inspect.signature(iwfm_read_param_table_floats)
        params = list(sig.parameters.keys())

        assert 'file_lines' in params
        assert 'line_index' in params
        assert 'lines' in params


class TestIwfmReadParamTableFloatsReturnValue:
    """Test the return value structure of iwfm_read_param_table_floats."""

    def test_returns_tuple(self):
        """Test that function returns a tuple."""
        file_lines = ["1    0.5    0.6", "C next section"]
        result = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert isinstance(result, tuple)

    def test_returns_tuple_of_two_elements(self):
        """Test that function returns tuple with two elements."""
        file_lines = ["1    0.5    0.6", "C next section"]
        result = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert len(result) == 2

    def test_first_element_is_numpy_array(self):
        """Test that first element of return tuple is numpy array."""
        file_lines = ["1    0.5    0.6", "C next section"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert isinstance(params, np.ndarray)

    def test_second_element_is_integer(self):
        """Test that second element of return tuple is integer (line index)."""
        file_lines = ["1    0.5    0.6", "C next section"]
        _, line_index = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert isinstance(line_index, int)


class TestIwfmReadParamTableFloatsSingleSetMode:
    """Test behavior when first value is 0 (single set for all elements)."""

    def test_single_set_mode_detection(self):
        """Test that function detects single set mode when first value is 0."""
        file_lines = ["0    0.5    0.6    0.7", "C next section"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 3)
        # Should return 1D array with values from columns 2+
        assert params.ndim == 1

    def test_single_set_mode_values(self):
        """Test that single set mode extracts correct values."""
        file_lines = ["0    0.5    0.6    0.7", "C next section"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 3)
        # Should skip the first value (0) and return the rest
        assert len(params) == 3
        assert abs(params[0] - 0.5) < 0.0001
        assert abs(params[1] - 0.6) < 0.0001
        assert abs(params[2] - 0.7) < 0.0001

    def test_single_set_mode_skips_element_id(self):
        """Test that single set mode skips the first column (element ID)."""
        file_lines = ["0    1.0    2.0", "C next section"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 2)
        # Should NOT include the 0
        assert 0 not in params


class TestIwfmReadParamTableFloatsMultipleRowsMode:
    """Test behavior when first value is not 0 (multiple rows)."""

    def test_multiple_rows_mode_detection(self):
        """Test that function detects multiple rows mode when first value is not 0."""
        file_lines = [
            "1    0.5    0.6",
            "2    0.7    0.8",
            "3    0.9    1.0",
            "C next section"
        ]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 3)
        # Should return 2D array
        assert params.ndim == 2

    def test_multiple_rows_mode_shape(self):
        """Test that multiple rows mode returns correct shape."""
        file_lines = [
            "1    0.5    0.6",
            "2    0.7    0.8",
            "3    0.9    1.0",
            "C next section"
        ]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 3)
        assert params.shape == (3, 2)  # 3 rows, 2 value columns (skipping element ID)

    def test_multiple_rows_mode_values(self):
        """Test that multiple rows mode extracts correct values."""
        file_lines = [
            "1    0.5    0.6",
            "2    0.7    0.8",
            "3    0.9    1.0",
            "C next section"
        ]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 3)

        # Check first row
        assert abs(params[0][0] - 0.5) < 0.0001
        assert abs(params[0][1] - 0.6) < 0.0001

        # Check second row
        assert abs(params[1][0] - 0.7) < 0.0001
        assert abs(params[1][1] - 0.8) < 0.0001

        # Check third row
        assert abs(params[2][0] - 0.9) < 0.0001
        assert abs(params[2][1] - 1.0) < 0.0001

    def test_multiple_rows_mode_skips_element_ids(self):
        """Test that multiple rows mode skips the first column (element IDs)."""
        file_lines = [
            "1    0.5    0.6",
            "2    0.7    0.8",
            "C next section"
        ]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 2)
        # Should NOT include element IDs (1, 2)
        assert 1 not in params.flatten()
        assert 2 not in params.flatten()


class TestIwfmReadParamTableFloatsLineIndex:
    """Test line index tracking."""

    def test_line_index_returned_single_set(self):
        """Test that line_index is returned for single set mode."""
        file_lines = [
            "0    0.5    0.6",
            "1    0.7    0.8",  # Next data line
            "C next section"
        ]
        # Function should read the single set line and use read_next_line_value
        params, new_line_index = iwfm_read_param_table_floats(file_lines, 0, 1)
        # Just verify we get an integer line index back
        assert isinstance(new_line_index, int)

    def test_line_index_advances_multiple_rows(self):
        """Test that line_index advances correctly for multiple rows."""
        file_lines = [
            "1    0.5    0.6",
            "2    0.7    0.8",
            "3    0.9    1.0",
            "C next section"
        ]
        _, new_line_index = iwfm_read_param_table_floats(file_lines, 0, 3)
        # After reading 3 lines, line_index should be 2 (0+3-1=2, due to line_index -= 1)
        assert new_line_index == 2

    def test_line_index_with_offset(self):
        """Test function works with non-zero starting line index."""
        file_lines = [
            "C header",
            "C more header",
            "1    0.5    0.6",
            "2    0.7    0.8",
            "C next section"
        ]
        params, new_line_index = iwfm_read_param_table_floats(file_lines, 2, 2)
        assert params.shape == (2, 2)
        assert new_line_index == 3


class TestIwfmReadParamTableFloatsDataTypes:
    """Test data type handling."""

    def test_returns_float_values(self):
        """Test that returned values are floats."""
        file_lines = ["1    0.5    0.6", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert params.dtype in [np.float64, np.float32]

    def test_handles_integer_like_floats(self):
        """Test handling of integer-like values written as floats."""
        file_lines = ["1    1.0    2.0    3.0", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert abs(params[0][0] - 1.0) < 0.0001
        assert abs(params[0][1] - 2.0) < 0.0001
        assert abs(params[0][2] - 3.0) < 0.0001

    def test_handles_scientific_notation(self):
        """Test handling of scientific notation."""
        file_lines = ["1    1.5e-3    2.0E+2", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert abs(params[0][0] - 0.0015) < 0.00001
        assert abs(params[0][1] - 200.0) < 0.1

    def test_handles_negative_values(self):
        """Test handling of negative values."""
        file_lines = ["1    -0.5    -1.5", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert abs(params[0][0] - (-0.5)) < 0.0001
        assert abs(params[0][1] - (-1.5)) < 0.0001


class TestIwfmReadParamTableFloatsWhitespace:
    """Test whitespace handling."""

    def test_handles_multiple_spaces(self):
        """Test handling of multiple spaces between values."""
        file_lines = ["1     0.5     0.6", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert abs(params[0][0] - 0.5) < 0.0001
        assert abs(params[0][1] - 0.6) < 0.0001

    def test_handles_tabs(self):
        """Test handling of tab-separated values."""
        file_lines = ["1\t0.5\t0.6", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert abs(params[0][0] - 0.5) < 0.0001
        assert abs(params[0][1] - 0.6) < 0.0001

    def test_handles_leading_whitespace(self):
        """Test handling of leading whitespace."""
        file_lines = ["    1    0.5    0.6", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert abs(params[0][0] - 0.5) < 0.0001
        assert abs(params[0][1] - 0.6) < 0.0001


class TestIwfmReadParamTableFloatsEdgeCases:
    """Test edge cases."""

    def test_single_row_single_value(self):
        """Test handling of single row with single value column."""
        file_lines = ["1    0.5", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert params.shape == (1, 1)
        assert abs(params[0][0] - 0.5) < 0.0001

    def test_many_columns(self):
        """Test handling of many value columns."""
        file_lines = ["1    0.1    0.2    0.3    0.4    0.5    0.6    0.7    0.8", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert params.shape == (1, 8)

    def test_many_rows(self):
        """Test handling of many rows."""
        file_lines = [f"{i}    {i*0.1:.1f}    {i*0.2:.1f}" for i in range(1, 101)]
        file_lines.append("C next section")
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 100)
        assert params.shape == (100, 2)

    def test_single_set_single_value(self):
        """Test single set mode with single value."""
        file_lines = ["0    0.5", "C next"]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 1)
        assert params.ndim == 1
        assert len(params) == 1
        assert abs(params[0] - 0.5) < 0.0001


class TestIwfmReadParamTableFloatsRealWorldData:
    """Test with data similar to IWFM initial conditions format."""

    def test_uz_initial_conditions_format(self):
        """Test with data matching UZ initial conditions format."""
        # Format: element_id  moisture_layer1  moisture_layer2
        file_lines = [
            "        1     0.05981     0.05985",
            "        2     0.05827     0.05689",
            "        3     0.05323     0.05604",
            "C next section"
        ]
        params, _ = iwfm_read_param_table_floats(file_lines, 0, 3)

        assert params.shape == (3, 2)
        # Check first row
        assert abs(params[0][0] - 0.05981) < 0.00001
        assert abs(params[0][1] - 0.05985) < 0.00001
        # Check second row
        assert abs(params[1][0] - 0.05827) < 0.00001
        assert abs(params[1][1] - 0.05689) < 0.00001

    def test_consistent_results(self):
        """Test that results are consistent for same input."""
        file_lines = [
            "1    0.5    0.6",
            "2    0.7    0.8",
            "C next"
        ]
        result1 = iwfm_read_param_table_floats(file_lines, 0, 2)
        result2 = iwfm_read_param_table_floats(file_lines, 0, 2)

        assert np.array_equal(result1[0], result2[0])
        assert result1[1] == result2[1]
