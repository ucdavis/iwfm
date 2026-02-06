# test_gis_shp_type_txt.py
# Tests for gis/shp_type_txt.py - Return text string of shape type
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
from unittest.mock import Mock


class TestShpTypeTxt:
    """Tests for shp_type_txt function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 1

        result = shp_type_txt(mock_shp)

        assert isinstance(result, str)

    def test_point_type(self):
        """Test POINT type (1)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 1

        result = shp_type_txt(mock_shp)

        assert result == 'POINT'

    def test_line_type(self):
        """Test LINE type (3)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 3

        result = shp_type_txt(mock_shp)

        assert result == 'LINE'

    def test_polygon_type(self):
        """Test POLYGON type (5)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 5

        result = shp_type_txt(mock_shp)

        assert result == 'POLYGON'

    def test_multipoint_type(self):
        """Test MULTIPOINT type (8)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 8

        result = shp_type_txt(mock_shp)

        assert result == 'MULTIPOINT'

    def test_pointz_type(self):
        """Test POINTZ type (11)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 11

        result = shp_type_txt(mock_shp)

        assert result == 'POINTZ'

    def test_polylinez_type(self):
        """Test POLYLINEZ type (13)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 13

        result = shp_type_txt(mock_shp)

        assert result == 'POLYLINEZ'

    def test_polygonz_type(self):
        """Test POLYGONZ type (15)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 15

        result = shp_type_txt(mock_shp)

        assert result == 'POLYGONZ'

    def test_null_type(self):
        """Test NULL type (unknown)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 999

        result = shp_type_txt(mock_shp)

        assert result == 'NULL'

    def test_pointm_type(self):
        """Test POINTM type (21)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 21

        result = shp_type_txt(mock_shp)

        assert result == 'POINTM'

    def test_multipatch_type(self):
        """Test MULTIPATCH type (31)."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        mock_shp = Mock()
        mock_shp.shapeType = 31

        result = shp_type_txt(mock_shp)

        assert result == 'MULTIPATCH'


class TestShpTypeTxtImports:
    """Tests for shp_type_txt imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_type_txt
        assert callable(shp_type_txt)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_type_txt import shp_type_txt
        assert callable(shp_type_txt)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_type_txt import shp_type_txt

        assert shp_type_txt.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
