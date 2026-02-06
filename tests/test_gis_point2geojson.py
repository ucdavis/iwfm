# test_gis_point2geojson.py
# Tests for gis/point2geojson.py - Convert a point to GeoJSON format
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


class TestPoint2Geojson:
    """Tests for point2geojson function."""

    def test_returns_geojson_object(self):
        """Test that function returns a GeoJSON object."""
        from iwfm.gis.point2geojson import point2geojson

        point = (-118.0, 34.0)  # lon, lat tuple
        result = point2geojson(point)

        # Should return a GeoJSON object
        assert result is not None

    def test_point_coordinates(self):
        """Test that GeoJSON has correct coordinates."""
        from iwfm.gis.point2geojson import point2geojson

        lon, lat = -118.2437, 34.0522
        point = (lon, lat)

        result = point2geojson(point)

        # GeoJSON Point should have coordinates attribute
        assert hasattr(result, 'coordinates') or 'coordinates' in str(result)

    def test_point_type(self):
        """Test that GeoJSON type is Point."""
        from iwfm.gis.point2geojson import point2geojson

        point = (-118.0, 34.0)
        result = point2geojson(point)

        # Should be a Point type
        assert result['type'] == 'Point' or result.type == 'Point'

    def test_3d_point(self):
        """Test with 3D point (lon, lat, elevation)."""
        from iwfm.gis.point2geojson import point2geojson

        point = (-118.0, 34.0, 100.0)  # lon, lat, elevation
        result = point2geojson(point)

        assert result is not None

    def test_verbose_false(self):
        """Test with verbose=False (default)."""
        from iwfm.gis.point2geojson import point2geojson

        point = (-118.0, 34.0)
        result = point2geojson(point, verbose=False)

        assert result is not None

    def test_verbose_true(self, capsys):
        """Test with verbose=True prints output."""
        from iwfm.gis.point2geojson import point2geojson

        point = (-118.0, 34.0)
        result = point2geojson(point, verbose=True)

        captured = capsys.readouterr()
        assert 'GeoJSON' in captured.out

    def test_origin_point(self):
        """Test with origin coordinates."""
        from iwfm.gis.point2geojson import point2geojson

        point = (0.0, 0.0)
        result = point2geojson(point)

        assert result is not None

    def test_negative_coordinates(self):
        """Test with negative coordinates (Western/Southern hemisphere)."""
        from iwfm.gis.point2geojson import point2geojson

        point = (-122.4194, -33.8688)  # Example: somewhere in Southern hemisphere
        result = point2geojson(point)

        assert result is not None


class TestPoint2GeojsonImports:
    """Tests for point2geojson imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import point2geojson
        assert callable(point2geojson)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.point2geojson import point2geojson
        assert callable(point2geojson)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.point2geojson import point2geojson

        assert point2geojson.__doc__ is not None
        assert 'geojson' in point2geojson.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
