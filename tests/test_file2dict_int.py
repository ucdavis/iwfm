# test_file2dict_int.py
# Unit tests for the file2dict_int function in the iwfm package
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
import os
import tempfile

# Import directly from module since it's not exported in __init__.py
from iwfm.file2dict_int import file2dict_int


class TestFile2DictIntFunctionExists:
    """Test that the file2dict_int function exists and is callable."""

    def test_file2dict_int_exists(self):
        """Test that file2dict_int function exists and is callable."""
        assert file2dict_int is not None
        assert callable(file2dict_int)


class TestFile2DictIntBasicFunctionality:
    """Test basic functionality of file2dict_int."""

    def test_simple_two_column_file(self):
        """Test reading a simple two-column file.

        Note: The function uses 'i > skip' so line index 0 is always skipped.
        Files need a header line that gets skipped.
        """
        content = "header\n1,100\n2,200\n3,300\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            assert result == {1: 100, 2: 200, 3: 300}
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_tab_delimited_file(self):
        """Test reading a tab-delimited file."""
        content = "header\n1\t100\n2\t200\n3\t300\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            assert result == {1: 100, 2: 200, 3: 300}
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_semicolon_delimited_file(self):
        """Test reading a semicolon-delimited file."""
        content = "header\n1;100\n2;200\n3;300\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            assert result == {1: 100, 2: 200, 3: 300}
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_asterisk_delimited_file(self):
        """Test reading an asterisk-delimited file."""
        content = "header\n1*100\n2*200\n3*300\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            assert result == {1: 100, 2: 200, 3: 300}
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFile2DictIntReturnType:
    """Test the return type of file2dict_int."""

    def test_returns_dict(self):
        """Test that file2dict_int returns a dictionary."""
        content = "1,100\n2,200\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            assert isinstance(result, dict)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_keys_are_integers(self):
        """Test that dictionary keys are integers."""
        content = "1,100\n2,200\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            for key in result.keys():
                assert isinstance(key, int)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_values_are_integers(self):
        """Test that dictionary values are integers."""
        content = "1,100\n2,200\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            for value in result.values():
                assert isinstance(value, int)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFile2DictIntKeyFieldParameter:
    """Test file2dict_int key_field parameter."""

    def test_key_field_default(self):
        """Test default key_field=0 (first column)."""
        content = "header\n1,100,1000\n2,200,2000\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            # Keys should be from first column
            assert 1 in result
            assert 2 in result
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_key_field_second_column(self):
        """Test key_field=1 (second column as key)."""
        content = "header\n1,100,1000\n2,200,2000\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file, key_field=1, val_field=0)

            # Keys should be from second column
            assert 100 in result
            assert 200 in result
            assert result[100] == 1
            assert result[200] == 2
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_key_field_third_column(self):
        """Test key_field=2 (third column as key)."""
        content = "header\n1,100,1000\n2,200,2000\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file, key_field=2, val_field=0)

            # Keys should be from third column
            assert 1000 in result
            assert 2000 in result
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFile2DictIntValFieldParameter:
    """Test file2dict_int val_field parameter."""

    def test_val_field_default(self):
        """Test default val_field=1 (second column)."""
        content = "header\n1,100,1000\n2,200,2000\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            # Values should be from second column
            assert result[1] == 100
            assert result[2] == 200
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_val_field_third_column(self):
        """Test val_field=2 (third column as value)."""
        content = "header\n1,100,1000\n2,200,2000\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file, key_field=0, val_field=2)

            # Values should be from third column
            assert result[1] == 1000
            assert result[2] == 2000
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFile2DictIntSkipParameter:
    """Test file2dict_int skip parameter for header rows."""

    def test_skip_zero_default(self):
        """Test default skip=0 (no header rows skipped)."""
        # Note: with skip=0, line 0 is still processed (i > skip means i > 0)
        # So first line IS skipped with skip=0
        content = "header1,header2\n1,100\n2,200\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file, skip=0)

            # First line (header) should be skipped since i > 0 starts at line 1
            assert 1 in result
            assert 2 in result
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_skip_one_header_row(self):
        """Test skip=1 to skip one header row."""
        content = "header1,header2\n1,100\n2,200\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file, skip=1)

            # Should skip header and second line, only get third line
            assert 2 in result
            assert result[2] == 200
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_skip_multiple_header_rows(self):
        """Test skip=2 to skip multiple header rows."""
        content = "Title Line\nColumn1,Column2\n1,100\n2,200\n3,300\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file, skip=2)

            # Should skip first 3 lines (indices 0, 1, 2), only process indices 3, 4
            assert 2 in result
            assert 3 in result
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFile2DictIntEdgeCases:
    """Test edge cases for file2dict_int."""

    def test_single_line_file(self):
        """Test file with a single data line."""
        content = "1,100\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            # With skip=0, line index 0 is not processed (i > skip means i > 0)
            # So single line file returns empty dict
            assert result == {}
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_negative_integers(self):
        """Test with negative integer values."""
        content = "skip\n-1,-100\n-2,-200\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            assert result[-1] == -100
            assert result[-2] == -200
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_zero_values(self):
        """Test with zero values."""
        content = "skip\n0,0\n1,0\n0,1\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            assert 0 in result
            assert 1 in result
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_large_integers(self):
        """Test with large integer values."""
        content = "skip\n1000000,9999999\n2000000,8888888\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            assert result[1000000] == 9999999
            assert result[2000000] == 8888888
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_duplicate_keys_last_wins(self):
        """Test that duplicate keys are overwritten (last value wins)."""
        content = "skip\n1,100\n1,200\n1,300\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            # Last value for key 1 should be 300
            assert result[1] == 300
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFile2DictIntErrorHandling:
    """Test error handling in file2dict_int."""

    def test_nonexistent_file(self):
        """Test that nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            file2dict_int('nonexistent_file.txt')

    def test_non_integer_values(self):
        """Test that non-integer values raise error."""
        content = "skip\n1,abc\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            with pytest.raises(ValueError):
                file2dict_int(temp_file)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_float_values_truncated(self):
        """Test that float values raise error (not silently truncated)."""
        content = "skip\n1,100.5\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            # int() on a string with decimal point raises ValueError
            with pytest.raises(ValueError):
                file2dict_int(temp_file)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFile2DictIntRealWorldScenarios:
    """Test file2dict_int with realistic data scenarios."""

    def test_node_mapping_file(self):
        """Test reading a node ID mapping file.

        The function skips lines where index <= skip, so with skip=1,
        lines 0 and 1 are skipped (i > 1 means i >= 2).
        """
        content = """# Node mapping file
# Old ID, New ID
1,101
2,102
3,103
4,104
5,105
"""
        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            # Skip header lines: skip=1 means process lines where i > 1 (i.e., index 2+)
            result = file2dict_int(temp_file, skip=1)

            assert len(result) == 5
            assert result[1] == 101
            assert result[5] == 105
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_element_zone_assignment(self):
        """Test reading element to zone assignment file."""
        content = """Element,Zone
1,1
2,1
3,2
4,2
5,3
"""
        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = file2dict_int(temp_file)

            assert result[1] == 1
            assert result[3] == 2
            assert result[5] == 3
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
