# test_gis_shp_norec.py
# Tests for gis/shp_norec.py - Return number of records in shapefile
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


class TestShpNorec:
    """Tests for shp_norec function."""

    def test_returns_integer(self):
        """Test that function returns an integer."""
        from iwfm.gis.shp_norec import shp_norec
        
        mock_shp = Mock()
        mock_shp.numRecords = 100
        
        result = shp_norec(mock_shp)
        
        assert isinstance(result, int)

    def test_returns_num_records(self):
        """Test that function returns numRecords attribute."""
        from iwfm.gis.shp_norec import shp_norec
        
        mock_shp = Mock()
        mock_shp.numRecords = 42
        
        result = shp_norec(mock_shp)
        
        assert result == 42

    def test_zero_records(self):
        """Test with zero records."""
        from iwfm.gis.shp_norec import shp_norec
        
        mock_shp = Mock()
        mock_shp.numRecords = 0
        
        result = shp_norec(mock_shp)
        
        assert result == 0

    def test_large_number_of_records(self):
        """Test with large number of records."""
        from iwfm.gis.shp_norec import shp_norec
        
        mock_shp = Mock()
        mock_shp.numRecords = 1000000
        
        result = shp_norec(mock_shp)
        
        assert result == 1000000


class TestShpNorecImports:
    """Tests for shp_norec imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_norec
        assert callable(shp_norec)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_norec import shp_norec
        assert callable(shp_norec)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_norec import shp_norec
        
        assert shp_norec.__doc__ is not None
        assert 'record' in shp_norec.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
