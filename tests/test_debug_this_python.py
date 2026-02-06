# test_debug_this_python.py
# Tests for debug/this_python.py - Return Python version
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
import sys


class TestThisPython:
    """Tests for this_python function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        from iwfm.debug.this_python import this_python
        
        result = this_python()
        
        assert isinstance(result, str)

    def test_contains_dot(self):
        """Test that version string contains a dot (e.g., 3.9)."""
        from iwfm.debug.this_python import this_python
        
        result = this_python()
        
        assert "." in result

    def test_version_format(self):
        """Test that version has expected format (major.minor.patch)."""
        from iwfm.debug.this_python import this_python
        
        result = this_python()
        parts = result.split(".")
        
        assert len(parts) >= 2  # At least major.minor
        assert parts[0].isdigit()  # Major version is numeric
        assert parts[1].isdigit()  # Minor version is numeric

    def test_matches_sys_version(self):
        """Test that result matches sys.version_info."""
        from iwfm.debug.this_python import this_python
        
        result = this_python()
        
        # Should start with major.minor
        expected_start = f"{sys.version_info.major}.{sys.version_info.minor}"
        assert result.startswith(expected_start)

    def test_major_version_reasonable(self):
        """Test that major version is reasonable (2 or 3)."""
        from iwfm.debug.this_python import this_python
        
        result = this_python()
        major = int(result.split(".")[0])
        
        assert major in [2, 3]  # Python 2.x or 3.x


class TestThisPythonImports:
    """Tests for this_python imports."""

    def test_import_from_debug(self):
        """Test import from iwfm.debug."""
        from iwfm.debug import this_python
        assert callable(this_python)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.debug.this_python import this_python
        assert callable(this_python)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.debug.this_python import this_python
        
        assert this_python.__doc__ is not None
        assert 'python' in this_python.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
