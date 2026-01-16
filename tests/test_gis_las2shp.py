# test_gis_las2shp.py 
# Test gis/las2shp function for converting LAS to shapefile
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
from unittest.mock import Mock, patch
import numpy as np


def test_las2shp_imports():
    '''Test that las2shp imports math, time, and File (verifies fixes).'''
    # This verifies the fixes: added 'import math', 'import time', 'from laspy.file import File'
    from iwfm.gis.las2shp import math, time, File

    assert math is not None
    assert time is not None
    assert File is not None
    assert hasattr(math, 'sqrt')
    assert hasattr(time, 'asctime')


def test_las2shp_typo_fix():
    '''Test that las2shp has typo fix in print statement (verifies fix).'''
    # This verifies the fix: changed '{x1},{x2},{x3}' to '{x1},{y1},{z1}'
    from iwfm.gis import las2shp
    import inspect

    source = inspect.getsource(las2shp)
    # The fixed line should have y1, z1
    assert '{x1},{y1},{z1}' in source or 'x1,y1,z1' in source


@patch('iwfm.gis.las2shp.File')
@patch('iwfm.gis.las2shp.shapefile')
@patch('iwfm.gis.las2shp.Delaunay')
def test_las2shp_basic(mock_delaunay, mock_shapefile, mock_file_class, tmp_path):
    '''Test basic functionality of las2shp.'''
    from iwfm.gis.las2shp import las2shp

    # Create mock LAS file
    mock_las = Mock()
    mock_las.x = np.array([0.0, 1.0, 2.0])
    mock_las.y = np.array([0.0, 1.0, 0.0])
    mock_las.z = np.array([0.0, 0.0, 0.0])

    mock_file_class.return_value = mock_las

    # Create mock triangulation
    mock_tri = Mock()
    mock_tri.simplices = np.array([[0, 1, 2]])
    mock_delaunay.return_value = mock_tri

    # Mock shapefile writer
    mock_writer = Mock()
    mock_shapefile.Writer.return_value = mock_writer
    mock_shapefile.POLYGONZ = 15

    source = tmp_path / 'test.las'
    target = tmp_path / 'test.shp'

    source.write_text('dummy')

    las2shp(str(source), str(target), verbose=0)

    mock_file_class.assert_called_once()


def test_las2shp_function_signature():
    '''Test that las2shp has correct function signature.'''
    from iwfm.gis.las2shp import las2shp
    import inspect

    sig = inspect.signature(las2shp)
    params = list(sig.parameters.keys())

    assert 'source' in params
    assert 'target' in params
    assert 'verbose' in params


@patch('iwfm.gis.las2shp.File')
def test_las2shp_uses_file_not_builtin(mock_file_class):
    '''Test that las2shp uses laspy.file.File not built-in file (verifies fix).'''
    from iwfm.gis import las2shp
    import inspect

    source = inspect.getsource(las2shp)
    # Should use File() not file()
    assert 'File(source' in source
