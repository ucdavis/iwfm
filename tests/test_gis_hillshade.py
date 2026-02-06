# test_gis_hillshade.py
# Tests for gis/hillshade.py - Convert array to hillshade
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
import numpy as np


class TestHillshade:
    """Tests for hillshade function."""

    def test_returns_array(self):
        """Test that function returns a numpy array."""
        from iwfm.gis.hillshade import hillshade
        
        array = np.array([[100, 110, 120],
                          [105, 115, 125],
                          [110, 120, 130]])
        
        result = hillshade(array, azimuth=315, angle_altitude=45)
        
        assert isinstance(result, np.ndarray)

    def test_output_same_shape(self):
        """Test that output has same shape as input."""
        from iwfm.gis.hillshade import hillshade
        
        array = np.array([[100, 110, 120],
                          [105, 115, 125],
                          [110, 120, 130]])
        
        result = hillshade(array, azimuth=315, angle_altitude=45)
        
        assert result.shape == array.shape

    def test_output_range(self):
        """Test that output values are in valid range (0-255)."""
        from iwfm.gis.hillshade import hillshade
        
        array = np.array([[100, 110, 120],
                          [105, 115, 125],
                          [110, 120, 130]])
        
        result = hillshade(array, azimuth=315, angle_altitude=45)
        
        assert np.all(result >= 0)
        assert np.all(result <= 255)

    def test_flat_surface(self):
        """Test hillshade on flat surface."""
        from iwfm.gis.hillshade import hillshade
        
        # Flat surface (all same elevation)
        array = np.ones((10, 10)) * 100
        
        result = hillshade(array, azimuth=315, angle_altitude=45)
        
        # Flat surface should have uniform shading
        assert np.std(result) < 1  # Very low variation

    def test_different_azimuths(self):
        """Test that different azimuths produce different results."""
        from iwfm.gis.hillshade import hillshade
        
        array = np.array([[100, 110, 120],
                          [105, 115, 125],
                          [110, 120, 130]])
        
        result1 = hillshade(array, azimuth=0, angle_altitude=45)
        result2 = hillshade(array, azimuth=180, angle_altitude=45)
        
        # Different azimuths should give different results
        assert not np.allclose(result1, result2)

    def test_different_altitudes(self):
        """Test that different sun altitudes produce different results."""
        from iwfm.gis.hillshade import hillshade
        
        array = np.array([[100, 110, 120],
                          [105, 115, 125],
                          [110, 120, 130]])
        
        result1 = hillshade(array, azimuth=315, angle_altitude=30)
        result2 = hillshade(array, azimuth=315, angle_altitude=60)
        
        # Different altitudes should give different results
        assert not np.allclose(result1, result2)

    def test_large_array(self):
        """Test with larger array."""
        from iwfm.gis.hillshade import hillshade
        
        # Create a simple terrain
        x = np.linspace(0, 100, 50)
        y = np.linspace(0, 100, 50)
        X, Y = np.meshgrid(x, y)
        array = X + Y  # Simple slope
        
        result = hillshade(array, azimuth=315, angle_altitude=45)
        
        assert result.shape == (50, 50)
        assert np.all(result >= 0)
        assert np.all(result <= 255)

    def test_steep_terrain(self):
        """Test with steep terrain."""
        from iwfm.gis.hillshade import hillshade
        
        # Create steep terrain
        array = np.array([[0, 100, 200],
                          [0, 100, 200],
                          [0, 100, 200]])
        
        result = hillshade(array, azimuth=315, angle_altitude=45)
        
        # Should still be in valid range
        assert np.all(result >= 0)
        assert np.all(result <= 255)


class TestHillshadeImports:
    """Tests for hillshade imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import hillshade
        assert callable(hillshade)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.hillshade import hillshade
        assert callable(hillshade)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.hillshade import hillshade
        
        assert hillshade.__doc__ is not None
        assert 'hillshade' in hillshade.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
