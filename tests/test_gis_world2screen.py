# test_gis_world2screen.py
# Tests for gis/world2screen.py - Convert geospatial coordinates to screen pixels
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


class TestWorld2Screen:
    """Tests for world2screen function."""

    def test_returns_tuple(self):
        """Test that function returns a tuple of 2 values (px, py)."""
        from iwfm.gis.world2screen import world2screen

        bbox = [0, 0, 100, 100]  # minx, miny, maxx, maxy
        w, h = 800, 600  # screen dimensions
        x, y = 50, 50  # world coordinates

        result = world2screen(bbox, w, h, x, y)

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_integers(self):
        """Test that function returns integer pixel values."""
        from iwfm.gis.world2screen import world2screen

        bbox = [0, 0, 100, 100]
        w, h = 800, 600
        x, y = 50, 50

        px, py = world2screen(bbox, w, h, x, y)

        assert isinstance(px, int)
        assert isinstance(py, int)

    def test_center_of_bbox(self):
        """Test that center of bbox maps to center of screen."""
        from iwfm.gis.world2screen import world2screen

        bbox = [0, 0, 100, 100]
        w, h = 800, 600
        x, y = 50, 50  # Center of bbox

        px, py = world2screen(bbox, w, h, x, y)

        # Center should be at half of screen dimensions
        assert px == 400  # w/2
        assert py == 300  # h/2

    def test_origin_of_bbox(self):
        """Test that origin (minx, miny) maps correctly."""
        from iwfm.gis.world2screen import world2screen

        bbox = [0, 0, 100, 100]
        w, h = 800, 600
        x, y = 0, 0  # Bottom-left corner of bbox

        px, py = world2screen(bbox, w, h, x, y)

        # Bottom-left in world should be top-left in screen? No, origin check
        assert px == 0
        assert py == 600  # y is flipped (world y=0 is at screen bottom)

    def test_max_corner_of_bbox(self):
        """Test that max corner (maxx, maxy) maps correctly."""
        from iwfm.gis.world2screen import world2screen

        bbox = [0, 0, 100, 100]
        w, h = 800, 600
        x, y = 100, 100  # Top-right corner of bbox

        px, py = world2screen(bbox, w, h, x, y)

        assert px == 800  # Full width
        assert py == 0  # Top of screen

    def test_point_outside_bbox(self):
        """Test behavior with point outside bbox."""
        from iwfm.gis.world2screen import world2screen

        bbox = [0, 0, 100, 100]
        w, h = 800, 600
        x, y = 150, 150  # Outside bbox

        px, py = world2screen(bbox, w, h, x, y)

        # Should return values outside screen bounds
        assert px > 800
        assert py < 0

    def test_rectangular_bbox(self):
        """Test with non-square bounding box."""
        from iwfm.gis.world2screen import world2screen

        bbox = [0, 0, 200, 100]  # Wider than tall
        w, h = 800, 400  # Matching aspect ratio
        x, y = 100, 50  # Center

        px, py = world2screen(bbox, w, h, x, y)

        assert px == 400  # Half of width
        assert py == 200  # Half of height

    def test_negative_bbox(self):
        """Test with negative coordinates in bbox."""
        from iwfm.gis.world2screen import world2screen

        bbox = [-100, -100, 100, 100]
        w, h = 800, 800
        x, y = 0, 0  # Origin (center of bbox)

        px, py = world2screen(bbox, w, h, x, y)

        assert px == 400
        assert py == 400


class TestWorld2ScreenImports:
    """Tests for world2screen imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import world2screen
        assert callable(world2screen)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.world2screen import world2screen
        assert callable(world2screen)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.world2screen import world2screen

        assert world2screen.__doc__ is not None
        assert 'screen' in world2screen.__doc__.lower() or 'pixel' in world2screen.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
