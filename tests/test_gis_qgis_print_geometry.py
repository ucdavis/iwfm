# test_gis_qgis_print_geometry.py
# Tests for gis/qgis_print_geometry.py
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

# Check if QGIS is available
try:
    from qgis.core import QgsWkbTypes  # noqa: F401
    del QgsWkbTypes
    HAS_QGIS = True
except ImportError:
    HAS_QGIS = False


@pytest.mark.skipif(not HAS_QGIS, reason="QGIS not installed")
class TestQgisPrintGeometryImports:
    """Tests for qgis_print_geometry imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import qgis_print_geometry
        assert callable(qgis_print_geometry)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.qgis_print_geometry import qgis_print_geometry
        assert callable(qgis_print_geometry)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.qgis_print_geometry import qgis_print_geometry

        assert qgis_print_geometry.__doc__ is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
