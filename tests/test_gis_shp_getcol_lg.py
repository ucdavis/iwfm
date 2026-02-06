# test_gis_shp_getcol_lg.py
# Tests for gis/shp_getcol_lg.py
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


class TestShpGetcolLgImports:
    """Tests for shp_getcol_lg imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_getcol_lg
        assert callable(shp_getcol_lg)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_getcol_lg import shp_getcol_lg
        assert callable(shp_getcol_lg)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_getcol_lg import shp_getcol_lg

        assert shp_getcol_lg.__doc__ is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
