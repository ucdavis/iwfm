#!/usr/bin/env python
# test_iwfm_read_nodes.py
# Unit tests for iwfm_read_nodes.py
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
import tempfile
import os


def create_nodes_file(nnodes, fact, nodes_data):
    """Create IWFM Nodes file for testing.

    Parameters
    ----------
    nnodes : int
        Number of nodes
    fact : float
        Conversion factor for nodal coordinates
    nodes_data : list of tuples
        Each tuple: (node_id, x, y)

    Returns
    -------
    str
        File contents
    """
    content = "C IWFM Nodes File\n"
    content += "C\n"
    content += f"    {nnodes}                          /ND\n"
    content += f"    {fact}                        /FACT\n"
    content += "C\n"
    content += "C   Node     ----------Coordinates----------\n"
    content += "C    ID            X                 Y\n"
    content += "C\n"

    # Add node data
    for node_id, x, y in nodes_data:
        content += f"      {node_id}        {x}         {y}\n"

    return content


class TestIwfmReadNodes:
    """Tests for iwfm_read_nodes function"""

    def test_single_node(self):
        """Test reading single node"""
        nodes_data = [
            (1, 551396.4, 4496226.0)
        ]

        content = create_nodes_file(1, 3.2808, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            node_coord, node_list, factor = iwfm_read_nodes(temp_file)

            # Verify node list
            assert len(node_list) == 1
            assert node_list[0] == 1

            # Verify node coordinates
            assert len(node_coord) == 1
            assert node_coord[0][0] == 1
            assert node_coord[0][1] == pytest.approx(551396.4, abs=0.1)
            assert node_coord[0][2] == pytest.approx(4496226.0, abs=0.1)

            # Verify factor
            assert factor == 3.2808

        finally:
            os.unlink(temp_file)

    def test_multiple_nodes(self):
        """Test reading multiple nodes"""
        nodes_data = [
            (1, 551396.4, 4496226.0),
            (2, 555618.8, 4497861.0),
            (3, 561555.5, 4500441.0),
            (4, 568374.3, 4498058.0),
            (5, 553186.9, 4492706.0)
        ]

        content = create_nodes_file(5, 3.2808, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            node_coord, node_list, factor = iwfm_read_nodes(temp_file)

            # Verify node count
            assert len(node_list) == 5
            assert len(node_coord) == 5

            # Verify node IDs
            assert node_list == [1, 2, 3, 4, 5]

            # Verify first node
            assert node_coord[0][0] == 1
            assert node_coord[0][1] == pytest.approx(551396.4, abs=0.1)
            assert node_coord[0][2] == pytest.approx(4496226.0, abs=0.1)

            # Verify last node
            assert node_coord[4][0] == 5
            assert node_coord[4][1] == pytest.approx(553186.9, abs=0.1)
            assert node_coord[4][2] == pytest.approx(4492706.0, abs=0.1)

        finally:
            os.unlink(temp_file)

    def test_default_factor(self):
        """Test reading with default factor from file"""
        nodes_data = [
            (1, 100.0, 200.0),
            (2, 110.0, 210.0)
        ]

        content = create_nodes_file(2, 1.5, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            # Read with factor=0.0 (default, use file factor)
            node_coord, node_list, factor = iwfm_read_nodes(temp_file, factor=0.0)

            # Should use factor from file
            assert factor == 1.5

        finally:
            os.unlink(temp_file)

    def test_override_factor(self):
        """Test reading with override factor"""
        nodes_data = [
            (1, 100.0, 200.0),
            (2, 110.0, 210.0)
        ]

        content = create_nodes_file(2, 1.5, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            # Read with factor override
            node_coord, node_list, factor = iwfm_read_nodes(temp_file, factor=2.5)

            # Should use override factor
            assert factor == 2.5

        finally:
            os.unlink(temp_file)

    def test_non_sequential_node_ids(self):
        """Test reading nodes with non-sequential IDs"""
        nodes_data = [
            (5, 100.0, 200.0),
            (10, 110.0, 210.0),
            (15, 120.0, 220.0),
            (20, 130.0, 230.0)
        ]

        content = create_nodes_file(4, 1.0, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            node_coord, node_list, factor = iwfm_read_nodes(temp_file)

            # Verify non-sequential IDs are preserved
            assert node_list == [5, 10, 15, 20]
            assert node_coord[0][0] == 5
            assert node_coord[1][0] == 10
            assert node_coord[2][0] == 15
            assert node_coord[3][0] == 20

        finally:
            os.unlink(temp_file)

    def test_large_coordinates(self):
        """Test reading nodes with large coordinate values"""
        nodes_data = [
            (1, 551396.4, 4496226.0),
            (2, 555618.8, 4497861.0),
            (3, 561555.5, 4500441.0)
        ]

        content = create_nodes_file(3, 3.2808, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            node_coord, node_list, factor = iwfm_read_nodes(temp_file)

            # Verify large coordinates are read correctly
            assert node_coord[0][1] == pytest.approx(551396.4, abs=0.1)
            assert node_coord[0][2] == pytest.approx(4496226.0, abs=0.1)
            assert node_coord[2][1] == pytest.approx(561555.5, abs=0.1)
            assert node_coord[2][2] == pytest.approx(4500441.0, abs=0.1)

        finally:
            os.unlink(temp_file)

    def test_negative_coordinates(self):
        """Test reading nodes with negative coordinates"""
        nodes_data = [
            (1, -100.5, -200.5),
            (2, 100.5, -200.5),
            (3, -100.5, 200.5),
            (4, 100.5, 200.5)
        ]

        content = create_nodes_file(4, 1.0, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            node_coord, node_list, factor = iwfm_read_nodes(temp_file)

            # Verify negative coordinates
            assert node_coord[0][1] == pytest.approx(-100.5, abs=0.1)
            assert node_coord[0][2] == pytest.approx(-200.5, abs=0.1)
            assert node_coord[1][1] == pytest.approx(100.5, abs=0.1)
            assert node_coord[1][2] == pytest.approx(-200.5, abs=0.1)

        finally:
            os.unlink(temp_file)

    def test_integer_coordinates(self):
        """Test reading nodes with integer coordinates"""
        nodes_data = [
            (1, 100, 200),
            (2, 150, 250),
            (3, 200, 300)
        ]

        content = create_nodes_file(3, 1.0, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            node_coord, node_list, factor = iwfm_read_nodes(temp_file)

            # Verify integer coordinates are read as floats
            assert isinstance(node_coord[0][1], float)
            assert isinstance(node_coord[0][2], float)
            assert node_coord[0][1] == 100.0
            assert node_coord[0][2] == 200.0

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Nodes File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += "# Hash comment\n"
        content += "    3                          /ND\n"
        content += "C More comments\n"
        content += "    1.0                        /FACT\n"
        content += "C\n"
        content += "      1        100.0         200.0\n"
        content += "      2        110.0         210.0\n"
        content += "      3        120.0         220.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            node_coord, node_list, factor = iwfm_read_nodes(temp_file)

            # Should read correctly despite comment lines
            assert len(node_list) == 3
            assert node_list == [1, 2, 3]

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM C2VSimCG file"""
        nodes_data = [
            (1, 551396.4, 4496226),
            (2, 555618.8, 4497861),
            (3, 561555.5, 4500441),
            (4, 568374.3, 4498058),
            (5, 553186.9, 4492706),
            (6, 558611.6, 4492797),
            (7, 566864.0, 4493337),
            (8, 548989.2, 4487360),
            (9, 553710.4, 4488293),
            (10, 559339.9, 4488690)
        ]

        content = create_nodes_file(10, 3.2808, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            node_coord, node_list, factor = iwfm_read_nodes(temp_file)

            # Verify data structure
            assert len(node_list) == 10
            assert len(node_coord) == 10

            # Verify factor
            assert factor == 3.2808

            # Verify first node
            assert node_coord[0][0] == 1
            assert node_coord[0][1] == pytest.approx(551396.4, abs=0.1)
            assert node_coord[0][2] == pytest.approx(4496226, abs=0.1)

            # Verify middle node
            assert node_coord[4][0] == 5
            assert node_coord[4][1] == pytest.approx(553186.9, abs=0.1)

            # Verify last node
            assert node_coord[9][0] == 10
            assert node_coord[9][2] == pytest.approx(4488690, abs=0.1)

        finally:
            os.unlink(temp_file)

    def test_large_number_of_nodes(self):
        """Test reading many nodes"""
        # Create 100 nodes
        nodes_data = [(i+1, 100.0 + i, 200.0 + i) for i in range(100)]

        content = create_nodes_file(100, 1.0, nodes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_nodes import iwfm_read_nodes

            node_coord, node_list, factor = iwfm_read_nodes(temp_file)

            # Verify all nodes read
            assert len(node_list) == 100
            assert len(node_coord) == 100

            # Spot check first, middle, and last
            assert node_list[0] == 1
            assert node_list[50] == 51
            assert node_list[99] == 100

            assert node_coord[0][1] == 100.0
            assert node_coord[50][1] == 150.0
            assert node_coord[99][1] == 199.0

        finally:
            os.unlink(temp_file)
