# test_gis_grid_colorize.py 
# Test gis/grid_colorize function for colorizing grids
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


from unittest.mock import patch, Mock
import numpy as np


def test_grid_colorize_imports():
    '''Test that grid_colorize imports colorsys (verifies fix).'''
    # This verifies the fix: added 'import colorsys'
    from iwfm.gis.grid_colorize import colorsys

    assert colorsys is not None
    assert hasattr(colorsys, 'hsv_to_rgb')


@patch('iwfm.gis.grid_colorize.ImageOps')
@patch('iwfm.gis.grid_colorize.Image')
@patch('iwfm.gis.grid_colorize.np')
def test_grid_colorize_basic(mock_np, mock_Image, mock_ImageOps, tmp_path):
    '''Test basic functionality of grid_colorize.'''
    from iwfm.gis.grid_colorize import grid_colorize

    # Create mock array from loadtxt
    mock_array = np.array([[0, 50, 100], [150, 200, 255]])
    mock_np.loadtxt.return_value = mock_array

    # Create mock PIL image
    mock_image = Mock()
    mock_image.convert.return_value = mock_image
    mock_Image.fromarray.return_value = mock_image

    # Mock ImageOps operations
    mock_ImageOps.equalize.return_value = mock_image
    mock_ImageOps.autocontrast.return_value = mock_image

    source = tmp_path / 'input.asc'
    target = tmp_path / 'output.png'

    # Create a proper ASCII DEM file for testing
    ascii_dem_content = '''ncols 3
nrows 2
xllcorner 0
yllcorner 0
cellsize 1
NODATA_value -9999
0 50 100
150 200 255'''
    source.write_text(ascii_dem_content)

    grid_colorize(str(source), str(target))

    # Verify the function called the expected methods
    mock_np.loadtxt.assert_called_once_with(str(source), skiprows=6)
    mock_Image.fromarray.assert_called_once()
    mock_image.convert.assert_called_once_with("L")
    mock_ImageOps.equalize.assert_called_once()
    mock_ImageOps.autocontrast.assert_called_once()
    mock_image.putpalette.assert_called_once()
    mock_image.save.assert_called_once_with(str(target))


def test_grid_colorize_function_signature():
    '''Test that grid_colorize has correct function signature.'''
    from iwfm.gis.grid_colorize import grid_colorize
    import inspect

    sig = inspect.signature(grid_colorize)
    params = list(sig.parameters.keys())

    assert 'source' in params
    assert 'target' in params
