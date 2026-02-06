# test_gis_shp_getrec_lg.py
# Tests for gis/shp_getrec_lg.py - Return record for large DBF files
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


class TestShpGetrecLg:
    """Tests for shp_getrec_lg function."""

    def test_calls_iterRecord(self):
        """Test that function calls iterRecord."""
        from iwfm.gis.shp_getrec_lg import shp_getrec_lg
        
        mock_record = Mock()
        mock_shp = Mock()
        mock_shp.iterRecord.return_value = mock_record
        
        result = shp_getrec_lg(mock_shp, 5)
        
        mock_shp.iterRecord.assert_called_once_with(5)

    def test_returns_record(self):
        """Test that function returns the record."""
        from iwfm.gis.shp_getrec_lg import shp_getrec_lg
        
        mock_record = ['value1', 'value2', 'value3']
        mock_shp = Mock()
        mock_shp.iterRecord.return_value = mock_record
        
        result = shp_getrec_lg(mock_shp, 0)
        
        assert result == mock_record

    def test_different_indices(self):
        """Test with different record indices."""
        from iwfm.gis.shp_getrec_lg import shp_getrec_lg
        
        mock_shp = Mock()
        mock_shp.iterRecord.side_effect = lambda i: f'record_{i}'
        
        assert shp_getrec_lg(mock_shp, 0) == 'record_0'
        assert shp_getrec_lg(mock_shp, 10) == 'record_10'
        assert shp_getrec_lg(mock_shp, 99) == 'record_99'


class TestShpGetrecLgImports:
    """Tests for shp_getrec_lg imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_getrec_lg
        assert callable(shp_getrec_lg)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_getrec_lg import shp_getrec_lg
        assert callable(shp_getrec_lg)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_getrec_lg import shp_getrec_lg
        
        assert shp_getrec_lg.__doc__ is not None
        assert 'record' in shp_getrec_lg.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
