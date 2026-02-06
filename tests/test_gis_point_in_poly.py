# test_gis_point_in_poly.py
# Tests for gis/point_in_poly.py - Check if point is inside polygon
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


class TestPointInPoly:
    """Tests for point_in_poly function."""

    def test_returns_boolean(self):
        """Test that function returns a boolean."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        # Simple square polygon
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        
        result = point_in_poly(5, 5, poly)
        
        assert isinstance(result, bool)

    def test_point_inside_square(self):
        """Test point inside a square polygon."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        
        assert point_in_poly(5, 5, poly) is True

    def test_point_outside_square(self):
        """Test point outside a square polygon."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        
        assert point_in_poly(15, 15, poly) is False
        assert point_in_poly(-5, 5, poly) is False

    def test_point_on_vertex(self):
        """Test point on polygon vertex."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        
        assert point_in_poly(0, 0, poly) is True
        assert point_in_poly(10, 10, poly) is True

    def test_point_on_edge(self):
        """Test point on polygon edge."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        
        # Point on bottom edge
        assert point_in_poly(5, 0, poly) is True

    def test_triangle_inside(self):
        """Test point inside a triangle."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        poly = [(0, 0), (10, 0), (5, 10)]
        
        assert point_in_poly(5, 3, poly) is True

    def test_triangle_outside(self):
        """Test point outside a triangle."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        poly = [(0, 0), (10, 0), (5, 10)]
        
        assert point_in_poly(0, 10, poly) is False

    def test_concave_polygon(self):
        """Test with concave (L-shaped) polygon."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        # L-shaped polygon
        poly = [(0, 0), (10, 0), (10, 5), (5, 5), (5, 10), (0, 10)]
        
        # Inside the L
        assert point_in_poly(2, 2, poly) is True
        assert point_in_poly(2, 8, poly) is True
        
        # In the cut-out area (outside)
        assert point_in_poly(8, 8, poly) is False

    def test_point_far_outside(self):
        """Test point far outside polygon."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        
        assert point_in_poly(1000, 1000, poly) is False
        assert point_in_poly(-1000, -1000, poly) is False

    def test_negative_coordinates(self):
        """Test with negative coordinates."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        poly = [(-10, -10), (10, -10), (10, 10), (-10, 10)]
        
        assert point_in_poly(0, 0, poly) is True
        assert point_in_poly(-5, -5, poly) is True
        assert point_in_poly(20, 20, poly) is False


class TestPointInPolyImports:
    """Tests for point_in_poly imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import point_in_poly
        assert callable(point_in_poly)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.point_in_poly import point_in_poly
        assert callable(point_in_poly)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.point_in_poly import point_in_poly
        
        assert point_in_poly.__doc__ is not None
        assert 'polygon' in point_in_poly.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
