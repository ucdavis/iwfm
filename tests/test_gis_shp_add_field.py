# test_gis_shp_add_field.py
# Tests for gis/shp_add_field.py
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


class TestShpAddFieldImports:
    """Tests for shp_add_field imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import shp_add_field
        assert callable(shp_add_field)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.shp_add_field import shp_add_field
        assert callable(shp_add_field)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.shp_add_field import shp_add_field

        assert shp_add_field.__doc__ is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
