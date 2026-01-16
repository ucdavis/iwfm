# test_nearest_node.py 
# Test nearest_node function for finding nearest IWFM node
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
import iwfm


def test_nearest_node_basic():
    '''Test basic functionality of nearest_node.'''
    point = (100.0, 200.0)
    node_set = [
        [1, 90.0, 190.0],   # Close to point
        [2, 150.0, 250.0],  # Far from point
        [3, 105.0, 205.0],  # Very close to point
    ]

    result = iwfm.nearest_node(point, node_set)

    # Node 3 should be nearest (distance ~7.07)
    assert result == 3


def test_nearest_node_exact_match():
    '''Test nearest_node when point exactly matches a node.'''
    point = (100.0, 200.0)
    node_set = [
        [1, 100.0, 200.0],  # Exact match
        [2, 150.0, 250.0],
    ]

    result = iwfm.nearest_node(point, node_set)

    assert result == 1


def test_nearest_node_single_node():
    '''Test nearest_node with single node.'''
    point = (100.0, 200.0)
    node_set = [
        [42, 150.0, 250.0],
    ]

    result = iwfm.nearest_node(point, node_set)

    assert result == 42


def test_nearest_node_multiple_nodes():
    '''Test nearest_node with many nodes.'''
    point = (100.0, 200.0)
    node_set = [
        [1, 200.0, 300.0],
        [2, 110.0, 210.0],
        [3, 300.0, 400.0],
        [4, 101.0, 201.0],  # Should be closest
        [5, 400.0, 500.0],
    ]

    result = iwfm.nearest_node(point, node_set)

    assert result == 4


def test_nearest_node_uses_iwfm_distance():
    '''Test that nearest_node uses iwfm.distance function.'''
    # Verifies that the function imports and uses iwfm properly
    point = (0.0, 0.0)
    node_set = [
        [1, 3.0, 4.0],  # Distance should be 5.0
    ]

    result = iwfm.nearest_node(point, node_set)

    assert result == 1


def test_nearest_node_negative_coordinates():
    '''Test nearest_node with negative coordinates.'''
    point = (-100.0, -200.0)
    node_set = [
        [1, -90.0, -190.0],
        [2, -150.0, -250.0],
        [3, -105.0, -205.0],
    ]

    result = iwfm.nearest_node(point, node_set)

    # Node 3 should be nearest
    assert result == 3


def test_nearest_node_import_iwfm():
    '''Test that nearest_node imports iwfm correctly (verifies redundant import fix).'''
    # This verifies the fix: changed 'import iwfm as iwfm' to 'import iwfm'
    from iwfm import nearest_node
    import inspect

    source = inspect.getsource(nearest_node)
    # Should contain 'import iwfm' not 'import iwfm as iwfm'
    assert 'import iwfm' in source
