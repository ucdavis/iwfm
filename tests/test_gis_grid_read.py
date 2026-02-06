# test_gis_grid_read.py
# Tests for gis/grid_read.py - Read an ASCII Grid file
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
import numpy as np


class TestGridRead:
    """Tests for grid_read function."""

    def test_returns_tuple(self, tmp_path):
        """Test that function returns a tuple of (header, array)."""
        from iwfm.gis.grid_read import grid_read

        # Create a test ASCII grid file
        grid_file = tmp_path / "test_grid.asc"
        content = """ncols 5
nrows 4
xllcorner 0.0
yllcorner 0.0
cellsize 1.0
NODATA_value -9999
1.0 2.0 3.0 4.0 5.0
6.0 7.0 8.0 9.0 10.0
11.0 12.0 13.0 14.0 15.0
16.0 17.0 18.0 19.0 20.0
"""
        grid_file.write_text(content)

        result = grid_read(str(grid_file))

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_header_content(self, tmp_path):
        """Test that header contains correct information."""
        from iwfm.gis.grid_read import grid_read

        grid_file = tmp_path / "test_grid.asc"
        content = """ncols 5
nrows 4
xllcorner 100.0
yllcorner 200.0
cellsize 10.0
NODATA_value -9999
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
"""
        grid_file.write_text(content)

        header, array = grid_read(str(grid_file))

        assert 'ncols' in header.lower()
        assert 'nrows' in header.lower()
        assert 'xllcorner' in header.lower()
        assert 'cellsize' in header.lower()

    def test_array_shape(self, tmp_path):
        """Test that array has correct shape."""
        from iwfm.gis.grid_read import grid_read

        grid_file = tmp_path / "test_grid.asc"
        content = """ncols 5
nrows 4
xllcorner 0.0
yllcorner 0.0
cellsize 1.0
NODATA_value -9999
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
"""
        grid_file.write_text(content)

        header, array = grid_read(str(grid_file))

        assert array.shape == (4, 5)  # nrows x ncols

    def test_array_values(self, tmp_path):
        """Test that array contains correct values."""
        from iwfm.gis.grid_read import grid_read

        grid_file = tmp_path / "test_grid.asc"
        content = """ncols 3
nrows 2
xllcorner 0.0
yllcorner 0.0
cellsize 1.0
NODATA_value -9999
1.5 2.5 3.5
4.5 5.5 6.5
"""
        grid_file.write_text(content)

        header, array = grid_read(str(grid_file))

        assert array[0, 0] == pytest.approx(1.5)
        assert array[0, 2] == pytest.approx(3.5)
        assert array[1, 0] == pytest.approx(4.5)

    def test_array_is_numpy(self, tmp_path):
        """Test that array is a numpy array."""
        from iwfm.gis.grid_read import grid_read

        grid_file = tmp_path / "test_grid.asc"
        content = """ncols 3
nrows 2
xllcorner 0.0
yllcorner 0.0
cellsize 1.0
NODATA_value -9999
1 2 3
4 5 6
"""
        grid_file.write_text(content)

        header, array = grid_read(str(grid_file))

        assert isinstance(array, np.ndarray)

    def test_nodata_values(self, tmp_path):
        """Test handling of NODATA values."""
        from iwfm.gis.grid_read import grid_read

        grid_file = tmp_path / "test_grid.asc"
        content = """ncols 3
nrows 2
xllcorner 0.0
yllcorner 0.0
cellsize 1.0
NODATA_value -9999
1 -9999 3
4 5 -9999
"""
        grid_file.write_text(content)

        header, array = grid_read(str(grid_file))

        assert array[0, 1] == -9999
        assert array[1, 2] == -9999


class TestGridReadImports:
    """Tests for grid_read imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import grid_read
        assert callable(grid_read)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.grid_read import grid_read
        assert callable(grid_read)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.grid_read import grid_read

        assert grid_read.__doc__ is not None
        assert 'grid' in grid_read.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
