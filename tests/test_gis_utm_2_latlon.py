# test_gis_utm_2_latlon.py
# Tests for gis/utm_2_latlon.py - Reproject from UTM to geographic coordinates
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


class TestUtm2Latlon:
    """Tests for utm_2_latlon function."""

    def test_returns_tuple(self):
        """Test that function returns a tuple of 2 values."""
        from iwfm.gis.utm_2_latlon import utm_2_latlon

        # UTM coordinates for Los Angeles area
        result = utm_2_latlon(385000, 3770000, 11, 'S')

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_los_angeles_coordinates(self):
        """Test conversion of Los Angeles UTM coordinates."""
        from iwfm.gis.utm_2_latlon import utm_2_latlon

        # Approximate UTM for LA: Zone 11, ~385000E, ~3770000N
        easting, northing = 385000, 3770000
        zone = 11

        lat, lon = utm_2_latlon(easting, northing, zone, 'S')

        # Should be approximately 34°N, 118°W
        assert 33 < lat < 35
        assert -119 < lon < -117

    def test_round_trip_conversion(self):
        """Test that converting to UTM and back gives original coordinates."""
        from iwfm.gis.utm_2_latlon import utm_2_latlon
        from iwfm.gis.latlon_2_utm import latlon_2_utm

        original_lat, original_lon = 34.0522, -118.2437

        # Convert to UTM
        easting, northing, zone, letter = latlon_2_utm(original_lat, original_lon)

        # Convert back to lat/lon
        lat, lon = utm_2_latlon(easting, northing, zone, letter)

        # Should be close to original (within ~0.001 degrees)
        assert abs(lat - original_lat) < 0.001
        assert abs(lon - original_lon) < 0.001

    def test_northern_hemisphere(self):
        """Test coordinates in northern hemisphere."""
        from iwfm.gis.utm_2_latlon import utm_2_latlon

        # UTM coordinates in Zone 15 (Central US)
        easting, northing = 500000, 4500000
        zone = 15

        lat, lon = utm_2_latlon(easting, northing, zone, 'T')

        # Should be in northern hemisphere
        assert lat > 0

    def test_default_band(self):
        """Test that default band parameter works."""
        from iwfm.gis.utm_2_latlon import utm_2_latlon

        # Should not raise error with default band
        lat, lon = utm_2_latlon(500000, 4500000, 11)

        assert isinstance(lat, float)
        assert isinstance(lon, float)


class TestUtm2LatlonImports:
    """Tests for utm_2_latlon imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import utm_2_latlon
        assert callable(utm_2_latlon)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.utm_2_latlon import utm_2_latlon
        assert callable(utm_2_latlon)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.utm_2_latlon import utm_2_latlon

        assert utm_2_latlon.__doc__ is not None
        assert 'utm' in utm_2_latlon.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
