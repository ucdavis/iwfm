# test_gis_kml_points.py
# Tests for gis/kml_points.py - Get point coordinates from a KML file
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


class TestKmlPoints:
    """Tests for kml_points function."""

    def test_returns_list(self, tmp_path):
        """Test that function returns a list."""
        from iwfm.gis.kml_points import kml_points

        kml_file = tmp_path / "test.kml"
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <name>Test Point</name>
      <Point>
        <coordinates>-118.0,34.0,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>
"""
        kml_file.write_text(kml_content)

        result = kml_points(str(kml_file))

        assert isinstance(result, list)

    def test_single_point(self, tmp_path):
        """Test extraction of a single point."""
        from iwfm.gis.kml_points import kml_points

        kml_file = tmp_path / "single_point.kml"
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <name>Los Angeles</name>
      <Point>
        <coordinates>-118.2437,34.0522,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>
"""
        kml_file.write_text(kml_content)

        points = kml_points(str(kml_file))

        assert len(points) == 1
        # Coordinates are returned as string array split by comma
        assert '-118.2437' in points[0][0]

    def test_multiple_points(self, tmp_path):
        """Test extraction of multiple points."""
        from iwfm.gis.kml_points import kml_points

        kml_file = tmp_path / "multi_points.kml"
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <name>Point 1</name>
      <Point>
        <coordinates>-118.0,34.0,0</coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>Point 2</name>
      <Point>
        <coordinates>-122.0,37.0,0</coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>Point 3</name>
      <Point>
        <coordinates>-117.0,33.0,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>
"""
        kml_file.write_text(kml_content)

        points = kml_points(str(kml_file))

        assert len(points) == 3

    def test_empty_kml(self, tmp_path):
        """Test with KML file containing no placemarks."""
        from iwfm.gis.kml_points import kml_points

        kml_file = tmp_path / "empty.kml"
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
  </Document>
</kml>
"""
        kml_file.write_text(kml_content)

        points = kml_points(str(kml_file))

        assert len(points) == 0

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output."""
        from iwfm.gis.kml_points import kml_points

        kml_file = tmp_path / "verbose.kml"
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <name>Test</name>
      <Point>
        <coordinates>-118.0,34.0,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>
"""
        kml_file.write_text(kml_content)

        points = kml_points(str(kml_file), verbose=True)

        captured = capsys.readouterr()
        assert 'placemark' in captured.out.lower()


class TestKmlPointsImports:
    """Tests for kml_points imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import kml_points
        assert callable(kml_points)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.kml_points import kml_points
        assert callable(kml_points)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.kml_points import kml_points

        assert kml_points.__doc__ is not None
        assert 'kml' in kml_points.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
