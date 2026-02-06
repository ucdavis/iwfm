# test_gis_choropleth.py
# Test gis/choropleth function
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
from pathlib import Path
import sys
import importlib.util


def _import_choropleth_directly():
    '''Import choropleth module directly bypassing iwfm.gis.__init__.py'''
    choropleth_path = Path(__file__).parent.parent / 'iwfm' / 'gis' / 'choropleth.py'
    world2screen_path = Path(__file__).parent.parent / 'iwfm' / 'gis' / 'world2screen.py'

    # Import world2screen first
    spec_w2s = importlib.util.spec_from_file_location("world2screen_module", world2screen_path)
    module_w2s = importlib.util.module_from_spec(spec_w2s)
    sys.modules['world2screen_module'] = module_w2s
    spec_w2s.loader.exec_module(module_w2s)

    # Create mock iwfm.gis module
    if 'iwfm' not in sys.modules:
        sys.modules['iwfm'] = type(sys)('iwfm')
    if 'iwfm.gis' not in sys.modules:
        sys.modules['iwfm.gis'] = type(sys)('iwfm.gis')
    sys.modules['iwfm'].gis = sys.modules['iwfm.gis']
    sys.modules['iwfm.gis'].world2screen = module_w2s.world2screen

    # Now import choropleth
    spec = importlib.util.spec_from_file_location("choropleth_module", choropleth_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules['choropleth_module'] = module
    spec.loader.exec_module(module)
    return module


def test_choropleth_imports():
    '''Test that choropleth imports are clean (verifies fix).'''
    choropleth_path = Path(__file__).parent.parent / 'iwfm' / 'gis' / 'choropleth.py'
    source = choropleth_path.read_text()

    # Should use direct import, not 'import iwfm' or 'import iwfm as iwfm'
    assert 'import iwfm as iwfm' not in source
    assert 'from iwfm.gis.world2screen import world2screen' in source
    # ImageOps should not be imported (unused)
    assert 'ImageOps' not in source


def test_choropleth_spelling():
    '''Test that choropleth spelling is correct (verifies fix).'''
    choropleth_path = Path(__file__).parent.parent / 'iwfm' / 'gis' / 'choropleth.py'
    source = choropleth_path.read_text()

    # Should be "choropleth" not "chloropleth"
    assert 'chloropleth' not in source.lower()


def test_choropleth_error_handling_field_not_found():
    '''Test that choropleth raises error when field not found (verifies fix).'''
    module = _import_choropleth_directly()
    choropleth = module.choropleth

    # Mock shapefile reader
    mock_reader = Mock()
    mock_reader.fields = [
        ['DeletionFlag', 'C', 1, 0],  # Standard deletion flag
        ['Field1', 'N', 10, 2],
        ['Field2', 'N', 10, 2],
    ]
    mock_reader.bbox = [0, 0, 100, 100]
    mock_reader.shapeRecords.return_value = []

    with patch('choropleth_module.shapefile.Reader', return_value=mock_reader):
        # Test missing fieldname1
        with pytest.raises(ValueError, match="Field 'NonexistentField' not found"):
            choropleth('test.shp', 'NonexistentField', 'Field2')

        # Test missing fieldname2
        with pytest.raises(ValueError, match="Field 'MissingField' not found"):
            choropleth('test.shp', 'Field1', 'MissingField')


def test_choropleth_division_by_zero_handling():
    '''Test that choropleth handles division by zero (verifies fix).'''
    module = _import_choropleth_directly()
    choropleth = module.choropleth

    # Mock shapefile reader
    mock_reader = Mock()
    mock_reader.fields = [
        ['DeletionFlag', 'C', 1, 0],
        ['Field1', 'N', 10, 2],
        ['Field2', 'N', 10, 2],
    ]
    mock_reader.bbox = [0, 0, 100, 100]

    # Create mock shape record with zero in Field2
    mock_shape = Mock()
    mock_shape.record = [10.0, 0.0]  # Field1=10, Field2=0
    mock_shape.shape.points = [(10, 10), (20, 10), (20, 20), (10, 20)]

    mock_reader.shapeRecords.return_value = [mock_shape]

    with patch('choropleth_module.shapefile.Reader', return_value=mock_reader):
        with patch('iwfm.gis.world2screen', return_value=(50, 50)):
            # Should not raise ZeroDivisionError, should skip the shape
            try:
                choropleth('test.shp', 'Field1', 'Field2')
            except ZeroDivisionError:
                pytest.fail("Division by zero not handled properly")


def test_choropleth_basic(tmp_path):
    '''Test basic functionality of choropleth.'''
    module = _import_choropleth_directly()
    choropleth = module.choropleth

    # Mock shapefile reader
    mock_reader = Mock()
    mock_reader.fields = [
        ['DeletionFlag', 'C', 1, 0],
        ['Population', 'N', 10, 2],
        ['Area', 'N', 10, 2],
    ]
    mock_reader.bbox = [0, 0, 100, 100]

    # Create mock shape record
    mock_shape = Mock()
    mock_shape.record = [1000.0, 100.0]  # Population=1000, Area=100, density=10
    mock_shape.shape.points = [(10, 10), (20, 10), (20, 20), (10, 20)]

    mock_reader.shapeRecords.return_value = [mock_shape]

    output_file = tmp_path / 'test_choropleth.png'

    with patch('choropleth_module.shapefile.Reader', return_value=mock_reader):
        with patch('iwfm.gis.world2screen', return_value=(50, 50)):
            # Should not raise any errors
            choropleth('test.shp', 'Population', 'Area', savename=str(output_file))

    # Verify file was created
    assert output_file.exists()


def test_choropleth_no_save():
    '''Test choropleth without saving (savename=None).'''
    module = _import_choropleth_directly()
    choropleth = module.choropleth

    # Mock shapefile reader
    mock_reader = Mock()
    mock_reader.fields = [
        ['DeletionFlag', 'C', 1, 0],
        ['Value1', 'N', 10, 2],
        ['Value2', 'N', 10, 2],
    ]
    mock_reader.bbox = [0, 0, 100, 100]

    mock_shape = Mock()
    mock_shape.record = [50.0, 10.0]
    mock_shape.shape.points = [(0, 0), (10, 0), (10, 10), (0, 10)]

    mock_reader.shapeRecords.return_value = [mock_shape]

    with patch('choropleth_module.shapefile.Reader', return_value=mock_reader):
        with patch('iwfm.gis.world2screen', return_value=(50, 50)):
            # Should not raise any errors and not save
            choropleth('test.shp', 'Value1', 'Value2', savename=None)


def test_choropleth_function_signature():
    '''Test that choropleth has correct function signature.'''
    module = _import_choropleth_directly()
    choropleth = module.choropleth
    import inspect

    sig = inspect.signature(choropleth)
    params = list(sig.parameters.keys())

    assert 'infile' in params
    assert 'fieldname1' in params
    assert 'fieldname2' in params
    assert 'iwidth' in params
    assert 'iheight' in params
    assert 'denrat' in params
    assert 'savename' in params

    # Check defaults
    assert sig.parameters['iwidth'].default == 600
    assert sig.parameters['iheight'].default == 400
    assert sig.parameters['denrat'].default == 80.0
    assert sig.parameters['savename'].default is None
