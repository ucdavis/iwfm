# test_gis_shp_to_utm_pts.py 
# Test gis/shp_to_utm_pts function for reprojecting shapefiles
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


def test_shp_to_utm_pts_imports():
    '''Test that shp_to_utm_pts imports urlopen and utm (verifies fixes).'''
    # This verifies the fixes: added 'from urllib.request import urlopen'
    # and changed 'import utm as utm' to 'import utm'
    from iwfm.gis.shp_to_utm_pts import urlopen, utm

    assert urlopen is not None
    assert utm is not None
    assert hasattr(utm, 'from_latlon')


def test_shp_to_utm_pts_import_cleanup():
    '''Test that imports are clean (verifies redundant import fix).'''
    from iwfm.gis import shp_to_utm_pts
    import inspect

    source = inspect.getsource(shp_to_utm_pts)
    # Should have 'import utm' not 'import utm as utm'
    assert 'import utm' in source


@patch('iwfm.gis.shp_to_utm_pts.urlopen')
@patch('iwfm.gis.shp_to_utm_pts.utm')
@patch('iwfm.gis.shp_to_utm_pts.shapefile')
def test_shp_to_utm_pts_basic(mock_shapefile, mock_utm, mock_urlopen, tmp_path):
    '''Test basic functionality of shp_to_utm_pts.'''
    from iwfm.gis.shp_to_utm_pts import shp_to_utm_pts

    # Create mock shape
    mock_shape = Mock()
    mock_shape.shapeType = 1  # Point
    mock_shape.fields = [['DeletionFlag'], ['ID', 'N', 10, 0], ['NAME', 'C', 50, 0]]

    mock_record = Mock()
    mock_record.record = ['001', 'Test']

    mock_shape_obj = Mock()
    mock_shape_obj.points = [(-120.5, 38.5)]

    mock_shape.iterShapeRecords.return_value = [mock_record]
    mock_shape.iterShapes.return_value = [mock_shape_obj]

    # Mock UTM conversion
    mock_utm.from_latlon.return_value = (500000.0, 4000000.0, 10, 'N')

    # Mock urlopen
    mock_prj = Mock()
    mock_prj.read.return_value = b'PROJCS["UTM Zone 10N"]'
    mock_urlopen.return_value = mock_prj

    # Mock writer
    mock_writer = MagicMock()
    mock_shapefile.Writer.return_value.__enter__.return_value = mock_writer

    outfile = tmp_path / 'output.shp'

    shp_to_utm_pts(mock_shape, str(outfile), verbose=False)

    mock_writer.point.assert_called()


@patch('iwfm.gis.shp_to_utm_pts.urlopen')
@patch('iwfm.gis.shp_to_utm_pts.utm')
@patch('iwfm.gis.shp_to_utm_pts.shapefile')
def test_shp_to_utm_pts_verbose(mock_shapefile, mock_utm, mock_urlopen, tmp_path, capsys):
    '''Test shp_to_utm_pts with verbose output.'''
    from iwfm.gis.shp_to_utm_pts import shp_to_utm_pts

    mock_shape = Mock()
    mock_shape.shapeType = 1
    mock_shape.fields = [['DeletionFlag'], ['ID', 'N', 10, 0]]
    mock_shape.iterShapeRecords.return_value = []
    mock_shape.iterShapes.return_value = []

    mock_utm.from_latlon.return_value = (500000.0, 4000000.0, 10, 'N')

    mock_prj = Mock()
    mock_prj.read.return_value = b'PROJCS["UTM"]'
    mock_urlopen.return_value = mock_prj

    mock_writer = MagicMock()
    mock_shapefile.Writer.return_value.__enter__.return_value = mock_writer

    outfile = tmp_path / 'output.shp'

    shp_to_utm_pts(mock_shape, str(outfile), verbose=True)

    captured = capsys.readouterr()
    assert 'Wrote' in captured.out


def test_shp_to_utm_pts_function_signature():
    '''Test that shp_to_utm_pts has correct function signature.'''
    from iwfm.gis.shp_to_utm_pts import shp_to_utm_pts
    import inspect

    sig = inspect.signature(shp_to_utm_pts)
    params = list(sig.parameters.keys())

    assert 'shape' in params
    assert 'outfile' in params
    assert 'verbose' in params
