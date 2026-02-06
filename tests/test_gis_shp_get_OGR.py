# test_gis_shp_get_OGR.py
# Tests for gis/shp_get_OGR.py - Open shapefile with OGR
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


class TestShpGetOGRImports:
    """Tests for shp_get_OGR imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_get_OGR
        assert callable(shp_get_OGR)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_get_OGR import shp_get_OGR
        assert callable(shp_get_OGR)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_get_OGR import shp_get_OGR

        assert shp_get_OGR.__doc__ is not None
        assert 'ogr' in shp_get_OGR.__doc__.lower()

    def test_function_has_verbose_parameter(self):
        """Test that function has verbose parameter."""
        import inspect
        from iwfm.gis.shp_get_OGR import shp_get_OGR

        sig = inspect.signature(shp_get_OGR)
        params = list(sig.parameters.keys())
        assert 'verbose' in params


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
