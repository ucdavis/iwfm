#!/usr/bin/env python
# test_igsm_read_elements.py
# Unit tests for igsm_read_elements.py
# Copyright (C) 2020-2026 University of California
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


def create_igsm_elements_file(nelements, elements_data):
    """Create properly structured IGSM Elements file for testing.

    IWFM File Format Convention:
    - Comment lines start with 'C', 'c', '*', or '#' in column 1
    - Data lines MUST start with whitespace (space or tab)

    Parameters
    ----------
    nelements : int
        Number of elements
    elements_data : list of tuples
        Each tuple: (elem_id, node1, node2, node3, node4)
        node4 = 0 for triangular elements (3-sided)

    Returns
    -------
    str
        File contents
    """
    # Header comments (simplified from real file)
    content = "C IGSM Element Configuration File\n"
    content += "C\n"
    content += "C Elements are defined by nodes in counter-clockwise order\n"
    content += "C For triangular elements, the fourth node is zero\n"
    content += "C\n"

    # Number of elements
    content += f"    {nelements}                          /NE\n"
    content += "C\n"

    # Element data - MUST start with whitespace per IWFM convention
    for elem_id, node1, node2, node3, node4 in elements_data:
        # Format with proper spacing
        content += f"       {elem_id}       {node1}      {node2}     {node3}     {node4}\n"

    return content


class TestIgsmReadElements:
    """Tests for igsm_read_elements function"""

    def test_single_quadrilateral_element(self):
        """Test reading single 4-sided (quadrilateral) element"""
        elements_data = [
            (1, 1, 2, 22, 21)  # Quadrilateral element
        ]
        content = create_igsm_elements_file(1, elements_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify one element was read
            assert len(elem_nodes) == 1
            assert len(elem_list) == 1

            # Verify element ID
            assert elem_list[0] == 1

            # Verify nodes (should have 4 nodes for quadrilateral)
            assert len(elem_nodes[0]) == 4
            assert elem_nodes[0] == [1, 2, 22, 21]

        finally:
            os.unlink(temp_file)

    def test_single_triangular_element(self):
        """Test reading single 3-sided (triangular) element"""
        elements_data = [
            (1, 3, 4, 23, 0)  # Triangular element (node4 = 0)
        ]
        content = create_igsm_elements_file(1, elements_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify one element was read
            assert len(elem_nodes) == 1
            assert len(elem_list) == 1

            # Verify element ID
            assert elem_list[0] == 1

            # Verify nodes (should have 3 nodes for triangle, zero removed)
            assert len(elem_nodes[0]) == 3
            assert elem_nodes[0] == [3, 4, 23]

        finally:
            os.unlink(temp_file)

    def test_multiple_quadrilateral_elements(self):
        """Test reading multiple quadrilateral elements"""
        elements_data = [
            (1, 1, 2, 22, 21),
            (2, 2, 3, 23, 22),
            (4, 4, 5, 24, 23),
            (7, 6, 7, 26, 25)
        ]
        content = create_igsm_elements_file(4, elements_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify four elements were read
            assert len(elem_nodes) == 4
            assert len(elem_list) == 4

            # Verify element IDs
            assert elem_list == [1, 2, 4, 7]

            # Verify all are quadrilaterals
            for nodes in elem_nodes:
                assert len(nodes) == 4

            # Verify specific elements
            assert elem_nodes[0] == [1, 2, 22, 21]
            assert elem_nodes[1] == [2, 3, 23, 22]
            assert elem_nodes[3] == [6, 7, 26, 25]

        finally:
            os.unlink(temp_file)

    def test_multiple_triangular_elements(self):
        """Test reading multiple triangular elements"""
        elements_data = [
            (3, 3, 4, 23, 0),
            (5, 24, 5, 25, 0),
            (6, 25, 5, 6, 0),
            (9, 7, 8, 28, 0)
        ]
        content = create_igsm_elements_file(4, elements_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify four elements were read
            assert len(elem_nodes) == 4
            assert len(elem_list) == 4

            # Verify element IDs
            assert elem_list == [3, 5, 6, 9]

            # Verify all are triangles
            for nodes in elem_nodes:
                assert len(nodes) == 3

            # Verify specific elements
            assert elem_nodes[0] == [3, 4, 23]
            assert elem_nodes[1] == [24, 5, 25]
            assert elem_nodes[2] == [25, 5, 6]

        finally:
            os.unlink(temp_file)

    def test_mixed_element_types(self):
        """Test reading mix of triangular and quadrilateral elements"""
        elements_data = [
            (1, 1, 2, 22, 21),      # Quadrilateral
            (2, 2, 3, 23, 22),      # Quadrilateral
            (3, 3, 4, 23, 0),       # Triangle
            (4, 4, 5, 24, 23),      # Quadrilateral
            (5, 24, 5, 25, 0),      # Triangle
            (6, 25, 5, 6, 0),       # Triangle
            (7, 6, 7, 26, 25),      # Quadrilateral
        ]
        content = create_igsm_elements_file(7, elements_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify all elements were read
            assert len(elem_nodes) == 7
            assert len(elem_list) == 7

            # Verify element IDs
            assert elem_list == [1, 2, 3, 4, 5, 6, 7]

            # Verify element types (3 or 4 nodes)
            assert len(elem_nodes[0]) == 4  # Element 1: quad
            assert len(elem_nodes[1]) == 4  # Element 2: quad
            assert len(elem_nodes[2]) == 3  # Element 3: triangle
            assert len(elem_nodes[3]) == 4  # Element 4: quad
            assert len(elem_nodes[4]) == 3  # Element 5: triangle
            assert len(elem_nodes[5]) == 3  # Element 6: triangle
            assert len(elem_nodes[6]) == 4  # Element 7: quad

            # Verify specific nodes
            assert elem_nodes[2] == [3, 4, 23]      # Triangle
            assert elem_nodes[3] == [4, 5, 24, 23]  # Quad
            assert elem_nodes[4] == [24, 5, 25]     # Triangle

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        # Create file with various comment formats
        content = "C Comment with C\n"
        content += "c Comment with lowercase c\n"
        content += "* Comment with asterisk\n"
        content += "# Comment with hash\n"
        content += "    5                          /NE\n"
        content += "C More comments before data\n"
        content += "       1       1       2      22      21\n"
        content += "       2       2       3      23      22\n"
        content += "       3       3       4      23       0\n"
        content += "       4       4       5      24      23\n"
        content += "       5      24       5      25       0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify data was read correctly despite comment lines
            assert len(elem_nodes) == 5
            assert len(elem_list) == 5
            assert elem_list == [1, 2, 3, 4, 5]

        finally:
            os.unlink(temp_file)

    def test_non_sequential_element_ids(self):
        """Test elements with non-sequential IDs"""
        elements_data = [
            (10, 1, 2, 3, 4),
            (25, 5, 6, 7, 8),
            (100, 9, 10, 11, 12),
            (5, 13, 14, 15, 16)
        ]
        content = create_igsm_elements_file(4, elements_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify element IDs preserved correctly
            assert elem_list == [10, 25, 100, 5]

            # Verify nodes for each element
            assert elem_nodes[0] == [1, 2, 3, 4]
            assert elem_nodes[1] == [5, 6, 7, 8]
            assert elem_nodes[2] == [9, 10, 11, 12]
            assert elem_nodes[3] == [13, 14, 15, 16]

        finally:
            os.unlink(temp_file)

    def test_large_node_numbers(self):
        """Test elements with large node numbers"""
        elements_data = [
            (1, 1000, 1001, 2000, 1999),
            (2, 5000, 5001, 6000, 5999),
            (3, 10000, 10001, 11000, 0)
        ]
        content = create_igsm_elements_file(3, elements_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify large node numbers handled correctly
            assert elem_nodes[0] == [1000, 1001, 2000, 1999]
            assert elem_nodes[1] == [5000, 5001, 6000, 5999]
            assert elem_nodes[2] == [10000, 10001, 11000]  # Triangle, zero removed

        finally:
            os.unlink(temp_file)

    def test_element_count_parsing(self):
        """Test that element count is parsed correctly from various formats"""
        # Test with just the number
        content = "C IGSM Elements File\n"
        content += "    42                          /NE\n"
        content += "C\n"
        for i in range(1, 43):
            content += f"       {i}       {i}       {i+1}      {i+100}      {i+99}\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify correct number parsed
            assert len(elem_nodes) == 42
            assert len(elem_list) == 42

        finally:
            os.unlink(temp_file)

    def test_counter_clockwise_node_order(self):
        """Test that node order is preserved (counter-clockwise)"""
        elements_data = [
            (1, 13, 15, 16, 14),  # Nodes in counter-clockwise order
            (2, 14, 16, 17, 0)    # Triangle in counter-clockwise order
        ]
        content = create_igsm_elements_file(2, elements_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify node order is preserved
            assert elem_nodes[0] == [13, 15, 16, 14]
            assert elem_nodes[1] == [14, 16, 17]

        finally:
            os.unlink(temp_file)

    def test_return_values_correspondence(self):
        """Test that elem_nodes and elem_list correspond correctly"""
        elements_data = [
            (5, 1, 2, 3, 4),
            (10, 5, 6, 7, 0),
            (15, 8, 9, 10, 11)
        ]
        content = create_igsm_elements_file(3, elements_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_elements import igsm_read_elements

            elem_nodes, elem_list = igsm_read_elements(temp_file)

            # Verify correspondence between elem_list and elem_nodes
            assert len(elem_list) == len(elem_nodes)

            # Element IDs should match positions
            assert elem_list[0] == 5
            assert elem_nodes[0] == [1, 2, 3, 4]

            assert elem_list[1] == 10
            assert elem_nodes[1] == [5, 6, 7]

            assert elem_list[2] == 15
            assert elem_nodes[2] == [8, 9, 10, 11]

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
