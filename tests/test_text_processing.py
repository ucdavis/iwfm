# test_text_processing.py
# unit tests for text processing utility functions in the iwfm package
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

import pytest
import iwfm


class TestSkipAhead:
    """Test the skip_ahead function."""
    
    def test_skip_ahead_no_comments_no_skip(self):
        """Test skipping with no comments and no skip."""
        lines = ["line1", "line2", "line3"]
        result = iwfm.skip_ahead(0, lines, skip=0)
        assert result == 0  # should stay at same position
    
    def test_skip_ahead_with_skip(self):
        """Test skipping specified number of non-comment lines."""
        lines = ["line1", "line2", "line3", "line4"]
        result = iwfm.skip_ahead(0, lines, skip=2)
        assert result == 2  # should skip 2 lines
    
    def test_skip_ahead_with_comments(self):
        """Test skipping comment lines."""
        lines = ["line1", "C comment", "c comment", "* comment", "# comment", "line2"]
        result = iwfm.skip_ahead(1, lines, skip=0)
        assert result == 5  # should skip all comment lines and land on "line2"
    
    def test_skip_ahead_mixed_comments_and_skip(self):
        """Test skipping with both comment lines and skip parameter."""
        lines = ["line1", "line2", "C comment", "line3", "* comment", "line4"]
        result = iwfm.skip_ahead(0, lines, skip=2)
        # Should skip line1, line2 (skip=2), then skip "C comment", land on "line3"
        assert result == 3
    
    def test_skip_ahead_beyond_end(self):
        """Test skipping beyond end of list."""
        lines = ["line1", "line2"]
        result = iwfm.skip_ahead(0, lines, skip=5)
        assert result == -1  # should return -1 when end reached
    
    def test_skip_ahead_at_end(self):
        """Test starting at end of list."""
        lines = ["line1", "line2"]
        result = iwfm.skip_ahead(2, lines, skip=0)
        assert result == -1  # should return -1 when starting beyond end
    
    def test_skip_ahead_beyond_end_edge_cases(self):
        """Test additional edge cases for end-of-list handling."""
        lines = ["line1", "line2"]
        
        # Starting way beyond end
        result = iwfm.skip_ahead(10, lines, skip=0)
        assert result == -1
        
        # Starting at exact end with skip
        result = iwfm.skip_ahead(2, lines, skip=1)
        assert result == -1
        
        # Starting near end with comments at end
        lines_with_comments = ["line1", "C comment"]
        result = iwfm.skip_ahead(1, lines_with_comments, skip=0)
        assert result == -1  # should skip comment and reach end
    
    def test_skip_ahead_all_comments(self):
        """Test with all lines being comments."""
        lines = ["C comment1", "c comment2", "* comment3", "# comment4"]
        result = iwfm.skip_ahead(0, lines, skip=0)
        assert result == -1  # should return -1 as no non-comment lines found


class TestPadFront:
    """Test the pad_front function."""
    
    def test_pad_front_basic(self):
        """Test basic front padding with spaces."""
        result = iwfm.pad_front("test", 8)
        assert result == "    test"
        assert len(result) == 8
    
    def test_pad_front_no_padding_needed(self):
        """Test when string is already long enough."""
        result = iwfm.pad_front("test", 4)
        assert result == "test"
        
        result = iwfm.pad_front("test", 2)
        assert result == "test"  # should not truncate
    
    def test_pad_front_custom_character(self):
        """Test padding with custom character."""
        result = iwfm.pad_front("test", 8, "0")
        assert result == "0000test"
    
    def test_pad_front_number_input(self):
        """Test with numeric input."""
        result = iwfm.pad_front(123, 6)
        assert result == "   123"
        
        result = iwfm.pad_front(45.67, 7, "0")
        assert result == "0045.67"
    
    def test_pad_front_default_parameters(self):
        """Test with default parameters."""
        result = iwfm.pad_front("a")
        assert result == "a"  # n=1, so no padding needed


class TestPadBack:
    """Test the pad_back function."""
    
    def test_pad_back_basic(self):
        """Test basic back padding with spaces."""
        result = iwfm.pad_back("test", 8)
        assert result == "test    "
        assert len(result) == 8
    
    def test_pad_back_no_padding_needed(self):
        """Test when string is already long enough."""
        result = iwfm.pad_back("test", 4)
        assert result == "test"
        
        result = iwfm.pad_back("test", 2)
        assert result == "test"  # should not truncate
    
    def test_pad_back_custom_character(self):
        """Test padding with custom character."""
        result = iwfm.pad_back("test", 8, ".")
        assert result == "test...."
    
    def test_pad_back_number_input(self):
        """Test with numeric input."""
        result = iwfm.pad_back(123, 6)
        assert result == "123   "
        
        result = iwfm.pad_back(45.67, 8, "0")
        assert result == "45.67000"
    
    def test_pad_back_default_parameters(self):
        """Test with default parameters."""
        result = iwfm.pad_back("a")
        assert result == "a"  # n=1, so no padding needed


class TestPadBoth:
    """Test the pad_both function."""
    
    def test_pad_both_basic(self):
        """Test basic padding on both sides."""
        result = iwfm.pad_both("test", f=1, b=8)
        assert result == " test   "
        assert len(result) == 8
    
    def test_pad_both_multiple_front(self):
        """Test with multiple front padding characters."""
        result = iwfm.pad_both("test", f=3, b=10)
        assert result == "   test   "
        assert len(result) == 10
    
    def test_pad_both_custom_character(self):
        """Test with custom padding character."""
        result = iwfm.pad_both("test", f=2, b=10, t="*")
        assert result == "**test****"
        assert len(result) == 10
    
    def test_pad_both_no_back_padding_needed(self):
        """Test when front padding makes string long enough."""
        result = iwfm.pad_both("test", f=2, b=6)
        assert result == "  test"
        assert len(result) == 6
    
    def test_pad_both_number_input(self):
        """Test with numeric input."""
        result = iwfm.pad_both(123, f=1, b=7, t="0")
        assert result == "0123000"
    
    def test_pad_both_default_parameters(self):
        """Test with default parameters."""
        result = iwfm.pad_both("a")
        assert result == " a"  # f=1, b=1, but f takes precedence


class TestPrintToString:
    """Test the print_to_string function."""
    
    def test_print_to_string_single_argument(self):
        """Test with single argument."""
        result = iwfm.print_to_string("hello")
        assert result == "hello\n"
    
    def test_print_to_string_multiple_arguments(self):
        """Test with multiple arguments."""
        result = iwfm.print_to_string("hello", "world", 123)
        assert result == "hello world 123\n"
    
    def test_print_to_string_separator(self):
        """Test with custom separator."""
        result = iwfm.print_to_string("a", "b", "c", sep="-")
        assert result == "a-b-c\n"
    
    def test_print_to_string_end_parameter(self):
        """Test with custom end parameter."""
        result = iwfm.print_to_string("hello", end="")
        assert result == "hello"
        
        result = iwfm.print_to_string("hello", end="!\n")
        assert result == "hello!\n"
    
    def test_print_to_string_mixed_types(self):
        """Test with mixed data types."""
        result = iwfm.print_to_string(1, 2.5, "text", [1, 2])
        assert result == "1 2.5 text [1, 2]\n"
    
    def test_print_to_string_empty_call(self):
        """Test with no arguments."""
        result = iwfm.print_to_string()
        assert result == "\n"