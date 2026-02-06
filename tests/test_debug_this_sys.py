# test_debug_this_sys.py
# Tests for debug/this_sys.py - Return OS name
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
import platform


class TestThisSys:
    """Tests for this_sys function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        from iwfm.debug.this_sys import this_sys
        
        result = this_sys()
        
        assert isinstance(result, str)

    def test_returns_valid_os_name(self):
        """Test that function returns a valid OS name."""
        from iwfm.debug.this_sys import this_sys
        
        result = this_sys()
        
        assert result in ["Linux", "Darwin", "Windows"]

    def test_matches_platform_system(self):
        """Test that result matches platform.system()."""
        from iwfm.debug.this_sys import this_sys
        
        result = this_sys()
        expected = platform.system()
        
        assert result == expected

    def test_not_empty(self):
        """Test that result is not empty."""
        from iwfm.debug.this_sys import this_sys
        
        result = this_sys()
        
        assert len(result) > 0

    def test_result_is_title_case(self):
        """Test that result is in title case (e.g., 'Linux' not 'linux')."""
        from iwfm.debug.this_sys import this_sys
        
        result = this_sys()
        
        # First letter should be uppercase
        assert result[0].isupper()


class TestThisSysImports:
    """Tests for this_sys imports."""

    def test_import_from_debug(self):
        """Test import from iwfm.debug."""
        from iwfm.debug import this_sys
        assert callable(this_sys)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.debug.this_sys import this_sys
        assert callable(this_sys)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.debug.this_sys import this_sys
        
        assert this_sys.__doc__ is not None
        # Check for OS names in docstring
        assert 'Linux' in this_sys.__doc__ or 'Darwin' in this_sys.__doc__ or 'Windows' in this_sys.__doc__


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
