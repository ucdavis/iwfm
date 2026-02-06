# test_gis_distance_sphere.py
# Tests for gis/distance_sphere.py - Haversine distance on sphere
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


class TestDistanceSphere:
    """Tests for distance_sphere function."""

    def test_returns_float(self):
        """Test that function returns a float."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        p1 = [34.0522, -118.2437]  # Los Angeles
        p2 = [37.7749, -122.4194]  # San Francisco
        
        result = distance_sphere(p1, p2)
        
        assert isinstance(result, float)

    def test_same_point_zero_distance(self):
        """Test that same point returns zero distance."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        p1 = [34.0522, -118.2437]
        p2 = [34.0522, -118.2437]
        
        result = distance_sphere(p1, p2)
        
        assert result == 0.0

    def test_distance_is_positive(self):
        """Test that distance is always positive."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        p1 = [34.0522, -118.2437]
        p2 = [37.7749, -122.4194]
        
        result = distance_sphere(p1, p2)
        
        assert result > 0

    def test_distance_symmetric(self):
        """Test that distance is symmetric (A to B = B to A)."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        p1 = [34.0522, -118.2437]
        p2 = [37.7749, -122.4194]
        
        result1 = distance_sphere(p1, p2)
        result2 = distance_sphere(p2, p1)
        
        assert abs(result1 - result2) < 0.001

    def test_default_units_km(self):
        """Test that default units are kilometers."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        # LA to SF is about 559 km
        p1 = [34.0522, -118.2437]
        p2 = [37.7749, -122.4194]
        
        result = distance_sphere(p1, p2)
        
        # Should be in km range (not meters or miles)
        assert 500 < result < 700

    def test_units_miles(self):
        """Test distance in miles."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        p1 = [34.0522, -118.2437]
        p2 = [37.7749, -122.4194]
        
        result = distance_sphere(p1, p2, units='mi')
        
        # LA to SF is about 347 miles
        assert 300 < result < 400

    def test_units_feet(self):
        """Test distance in feet."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        p1 = [34.0522, -118.2437]
        p2 = [37.7749, -122.4194]
        
        result = distance_sphere(p1, p2, units='ft')
        
        # Should be in millions of feet
        assert result > 1e6

    def test_km_vs_miles_ratio(self):
        """Test that km and miles have correct ratio (~1.609)."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        p1 = [34.0522, -118.2437]
        p2 = [37.7749, -122.4194]
        
        km = distance_sphere(p1, p2, units='km')
        mi = distance_sphere(p1, p2, units='mi')
        
        ratio = km / mi
        assert 1.5 < ratio < 1.7  # Should be ~1.609

    def test_known_distance(self):
        """Test with known distance (New York to London ~5570 km)."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        p1 = [40.7128, -74.0060]  # New York
        p2 = [51.5074, -0.1278]   # London
        
        result = distance_sphere(p1, p2, units='km')
        
        # Should be approximately 5570 km
        assert 5400 < result < 5700

    def test_equator_distance(self):
        """Test distance along equator."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        # 1 degree of longitude at equator ≈ 111 km
        p1 = [0.0, 0.0]
        p2 = [0.0, 1.0]
        
        result = distance_sphere(p1, p2, units='km')
        
        assert 100 < result < 120


class TestDistanceSphereImports:
    """Tests for distance_sphere imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import distance_sphere
        assert callable(distance_sphere)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.distance_sphere import distance_sphere
        assert callable(distance_sphere)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.distance_sphere import distance_sphere
        
        assert distance_sphere.__doc__ is not None
        assert 'haversine' in distance_sphere.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
