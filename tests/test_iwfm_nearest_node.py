# test_iwfm_nearest_node.py
# Tests for iwfm_nearest_node function
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

"""
Tests for iwfm.iwfm_nearest_node function.

The iwfm_nearest_node function takes an (x, y) location and a node set,
and returns the nearest IWFM node and the distance to it.

Example files used for testing:
- Node file: iwfm/tests/C2VSimCG-2021/Preprocessor/C2VSimCG_Nodes.dat

C2VSimCG model characteristics:
- 1,393 nodes
- Factor: 3.2808 (feet to meters conversion)

Parameters:
- point: [x, y] values of a point
- node_set: list of [node_id, x, y] for each node

Returns:
- nearest_node: [node_id, x, y] of the nearest node
- nearest_distance: distance between point and nearest node
"""

import pytest
import os
import sys
import inspect
import math

# Add the iwfm directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from iwfm.iwfm_nearest_node import iwfm_nearest_node

# Path to example files
EXAMPLE_NODE_FILE = os.path.join(
    os.path.dirname(__file__),
    'C2VSimCG-2021', 'Preprocessor', 'C2VSimCG_Nodes.dat'
)

# Check if example files exist
EXAMPLE_FILES_EXIST = os.path.exists(EXAMPLE_NODE_FILE)


class TestIwfmNearestNodeFunctionExists:
    """Test that iwfm_nearest_node function exists and has correct signature."""

    def test_function_exists(self):
        """Test that iwfm_nearest_node function is importable."""
        assert iwfm_nearest_node is not None

    def test_function_is_callable(self):
        """Test that iwfm_nearest_node is callable."""
        assert callable(iwfm_nearest_node)

    def test_function_has_docstring(self):
        """Test that iwfm_nearest_node has a docstring."""
        assert iwfm_nearest_node.__doc__ is not None
        assert len(iwfm_nearest_node.__doc__) > 0

    def test_function_signature(self):
        """Test that iwfm_nearest_node has the expected parameters."""
        sig = inspect.signature(iwfm_nearest_node)
        params = list(sig.parameters.keys())

        assert 'point' in params
        assert 'node_set' in params


class TestIwfmNearestNodeReturnValue:
    """Test the return value structure of iwfm_nearest_node."""

    def test_returns_two_values(self):
        """Test that iwfm_nearest_node returns two values."""
        node_set = [[1, 0.0, 0.0], [2, 10.0, 0.0]]
        point = [5.0, 0.0]

        result = iwfm_nearest_node(point, node_set)

        assert len(result) == 2

    def test_returns_node_and_distance(self):
        """Test that returns node info and distance."""
        node_set = [[1, 0.0, 0.0], [2, 10.0, 0.0]]
        point = [5.0, 0.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # nearest_node should be a list with node info
        assert isinstance(nearest_node, list)
        # nearest_distance should be a number
        assert isinstance(nearest_distance, (int, float))

    def test_returns_node_with_id_x_y(self):
        """Test that returned node has id, x, y."""
        node_set = [[1, 0.0, 0.0], [2, 10.0, 0.0]]
        point = [5.0, 0.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # Node should have at least 3 elements: id, x, y
        assert len(nearest_node) >= 3


class TestIwfmNearestNodeSingleNode:
    """Test iwfm_nearest_node with single node."""

    def test_single_node_returned(self):
        """Test with single node in set."""
        node_set = [[1, 100.0, 200.0]]
        point = [150.0, 250.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_node[0] == 1
        assert nearest_node[1] == 100.0
        assert nearest_node[2] == 200.0

    def test_single_node_distance(self):
        """Test distance calculation with single node."""
        node_set = [[1, 0.0, 0.0]]
        point = [3.0, 4.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # Distance should be 5 (3-4-5 triangle)
        assert nearest_distance == pytest.approx(5.0, abs=0.0001)


class TestIwfmNearestNodeBasicCases:
    """Test basic cases for iwfm_nearest_node."""

    def test_point_on_node(self):
        """Test when point is exactly on a node."""
        node_set = [[1, 100.0, 200.0], [2, 300.0, 400.0]]
        point = [100.0, 200.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_node[0] == 1
        assert nearest_distance == 0.0

    def test_finds_nearest_of_two(self):
        """Test finding nearest of two nodes."""
        node_set = [[1, 0.0, 0.0], [2, 100.0, 0.0]]
        point = [30.0, 0.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # Point is closer to node 1 (distance 30 vs 70)
        assert nearest_node[0] == 1
        assert nearest_distance == pytest.approx(30.0, abs=0.0001)

    def test_finds_nearest_of_multiple(self):
        """Test finding nearest of multiple nodes."""
        node_set = [
            [1, 0.0, 0.0],
            [2, 100.0, 0.0],
            [3, 50.0, 50.0],
            [4, 200.0, 200.0]
        ]
        point = [45.0, 45.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # Point is closest to node 3 at (50, 50)
        assert nearest_node[0] == 3

    def test_equidistant_nodes(self):
        """Test when two nodes are equidistant - returns first found."""
        node_set = [[1, 0.0, 0.0], [2, 10.0, 0.0]]
        point = [5.0, 0.0]  # Equidistant from both

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # Both nodes are 5 units away, should return node 1 (first found)
        assert nearest_node[0] == 1
        assert nearest_distance == pytest.approx(5.0, abs=0.0001)


class TestIwfmNearestNodeDistanceCalculation:
    """Test distance calculation in iwfm_nearest_node."""

    def test_distance_horizontal(self):
        """Test distance calculation for horizontal separation."""
        node_set = [[1, 0.0, 0.0]]
        point = [100.0, 0.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_distance == pytest.approx(100.0, abs=0.0001)

    def test_distance_vertical(self):
        """Test distance calculation for vertical separation."""
        node_set = [[1, 0.0, 0.0]]
        point = [0.0, 100.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_distance == pytest.approx(100.0, abs=0.0001)

    def test_distance_diagonal(self):
        """Test distance calculation for diagonal separation."""
        node_set = [[1, 0.0, 0.0]]
        point = [100.0, 100.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # Distance should be sqrt(100^2 + 100^2) = sqrt(20000) ≈ 141.42
        expected = math.sqrt(20000)
        assert nearest_distance == pytest.approx(expected, abs=0.0001)

    def test_distance_3_4_5_triangle(self):
        """Test distance calculation for 3-4-5 triangle."""
        node_set = [[1, 0.0, 0.0]]
        point = [3.0, 4.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_distance == pytest.approx(5.0, abs=0.0001)

    def test_distance_large_coordinates(self):
        """Test distance calculation with large coordinates."""
        node_set = [[1, 550000.0, 4400000.0]]
        point = [550003.0, 4400004.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # 3-4-5 triangle, distance should be 5
        assert nearest_distance == pytest.approx(5.0, abs=0.0001)


class TestIwfmNearestNodeNegativeCoordinates:
    """Test iwfm_nearest_node with negative coordinates."""

    def test_negative_node_coordinates(self):
        """Test with negative node coordinates."""
        node_set = [[1, -100.0, -200.0], [2, 100.0, 200.0]]
        point = [-90.0, -190.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # Point is closer to node 1
        assert nearest_node[0] == 1

    def test_negative_point_coordinates(self):
        """Test with negative point coordinates."""
        node_set = [[1, 0.0, 0.0], [2, 100.0, 100.0]]
        point = [-10.0, -10.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # Point is closer to node 1
        assert nearest_node[0] == 1

    def test_distance_across_origin(self):
        """Test distance calculation across origin."""
        node_set = [[1, -3.0, 0.0]]
        point = [4.0, 0.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        # Distance should be 7
        assert nearest_distance == pytest.approx(7.0, abs=0.0001)


class TestIwfmNearestNodeGridPattern:
    """Test iwfm_nearest_node with grid pattern of nodes."""

    def test_center_of_grid(self):
        """Test finding nearest node when point is in center of grid."""
        # 3x3 grid of nodes
        node_set = [
            [1, 0.0, 0.0], [2, 50.0, 0.0], [3, 100.0, 0.0],
            [4, 0.0, 50.0], [5, 50.0, 50.0], [6, 100.0, 50.0],
            [7, 0.0, 100.0], [8, 50.0, 100.0], [9, 100.0, 100.0]
        ]
        point = [50.0, 50.0]  # Exactly on node 5

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_node[0] == 5
        assert nearest_distance == 0.0

    def test_between_grid_nodes(self):
        """Test finding nearest node when point is between grid nodes."""
        # 2x2 grid of nodes
        node_set = [
            [1, 0.0, 0.0], [2, 100.0, 0.0],
            [3, 0.0, 100.0], [4, 100.0, 100.0]
        ]
        point = [25.0, 25.0]  # Closer to node 1

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_node[0] == 1

    def test_corner_of_grid(self):
        """Test point outside grid corner."""
        node_set = [
            [1, 0.0, 0.0], [2, 100.0, 0.0],
            [3, 0.0, 100.0], [4, 100.0, 100.0]
        ]
        point = [-10.0, -10.0]  # Outside, closest to node 1

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_node[0] == 1


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST,
                    reason="Example node file not available")
class TestIwfmNearestNodeWithC2VSimCG:
    """Test iwfm_nearest_node with real C2VSimCG node data."""

    @pytest.fixture
    def c2vsimcg_nodes(self):
        """Load C2VSimCG node coordinates."""
        import iwfm
        node_coords, node_list, factor = iwfm.iwfm_read_nodes(EXAMPLE_NODE_FILE)
        return node_coords

    def test_finds_node_within_model(self, c2vsimcg_nodes):
        """Test finding nearest node for point within model domain."""
        # Point somewhere in the Central Valley
        point = [560000.0, 4200000.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, c2vsimcg_nodes)

        # Should find a valid node
        assert nearest_node[0] > 0
        assert nearest_node[0] <= 1393
        # Distance should be reasonable (less than typical element size)
        assert nearest_distance < 50000

    def test_finds_node_outside_model(self, c2vsimcg_nodes):
        """Test finding nearest node for point outside model domain."""
        # Point far outside the model
        point = [0.0, 0.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, c2vsimcg_nodes)

        # Should still find a node
        assert nearest_node[0] > 0
        assert nearest_node[0] <= 1393
        # Distance should be large
        assert nearest_distance > 100000

    def test_point_on_existing_node(self, c2vsimcg_nodes):
        """Test when point is exactly on an existing node."""
        # Use coordinates of node 1
        node_1 = c2vsimcg_nodes[0]
        point = [node_1[1], node_1[2]]

        nearest_node, nearest_distance = iwfm_nearest_node(point, c2vsimcg_nodes)

        # Should return node 1 with zero distance
        assert nearest_node[0] == 1
        assert nearest_distance == pytest.approx(0.0, abs=0.0001)

    def test_consistent_results(self, c2vsimcg_nodes):
        """Test that results are consistent for same input."""
        point = [560000.0, 4200000.0]

        result1 = iwfm_nearest_node(point, c2vsimcg_nodes)
        result2 = iwfm_nearest_node(point, c2vsimcg_nodes)

        assert result1[0][0] == result2[0][0]  # Same node ID
        assert result1[1] == result2[1]  # Same distance

    def test_different_points_different_nodes(self, c2vsimcg_nodes):
        """Test that different points can return different nodes."""
        point1 = [550000.0, 4500000.0]  # Northern part
        point2 = [650000.0, 3900000.0]  # Southern part

        nearest1, _ = iwfm_nearest_node(point1, c2vsimcg_nodes)
        nearest2, _ = iwfm_nearest_node(point2, c2vsimcg_nodes)

        # Different regions should find different nearest nodes
        assert nearest1[0] != nearest2[0]


class TestIwfmNearestNodeEdgeCases:
    """Test edge cases for iwfm_nearest_node."""

    def test_very_small_distance(self):
        """Test with very small distance."""
        node_set = [[1, 0.0, 0.0]]
        point = [0.0001, 0.0001]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_distance < 0.001

    def test_very_large_distance(self):
        """Test with very large distance."""
        node_set = [[1, 0.0, 0.0]]
        point = [1000000.0, 1000000.0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        expected = math.sqrt(2 * 1000000.0**2)
        assert nearest_distance == pytest.approx(expected, abs=1.0)

    def test_string_coordinates(self):
        """Test that string coordinates are handled (converted to float)."""
        node_set = [[1, '100.0', '200.0']]
        point = ['100.0', '200.0']

        # Should work because function converts to float
        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_distance == pytest.approx(0.0, abs=0.0001)

    def test_integer_coordinates(self):
        """Test with integer coordinates."""
        node_set = [[1, 0, 0], [2, 100, 0]]
        point = [30, 0]

        nearest_node, nearest_distance = iwfm_nearest_node(point, node_set)

        assert nearest_node[0] == 1
        assert nearest_distance == pytest.approx(30.0, abs=0.0001)
