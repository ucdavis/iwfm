#!/usr/bin/env python
# test_file_utils.py
# Unit tests for iwfm/file_utils.py utility functions
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


class TestReadNextLineValue:
    """Tests for read_next_line_value function"""

    def test_basic_read(self):
        """Test basic reading of next line value"""
        lines = ['file1.txt', 'file2.txt', 'file3.txt']
        value, idx = iwfm.read_next_line_value(lines, -1)
        assert value == 'file1.txt'
        assert idx == 0

    def test_skip_comment_lines(self):
        """Test skipping comment lines marked with C"""
        lines = ['C Comment line', 'C Another comment', 'data.txt']
        value, idx = iwfm.read_next_line_value(lines, -1, skip_lines=0)
        assert value == 'data.txt'
        assert idx == 2

    def test_inline_comments(self):
        """Test handling inline comments after data"""
        lines = ['file.txt  ! This is a comment', 'other.txt']
        value, idx = iwfm.read_next_line_value(lines, -1)
        assert value == 'file.txt'
        assert idx == 0

    def test_column_selection(self):
        """Test extracting from specific column"""
        lines = ['10 20 30', '40 50 60']
        value, idx = iwfm.read_next_line_value(lines, -1, column=1)
        assert value == '20'
        assert idx == 0

        value, idx = iwfm.read_next_line_value(lines, 0, column=2)
        assert value == '60'
        assert idx == 1

    def test_strip_whitespace(self):
        """Test whitespace stripping"""
        lines = ['  file.txt  ', 'other.txt']
        value, idx = iwfm.read_next_line_value(lines, -1, strip=True)
        assert value == 'file.txt'

        value, idx = iwfm.read_next_line_value(lines, -1, strip=False)
        assert value == 'file.txt'  # split() already removes leading/trailing

    def test_sequential_reads(self):
        """Test reading multiple values sequentially"""
        lines = ['file1.txt', 'file2.txt', 'file3.txt']
        value1, idx1 = iwfm.read_next_line_value(lines, -1)
        value2, idx2 = iwfm.read_next_line_value(lines, idx1)
        value3, idx3 = iwfm.read_next_line_value(lines, idx2)

        assert value1 == 'file1.txt'
        assert value2 == 'file2.txt'
        assert value3 == 'file3.txt'
        assert idx3 == 2

    def test_column_out_of_range(self):
        """Test error handling for non-existent column"""
        lines = ['10 20', '30 40']
        with pytest.raises(IndexError, match='Column 5 not found'):
            iwfm.read_next_line_value(lines, -1, column=5)

    def test_with_skip_lines_parameter(self):
        """Test using skip_lines to skip comment blocks"""
        lines = [
            'C Comment 1',
            'C Comment 2',
            '# Comment 3',
            'data.txt'
        ]
        value, idx = iwfm.read_next_line_value(lines, -1, skip_lines=0)
        assert value == 'data.txt'
        assert idx == 3


class TestReadMultipleLineValues:
    """Tests for read_multiple_line_values function"""

    def test_basic_multiple_read(self):
        """Test reading multiple consecutive values"""
        lines = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
        values, idx = iwfm.read_multiple_line_values(lines, -1, 3)
        assert values == ['file1.txt', 'file2.txt', 'file3.txt']
        assert idx == 2

    def test_read_all_lines(self):
        """Test reading all available lines"""
        # Note: avoid filenames starting with 'c' or 'C' as they're treated as comments by skip_ahead
        lines = ['file1.dat', 'file2.dat', 'file3.dat']
        values, idx = iwfm.read_multiple_line_values(lines, -1, 3)
        assert values == ['file1.dat', 'file2.dat', 'file3.dat']
        assert idx == 2

    def test_column_selection_multiple(self):
        """Test reading from specific column across multiple lines"""
        lines = ['1 data1.dat', '2 data2.dat', '3 data3.dat']
        values, idx = iwfm.read_multiple_line_values(lines, -1, 3, column=1)
        assert values == ['data1.dat', 'data2.dat', 'data3.dat']

    def test_empty_count(self):
        """Test reading zero values"""
        lines = ['file1.txt', 'file2.txt']
        values, idx = iwfm.read_multiple_line_values(lines, -1, 0)
        assert values == []
        assert idx == -1

    def test_with_comments_between(self):
        """Test reading with comment lines interspersed"""
        lines = [
            'file1.txt',
            'C Comment',
            'file2.txt',
            'C Another comment',
            'file3.txt'
        ]
        values, idx = iwfm.read_multiple_line_values(lines, -1, 3, skip_lines=0)
        assert values == ['file1.txt', 'file2.txt', 'file3.txt']

    def test_sequential_calls(self):
        """Test multiple sequential calls to read different blocks"""
        # Avoid single letters that might be treated as comments (c, C, *, #)
        lines = ['file1', 'file2', 'file3', 'file4', 'file5', 'file6']
        values1, idx1 = iwfm.read_multiple_line_values(lines, -1, 2)
        values2, idx2 = iwfm.read_multiple_line_values(lines, idx1, 2)
        values3, idx3 = iwfm.read_multiple_line_values(lines, idx2, 2)

        assert values1 == ['file1', 'file2']
        assert values2 == ['file3', 'file4']
        assert values3 == ['file5', 'file6']
        assert idx3 == 5


class TestReadLineValuesToDict:
    """Tests for read_line_values_to_dict function"""

    def test_basic_dict_creation(self):
        """Test basic dictionary creation from lines"""
        lines = ['np_crops.dat', 'p_crops.dat', 'urban.dat', 'native.dat']
        keys = ['np_file', 'p_file', 'ur_file', 'nr_file']
        result, idx = iwfm.read_line_values_to_dict(lines, -1, keys)

        assert result == {
            'np_file': 'np_crops.dat',
            'p_file': 'p_crops.dat',
            'ur_file': 'urban.dat',
            'nr_file': 'native.dat'
        }
        assert idx == 3

    def test_single_entry_dict(self):
        """Test creating dict with single entry"""
        lines = ['data.txt']
        keys = ['datafile']
        result, idx = iwfm.read_line_values_to_dict(lines, -1, keys)

        assert result == {'datafile': 'data.txt'}
        assert idx == 0

    def test_column_selection_dict(self):
        """Test creating dict from specific column"""
        lines = ['1 file1.dat', '2 file2.dat', '3 file3.dat']
        keys = ['first', 'second', 'third']
        result, idx = iwfm.read_line_values_to_dict(lines, -1, keys, column=1)

        assert result == {
            'first': 'file1.dat',
            'second': 'file2.dat',
            'third': 'file3.dat'
        }

    def test_empty_keys_list(self):
        """Test with empty keys list"""
        lines = ['file1.txt', 'file2.txt']
        keys = []
        result, idx = iwfm.read_line_values_to_dict(lines, -1, keys)

        assert result == {}
        assert idx == -1

    def test_keys_value_ordering(self):
        """Test that dictionary maintains key-value pairs correctly"""
        lines = ['value1', 'value2', 'value3']
        keys = ['key_a', 'key_b', 'key_c']
        result, idx = iwfm.read_line_values_to_dict(lines, -1, keys)

        assert list(result.keys()) == keys
        assert result['key_a'] == 'value1'
        assert result['key_b'] == 'value2'
        assert result['key_c'] == 'value3'

    def test_with_comment_lines(self):
        """Test dictionary creation with comment lines"""
        lines = [
            'C Configuration section',
            'file1.dat',
            'C Intermediate comment',
            'file2.dat',
            'file3.dat'
        ]
        keys = ['input', 'output', 'temp']
        result, idx = iwfm.read_line_values_to_dict(lines, -1, keys, skip_lines=0)

        assert result == {
            'input': 'file1.dat',
            'output': 'file2.dat',
            'temp': 'file3.dat'
        }


class TestIntegrationScenarios:
    """Integration tests simulating real IWFM file reading scenarios"""

    def test_rootzone_file_pattern(self):
        """Test pattern used in iwfm_read_rz.py"""
        # Simulate rootzone main file structure
        lines = [
            'C Root zone main file',
            'C IWFM Version 2015',
            'C Comment line 3',
            'C Comment line 4',
            'npc_file.dat   ! Non-ponded crops',
            'pc_file.dat    ! Ponded crops',
            'urban_file.dat ! Urban',
            'native_file.dat ! Native and riparian',
            'return_file.dat ! Return flow',
            'reuse_file.dat ! Reuse',
            'irrig_file.dat ! Irrigation period'
        ]

        # Simulate the old pattern
        line_index = -1
        for _ in range(4):  # Skip 4 comment lines
            line_index += 1

        # New pattern using utility function
        keys = ['np_file', 'p_file', 'ur_file', 'nr_file',
                'rf_file', 'ru_file', 'ir_file']
        result, idx = iwfm.read_line_values_to_dict(lines, line_index, keys)

        assert result['np_file'] == 'npc_file.dat'
        assert result['p_file'] == 'pc_file.dat'
        assert result['ur_file'] == 'urban_file.dat'
        assert result['nr_file'] == 'native_file.dat'
        assert result['rf_file'] == 'return_file.dat'
        assert result['ru_file'] == 'reuse_file.dat'
        assert result['ir_file'] == 'irrig_file.dat'

    def test_groundwater_file_pattern(self):
        """Test pattern used in iwfm_read_gw.py"""
        lines = [
            'C Groundwater main file',
            'bc_file.dat      ! Boundary conditions',
            'td_file.dat      ! Tile drains',
            'pump_file.dat    ! Pumping',
            'subs_file.dat    ! Subsidence'
        ]

        line_index = 0  # Start after first comment
        keys = ['bc', 'tiledrain', 'pumping', 'subsidence']
        result, idx = iwfm.read_line_values_to_dict(lines, line_index, keys, skip_lines=0)

        assert result['bc'] == 'bc_file.dat'
        assert result['tiledrain'] == 'td_file.dat'
        assert result['pumping'] == 'pump_file.dat'
        assert result['subsidence'] == 'subs_file.dat'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
