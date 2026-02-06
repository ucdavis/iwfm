# test_gis_rasterio_open.py
# Tests for gis/rasterio_open.py
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


class TestRasterioOpenImports:
    """Tests for rasterio_open imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import rasterio_open
        assert callable(rasterio_open)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.rasterio_open import rasterio_open
        assert callable(rasterio_open)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.rasterio_open import rasterio_open

        assert rasterio_open.__doc__ is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
