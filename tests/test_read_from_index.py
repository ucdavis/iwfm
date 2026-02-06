# test_read_from_index.py
# unit tests for read_from_index function
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


class TestReadFromIndex:
    """Tests for the read_from_index function."""

    def test_basic_read_from_start(self, tmp_path):
        """Test reading from the beginning of the file."""
        test_file = tmp_path / "test.dat"
        content = """\
100 200 300 400 500
110 210 310 410 510
120 220 320 420 520
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        assert len(result) == 3
        assert result[0] == ['100', '200', '300', '400', '500']
        assert result[1] == ['110', '210', '310', '410', '510']
        assert result[2] == ['120', '220', '320', '420', '520']

    def test_read_from_middle(self, tmp_path):
        """Test reading starting from the middle of the file."""
        test_file = tmp_path / "test.dat"
        content = """\
line 1
line 2
100 200 300 400 500
110 210 310 410 510
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 3)

        assert len(result) == 2
        assert result[0] == ['100', '200', '300', '400', '500']
        assert result[1] == ['110', '210', '310', '410', '510']

    def test_stops_at_blank_line(self, tmp_path):
        """Test that reading stops at blank line."""
        test_file = tmp_path / "test.dat"
        content = """\
100 200 300 400 500
110 210 310 410 510

120 220 320 420 520
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        # Should only read lines before the blank line
        assert len(result) == 2
        assert result[0] == ['100', '200', '300', '400', '500']
        assert result[1] == ['110', '210', '310', '410', '510']

    def test_stops_at_comment_line(self, tmp_path):
        """Test that reading stops at line starting with 'C'."""
        test_file = tmp_path / "test.dat"
        content = """\
100 200 300 400 500
110 210 310 410 510
C This is a comment line
120 220 320 420 520
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        # Should only read lines before the comment
        assert len(result) == 2
        assert result[0] == ['100', '200', '300', '400', '500']
        assert result[1] == ['110', '210', '310', '410', '510']

    def test_six_element_line_removes_first(self, tmp_path):
        """Test that lines with 6 elements have first element removed."""
        test_file = tmp_path / "test.dat"
        content = """\
1 100 200 300 400 500
2 110 210 310 410 510
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        # First element (node number) should be removed
        assert len(result) == 2
        assert result[0] == ['100', '200', '300', '400', '500']
        assert result[1] == ['110', '210', '310', '410', '510']
        assert len(result[0]) == 5

    def test_five_element_line_kept_intact(self, tmp_path):
        """Test that lines with 5 elements are kept intact."""
        test_file = tmp_path / "test.dat"
        content = """\
100 200 300 400 500
110 210 310 410 510
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        assert len(result[0]) == 5
        assert result[0] == ['100', '200', '300', '400', '500']

    def test_mixed_element_counts(self, tmp_path):
        """Test handling of mixed 5 and 6 element lines."""
        test_file = tmp_path / "test.dat"
        content = """\
1 100 200 300 400 500
110 210 310 410 510
2 120 220 320 420 520
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        # 6-element lines should have first removed, 5-element kept
        assert result[0] == ['100', '200', '300', '400', '500']
        assert result[1] == ['110', '210', '310', '410', '510']
        assert result[2] == ['120', '220', '320', '420', '520']

    def test_returns_list_of_lists(self, tmp_path):
        """Test that function returns list of lists."""
        test_file = tmp_path / "test.dat"
        content = "100 200 300 400 500\n"
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        assert isinstance(result, list)
        assert isinstance(result[0], list)

    def test_returns_strings(self, tmp_path):
        """Test that values are returned as strings."""
        test_file = tmp_path / "test.dat"
        content = "100 200 300 400 500\n"
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        for item in result[0]:
            assert isinstance(item, str)

    def test_empty_result_at_end_of_file(self, tmp_path):
        """Test reading from index at end of file."""
        test_file = tmp_path / "test.dat"
        content = """\
line 1
line 2
line 3
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 4)

        # Reading beyond content should return empty list
        assert result == []

    def test_skip_header_lines(self, tmp_path):
        """Test skipping header/comment lines at start."""
        test_file = tmp_path / "test.dat"
        content = """\
C Header line 1
C Header line 2
C Header line 3
100 200 300 400 500
110 210 310 410 510
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 4)

        assert len(result) == 2
        assert result[0] == ['100', '200', '300', '400', '500']

    def test_file_not_found_raises_error(self, tmp_path):
        """Test that nonexistent file raises FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent.dat"

        with pytest.raises(FileNotFoundError):
            iwfm.read_from_index(str(nonexistent), 1)

    def test_single_line(self, tmp_path):
        """Test reading single line."""
        test_file = tmp_path / "test.dat"
        content = "100 200 300 400 500\n"
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        assert len(result) == 1
        assert result[0] == ['100', '200', '300', '400', '500']

    def test_whitespace_handling(self, tmp_path):
        """Test handling of various whitespace."""
        test_file = tmp_path / "test.dat"
        content = "  100   200    300  400   500  \n"
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        # Should handle multiple spaces correctly
        assert result[0] == ['100', '200', '300', '400', '500']

    def test_tab_separated_values(self, tmp_path):
        """Test handling of tab-separated values."""
        test_file = tmp_path / "test.dat"
        content = "100\t200\t300\t400\t500\n"
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        assert result[0] == ['100', '200', '300', '400', '500']

    def test_fewer_than_five_elements(self, tmp_path):
        """Test lines with fewer than 5 elements."""
        test_file = tmp_path / "test.dat"
        content = """\
100 200 300
110 210
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        assert result[0] == ['100', '200', '300']
        assert result[1] == ['110', '210']

    def test_more_than_six_elements(self, tmp_path):
        """Test lines with more than 6 elements."""
        test_file = tmp_path / "test.dat"
        content = "100 200 300 400 500 600 700\n"
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        # More than 6 elements should be kept intact
        assert result[0] == ['100', '200', '300', '400', '500', '600', '700']

    def test_comment_with_lowercase_c_not_stop(self, tmp_path):
        """Test that lowercase 'c' does not stop reading."""
        test_file = tmp_path / "test.dat"
        content = """\
100 200 300 400 500
c_value 200 300 400 500
110 210 310 410 510
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        # Lowercase 'c' at start should NOT stop reading (only uppercase 'C')
        # Wait - let me check the actual behavior
        # The code checks: line.strip().startswith("C")
        # So lowercase 'c' would continue, but 'c_value' starts with lowercase
        assert len(result) == 3


class TestReadFromIndexIwfmFormat:
    """Tests using IWFM-style file formats."""

    def test_iwfm_style_data_section(self, tmp_path):
        """Test reading IWFM-style data section."""
        test_file = tmp_path / "test.dat"
        content = """\
C*******************************************************************************
C This is a header comment
C*******************************************************************************
C   VALUE                         DESCRIPTION
C-------------------------------------------------------------------------------
    1392                          / NE
    21                            / NREGN
C*******************************************************************************
C                         Data Section
C
    1    100.5    200.3    300.1    400.2    500.0
    2    110.5    210.3    310.1    410.2    510.0
    3    120.5    220.3    320.1    420.2    520.0
C End of data section
    4    130.5    230.3    330.1    430.2    530.0
"""
        test_file.write_text(content)

        # Start at line 11 (first data line)
        result = iwfm.read_from_index(str(test_file), 11)

        assert len(result) == 3
        # 6 elements, so first (node number) is removed
        assert result[0] == ['100.5', '200.3', '300.1', '400.2', '500.0']
        assert result[1] == ['110.5', '210.3', '310.1', '410.2', '510.0']
        assert result[2] == ['120.5', '220.3', '320.1', '420.2', '520.0']

    def test_iwfm_node_data(self, tmp_path):
        """Test reading IWFM-style node coordinate data."""
        test_file = tmp_path / "test.dat"
        content = """\
C Node data
C ID    X         Y        Elev     Status
    1    6500000   2000000  100.0    1
    2    6500100   2000000  101.5    1
    3    6500200   2000000  102.0    1

C Next section
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 3)

        assert len(result) == 3
        # 5 elements, kept intact
        assert result[0] == ['1', '6500000', '2000000', '100.0', '1']

    def test_stops_at_iwfm_comment_marker(self, tmp_path):
        """Test stopping at IWFM-style comment marker."""
        test_file = tmp_path / "test.dat"
        content = """\
100 200 300 400 500
110 210 310 410 510
C***************
120 220 320 420 520
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        # Should stop at C*** comment line
        assert len(result) == 2

    def test_decimal_values(self, tmp_path):
        """Test handling of decimal values."""
        test_file = tmp_path / "test.dat"
        content = """\
100.123 200.456 300.789 400.012 500.345
-110.5 210.0 -310.25 410.75 510.125
"""
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        assert result[0] == ['100.123', '200.456', '300.789', '400.012', '500.345']
        assert result[1] == ['-110.5', '210.0', '-310.25', '410.75', '510.125']

    def test_scientific_notation(self, tmp_path):
        """Test handling of scientific notation."""
        test_file = tmp_path / "test.dat"
        content = "1.5E+06 2.0E-03 3.14159 4.0E+00 5.0E-01\n"
        test_file.write_text(content)

        result = iwfm.read_from_index(str(test_file), 1)

        assert result[0] == ['1.5E+06', '2.0E-03', '3.14159', '4.0E+00', '5.0E-01']
