# test_gis_shp_get_PyShp.py
# Tests for gis/shp_get_PyShp.py - Read shapefile with PyShp
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
from unittest.mock import Mock, patch


class TestShpGetPyShp:
    """Tests for shp_get_PyShp function."""

    def test_calls_shapefile_reader(self):
        """Test that function calls shapefile.Reader."""
        from iwfm.gis.shp_get_PyShp import shp_get_PyShp

        mock_shp = Mock()

        with patch('shapefile.Reader', return_value=mock_shp) as mock_reader:
            result = shp_get_PyShp('input.shp')

            mock_reader.assert_called_once_with('input.shp')

    def test_returns_reader_object(self):
        """Test that function returns reader object."""
        from iwfm.gis.shp_get_PyShp import shp_get_PyShp

        mock_reader_instance = Mock()

        with patch('shapefile.Reader', return_value=mock_reader_instance):
            result = shp_get_PyShp('input.shp')

            assert result == mock_reader_instance

    def test_verbose_prints_message(self, capsys):
        """Test that verbose mode prints message."""
        from iwfm.gis.shp_get_PyShp import shp_get_PyShp

        with patch('shapefile.Reader', return_value=Mock()):
            shp_get_PyShp('test.shp', verbose=True)

            captured = capsys.readouterr()
            assert 'test.shp' in captured.out

    def test_verbose_false_no_output(self, capsys):
        """Test that verbose=False produces no output."""
        from iwfm.gis.shp_get_PyShp import shp_get_PyShp

        with patch('shapefile.Reader', return_value=Mock()):
            shp_get_PyShp('test.shp', verbose=False)

            captured = capsys.readouterr()
            assert captured.out == ''


class TestShpGetPyShpImports:
    """Tests for shp_get_PyShp imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_get_PyShp
        assert callable(shp_get_PyShp)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_get_PyShp import shp_get_PyShp
        assert callable(shp_get_PyShp)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_get_PyShp import shp_get_PyShp

        assert shp_get_PyShp.__doc__ is not None
        assert 'shapefile' in shp_get_PyShp.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
