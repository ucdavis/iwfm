# test_gis_latlon_2_utm.py
# Tests for gis/latlon_2_utm.py - Reproject from geographic coordinates to UTM
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


class TestLatlon2Utm:
    """Tests for latlon_2_utm function."""

    def test_returns_tuple(self):
        """Test that function returns a tuple of 4 values."""
        from iwfm.gis.latlon_2_utm import latlon_2_utm

        result = latlon_2_utm(34.0, -118.0)

        assert isinstance(result, tuple)
        assert len(result) == 4

    def test_los_angeles_coordinates(self):
        """Test conversion of Los Angeles area coordinates."""
        from iwfm.gis.latlon_2_utm import latlon_2_utm

        # Los Angeles area: ~34°N, 118°W -> UTM Zone 11
        lat, lon = 34.0522, -118.2437

        easting, northing, zone_number, zone_letter = latlon_2_utm(lat, lon)

        assert zone_number == 11
        assert zone_letter == 'S'
        # Check that easting/northing are reasonable values
        assert 300000 < easting < 800000
        assert 3000000 < northing < 4500000

    def test_san_francisco_coordinates(self):
        """Test conversion of San Francisco area coordinates."""
        from iwfm.gis.latlon_2_utm import latlon_2_utm

        # San Francisco: ~37.77°N, 122.42°W -> UTM Zone 10
        lat, lon = 37.7749, -122.4194

        easting, northing, zone_number, zone_letter = latlon_2_utm(lat, lon)

        assert zone_number == 10
        assert zone_letter == 'S'

    def test_northern_hemisphere(self):
        """Test coordinates in northern hemisphere."""
        from iwfm.gis.latlon_2_utm import latlon_2_utm

        lat, lon = 45.0, -93.0  # Minneapolis area

        easting, northing, zone_number, zone_letter = latlon_2_utm(lat, lon)

        # Zone letter should be in northern hemisphere range (N-X)
        assert zone_letter in 'NPQRSTUVWX'

    def test_southern_hemisphere(self):
        """Test coordinates in southern hemisphere."""
        from iwfm.gis.latlon_2_utm import latlon_2_utm

        lat, lon = -33.9, 18.4  # Cape Town, South Africa

        easting, northing, zone_number, zone_letter = latlon_2_utm(lat, lon)

        # Zone letter should be in southern hemisphere range (C-M)
        assert zone_letter in 'CDEFGHJKLM'

    def test_equator(self):
        """Test coordinates at the equator."""
        from iwfm.gis.latlon_2_utm import latlon_2_utm

        lat, lon = 0.0, 0.0

        easting, northing, zone_number, zone_letter = latlon_2_utm(lat, lon)

        assert zone_number == 31
        # Equator is boundary between N and M zones
        assert zone_letter in 'NM'

    def test_array_input(self):
        """Test with array/list input."""
        from iwfm.gis.latlon_2_utm import latlon_2_utm

        lats = [34.0, 35.0, 36.0]
        lons = [-118.0, -118.0, -118.0]

        easting, northing, zone_number, zone_letter = latlon_2_utm(lats, lons)

        # Should return arrays of same length
        assert len(easting) == 3
        assert len(northing) == 3


class TestLatlon2UtmImports:
    """Tests for latlon_2_utm imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import latlon_2_utm
        assert callable(latlon_2_utm)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.latlon_2_utm import latlon_2_utm
        assert callable(latlon_2_utm)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.latlon_2_utm import latlon_2_utm

        assert latlon_2_utm.__doc__ is not None
        assert 'utm' in latlon_2_utm.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
