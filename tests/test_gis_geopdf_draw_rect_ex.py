# test_gis_geopdf_draw_rect_ex.py
# Tests for gis/geopdf_draw_rect_ex.py - Example drawing rectangle on GeoPDF canvas
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


class TestGeopdfDrawRectEx:
    """Tests for geopdf_draw_rect_ex function."""

    def test_calls_rect_method(self):
        """Test that function calls canvas.rect method."""
        from iwfm.gis.geopdf_draw_rect_ex import geopdf_draw_rect_ex

        mock_canvas = Mock()

        geopdf_draw_rect_ex(mock_canvas)

        mock_canvas.rect.assert_called_once()

    def test_rect_parameters(self):
        """Test that rect is called with correct parameters."""
        from iwfm.gis.geopdf_draw_rect_ex import geopdf_draw_rect_ex

        mock_canvas = Mock()

        geopdf_draw_rect_ex(mock_canvas)

        # Check that rect was called with the expected parameters
        mock_canvas.rect.assert_called_with(100, 400, 400, 250, stroke=1)

    def test_returns_none(self):
        """Test that function returns None."""
        from iwfm.gis.geopdf_draw_rect_ex import geopdf_draw_rect_ex

        mock_canvas = Mock()

        result = geopdf_draw_rect_ex(mock_canvas)

        assert result is None


class TestGeopdfDrawRectExImports:
    """Tests for geopdf_draw_rect_ex imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import geopdf_draw_rect_ex
        assert callable(geopdf_draw_rect_ex)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.geopdf_draw_rect_ex import geopdf_draw_rect_ex
        assert callable(geopdf_draw_rect_ex)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.geopdf_draw_rect_ex import geopdf_draw_rect_ex

        assert geopdf_draw_rect_ex.__doc__ is not None
        assert 'example' in geopdf_draw_rect_ex.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
