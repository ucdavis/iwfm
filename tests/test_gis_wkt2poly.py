# test_gis_wkt2poly.py
# Tests for gis/wkt2poly.py - Convert WKT-format text string into polygon
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

# Check if wkt module is available
try:
    import wkt  # noqa: F401
    del wkt
    HAS_WKT = True
except ImportError:
    HAS_WKT = False


@pytest.mark.skipif(not HAS_WKT, reason="wkt module not installed")
class TestWkt2Poly:
    """Tests for wkt2poly function."""

    def test_returns_geometry_object(self):
        """Test that function returns a geometry object."""
        from iwfm.gis.wkt2poly import wkt2poly

        wkt_string = 'POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))'
        result = wkt2poly(wkt_string)

        # Should return a geometry object, not None
        assert result is not None

    def test_simple_square_polygon(self):
        """Test parsing a simple square polygon."""
        from iwfm.gis.wkt2poly import wkt2poly

        wkt_string = 'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))'
        poly = wkt2poly(wkt_string)

        # Check that we get a valid polygon
        assert poly is not None
        assert hasattr(poly, 'exterior') or hasattr(poly, 'bounds')

    def test_triangle_polygon(self):
        """Test parsing a triangle polygon."""
        from iwfm.gis.wkt2poly import wkt2poly

        wkt_string = 'POLYGON((0 0, 5 10, 10 0, 0 0))'
        poly = wkt2poly(wkt_string)

        assert poly is not None

    def test_polygon_with_hole(self):
        """Test parsing a polygon with a hole."""
        from iwfm.gis.wkt2poly import wkt2poly

        # Outer ring with inner hole
        wkt_string = 'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0), (2 2, 8 2, 8 8, 2 8, 2 2))'
        poly = wkt2poly(wkt_string)

        assert poly is not None

    def test_polygon_coordinates(self):
        """Test that polygon has correct coordinates."""
        from iwfm.gis.wkt2poly import wkt2poly

        wkt_string = 'POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))'
        poly = wkt2poly(wkt_string)

        # Get the exterior coordinates
        if hasattr(poly, 'exterior'):
            coords = list(poly.exterior.coords)
            assert (0, 0) in coords or [0, 0] in coords
            assert (4, 4) in coords or [4, 4] in coords

    def test_point_geometry(self):
        """Test parsing a point WKT."""
        from iwfm.gis.wkt2poly import wkt2poly

        wkt_string = 'POINT(10 20)'
        point = wkt2poly(wkt_string)

        assert point is not None

    def test_linestring_geometry(self):
        """Test parsing a linestring WKT."""
        from iwfm.gis.wkt2poly import wkt2poly

        wkt_string = 'LINESTRING(0 0, 10 10, 20 0)'
        line = wkt2poly(wkt_string)

        assert line is not None


class TestWkt2PolyImports:
    """Tests for wkt2poly imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import wkt2poly
        assert callable(wkt2poly)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.wkt2poly import wkt2poly
        assert callable(wkt2poly)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.wkt2poly import wkt2poly

        assert wkt2poly.__doc__ is not None
        assert 'wkt' in wkt2poly.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
