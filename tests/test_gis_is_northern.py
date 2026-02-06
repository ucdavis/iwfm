# test_gis_is_northern.py
# Tests for gis/is_northern.py - Check if latitude is northern hemisphere
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


class TestIsNorthern:
    """Tests for is_northern function."""

    def test_returns_boolean(self):
        """Test that function returns a boolean."""
        from iwfm.gis.is_northern import is_northern
        
        result = is_northern(34.0)
        
        assert isinstance(result, bool)

    def test_positive_latitude_is_northern(self):
        """Test that positive latitude is northern."""
        from iwfm.gis.is_northern import is_northern
        
        assert is_northern(34.0) is True
        assert is_northern(45.5) is True
        assert is_northern(89.9) is True

    def test_negative_latitude_is_southern(self):
        """Test that negative latitude is southern."""
        from iwfm.gis.is_northern import is_northern
        
        assert is_northern(-34.0) is False
        assert is_northern(-45.5) is False
        assert is_northern(-89.9) is False

    def test_zero_latitude_is_northern(self):
        """Test that zero latitude (equator) is considered northern."""
        from iwfm.gis.is_northern import is_northern
        
        assert is_northern(0.0) is True

    def test_small_positive(self):
        """Test with small positive latitude."""
        from iwfm.gis.is_northern import is_northern
        
        assert is_northern(0.001) is True

    def test_small_negative(self):
        """Test with small negative latitude."""
        from iwfm.gis.is_northern import is_northern
        
        assert is_northern(-0.001) is False

    def test_north_pole(self):
        """Test with North Pole latitude."""
        from iwfm.gis.is_northern import is_northern
        
        assert is_northern(90.0) is True

    def test_south_pole(self):
        """Test with South Pole latitude."""
        from iwfm.gis.is_northern import is_northern
        
        assert is_northern(-90.0) is False

    def test_integer_input(self):
        """Test with integer input."""
        from iwfm.gis.is_northern import is_northern
        
        assert is_northern(45) is True
        assert is_northern(-45) is False


class TestIsNorthernImports:
    """Tests for is_northern imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import is_northern
        assert callable(is_northern)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.is_northern import is_northern
        assert callable(is_northern)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.is_northern import is_northern
        
        assert is_northern.__doc__ is not None
        assert 'northern' in is_northern.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
