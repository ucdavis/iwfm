# test_gis_qgis_print_geometry.py 
# Test gis/qgis_print_geometry function
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


def test_qgis_print_geometry_imports():
    '''Test that qgis_print_geometry imports QgsWkbTypes (verifies fix).'''
    # This verifies the fix: added 'from qgis.core import QgsWkbTypes'
    from iwfm.gis.qgis_print_geometry import QgsWkbTypes

    assert QgsWkbTypes is not None


@patch('iwfm.gis.qgis_print_geometry.QgsWkbTypes')
def test_qgis_print_geometry_point(mock_wkb, capsys):
    '''Test qgis_print_geometry with point geometry.'''
    from iwfm.gis.qgis_print_geometry import qgis_print_geometry

    # Mock geometry object
    mock_geom = Mock()
    mock_geom.wkbType.return_value = 1
    mock_geom.type.return_value = 0  # PointGeometry
    mock_geom.asPoint.return_value = (100.0, 200.0)

    mock_wkb.isSingleType.return_value = True
    mock_wkb.PointGeometry = 0

    qgis_print_geometry(mock_geom)

    captured = capsys.readouterr()
    assert 'Point:' in captured.out


@patch('iwfm.gis.qgis_print_geometry.QgsWkbTypes')
def test_qgis_print_geometry_line(mock_wkb, capsys):
    '''Test qgis_print_geometry with line geometry.'''
    from iwfm.gis.qgis_print_geometry import qgis_print_geometry

    mock_geom = Mock()
    mock_geom.wkbType.return_value = 2
    mock_geom.type.return_value = 1  # LineGeometry
    mock_geom.asPolyline.return_value = [(0, 0), (1, 1)]
    mock_geom.length.return_value = 1.414

    mock_wkb.isSingleType.return_value = True
    mock_wkb.LineGeometry = 1

    qgis_print_geometry(mock_geom)

    captured = capsys.readouterr()
    assert 'Line:' in captured.out
    assert 'length:' in captured.out


@patch('iwfm.gis.qgis_print_geometry.QgsWkbTypes')
def test_qgis_print_geometry_polygon(mock_wkb, capsys):
    '''Test qgis_print_geometry with polygon geometry.'''
    from iwfm.gis.qgis_print_geometry import qgis_print_geometry

    mock_geom = Mock()
    mock_geom.wkbType.return_value = 3
    mock_geom.type.return_value = 2  # PolygonGeometry
    mock_geom.asPolygon.return_value = [[(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]]
    mock_geom.area.return_value = 1.0

    mock_wkb.isSingleType.return_value = True
    mock_wkb.PolygonGeometry = 2

    qgis_print_geometry(mock_geom)

    captured = capsys.readouterr()
    assert 'Polygon:' in captured.out
    assert 'Area:' in captured.out


@patch('iwfm.gis.qgis_print_geometry.QgsWkbTypes')
def test_qgis_print_geometry_multipoint(mock_wkb, capsys):
    '''Test qgis_print_geometry with multipoint geometry.'''
    from iwfm.gis.qgis_print_geometry import qgis_print_geometry

    mock_geom = Mock()
    mock_geom.wkbType.return_value = 4
    mock_geom.type.return_value = 0  # PointGeometry
    mock_geom.asMultiPoint.return_value = [(0, 0), (1, 1), (2, 2)]

    mock_wkb.isSingleType.return_value = False
    mock_wkb.PointGeometry = 0

    qgis_print_geometry(mock_geom)

    captured = capsys.readouterr()
    assert 'MultiPoint:' in captured.out


@patch('iwfm.gis.qgis_print_geometry.QgsWkbTypes')
def test_qgis_print_geometry_unknown(mock_wkb, capsys):
    '''Test qgis_print_geometry with unknown geometry type.'''
    from iwfm.gis.qgis_print_geometry import qgis_print_geometry

    mock_geom = Mock()
    mock_geom.wkbType.return_value = 999
    mock_geom.type.return_value = 999

    mock_wkb.isSingleType.return_value = True
    mock_wkb.PointGeometry = 0
    mock_wkb.LineGeometry = 1
    mock_wkb.PolygonGeometry = 2

    qgis_print_geometry(mock_geom)

    captured = capsys.readouterr()
    assert 'Unknown or invalid geometry' in captured.out


def test_qgis_print_geometry_function_signature():
    '''Test that qgis_print_geometry has correct function signature.'''
    from iwfm.gis.qgis_print_geometry import qgis_print_geometry
    import inspect

    sig = inspect.signature(qgis_print_geometry)
    params = list(sig.parameters.keys())

    assert 'geom' in params
    assert len(params) == 1
