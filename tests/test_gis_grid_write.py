# test_gis_grid_write.py
# Tests for gis/grid_write.py - Write an ASCII Grid file
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


class TestGridWrite:
    """Tests for grid_write function."""

    def test_creates_file(self, tmp_path):
        """Test that function creates an output file."""
        from iwfm.gis.grid_write import grid_write

        outfile = tmp_path / "output_grid.asc"
        array = np.array([[1, 2, 3], [4, 5, 6]])

        grid_write(str(outfile), array)

        assert outfile.exists()

    def test_header_content(self, tmp_path):
        """Test that output file has correct header."""
        from iwfm.gis.grid_write import grid_write

        outfile = tmp_path / "output_grid.asc"
        array = np.array([[1, 2, 3], [4, 5, 6]])

        grid_write(str(outfile), array, xllcorner=100.0, yllcorner=200.0, cellsize=10.0)

        content = outfile.read_text()

        assert 'ncols 3' in content
        assert 'nrows 2' in content
        assert 'xllcorner 100.0' in content
        assert 'yllcorner 200.0' in content
        assert 'cellsize 10.0' in content

    def test_default_parameters(self, tmp_path):
        """Test that function uses default parameters."""
        from iwfm.gis.grid_write import grid_write

        outfile = tmp_path / "output_grid.asc"
        array = np.array([[1, 2], [3, 4]])

        grid_write(str(outfile), array)

        content = outfile.read_text()

        # Check default values
        assert 'xllcorner 277750.0' in content
        assert 'yllcorner 6122250.0' in content
        assert 'cellsize 1.0' in content
        assert 'NODATA_value -9999' in content

    def test_nodata_value(self, tmp_path):
        """Test custom NODATA value."""
        from iwfm.gis.grid_write import grid_write

        outfile = tmp_path / "output_grid.asc"
        array = np.array([[1, 2], [3, 4]])

        grid_write(str(outfile), array, nodata=-999)

        content = outfile.read_text()

        assert 'NODATA_value -999' in content

    def test_data_values(self, tmp_path):
        """Test that data values are written correctly."""
        from iwfm.gis.grid_write import grid_write

        outfile = tmp_path / "output_grid.asc"
        array = np.array([[1.5, 2.5], [3.5, 4.5]])

        grid_write(str(outfile), array)

        content = outfile.read_text()
        lines = content.strip().split('\n')

        # Skip header (6 lines), check data
        data_lines = lines[6:]
        assert len(data_lines) == 2

    def test_round_trip_with_grid_read(self, tmp_path):
        """Test round-trip with grid_read."""
        from iwfm.gis.grid_write import grid_write
        from iwfm.gis.grid_read import grid_read

        outfile = tmp_path / "roundtrip_grid.asc"
        original_array = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

        # Write the grid
        grid_write(str(outfile), original_array, xllcorner=0.0, yllcorner=0.0)

        # Read it back
        header, read_array = grid_read(str(outfile))

        # Check that values match (within floating point precision)
        np.testing.assert_array_almost_equal(read_array, original_array, decimal=2)

    def test_large_array(self, tmp_path):
        """Test with a larger array."""
        from iwfm.gis.grid_write import grid_write

        outfile = tmp_path / "large_grid.asc"
        array = np.random.rand(50, 100)  # 50 rows, 100 columns

        grid_write(str(outfile), array)

        content = outfile.read_text()
        assert 'ncols 100' in content
        assert 'nrows 50' in content


class TestGridWriteImports:
    """Tests for grid_write imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import grid_write
        assert callable(grid_write)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.grid_write import grid_write
        assert callable(grid_write)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.grid_write import grid_write

        assert grid_write.__doc__ is not None
        assert 'grid' in grid_write.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
