# test_debug_test_dict.py
# Tests for debug/test_dict.py - Print dictionary value for key
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


class TestTestDict:
    """Tests for test_dict function."""

    def test_prints_dictionary_name(self, capsys):
        """Test that function prints dictionary name."""
        from iwfm.debug.test_dict import test_dict
        
        d = {"a": 1}
        test_dict("my_dict", d, "a")
        
        captured = capsys.readouterr()
        assert "my_dict" in captured.out

    def test_prints_key(self, capsys):
        """Test that function prints the key."""
        from iwfm.debug.test_dict import test_dict
        
        d = {"test_key": "test_value"}
        test_dict("d", d, "test_key")
        
        captured = capsys.readouterr()
        assert "test_key" in captured.out

    def test_prints_value(self, capsys):
        """Test that function prints the value."""
        from iwfm.debug.test_dict import test_dict
        
        d = {"key": "expected_value"}
        test_dict("d", d, "key")
        
        captured = capsys.readouterr()
        assert "expected_value" in captured.out

    def test_missing_key_prints_none(self, capsys):
        """Test that missing key prints None."""
        from iwfm.debug.test_dict import test_dict
        
        d = {"a": 1}
        test_dict("d", d, "missing")
        
        captured = capsys.readouterr()
        assert "None" in captured.out

    def test_integer_key(self, capsys):
        """Test with integer key."""
        from iwfm.debug.test_dict import test_dict
        
        d = {1: "one", 2: "two"}
        test_dict("numbers", d, 1)
        
        captured = capsys.readouterr()
        assert "1" in captured.out
        assert "one" in captured.out

    def test_prints_dictionary_label(self, capsys):
        """Test that output includes 'dictionary' label."""
        from iwfm.debug.test_dict import test_dict
        
        d = {"a": 1}
        test_dict("test", d, "a")
        
        captured = capsys.readouterr()
        assert "dictionary" in captured.out

    def test_returns_none(self):
        """Test that function returns None."""
        from iwfm.debug.test_dict import test_dict
        
        d = {"a": 1}
        result = test_dict("d", d, "a")
        
        assert result is None

    def test_complex_value(self, capsys):
        """Test with complex value (list)."""
        from iwfm.debug.test_dict import test_dict
        
        d = {"key": [1, 2, 3]}
        test_dict("d", d, "key")
        
        captured = capsys.readouterr()
        assert "[1, 2, 3]" in captured.out

    def test_nested_dictionary(self, capsys):
        """Test with nested dictionary value."""
        from iwfm.debug.test_dict import test_dict
        
        d = {"outer": {"inner": "value"}}
        test_dict("d", d, "outer")
        
        captured = capsys.readouterr()
        assert "inner" in captured.out


class TestTestDictImports:
    """Tests for test_dict imports."""

    def test_import_from_debug(self):
        """Test import from iwfm.debug."""
        from iwfm.debug import test_dict
        assert callable(test_dict)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.debug.test_dict import test_dict
        assert callable(test_dict)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.debug.test_dict import test_dict
        
        assert test_dict.__doc__ is not None
        assert 'dictionary' in test_dict.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
