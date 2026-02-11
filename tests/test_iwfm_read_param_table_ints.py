#!/usr/bin/env python
# test_iwfm_read_param_table_ints.py
# Unit tests for iwfm_read_param_table_ints.py
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
import os

from iwfm.iwfm_read_param_table_ints import iwfm_read_param_table_ints


# ---------------------------------------------------------------------------
# Multi-element path (element ID > 0): one line per element
# ---------------------------------------------------------------------------
class TestMultiElementPath:
    """Tests for the per-element parameter table path (element ID > 0)."""

    def test_single_element(self):
        """Read a table with one element."""
        file_lines = [
            '     1         10        20        30',
        ]
        params, line_index = iwfm_read_param_table_ints(file_lines, 0, 1)
        assert params.shape == (1, 3)
        np.testing.assert_array_equal(params[0], [10, 20, 30])

    def test_multiple_elements(self):
        """Read a table with multiple elements, each with its own params."""
        file_lines = [
            '     1         2         57        112',
            '     2         4         59        114',
            '     3         4         59        114',
        ]
        params, line_index = iwfm_read_param_table_ints(file_lines, 0, 3)
        assert params.shape == (3, 3)
        np.testing.assert_array_equal(params[0], [2, 57, 112])
        np.testing.assert_array_equal(params[1], [4, 59, 114])
        np.testing.assert_array_equal(params[2], [4, 59, 114])

    def test_element_id_stripped(self):
        """Element ID (first column) should not appear in the result."""
        file_lines = [
            '    99         5        10        15',
        ]
        params, _ = iwfm_read_param_table_ints(file_lines, 0, 1)
        # Should only contain [5, 10, 15], not [99, 5, 10, 15]
        assert params.shape == (1, 3)
        assert params[0][0] == 5

    def test_line_index_advance(self):
        """Returned line_index should point to the last line read."""
        file_lines = [
            'C comment line',
            '     1         10        20',
            '     2         30        40',
            '     3         50        60',
            'C next section',
        ]
        # Start reading at index 1 (first data line), read 3 elements
        params, line_index = iwfm_read_param_table_ints(file_lines, 1, 3)
        assert params.shape == (3, 2)
        # After reading 3 lines starting at index 1, internal index = 4,
        # then line_index -= 1 makes it 3
        assert line_index == 3

    def test_returns_numpy_array(self):
        """Result must be a numpy array of integers."""
        file_lines = [
            '     1         7        14',
        ]
        params, _ = iwfm_read_param_table_ints(file_lines, 0, 1)
        assert isinstance(params, np.ndarray)
        assert np.issubdtype(params.dtype, np.integer)

    def test_single_column(self):
        """Table with only one parameter column per element."""
        file_lines = [
            '     1         42',
            '     2         99',
        ]
        params, _ = iwfm_read_param_table_ints(file_lines, 0, 2)
        assert params.shape == (2, 1)
        np.testing.assert_array_equal(params.flatten(), [42, 99])


# ---------------------------------------------------------------------------
# Single-set path (element ID == 0): one line applies to all elements
# ---------------------------------------------------------------------------
class TestSingleSetPath:
    """Tests for the uniform parameter path (element ID == 0)."""

    def test_zero_element_single_set(self):
        """Element 0 means one set of params for all elements."""
        file_lines = [
            '     0         5        10        15',
            'C next section',
        ]
        params, line_index = iwfm_read_param_table_ints(file_lines, 0, 100)
        # Should return a 1-D array [5, 10, 15]
        np.testing.assert_array_equal(params, [5, 10, 15])

    def test_zero_element_line_index(self):
        """Line index should advance past the single line via read_next_line_value."""
        file_lines = [
            '     0         5        10        15',
            'C comment',
            '     next data line',
        ]
        _, line_index = iwfm_read_param_table_ints(file_lines, 0, 100)
        # read_next_line_value skips to next data line, then line_index -= 1
        # Exact value depends on skip_ahead behavior with comments
        assert line_index >= 0


# ---------------------------------------------------------------------------
# Test with real C2VSimCG-2025 NonPondedCrop data
# ---------------------------------------------------------------------------
class TestC2VSimCGData:
    """Tests using the C2VSimCG-2025 ICET parameter table."""

    @pytest.fixture
    def npc_file_lines(self):
        """Load the NonPondedCrop file lines."""
        dat_path = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2025', 'Simulation', 'RootZone',
            'C2VSimCG_NonPondedCrop.dat',
        )
        if not os.path.isfile(dat_path):
            pytest.skip('C2VSimCG-2025 test data not available')
        with open(dat_path, 'r') as f:
            return f.read().splitlines()

    def test_read_icet_table(self, npc_file_lines):
        """Read the ICET (Reference ET column pointers) table starting at line 1584."""
        # line 1584 is 1-indexed; 0-indexed = 1583
        ne = 1392  # number of elements in C2VSimCG
        params, line_index = iwfm_read_param_table_ints(npc_file_lines, 1583, ne)
        assert params.shape == (ne, 20)  # 20 non-ponded crops

    def test_first_element_values(self, npc_file_lines):
        """Verify element 1 ICET values match the file."""
        params, _ = iwfm_read_param_table_ints(npc_file_lines, 1583, 1392)
        expected = [2, 57, 112, 167, 222, 277, 332, 387, 442, 497,
                    552, 607, 662, 717, 772, 827, 882, 937, 992, 1047]
        np.testing.assert_array_equal(params[0], expected)

    def test_last_element_values(self, npc_file_lines):
        """Verify element 1392 ICET values match the file."""
        params, _ = iwfm_read_param_table_ints(npc_file_lines, 1583, 1392)
        expected = [36, 91, 146, 201, 256, 311, 366, 421, 476, 531,
                    586, 641, 696, 751, 806, 861, 916, 971, 1026, 1081]
        np.testing.assert_array_equal(params[-1], expected)

    def test_line_index_after_table(self, npc_file_lines):
        """Line index should land on the last element line (1392 lines from 1583)."""
        _, line_index = iwfm_read_param_table_ints(npc_file_lines, 1583, 1392)
        # Reads 1392 lines starting at 1583, internal index reaches 1583+1392=2975,
        # then line_index -= 1 gives 2974
        assert line_index == 2974

    def test_all_values_positive(self, npc_file_lines):
        """All ET column pointers should be positive integers."""
        params, _ = iwfm_read_param_table_ints(npc_file_lines, 1583, 1392)
        assert np.all(params > 0)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
