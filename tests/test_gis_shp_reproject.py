# test_gis_shp_reproject.py 
# Test gis/shp_reproject function for reprojecting shapefiles
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
from unittest.mock import patch, Mock


def test_shp_reproject_imports():
    '''Test that shp_reproject imports shutil (verifies fix).'''
    # This verifies the fix: added 'import shutil'
    from iwfm.gis.shp_reproject import shutil

    assert shutil is not None
    assert hasattr(shutil, 'copyfile')


@patch('iwfm.gis.shp_reproject.ogr')
@patch('iwfm.gis.shp_reproject.osr')
@patch('iwfm.gis.shp_reproject.shutil')
def test_shp_reproject_basic(mock_shutil, mock_osr, mock_ogr, tmp_path):
    '''Test basic functionality of shp_reproject.'''
    from iwfm.gis.shp_reproject import shp_reproject

    # Create mocks
    mock_driver = Mock()
    mock_ogr.GetDriverByName.return_value = mock_driver

    mock_src_ds = Mock()
    mock_src_layer = Mock()
    mock_src_layer.GetName.return_value = 'layer'
    mock_src_layer.GetLayerDefn.return_value = Mock()
    mock_src_ds.GetLayer.return_value = mock_src_layer

    mock_driver.Open.return_value = mock_src_ds
    mock_driver.CreateDataSource.return_value = Mock()

    source = tmp_path / 'input.shp'
    target = tmp_path / 'output.shp'

    source.write_text('dummy')

    shp_reproject(str(source), str(target), 4326, 32610)

    mock_shutil.copyfile.assert_called()


def test_shp_reproject_function_signature():
    '''Test that shp_reproject has correct function signature.'''
    from iwfm.gis.shp_reproject import shp_reproject
    import inspect

    sig = inspect.signature(shp_reproject)
    params = list(sig.parameters.keys())

    assert 'source' in params
    assert 'target' in params
    assert 'epsg_from' in params
    assert 'epsg_to' in params
