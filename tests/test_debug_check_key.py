# test_debug_check_key.py
# Tests for debug/check_key.py - Check if key is in dictionary
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


class TestCheckKey:
    """Tests for check_key function."""

    def test_key_present_string(self):
        """Test with string key that is present."""
        from iwfm.debug.check_key import check_key
        
        d = {"a": 1, "b": 2}
        assert check_key(d, "a") is True

    def test_key_absent_string(self):
        """Test with string key that is absent."""
        from iwfm.debug.check_key import check_key
        
        d = {"a": 1, "b": 2}
        assert check_key(d, "c") is False

    def test_key_present_integer(self):
        """Test with integer key that is present."""
        from iwfm.debug.check_key import check_key
        
        d = {1: "a", 2: "b"}
        assert check_key(d, 1) is True

    def test_key_absent_integer(self):
        """Test with integer key that is absent."""
        from iwfm.debug.check_key import check_key
        
        d = {1: "a", 2: "b"}
        assert check_key(d, 3) is False

    def test_key_present_tuple(self):
        """Test with tuple key that is present."""
        from iwfm.debug.check_key import check_key
        
        d = {(1, 2): "a", (3, 4): "b"}
        assert check_key(d, (1, 2)) is True

    def test_key_absent_tuple(self):
        """Test with tuple key that is absent."""
        from iwfm.debug.check_key import check_key
        
        d = {(1, 2): "a", (3, 4): "b"}
        assert check_key(d, (5, 6)) is False

    def test_empty_dictionary(self):
        """Test with empty dictionary."""
        from iwfm.debug.check_key import check_key
        
        d = {}
        assert check_key(d, "any") is False

    def test_none_key(self):
        """Test with None as key."""
        from iwfm.debug.check_key import check_key
        
        d = {None: "value"}
        assert check_key(d, None) is True

    def test_mixed_key_types(self):
        """Test with mixed key types in dictionary."""
        from iwfm.debug.check_key import check_key
        
        d = {"a": 1, 2: "b", (1, 2): "c"}
        assert check_key(d, "a") is True
        assert check_key(d, 2) is True
        assert check_key(d, (1, 2)) is True
        assert check_key(d, "missing") is False

    def test_returns_boolean(self):
        """Test that function returns boolean type."""
        from iwfm.debug.check_key import check_key
        
        d = {"a": 1}
        result_true = check_key(d, "a")
        result_false = check_key(d, "b")
        
        assert isinstance(result_true, bool)
        assert isinstance(result_false, bool)


class TestCheckKeyImports:
    """Tests for check_key imports."""

    def test_import_from_debug(self):
        """Test import from iwfm.debug."""
        from iwfm.debug import check_key
        assert callable(check_key)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.debug.check_key import check_key
        assert callable(check_key)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.debug.check_key import check_key
        
        assert check_key.__doc__ is not None
        assert 'dictionary' in check_key.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
