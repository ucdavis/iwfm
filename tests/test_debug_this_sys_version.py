# test_debug_this_sys_version.py
# Tests for debug/this_sys_version.py - Return OS version
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


class TestThisSysVersion:
    """Tests for this_sys_version function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        from iwfm.debug.this_sys_version import this_sys_version
        
        result = this_sys_version()
        
        assert isinstance(result, str)

    def test_not_empty(self):
        """Test that result is not empty."""
        from iwfm.debug.this_sys_version import this_sys_version
        
        result = this_sys_version()
        
        assert len(result) >= 1

    def test_matches_platform_release(self):
        """Test that result matches platform.release()."""
        from iwfm.debug.this_sys_version import this_sys_version
        
        result = this_sys_version()
        expected = platform.release()
        
        assert result == expected

    def test_result_is_consistent(self):
        """Test that multiple calls return same result."""
        from iwfm.debug.this_sys_version import this_sys_version
        
        result1 = this_sys_version()
        result2 = this_sys_version()
        
        assert result1 == result2


class TestThisSysVersionImports:
    """Tests for this_sys_version imports."""

    def test_import_from_debug(self):
        """Test import from iwfm.debug."""
        from iwfm.debug import this_sys_version
        assert callable(this_sys_version)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.debug.this_sys_version import this_sys_version
        assert callable(this_sys_version)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.debug.this_sys_version import this_sys_version
        
        assert this_sys_version.__doc__ is not None
        assert 'version' in this_sys_version.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
