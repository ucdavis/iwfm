# test_gis_stretch.py 
# Test gis/stretch function for histogram stretching
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
import numpy as np


def test_stretch_imports():
    '''Test that stretch imports operator (verifies fix).'''
    # This verifies the fix: added 'import operator'
    from iwfm.gis.stretch import operator

    assert operator is not None
    assert hasattr(operator, 'add')


def test_stretch_import_cleanup():
    '''Test that stretch has clean imports (verifies redundant import fixes).'''
    from iwfm.gis import stretch
    import inspect

    source = inspect.getsource(stretch)
    # Should have clean imports
    assert 'import iwfm' in source
    assert 'from osgeo import gdal_array' in source


@patch('iwfm.gis.stretch.gdal_array')
def test_stretch_basic(mock_gdal, tmp_path):
    '''Test basic functionality of stretch.'''
    from iwfm.gis.stretch import stretch

    # Create mock array
    mock_array = np.array([[0, 50, 100], [150, 200, 255]], dtype=np.uint8)
    mock_gdal.LoadFile.return_value = mock_array
    mock_gdal.SaveArray = Mock()

    source = tmp_path / 'input.tif'
    target = tmp_path / 'output.tif'

    source.write_text('dummy')

    stretch(str(source), str(target))

    mock_gdal.LoadFile.assert_called_once()


def test_stretch_function_signature():
    '''Test that stretch has correct function signature.'''
    from iwfm.gis.stretch import stretch
    import inspect

    sig = inspect.signature(stretch)
    params = list(sig.parameters.keys())

    assert 'source' in params
    assert 'target' in params
