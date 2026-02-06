# test_gis_shp_geomtype.py
# Tests for gis/shp_geomtype.py - Return shape geometry for shapefile
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


class TestShpGeomtype:
    """Tests for shp_geomtype function."""

    def test_returns_shape(self):
        """Test that function returns shape(0)."""
        from iwfm.gis.shp_geomtype import shp_geomtype
        
        mock_shape = Mock()
        mock_shp = Mock()
        mock_shp.shape.return_value = mock_shape
        
        result = shp_geomtype(mock_shp)
        
        mock_shp.shape.assert_called_once_with(0)
        assert result == mock_shape

    def test_calls_shape_with_zero(self):
        """Test that function calls shape with index 0."""
        from iwfm.gis.shp_geomtype import shp_geomtype
        
        mock_shp = Mock()
        
        shp_geomtype(mock_shp)
        
        mock_shp.shape.assert_called_with(0)


class TestShpGeomtypeImports:
    """Tests for shp_geomtype imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_geomtype
        assert callable(shp_geomtype)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_geomtype import shp_geomtype
        assert callable(shp_geomtype)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_geomtype import shp_geomtype
        
        assert shp_geomtype.__doc__ is not None
        assert 'geometry' in shp_geomtype.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
