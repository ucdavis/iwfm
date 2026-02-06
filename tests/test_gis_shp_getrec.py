# test_gis_shp_getrec.py
# Tests for gis/shp_getrec.py - Return a shapefile record as a string
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


class TestShpGetrec:
    """Tests for shp_getrec function."""

    def test_returns_record(self):
        """Test that function returns record at index."""
        from iwfm.gis.shp_getrec import shp_getrec
        
        mock_record = Mock()
        mock_shp = Mock()
        mock_shp.record.return_value = mock_record
        
        result = shp_getrec(mock_shp, 0)
        
        mock_shp.record.assert_called_once_with(0)
        assert result == mock_record

    def test_calls_record_with_index(self):
        """Test that function calls record with specified index."""
        from iwfm.gis.shp_getrec import shp_getrec
        
        mock_shp = Mock()
        
        shp_getrec(mock_shp, 5)
        
        mock_shp.record.assert_called_with(5)

    def test_different_indices(self):
        """Test with different record indices."""
        from iwfm.gis.shp_getrec import shp_getrec
        
        mock_shp = Mock()
        mock_shp.record.side_effect = lambda i: f'record_{i}'
        
        assert shp_getrec(mock_shp, 0) == 'record_0'
        assert shp_getrec(mock_shp, 10) == 'record_10'
        assert shp_getrec(mock_shp, 99) == 'record_99'


class TestShpGetrecImports:
    """Tests for shp_getrec imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_getrec
        assert callable(shp_getrec)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_getrec import shp_getrec
        assert callable(shp_getrec)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_getrec import shp_getrec
        
        assert shp_getrec.__doc__ is not None
        assert 'record' in shp_getrec.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
