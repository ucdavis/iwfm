# test_gis_bearing.py
# Tests for gis/bearing.py - Calculate bearing between two lat-lon points
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


class TestBearing:
    """Tests for bearing function."""

    def test_returns_float(self):
        """Test that function returns a float."""
        from iwfm.gis.bearing import bearing
        
        p1 = [34.0, -118.0]  # Los Angeles area
        p2 = [37.0, -122.0]  # San Francisco area
        
        result = bearing(p1, p2)
        
        assert isinstance(result, float)

    def test_bearing_north(self):
        """Test bearing going due north (should be ~0 or 360)."""
        from iwfm.gis.bearing import bearing
        
        p1 = [34.0, -118.0]
        p2 = [35.0, -118.0]  # Same longitude, higher latitude
        
        result = bearing(p1, p2)
        
        # Should be close to 0 (north)
        assert result < 5 or result > 355

    def test_bearing_south(self):
        """Test bearing going due south (should be ~180)."""
        from iwfm.gis.bearing import bearing
        
        p1 = [35.0, -118.0]
        p2 = [34.0, -118.0]  # Same longitude, lower latitude
        
        result = bearing(p1, p2)
        
        # Should be close to 180 (south)
        assert 175 < result < 185

    def test_bearing_east(self):
        """Test bearing going due east (should be ~90)."""
        from iwfm.gis.bearing import bearing
        
        p1 = [34.0, -118.0]
        p2 = [34.0, -117.0]  # Same latitude, higher longitude
        
        result = bearing(p1, p2)
        
        # Should be close to 90 (east)
        assert 85 < result < 95

    def test_bearing_west(self):
        """Test bearing going due west (should be ~270)."""
        from iwfm.gis.bearing import bearing
        
        p1 = [34.0, -117.0]
        p2 = [34.0, -118.0]  # Same latitude, lower longitude
        
        result = bearing(p1, p2)
        
        # Should be close to 270 (west)
        assert 265 < result < 275

    def test_bearing_range(self):
        """Test that bearing is always between 0 and 360."""
        from iwfm.gis.bearing import bearing
        
        test_points = [
            ([0.0, 0.0], [45.0, 90.0]),
            ([45.0, -90.0], [-45.0, 90.0]),
            ([-30.0, -60.0], [30.0, 60.0]),
        ]
        
        for p1, p2 in test_points:
            result = bearing(p1, p2)
            assert 0 <= result < 360

    def test_same_point(self):
        """Test bearing when both points are the same."""
        from iwfm.gis.bearing import bearing
        
        p1 = [34.0, -118.0]
        p2 = [34.0, -118.0]
        
        # Should return a value (likely 0) without error
        result = bearing(p1, p2)
        assert isinstance(result, float)

    def test_antipodal_points(self):
        """Test bearing to antipodal point."""
        from iwfm.gis.bearing import bearing
        
        p1 = [0.0, 0.0]
        p2 = [0.0, 180.0]  # Opposite side of Earth
        
        result = bearing(p1, p2)
        
        # Should be east (90) or west (270)
        assert 85 < result < 95 or 265 < result < 275

    def test_known_bearing(self):
        """Test with known bearing calculation."""
        from iwfm.gis.bearing import bearing
        
        # New York to London (approximately northeast)
        p1 = [40.7128, -74.0060]  # New York
        p2 = [51.5074, -0.1278]   # London
        
        result = bearing(p1, p2)
        
        # Should be roughly northeast (between 30-60 degrees)
        assert 30 < result < 70


class TestBearingImports:
    """Tests for bearing imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import bearing
        assert callable(bearing)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.bearing import bearing
        assert callable(bearing)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.bearing import bearing
        
        assert bearing.__doc__ is not None
        assert 'bearing' in bearing.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
