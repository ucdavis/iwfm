# test_skip_ahead.py
# unit tests for skip_ahead function
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


class TestSkipAheadBasic:
    """Basic tests for skip_ahead function."""

    def test_no_skip_no_comments(self):
        """Test with skip=0 and no comment lines."""
        lines = ["line1", "line2", "line3"]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 0

    def test_skip_one_line(self):
        """Test skipping one non-comment line."""
        lines = ["line1", "line2", "line3"]

        result = iwfm.skip_ahead(0, lines, skip=1)

        assert result == 1

    def test_skip_multiple_lines(self):
        """Test skipping multiple non-comment lines."""
        lines = ["line1", "line2", "line3", "line4", "line5"]

        result = iwfm.skip_ahead(0, lines, skip=3)

        assert result == 3

    def test_returns_int(self):
        """Test that function returns an integer."""
        lines = ["line1", "line2"]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert isinstance(result, int)

    def test_default_skip_is_zero(self):
        """Test that default skip parameter is 0."""
        lines = ["line1", "line2"]

        result = iwfm.skip_ahead(0, lines)

        assert result == 0

    def test_start_from_middle(self):
        """Test starting from middle of list."""
        lines = ["line1", "line2", "line3", "line4"]

        result = iwfm.skip_ahead(2, lines, skip=1)

        assert result == 3


class TestSkipAheadComments:
    """Tests for comment line handling."""

    def test_skip_c_uppercase_comment(self):
        """Test skipping line starting with uppercase C."""
        lines = ["C This is a comment", "data line"]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 1

    def test_skip_c_lowercase_comment(self):
        """Test skipping line starting with lowercase c."""
        lines = ["c This is a comment", "data line"]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 1

    def test_skip_asterisk_comment(self):
        """Test skipping line starting with asterisk."""
        lines = ["* This is a comment", "data line"]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 1

    def test_skip_hash_comment(self):
        """Test skipping line starting with hash."""
        lines = ["# This is a comment", "data line"]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 1

    def test_skip_multiple_comment_lines(self):
        """Test skipping multiple consecutive comment lines."""
        lines = [
            "C Comment 1",
            "c Comment 2",
            "* Comment 3",
            "# Comment 4",
            "data line"
        ]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 4

    def test_mixed_comments_and_data(self):
        """Test with mixed comments and data lines."""
        lines = [
            "C Comment",
            "data1",
            "C Another comment",
            "data2"
        ]

        # Start at 0, skip 0 non-comment lines -> should skip C Comment, land on data1
        result = iwfm.skip_ahead(0, lines, skip=0)
        assert result == 1

    def test_skip_with_comments_interspersed(self):
        """Test skipping non-comment lines with comments in between."""
        lines = [
            "data1",
            "C Comment",
            "data2",
            "* Another comment",
            "data3"
        ]

        # Skip 2 non-comment lines (data1 and data2), landing on data3
        result = iwfm.skip_ahead(0, lines, skip=2)

        assert result == 4

    def test_comments_after_skip_target(self):
        """Test that comments after skip target are also skipped."""
        lines = [
            "data1",
            "C Comment 1",
            "C Comment 2",
            "data2"
        ]

        # Skip 1 non-comment line (data1), then skip comments, land on data2
        result = iwfm.skip_ahead(0, lines, skip=1)

        assert result == 3


class TestSkipAheadEndOfFile:
    """Tests for end-of-file handling."""

    def test_returns_negative_one_at_end(self):
        """Test that -1 is returned when end of list is reached."""
        lines = ["line1", "line2"]

        result = iwfm.skip_ahead(0, lines, skip=5)

        assert result == -1

    def test_empty_list(self):
        """Test with empty list."""
        lines = []

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == -1

    def test_start_at_end(self):
        """Test starting at the end of list."""
        lines = ["line1", "line2"]

        result = iwfm.skip_ahead(2, lines, skip=0)

        assert result == -1

    def test_only_comments_returns_negative_one(self):
        """Test that -1 is returned when only comments remain."""
        lines = [
            "C Comment 1",
            "C Comment 2",
            "* Comment 3"
        ]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == -1

    def test_skip_past_end(self):
        """Test skipping past end of list."""
        lines = ["line1", "line2", "line3"]

        result = iwfm.skip_ahead(0, lines, skip=10)

        assert result == -1

    def test_comments_then_end(self):
        """Test comments at end of list."""
        lines = [
            "data1",
            "C Comment at end"
        ]

        result = iwfm.skip_ahead(0, lines, skip=1)

        assert result == -1


class TestSkipAheadInputValidation:
    """Tests for input validation."""

    def test_negative_line_index_raises_error(self):
        """Test that negative line_index raises ValueError."""
        lines = ["line1", "line2"]

        with pytest.raises(ValueError, match="line_index must be non-negative"):
            iwfm.skip_ahead(-1, lines, skip=0)

    def test_negative_skip_raises_error(self):
        """Test that negative skip raises ValueError."""
        lines = ["line1", "line2"]

        with pytest.raises(ValueError, match="skip must be non-negative"):
            iwfm.skip_ahead(0, lines, skip=-1)

    def test_non_list_raises_error(self):
        """Test that non-list all_lines raises TypeError."""
        with pytest.raises(TypeError, match="all_lines must be a list"):
            iwfm.skip_ahead(0, "not a list", skip=0)

    def test_non_int_line_index_raises_error(self):
        """Test that non-integer line_index raises TypeError."""
        lines = ["line1", "line2"]

        with pytest.raises(TypeError, match="line_index must be an integer"):
            iwfm.skip_ahead(1.5, lines, skip=0)

    def test_non_int_skip_raises_error(self):
        """Test that non-integer skip raises TypeError."""
        lines = ["line1", "line2"]

        with pytest.raises(TypeError, match="skip must be an integer"):
            iwfm.skip_ahead(0, lines, skip=1.5)

    def test_tuple_raises_error(self):
        """Test that tuple raises TypeError."""
        with pytest.raises(TypeError, match="all_lines must be a list"):
            iwfm.skip_ahead(0, ("line1", "line2"), skip=0)

    def test_none_raises_error(self):
        """Test that None raises TypeError."""
        with pytest.raises(TypeError, match="all_lines must be a list"):
            iwfm.skip_ahead(0, None, skip=0)


class TestSkipAheadEdgeCases:
    """Edge case tests."""

    def test_empty_string_line(self):
        """Test handling of empty string lines."""
        lines = ["", "data line"]

        # Empty string is treated as non-comment
        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 0

    def test_whitespace_only_line(self):
        """Test handling of whitespace-only lines."""
        lines = ["   ", "data line"]

        # Whitespace line doesn't start with comment char
        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 0

    def test_line_with_leading_space_then_c(self):
        """Test that line with leading space then C is not a comment."""
        lines = [" C Not a comment", "data line"]

        # Leading space means first char is space, not C
        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 0

    def test_single_character_comment(self):
        """Test single character comment lines."""
        lines = ["C", "data line"]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 1

    def test_single_data_line(self):
        """Test list with single data line."""
        lines = ["only line"]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 0

    def test_skip_exact_count(self):
        """Test skipping exact number of lines available."""
        lines = ["line1", "line2", "line3"]

        result = iwfm.skip_ahead(0, lines, skip=3)

        assert result == -1

    def test_data_line_starting_with_lowercase_letter(self):
        """Test that data lines starting with other letters are not skipped."""
        lines = ["data line", "another line"]

        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 0

    def test_line_index_at_valid_position(self):
        """Test line_index at a valid middle position."""
        lines = ["line1", "line2", "line3", "line4"]

        result = iwfm.skip_ahead(1, lines, skip=1)

        assert result == 2


class TestSkipAheadIWFMFileFormat:
    """Tests simulating real IWFM file formats."""

    def test_iwfm_header_format(self):
        """Test typical IWFM file header format."""
        lines = [
            "C *******************************************",
            "C *         IWFM INPUT FILE                 *",
            "C *******************************************",
            "C Version: 2021",
            " file1.dat                    / Input file 1",
            " file2.dat                    / Input file 2",
        ]

        # Skip all comments, land on first data line
        result = iwfm.skip_ahead(0, lines, skip=0)

        assert result == 4

    def test_iwfm_skip_14_lines(self):
        """Test skipping 14 non-comment lines (common in IWFM simulation files)."""
        lines = []
        # Add some header comments
        lines.append("C This is a simulation file")
        lines.append("C Created for testing")

        # Add 14 data lines
        for i in range(14):
            lines.append(f" file_{i+1}.dat                    / {i+1}")

        # Add more comments
        lines.append("C Simulation dates section")

        # Add date line
        lines.append("      09/30/1973_24:00          / BDT")

        # Skip 14 non-comment lines
        result = iwfm.skip_ahead(0, lines, skip=14)

        # Should be at index 17 (2 comments + 14 data + 1 comment = 17)
        assert result == 17

    def test_iwfm_mixed_comment_styles(self):
        """Test IWFM file with mixed comment styles."""
        lines = [
            "C Comment style 1",
            "c Comment style 2",
            "* Comment style 3",
            "# Comment style 4",
            " data_value_1",
            "C Inline comment",
            " data_value_2",
        ]

        # Skip 0 data lines, land on first data
        result = iwfm.skip_ahead(0, lines, skip=0)
        assert result == 4

        # Skip 1 data line from start
        result = iwfm.skip_ahead(0, lines, skip=1)
        assert result == 6

    def test_iwfm_preprocessor_section(self):
        """Test typical IWFM preprocessor file section."""
        lines = [
            "C Node Coordinates",
            "C ID        X           Y",
            "    1     100.0       200.0",
            "    2     150.0       250.0",
            "    3     200.0       300.0",
        ]

        # Skip comments, land on first node
        result = iwfm.skip_ahead(0, lines, skip=0)
        assert result == 2

        # Skip 2 nodes
        result = iwfm.skip_ahead(0, lines, skip=2)
        assert result == 4


class TestSkipAheadSequentialCalls:
    """Tests for sequential calls to skip_ahead."""

    def test_sequential_navigation(self):
        """Test navigating through file with sequential calls."""
        lines = [
            "C Header",
            " data1",
            "C Comment",
            " data2",
            " data3",
        ]

        # First call: skip to first data
        idx = iwfm.skip_ahead(0, lines, skip=0)
        assert idx == 1

        # Second call: skip one data line
        idx = iwfm.skip_ahead(idx, lines, skip=1)
        assert idx == 3

        # Third call: skip one more
        idx = iwfm.skip_ahead(idx, lines, skip=1)
        assert idx == 4

        # Fourth call: try to skip past end
        idx = iwfm.skip_ahead(idx, lines, skip=1)
        assert idx == -1

    def test_read_all_data_lines(self):
        """Test reading all data lines sequentially."""
        lines = [
            "C Comment",
            " line1",
            " line2",
            " line3",
        ]

        data_indices = []
        idx = iwfm.skip_ahead(0, lines, skip=0)

        while idx != -1:
            data_indices.append(idx)
            idx = iwfm.skip_ahead(idx, lines, skip=1)

        assert data_indices == [1, 2, 3]
