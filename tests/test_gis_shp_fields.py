# test_gis_shp_fields.py
# Tests for gis/shp_fields.py - Return field property strings for shapefile
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
from unittest.mock import Mock


class TestShpFields:
    """Tests for shp_fields function."""

    def test_returns_fields(self):
        """Test that function returns fields attribute."""
        from iwfm.gis.shp_fields import shp_fields
        
        mock_shp = Mock()
        mock_shp.fields = [
            ['DeletionFlag', 'C', 1, 0],
            ['ID', 'N', 10, 0],
            ['Name', 'C', 50, 0],
        ]
        
        result = shp_fields(mock_shp)
        
        assert result == mock_shp.fields

    def test_returns_list(self):
        """Test that function returns a list."""
        from iwfm.gis.shp_fields import shp_fields
        
        mock_shp = Mock()
        mock_shp.fields = [['ID', 'N', 10, 0]]
        
        result = shp_fields(mock_shp)
        
        assert isinstance(result, list)

    def test_empty_fields(self):
        """Test with empty fields list."""
        from iwfm.gis.shp_fields import shp_fields
        
        mock_shp = Mock()
        mock_shp.fields = []
        
        result = shp_fields(mock_shp)
        
        assert result == []

    def test_field_structure(self):
        """Test that fields have expected structure."""
        from iwfm.gis.shp_fields import shp_fields
        
        mock_shp = Mock()
        mock_shp.fields = [
            ['DeletionFlag', 'C', 1, 0],
            ['OBJECTID', 'N', 10, 0],
            ['AREA', 'F', 19, 11],
        ]
        
        result = shp_fields(mock_shp)
        
        # Each field should have name, type, size, decimal
        for field in result:
            assert len(field) == 4


class TestShpFieldsImports:
    """Tests for shp_fields imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_fields
        assert callable(shp_fields)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_fields import shp_fields
        assert callable(shp_fields)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_fields import shp_fields
        
        assert shp_fields.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
