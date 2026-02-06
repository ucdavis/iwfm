# test_gis_shp_bounds.py
# Tests for gis/shp_bounds.py - Return bounding box for shapefile
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


class TestShpBounds:
    """Tests for shp_bounds function."""

    def test_returns_bbox(self):
        """Test that function returns bbox attribute."""
        from iwfm.gis.shp_bounds import shp_bounds
        
        mock_shp = Mock()
        mock_shp.bbox = [-122.5, 37.0, -121.5, 38.0]
        
        result = shp_bounds(mock_shp)
        
        assert result == mock_shp.bbox

    def test_bbox_has_four_elements(self):
        """Test that bbox has four elements (minx, miny, maxx, maxy)."""
        from iwfm.gis.shp_bounds import shp_bounds
        
        mock_shp = Mock()
        mock_shp.bbox = [-122.5, 37.0, -121.5, 38.0]
        
        result = shp_bounds(mock_shp)
        
        assert len(result) == 4

    def test_utm_coordinates(self):
        """Test with UTM-style coordinates."""
        from iwfm.gis.shp_bounds import shp_bounds
        
        mock_shp = Mock()
        mock_shp.bbox = [500000.0, 4000000.0, 600000.0, 4100000.0]
        
        result = shp_bounds(mock_shp)
        
        assert result[0] == 500000.0  # minx
        assert result[1] == 4000000.0  # miny
        assert result[2] == 600000.0  # maxx
        assert result[3] == 4100000.0  # maxy

    def test_negative_coordinates(self):
        """Test with negative coordinates."""
        from iwfm.gis.shp_bounds import shp_bounds
        
        mock_shp = Mock()
        mock_shp.bbox = [-180.0, -90.0, 180.0, 90.0]
        
        result = shp_bounds(mock_shp)
        
        assert result == [-180.0, -90.0, 180.0, 90.0]


class TestShpBoundsImports:
    """Tests for shp_bounds imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_bounds
        assert callable(shp_bounds)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_bounds import shp_bounds
        assert callable(shp_bounds)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_bounds import shp_bounds
        
        assert shp_bounds.__doc__ is not None
        assert 'bound' in shp_bounds.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
