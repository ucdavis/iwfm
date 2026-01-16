# test_gis_las2dem.py 
# Test gis/las2dem function for converting LAS to DEM
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
from unittest.mock import Mock, patch, MagicMock
import numpy as np


def test_las2dem_imports_file():
    '''Test that las2dem imports File from laspy (verifies fix).'''
    # This verifies the fix: added 'from laspy.file import File'
    from iwfm.gis.las2dem import File

    assert File is not None


@patch('iwfm.gis.las2dem.File')
def test_las2dem_basic(mock_file_class, tmp_path):
    '''Test basic functionality of las2dem.'''
    from iwfm.gis.las2dem import las2dem

    # Create mock LAS file object
    mock_las = Mock()
    mock_las.header.min = [0.0, 0.0, 0.0]
    mock_las.header.max = [100.0, 100.0, 10.0]
    mock_las.x = np.array([10.0, 20.0, 30.0])
    mock_las.y = np.array([10.0, 20.0, 30.0])
    mock_las.z = np.array([5.0, 6.0, 7.0])

    mock_file_class.return_value = mock_las

    source = tmp_path / 'test.las'
    target = tmp_path / 'test.asc'

    source.write_text('dummy')

    las2dem(str(source), str(target), cell=1.0)

    assert target.exists()
    mock_file_class.assert_called_once()


@patch('iwfm.gis.las2dem.File')
def test_las2dem_adds_extension(mock_file_class, tmp_path):
    '''Test that las2dem adds .las and .asc extensions.'''
    from iwfm.gis.las2dem import las2dem

    mock_las = Mock()
    mock_las.header.min = [0.0, 0.0, 0.0]
    mock_las.header.max = [10.0, 10.0, 1.0]
    mock_las.x = np.array([5.0])
    mock_las.y = np.array([5.0])
    mock_las.z = np.array([1.0])

    mock_file_class.return_value = mock_las

    source = tmp_path / 'test'
    target = tmp_path / 'output'

    # Function should add .las to source and .asc to target
    las2dem(str(source), str(target))

    # Verify File was called with .las extension
    call_args = mock_file_class.call_args[0][0]
    assert call_args.endswith('.las')


@patch('iwfm.gis.las2dem.File')
def test_las2dem_custom_cell_size(mock_file_class, tmp_path):
    '''Test las2dem with custom cell size.'''
    from iwfm.gis.las2dem import las2dem

    mock_las = Mock()
    mock_las.header.min = [0.0, 0.0, 0.0]
    mock_las.header.max = [100.0, 100.0, 10.0]
    mock_las.x = np.array([10.0, 20.0])
    mock_las.y = np.array([10.0, 20.0])
    mock_las.z = np.array([5.0, 6.0])

    mock_file_class.return_value = mock_las

    source = tmp_path / 'test.las'
    target = tmp_path / 'test.asc'

    las2dem(str(source), str(target), cell=5.0, NODATA=-9999)

    assert target.exists()
    content = target.read_text()
    assert 'cellsize     5.0' in content
    assert 'NODATA_value      -9999' in content


def test_las2dem_function_signature():
    '''Test that las2dem has correct function signature.'''
    from iwfm.gis.las2dem import las2dem
    import inspect

    sig = inspect.signature(las2dem)
    params = list(sig.parameters.keys())

    assert 'source' in params
    assert 'target' in params
    assert 'cell' in params
    assert 'NODATA' in params
