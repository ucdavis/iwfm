# test_iwfm_nearest_nodes.py
# Tests for iwfm_nearest_nodes function
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
Tests for iwfm.iwfm_nearest_nodes function.

The iwfm_nearest_nodes function reads a CSV file with (x, y) locations,
finds the nearest IWFM node for each point, and writes results to an output file.

Example files used for testing:
- Node file: iwfm/tests/C2VSimCG-2021/Preprocessor/C2VSimCG_Nodes.dat

C2VSimCG model characteristics:
- 1,393 nodes
- Factor: 3.2808 (feet to meters conversion)

Input file format (CSV):
- Header: name,x,y
- Data rows: point_name,x_coord,y_coord

Output file format (CSV):
- Header: name,NdNear,NdDist
- Data rows: point_name,nearest_node_id,distance

Returns:
- Number of points processed
"""

import pytest
import os
import sys
import inspect
import tempfile

# Add the iwfm directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from iwfm.iwfm_nearest_nodes import iwfm_nearest_nodes

# Path to example files
EXAMPLE_NODE_FILE = os.path.join(
    os.path.dirname(__file__),
    'C2VSimCG-2021', 'Preprocessor', 'C2VSimCG_Nodes.dat'
)

# Check if example files exist
EXAMPLE_FILES_EXIST = os.path.exists(EXAMPLE_NODE_FILE)


class TestIwfmNearestNodesFunctionExists:
    """Test that iwfm_nearest_nodes function exists and has correct signature."""

    def test_function_exists(self):
        """Test that iwfm_nearest_nodes function is importable."""
        assert iwfm_nearest_nodes is not None

    def test_function_is_callable(self):
        """Test that iwfm_nearest_nodes is callable."""
        assert callable(iwfm_nearest_nodes)

    def test_function_has_docstring(self):
        """Test that iwfm_nearest_nodes has a docstring."""
        assert iwfm_nearest_nodes.__doc__ is not None
        assert len(iwfm_nearest_nodes.__doc__) > 0

    def test_function_signature(self):
        """Test that iwfm_nearest_nodes has the expected parameters."""
        sig = inspect.signature(iwfm_nearest_nodes)
        params = list(sig.parameters.keys())

        assert 'filename' in params
        assert 'node_set' in params


class TestIwfmNearestNodesReturnValue:
    """Test the return value of iwfm_nearest_nodes."""

    def test_returns_integer(self):
        """Test that iwfm_nearest_nodes returns an integer."""
        node_set = [[1, 0.0, 0.0], [2, 100.0, 100.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create input file
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,50.0,50.0\n')

            result = iwfm_nearest_nodes(input_file, node_set)

            assert isinstance(result, int)

    def test_returns_point_count(self):
        """Test that return value equals number of points processed."""
        node_set = [[1, 0.0, 0.0], [2, 100.0, 100.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,50.0,50.0\n')
                f.write('point2,75.0,75.0\n')
                f.write('point3,25.0,25.0\n')

            result = iwfm_nearest_nodes(input_file, node_set)

            assert result == 3


class TestIwfmNearestNodesOutputFile:
    """Test output file creation by iwfm_nearest_nodes."""

    def test_creates_output_file(self):
        """Test that iwfm_nearest_nodes creates an output file."""
        node_set = [[1, 0.0, 0.0], [2, 100.0, 100.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,50.0,50.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            # Output file should be created
            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            assert os.path.exists(output_file)

    def test_output_file_naming_convention(self):
        """Test that output file follows naming convention."""
        node_set = [[1, 0.0, 0.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'my_points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,50.0,50.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            # Output should be my_points_nearest_nodes.out
            output_file = os.path.join(temp_dir, 'my_points_nearest_nodes.out')
            assert os.path.exists(output_file)

    def test_output_file_not_empty(self):
        """Test that output file is not empty."""
        node_set = [[1, 0.0, 0.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,50.0,50.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            assert os.path.getsize(output_file) > 0


class TestIwfmNearestNodesOutputContent:
    """Test the content of output files created by iwfm_nearest_nodes."""

    def test_output_has_header(self):
        """Test that output file has correct header."""
        node_set = [[1, 0.0, 0.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,50.0,50.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                header = f.readline().strip()

            assert 'name' in header
            assert 'NdNear' in header
            assert 'NdDist' in header

    def test_output_has_correct_line_count(self):
        """Test that output file has correct number of lines."""
        node_set = [[1, 0.0, 0.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,50.0,50.0\n')
                f.write('point2,75.0,75.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            # 1 header + 2 data lines = 3 total
            assert len(lines) == 3

    def test_output_contains_point_names(self):
        """Test that output file preserves point names."""
        node_set = [[1, 0.0, 0.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('Well_A,50.0,50.0\n')
                f.write('Well_B,75.0,75.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                content = f.read()

            assert 'Well_A' in content
            assert 'Well_B' in content

    def test_output_contains_node_ids(self):
        """Test that output file contains node IDs."""
        node_set = [[1, 0.0, 0.0], [2, 100.0, 100.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,10.0,10.0\n')  # Closer to node 1

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            # Data line should contain node ID 1
            data_line = lines[1].strip().split(',')
            assert data_line[1] == '1'


class TestIwfmNearestNodesCalculation:
    """Test the nearest node calculation in iwfm_nearest_nodes."""

    def test_finds_correct_nearest_node(self):
        """Test that correct nearest node is found."""
        node_set = [
            [1, 0.0, 0.0],
            [2, 100.0, 0.0],
            [3, 0.0, 100.0],
            [4, 100.0, 100.0]
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,10.0,10.0\n')  # Closest to node 1
                f.write('point2,90.0,10.0\n')  # Closest to node 2
                f.write('point3,10.0,90.0\n')  # Closest to node 3
                f.write('point4,90.0,90.0\n')  # Closest to node 4

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            # Check each point found correct nearest node
            assert lines[1].split(',')[1] == '1'  # point1 -> node 1
            assert lines[2].split(',')[1] == '2'  # point2 -> node 2
            assert lines[3].split(',')[1] == '3'  # point3 -> node 3
            assert lines[4].split(',')[1] == '4'  # point4 -> node 4

    def test_calculates_correct_distance(self):
        """Test that distance is calculated correctly."""
        node_set = [[1, 0.0, 0.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,3.0,4.0\n')  # Distance should be 5 (3-4-5 triangle)

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            distance = float(lines[1].split(',')[2])
            assert distance == pytest.approx(5.0, abs=0.01)

    def test_point_on_node_zero_distance(self):
        """Test that point exactly on node has zero distance."""
        node_set = [[1, 100.0, 200.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,100.0,200.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            distance = float(lines[1].split(',')[2])
            assert distance == 0.0


class TestIwfmNearestNodesMultiplePoints:
    """Test iwfm_nearest_nodes with multiple points."""

    def test_processes_all_points(self):
        """Test that all points are processed."""
        node_set = [[1, 50.0, 50.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                for i in range(10):
                    f.write(f'point{i},{i*10},{i*10}\n')

            result = iwfm_nearest_nodes(input_file, node_set)

            assert result == 10

    def test_each_point_gets_result(self):
        """Test that each point has a result in output."""
        node_set = [[1, 50.0, 50.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('alpha,10.0,10.0\n')
                f.write('beta,20.0,20.0\n')
                f.write('gamma,30.0,30.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                content = f.read()

            assert 'alpha' in content
            assert 'beta' in content
            assert 'gamma' in content


class TestIwfmNearestNodesInputFormats:
    """Test different input formats for iwfm_nearest_nodes."""

    def test_handles_integer_coordinates(self):
        """Test handling of integer coordinates in input."""
        node_set = [[1, 0.0, 0.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,100,200\n')

            result = iwfm_nearest_nodes(input_file, node_set)

            assert result == 1

    def test_handles_large_coordinates(self):
        """Test handling of large UTM-style coordinates."""
        node_set = [[1, 550000.0, 4400000.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,550003.0,4400004.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            # Distance should be 5 (3-4-5 triangle)
            distance = float(lines[1].split(',')[2])
            assert distance == pytest.approx(5.0, abs=0.01)

    def test_handles_negative_coordinates(self):
        """Test handling of negative coordinates."""
        node_set = [[1, -100.0, -200.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('point1,-100.0,-200.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            distance = float(lines[1].split(',')[2])
            assert distance == 0.0


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST,
                    reason="Example node file not available")
class TestIwfmNearestNodesWithC2VSimCG:
    """Test iwfm_nearest_nodes with real C2VSimCG node data."""

    @pytest.fixture
    def c2vsimcg_nodes(self):
        """Load C2VSimCG node coordinates."""
        import iwfm
        node_coords, node_list, factor = iwfm.iwfm_read_nodes(EXAMPLE_NODE_FILE)
        return node_coords

    def test_processes_points_with_real_nodes(self, c2vsimcg_nodes):
        """Test processing points with real C2VSimCG nodes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('well1,560000.0,4200000.0\n')
                f.write('well2,580000.0,4100000.0\n')

            result = iwfm_nearest_nodes(input_file, c2vsimcg_nodes)

            assert result == 2

    def test_finds_valid_nodes(self, c2vsimcg_nodes):
        """Test that valid node IDs are found."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('well1,560000.0,4200000.0\n')

            iwfm_nearest_nodes(input_file, c2vsimcg_nodes)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            node_id = int(lines[1].split(',')[1])
            # C2VSimCG has nodes 1-1393
            assert 1 <= node_id <= 1393

    def test_reasonable_distances(self, c2vsimcg_nodes):
        """Test that distances are reasonable for points within model."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write('well1,560000.0,4200000.0\n')

            iwfm_nearest_nodes(input_file, c2vsimcg_nodes)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            distance = float(lines[1].split(',')[2])
            # Distance should be reasonable (less than typical element spacing)
            assert distance < 50000

    def test_point_on_existing_node(self, c2vsimcg_nodes):
        """Test point exactly on existing node."""
        # Use coordinates of node 1
        node_1 = c2vsimcg_nodes[0]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                f.write(f'node1_location,{node_1[1]},{node_1[2]}\n')

            iwfm_nearest_nodes(input_file, c2vsimcg_nodes)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            node_id = int(lines[1].split(',')[1])
            distance = float(lines[1].split(',')[2])

            assert node_id == 1
            assert distance == 0.0


class TestIwfmNearestNodesDistanceRounding:
    """Test distance rounding in output."""

    def test_distance_rounded_to_two_decimals(self):
        """Test that distance is rounded to 2 decimal places."""
        node_set = [[1, 0.0, 0.0]]

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'points.csv')
            with open(input_file, 'w') as f:
                f.write('name,x,y\n')
                # Creates distance of 1.41421356... (sqrt(2))
                f.write('point1,1.0,1.0\n')

            iwfm_nearest_nodes(input_file, node_set)

            output_file = os.path.join(temp_dir, 'points_nearest_nodes.out')
            with open(output_file, 'r') as f:
                lines = f.readlines()

            distance_str = lines[1].split(',')[2].strip()
            # Should be rounded to 1.41
            assert distance_str == '1.41'
