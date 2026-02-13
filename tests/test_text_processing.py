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


