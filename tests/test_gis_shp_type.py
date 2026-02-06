# test_gis_shp_type.py 
# Test gis/shp_type function for returning shapefile type
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


from unittest.mock import Mock
import iwfm.gis


def test_shp_type_with_point_shapefile():
    '''Test shp_type with point shapefile.'''
    # Create a mock shapefile object
    mock_shp = Mock()
    mock_shp.shapeType = 1  # POINT type

    result = iwfm.gis.shp_type(mock_shp)

    assert result == 1


def test_shp_type_with_polyline_shapefile():
    '''Test shp_type with polyline shapefile.'''
    mock_shp = Mock()
    mock_shp.shapeType = 3  # POLYLINE type

    result = iwfm.gis.shp_type(mock_shp)

    assert result == 3


def test_shp_type_with_polygon_shapefile():
    '''Test shp_type with polygon shapefile.'''
    mock_shp = Mock()
    mock_shp.shapeType = 5  # POLYGON type

    result = iwfm.gis.shp_type(mock_shp)

    assert result == 5


def test_shp_type_typo_fix():
    '''Test that shp_type uses correct variable name (verifies typo fix).'''
    # This verifies the fix: changed 'sho.shapeType' to 'shp.shapeType'
    from iwfm.gis.shp_type import shp_type
    import inspect

    source = inspect.getsource(shp_type)
    assert 'shp.shapeType' in source
    assert 'sho.shapeType' not in source


def test_shp_type_function_signature():
    '''Test that shp_type has correct function signature.'''
    from iwfm.gis.shp_type import shp_type
    import inspect

    sig = inspect.signature(shp_type)
    params = list(sig.parameters.keys())

    assert 'shp' in params
    assert len(params) == 1
