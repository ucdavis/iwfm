# test_gis_world2pixel.py
# Tests for gis/world2pixel.py - Convert world coordinates to pixel location
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


class TestWorld2Pixel:
    """Tests for world2pixel function."""

    def test_returns_tuple(self):
        """Test that function returns a tuple."""
        from iwfm.gis.world2pixel import world2pixel
        
        # Simple geomatrix: origin at (0, 100), 1 unit per pixel
        geoMatrix = [0, 1, 0, 100, 0, -1]
        
        result = world2pixel(geoMatrix, 50, 50)
        
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_integers(self):
        """Test that function returns integer pixel coordinates."""
        from iwfm.gis.world2pixel import world2pixel
        
        geoMatrix = [0, 1, 0, 100, 0, -1]
        
        pixel, line = world2pixel(geoMatrix, 50, 50)
        
        assert isinstance(pixel, int)
        assert isinstance(line, int)

    def test_origin_point(self):
        """Test point at origin."""
        from iwfm.gis.world2pixel import world2pixel
        
        # Origin at (0, 100), 1 unit per pixel
        geoMatrix = [0, 1, 0, 100, 0, -1]
        
        pixel, line = world2pixel(geoMatrix, 0, 100)
        
        assert pixel == 0
        assert line == 0

    def test_positive_offset(self):
        """Test point with positive offset from origin."""
        from iwfm.gis.world2pixel import world2pixel
        
        # Origin at (0, 100), 1 unit per pixel
        geoMatrix = [0, 1, 0, 100, 0, -1]
        
        pixel, line = world2pixel(geoMatrix, 10, 90)
        
        assert pixel == 10
        assert line == 10

    def test_larger_pixel_size(self):
        """Test with larger pixel size."""
        from iwfm.gis.world2pixel import world2pixel
        
        # Origin at (0, 100), 10 units per pixel
        geoMatrix = [0, 10, 0, 100, 0, -10]
        
        pixel, line = world2pixel(geoMatrix, 50, 50)
        
        assert pixel == 5
        assert line == 5

    def test_negative_x_distance(self):
        """Test with point to left of origin."""
        from iwfm.gis.world2pixel import world2pixel
        
        geoMatrix = [100, 1, 0, 100, 0, -1]
        
        pixel, line = world2pixel(geoMatrix, 50, 100)
        
        # x=50 is 50 pixels to the left of origin x=100
        assert pixel == -50

    def test_utm_like_coordinates(self):
        """Test with UTM-like coordinates."""
        from iwfm.gis.world2pixel import world2pixel
        
        # Typical UTM geomatrix: origin at (500000, 4000000), 30m resolution
        geoMatrix = [500000, 30, 0, 4000000, 0, -30]
        
        pixel, line = world2pixel(geoMatrix, 500300, 3999700)
        
        assert pixel == 10  # 300m / 30m
        assert line == 10   # 300m / 30m

    def test_fractional_coordinates(self):
        """Test that fractional coordinates are converted to integers."""
        from iwfm.gis.world2pixel import world2pixel
        
        geoMatrix = [0, 1, 0, 100, 0, -1]
        
        pixel, line = world2pixel(geoMatrix, 10.7, 89.3)
        
        # Should be truncated to integers
        assert pixel == 10
        assert line == 10


class TestWorld2PixelGeoMatrix:
    """Tests for understanding geomatrix format."""

    def test_geomatrix_format(self):
        """Document geomatrix format: [ulX, xDist, rtnX, ulY, rtnY, yDist]."""
        from iwfm.gis.world2pixel import world2pixel
        
        # geoMatrix[0] = ulX (upper left X)
        # geoMatrix[1] = xDist (pixel width)
        # geoMatrix[2] = rtnX (rotation, usually 0)
        # geoMatrix[3] = ulY (upper left Y)
        # geoMatrix[4] = rtnY (rotation, usually 0)
        # geoMatrix[5] = yDist (pixel height, usually negative)
        
        geoMatrix = [0, 1, 0, 100, 0, -1]
        
        pixel, line = world2pixel(geoMatrix, 50, 50)
        
        # This confirms the function works with standard GDAL geomatrix format
        assert isinstance(pixel, int)
        assert isinstance(line, int)


class TestWorld2PixelImports:
    """Tests for world2pixel imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import world2pixel
        assert callable(world2pixel)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.world2pixel import world2pixel
        assert callable(world2pixel)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.world2pixel import world2pixel
        
        assert world2pixel.__doc__ is not None
        assert 'pixel' in world2pixel.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
