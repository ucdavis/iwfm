# test_find_line_num.py
# Unit tests for the find_line_num function in the iwfm package
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

import iwfm


class TestFindLineNumFunctionExists:
    """Test that the find_line_num function exists and is callable."""

    def test_find_line_num_exists(self):
        """Test that find_line_num function exists in the iwfm module."""
        assert hasattr(iwfm, 'find_line_num')
        assert callable(getattr(iwfm, 'find_line_num'))


class TestFindLineNumBasicFunctionality:
    """Test basic functionality of find_line_num."""

    def test_find_string_first_line(self):
        """Test finding a string on the first line."""
        content = "This is the target line\nSecond line\nThird line\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "target")

            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_find_string_middle_line(self):
        """Test finding a string on a middle line."""
        content = "First line\nThis is the target line\nThird line\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "target")

            assert result == 2
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_find_string_last_line(self):
        """Test finding a string on the last line."""
        content = "First line\nSecond line\nThis is the target line\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "target")

            assert result == 3
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_find_exact_word(self):
        """Test finding an exact word in a line."""
        content = "apple banana cherry\norange grape\nlemon lime\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "grape")

            assert result == 2
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFindLineNumReturnType:
    """Test the return type of find_line_num."""

    def test_returns_int_when_found(self):
        """Test that find_line_num returns an integer when string is found."""
        content = "test line\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "test")

            assert isinstance(result, int)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_returns_none_when_not_found(self):
        """Test that find_line_num returns None when string is not found."""
        content = "First line\nSecond line\nThird line\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "nonexistent")

            assert result is None
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFindLineNumLineNumbering:
    """Test line numbering behavior in find_line_num."""

    def test_line_numbers_start_at_one(self):
        """Test that line numbers start at 1, not 0."""
        content = "first\nsecond\nthird\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "first")

            # Line numbers should be 1-indexed
            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_sequential_line_numbers(self):
        """Test that line numbers are sequential."""
        content = "line_one\nline_two\nline_three\nline_four\nline_five\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            assert iwfm.find_line_num(temp_file, "line_one") == 1
            assert iwfm.find_line_num(temp_file, "line_two") == 2
            assert iwfm.find_line_num(temp_file, "line_three") == 3
            assert iwfm.find_line_num(temp_file, "line_four") == 4
            assert iwfm.find_line_num(temp_file, "line_five") == 5
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFindLineNumFirstOccurrence:
    """Test that find_line_num returns first occurrence only."""

    def test_returns_first_occurrence(self):
        """Test that function returns line number of first occurrence."""
        content = "pattern here\nno match\npattern again\npattern third\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "pattern")

            # Should return first occurrence (line 1), not later ones
            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_multiple_occurrences_same_line(self):
        """Test finding string that occurs multiple times on same line."""
        content = "test test test\nother line\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "test")

            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFindLineNumSubstringMatching:
    """Test substring matching behavior in find_line_num."""

    def test_finds_substring(self):
        """Test that function finds substrings within words."""
        content = "This contains testing word\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "test")

            # Should find "test" within "testing"
            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_partial_match(self):
        """Test partial match behavior."""
        content = "prefix_match_suffix\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "match")

            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFindLineNumCaseSensitivity:
    """Test case sensitivity in find_line_num."""

    def test_case_sensitive_match(self):
        """Test that matching is case-sensitive."""
        content = "THIS IS UPPERCASE\nthis is lowercase\nThis Is Mixed\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            # Should only match exact case
            assert iwfm.find_line_num(temp_file, "UPPERCASE") == 1
            assert iwfm.find_line_num(temp_file, "lowercase") == 2
            assert iwfm.find_line_num(temp_file, "Mixed") == 3
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_case_sensitive_not_found(self):
        """Test that wrong case does not match."""
        content = "TEST\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            # Lowercase "test" should not match uppercase "TEST"
            result = iwfm.find_line_num(temp_file, "test")

            assert result is None
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFindLineNumSpecialCharacters:
    """Test find_line_num with special characters."""

    def test_find_with_spaces(self):
        """Test finding string with spaces."""
        content = "line one\nline two with spaces\nline three\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "two with spaces")

            assert result == 2
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_find_with_numbers(self):
        """Test finding string with numbers."""
        content = "ID: 12345\nName: Test\nValue: 99.99\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "12345")

            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_find_with_punctuation(self):
        """Test finding string with punctuation."""
        content = "Hello, world!\nGoodbye.\nQuestion?\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "world!")

            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_find_with_special_chars(self):
        """Test finding string with special characters."""
        content = "Path: /usr/local/bin\nEmail: test@example.com\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "@example.com")

            assert result == 2
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFindLineNumEdgeCases:
    """Test edge cases for find_line_num."""

    def test_empty_file(self):
        """Test with an empty file."""
        content = ""

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "anything")

            assert result is None
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_single_line_file(self):
        """Test with a single-line file."""
        content = "Only one line here"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "one line")

            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_empty_search_string(self):
        """Test with empty search string (matches any line)."""
        content = "First line\nSecond line\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "")

            # Empty string is in every non-empty line
            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_blank_lines(self):
        """Test file with blank lines."""
        content = "\n\nTarget line\n\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "Target")

            assert result == 3
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_very_long_line(self):
        """Test with a very long line."""
        long_text = "x" * 10000 + "TARGET" + "y" * 10000
        content = f"Short line\n{long_text}\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "TARGET")

            assert result == 2
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFindLineNumErrorHandling:
    """Test error handling in find_line_num."""

    def test_nonexistent_file(self):
        """Test that nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            iwfm.find_line_num('nonexistent_file.txt', "test")


class TestFindLineNumRealWorldScenarios:
    """Test find_line_num with realistic IWFM-related scenarios."""

    def test_find_iwfm_section_header(self):
        """Test finding IWFM file section headers."""
        content = """C IWFM Preprocessor Main File
C
C Preprocessor Data
C
NODE DATA
    1    100.0    200.0
    2    150.0    250.0
C
ELEMENT DATA
    1    1    2    3    4
"""
        fd, temp_file = tempfile.mkstemp(suffix='.dat', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            # Find section headers
            assert iwfm.find_line_num(temp_file, "NODE DATA") == 5
            assert iwfm.find_line_num(temp_file, "ELEMENT DATA") == 9
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_find_comment_marker(self):
        """Test finding lines with comment markers."""
        content = """C This is a comment
C Another comment
    DATA LINE 1
C More comments
    DATA LINE 2
"""
        fd, temp_file = tempfile.mkstemp(suffix='.dat', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            # Find first occurrence of "C " (comment marker)
            result = iwfm.find_line_num(temp_file, "C ")

            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_find_date_in_file(self):
        """Test finding a date string in a file."""
        content = """Header info
09/30/1973_24:00    Start date
09/30/2015_24:00    End date
Data follows
"""
        fd, temp_file = tempfile.mkstemp(suffix='.dat', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "09/30/1973")

            assert result == 2
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_find_budget_type(self):
        """Test finding budget type in budget file."""
        content = """GROUNDWATER BUDGET IN AC.FT. FOR SUBREGION 1
Time           Inflow        Outflow       Storage
01/31/1974     1000.0        800.0         200.0
"""
        fd, temp_file = tempfile.mkstemp(suffix='.bud', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = iwfm.find_line_num(temp_file, "GROUNDWATER BUDGET")

            assert result == 1
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
