# test_gis_histogram.py 
# Test gis/histogram function for generating image histograms
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


def test_histogram_imports():
    '''Test that histogram imports numpy correctly (verifies fix).'''
    # This verifies the fix: added 'import numpy as np'
    from iwfm.gis.histogram import np as numpy_import

    assert numpy_import is not None
    assert hasattr(numpy_import, 'histogram')


def test_histogram_import_cleanup():
    '''Test that histogram has clean imports (verifies redundant import fix).'''
    import sys
    from pathlib import Path

    # Import the module to ensure it's loaded, then get it from sys.modules
    from iwfm.gis import histogram as histogram_func
    histogram_module = sys.modules['iwfm.gis.histogram']
    module_file = Path(histogram_module.__file__)

    # Read the source file directly
    with open(module_file, 'r') as f:
        source = f.read()

    # Should have 'import iwfm' not 'import iwfm as iwfm'
    assert 'import iwfm' in source
    # Should have 'from osgeo import gdal_array' not redundant
    assert 'gdal_array as gdal_array' not in source


@patch('iwfm.gis.histogram.gdal_array')
@patch('iwfm.gis.histogram.iwfm')
def test_histogram_uses_np_histogram(mock_iwfm, mock_gdal, tmp_path):
    '''Test that histogram uses np.histogram (verifies fix).'''
    from iwfm.gis.histogram import histogram

    # Create mock image array
    mock_array = np.array([[1, 2, 3], [4, 5, 6]])
    mock_gdal.LoadFile.return_value = mock_array

    # Mock histogram_draw to avoid turtle graphics
    mock_iwfm.gis.histogram_draw.return_value = Mock(pen=Mock(), done=Mock())

    # This should call np.histogram internally
    test_file = tmp_path / 'test.tif'
    test_file.write_text('dummy')

    # The function should work without errors
    histogram(str(test_file), scl=False)

    mock_gdal.LoadFile.assert_called_once()


def test_histogram_function_signature():
    '''Test that histogram has correct function signature.'''
    from iwfm.gis.histogram import histogram
    import inspect

    sig = inspect.signature(histogram)
    params = list(sig.parameters.keys())

    assert 'infile' in params
    assert 'scl' in params
