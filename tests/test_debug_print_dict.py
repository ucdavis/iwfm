# test_debug_print_dict.py
# Tests for debug/print_dict.py - Print dictionary contents
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


class TestPrintDict:
    """Tests for print_dict function."""

    def test_prints_header(self, capsys):
        """Test that function prints header with 'key' and 'value'."""
        from iwfm.debug.print_dict import print_dict
        
        d = {"a": 1}
        print_dict(d)
        
        captured = capsys.readouterr()
        assert "key" in captured.out
        assert "value" in captured.out

    def test_prints_key_value_pairs(self, capsys):
        """Test that function prints key-value pairs."""
        from iwfm.debug.print_dict import print_dict
        
        d = {"name": "Alice", "age": 30}
        print_dict(d)
        
        captured = capsys.readouterr()
        assert "name" in captured.out
        assert "Alice" in captured.out
        assert "age" in captured.out
        assert "30" in captured.out

    def test_empty_dictionary(self, capsys):
        """Test with empty dictionary."""
        from iwfm.debug.print_dict import print_dict
        
        d = {}
        print_dict(d)
        
        captured = capsys.readouterr()
        # Should print header but no key-value pairs
        assert "key" in captured.out

    def test_integer_keys(self, capsys):
        """Test with integer keys."""
        from iwfm.debug.print_dict import print_dict
        
        d = {1: "one", 2: "two"}
        print_dict(d)
        
        captured = capsys.readouterr()
        assert "1" in captured.out
        assert "one" in captured.out

    def test_mixed_types(self, capsys):
        """Test with mixed key and value types."""
        from iwfm.debug.print_dict import print_dict
        
        d = {"string": 123, 456: "integer_key", "list": [1, 2, 3]}
        print_dict(d)
        
        captured = capsys.readouterr()
        assert "string" in captured.out
        assert "123" in captured.out
        assert "456" in captured.out

    def test_returns_none(self):
        """Test that function returns None."""
        from iwfm.debug.print_dict import print_dict
        
        d = {"a": 1}
        result = print_dict(d)
        
        assert result is None

    def test_large_dictionary(self, capsys):
        """Test with large dictionary."""
        from iwfm.debug.print_dict import print_dict
        
        d = {f"key_{i}": i * 10 for i in range(100)}
        print_dict(d)
        
        captured = capsys.readouterr()
        assert "key_0" in captured.out
        assert "key_99" in captured.out


class TestPrintDictImports:
    """Tests for print_dict imports."""

    def test_import_from_debug(self):
        """Test import from iwfm.debug."""
        from iwfm.debug import print_dict
        assert callable(print_dict)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.debug.print_dict import print_dict
        assert callable(print_dict)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.debug.print_dict import print_dict
        
        assert print_dict.__doc__ is not None
        assert 'dictionary' in print_dict.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
