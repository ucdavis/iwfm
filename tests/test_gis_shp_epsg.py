# test_gis_shp_epsg.py
# Tests for gis/shp_epsg.py
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


class TestShpEpsgImports:
    """Tests for shp_epsg imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_epsg
        assert callable(shp_epsg)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_epsg import shp_epsg
        assert callable(shp_epsg)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_epsg import shp_epsg

        assert shp_epsg.__doc__ is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
