# test_gis_xml_tracks.py
# Tests for gis/xml_tracks.py - Get tracking points from an XML file
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

# Check if lxml is available for BeautifulSoup XML parsing
try:
    import lxml  # noqa: F401
    del lxml
    HAS_LXML = True
except ImportError:
    HAS_LXML = False


@pytest.mark.skipif(not HAS_LXML, reason="lxml not installed (required for BeautifulSoup XML parsing)")
class TestXmlTracks:
    """Tests for xml_tracks function."""

    def test_returns_list(self, tmp_path):
        """Test that function returns a list (ResultSet)."""
        from iwfm.gis.xml_tracks import xml_tracks

        gpx_file = tmp_path / "track.gpx"
        gpx_content = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1">
  <trk>
    <trkseg>
      <trkpt lat="34.0" lon="-118.0">
        <ele>100</ele>
      </trkpt>
    </trkseg>
  </trk>
</gpx>
"""
        gpx_file.write_text(gpx_content)

        result = xml_tracks(str(gpx_file))

        # BeautifulSoup returns a ResultSet which is list-like
        assert hasattr(result, '__len__')

    def test_extracts_trackpoints(self, tmp_path):
        """Test extraction of track points."""
        from iwfm.gis.xml_tracks import xml_tracks

        gpx_file = tmp_path / "track.gpx"
        gpx_content = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1">
  <trk>
    <trkseg>
      <trkpt lat="34.0522" lon="-118.2437">
        <ele>100</ele>
      </trkpt>
      <trkpt lat="34.0530" lon="-118.2445">
        <ele>105</ele>
      </trkpt>
    </trkseg>
  </trk>
</gpx>
"""
        gpx_file.write_text(gpx_content)

        tracks = xml_tracks(str(gpx_file))

        assert len(tracks) == 2

    def test_multiple_segments(self, tmp_path):
        """Test extraction from multiple track segments."""
        from iwfm.gis.xml_tracks import xml_tracks

        gpx_file = tmp_path / "multi_track.gpx"
        gpx_content = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1">
  <trk>
    <trkseg>
      <trkpt lat="34.0" lon="-118.0"></trkpt>
    </trkseg>
    <trkseg>
      <trkpt lat="35.0" lon="-119.0"></trkpt>
      <trkpt lat="36.0" lon="-120.0"></trkpt>
    </trkseg>
  </trk>
</gpx>
"""
        gpx_file.write_text(gpx_content)

        tracks = xml_tracks(str(gpx_file))

        assert len(tracks) == 3

    def test_empty_gpx(self, tmp_path):
        """Test with GPX file containing no track points."""
        from iwfm.gis.xml_tracks import xml_tracks

        gpx_file = tmp_path / "empty.gpx"
        gpx_content = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1">
  <trk>
    <trkseg>
    </trkseg>
  </trk>
</gpx>
"""
        gpx_file.write_text(gpx_content)

        tracks = xml_tracks(str(gpx_file))

        assert len(tracks) == 0

    def test_track_point_attributes(self, tmp_path):
        """Test that track point attributes are accessible."""
        from iwfm.gis.xml_tracks import xml_tracks

        gpx_file = tmp_path / "attrs.gpx"
        gpx_content = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1">
  <trk>
    <trkseg>
      <trkpt lat="34.0522" lon="-118.2437">
        <ele>100</ele>
      </trkpt>
    </trkseg>
  </trk>
</gpx>
"""
        gpx_file.write_text(gpx_content)

        tracks = xml_tracks(str(gpx_file))

        # Check that lat/lon attributes are accessible
        assert tracks[0].get('lat') == '34.0522'
        assert tracks[0].get('lon') == '-118.2437'


class TestXmlTracksImports:
    """Tests for xml_tracks imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import xml_tracks
        assert callable(xml_tracks)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.xml_tracks import xml_tracks
        assert callable(xml_tracks)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.xml_tracks import xml_tracks

        assert xml_tracks.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
