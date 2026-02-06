# test_read_elements_csv.py
# unit tests for read_elements_csv function
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


class TestReadElementsCsv:
    """Tests for the read_elements_csv function."""

    def test_basic_quadrilateral_elements(self, tmp_path):
        """Test reading CSV with quadrilateral elements (4 nodes)."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1,10,20,30,40
2,20,30,40,50
3,30,40,50,60
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert elem_ids == [1, 2, 3]
        assert elem_nodes == [
            [1, 10, 20, 30, 40],
            [2, 20, 30, 40, 50],
            [3, 30, 40, 50, 60]
        ]

    def test_triangular_elements(self, tmp_path):
        """Test reading CSV with triangular elements (3 nodes, 4th is 0)."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1,10,20,30,0
2,20,30,40,0
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert elem_ids == [1, 2]
        assert elem_nodes == [
            [1, 10, 20, 30, 0],
            [2, 20, 30, 40, 0]
        ]

    def test_mixed_elements(self, tmp_path):
        """Test reading CSV with mixed triangular and quadrilateral elements."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1,10,20,30,40
2,20,30,40,0
3,30,40,50,60
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert elem_ids == [1, 2, 3]
        # First and third are quads, second is triangle
        assert elem_nodes[0] == [1, 10, 20, 30, 40]
        assert elem_nodes[1] == [2, 20, 30, 40, 0]
        assert elem_nodes[2] == [3, 30, 40, 50, 60]

    def test_header_row_skipped(self, tmp_path):
        """Test that the first row (header) is skipped."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
element,n1,n2,n3,n4
1,100,200,300,400
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        # Should only have one element (header skipped)
        assert len(elem_ids) == 1
        assert elem_ids[0] == 1

    def test_returns_two_lists(self, tmp_path):
        """Test that function returns two lists."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1,10,20,30,40
"""
        csv_file.write_text(csv_content)

        result = iwfm.read_elements_csv(str(csv_file))

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)

    def test_elem_ids_are_integers(self, tmp_path):
        """Test that element IDs are returned as integers."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1,10,20,30,40
2,20,30,40,50
"""
        csv_file.write_text(csv_content)

        elem_ids, _ = iwfm.read_elements_csv(str(csv_file))

        for elem_id in elem_ids:
            assert isinstance(elem_id, int)

    def test_node_ids_are_integers(self, tmp_path):
        """Test that node IDs are returned as integers."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1,10,20,30,40
"""
        csv_file.write_text(csv_content)

        _, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        for node_list in elem_nodes:
            for node_id in node_list:
                assert isinstance(node_id, int)

    def test_single_element(self, tmp_path):
        """Test reading CSV with single element."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
42,100,200,300,400
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert elem_ids == [42]
        assert elem_nodes == [[42, 100, 200, 300, 400]]

    def test_many_elements(self, tmp_path):
        """Test reading CSV with many elements."""
        csv_file = tmp_path / "elements.csv"
        lines = ["elem_id,node1,node2,node3,node4"]
        for i in range(1, 101):
            lines.append(f"{i},{i*10},{i*10+1},{i*10+2},{i*10+3}")
        csv_file.write_text('\n'.join(lines))

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert len(elem_ids) == 100
        assert len(elem_nodes) == 100
        assert elem_ids[0] == 1
        assert elem_ids[-1] == 100

    def test_empty_lines_ignored(self, tmp_path):
        """Test that empty lines are ignored."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1,10,20,30,40

2,20,30,40,50

"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        # Empty lines should be skipped (len(line) <= 1)
        assert len(elem_ids) == 2

    def test_large_node_numbers(self, tmp_path):
        """Test reading CSV with large node numbers."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1392,1388,1392,1393,1389
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert elem_ids == [1392]
        assert elem_nodes == [[1392, 1388, 1392, 1393, 1389]]

    def test_nonsequential_element_ids(self, tmp_path):
        """Test reading CSV with non-sequential element IDs."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
5,10,20,30,40
10,20,30,40,50
15,30,40,50,60
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert elem_ids == [5, 10, 15]

    def test_elem_nodes_contains_elem_id(self, tmp_path):
        """Test that elem_nodes includes the element ID as first value."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
7,100,200,300,400
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        # The elem_nodes list should contain [elem_id, n1, n2, n3, n4]
        assert elem_nodes[0][0] == 7
        assert elem_nodes[0][0] == elem_ids[0]

    def test_file_not_found_raises_error(self, tmp_path):
        """Test that nonexistent file raises FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent.csv"

        with pytest.raises(FileNotFoundError):
            iwfm.read_elements_csv(str(nonexistent))

    def test_with_extra_columns(self, tmp_path):
        """Test reading CSV with extra columns (like subregion)."""
        csv_file = tmp_path / "elements.csv"
        # Format similar to IWFM element file: elem, n1, n2, n3, n4, subregion
        csv_content = """\
elem_id,node1,node2,node3,node4,subregion
1,10,20,30,40,1
2,20,30,40,50,2
3,30,40,50,0,3
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert elem_ids == [1, 2, 3]
        # All columns are read as nodes
        assert elem_nodes[0] == [1, 10, 20, 30, 40, 1]
        assert elem_nodes[1] == [2, 20, 30, 40, 50, 2]
        assert elem_nodes[2] == [3, 30, 40, 50, 0, 3]

    def test_whitespace_in_values(self, tmp_path):
        """Test reading CSV with whitespace around values."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1, 10, 20, 30, 40
2 ,20 ,30 ,40 ,50
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        # CSV reader should handle whitespace, int() conversion strips it
        assert elem_ids == [1, 2]

    def test_header_only_returns_empty_lists(self, tmp_path):
        """Test that file with only header returns empty lists."""
        csv_file = tmp_path / "elements.csv"
        csv_content = "elem_id,node1,node2,node3,node4\n"
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert elem_ids == []
        assert elem_nodes == []


class TestReadElementsCsvRealData:
    """Tests using patterns from real IWFM element data."""

    def test_c2vsim_style_elements(self, tmp_path):
        """Test with data formatted like C2VSimCG elements."""
        csv_file = tmp_path / "elements.csv"
        # Sample based on C2VSimCG_Elements.dat format
        csv_content = """\
elem_id,node1,node2,node3,node4,subregion
1,1,2,7,6,1
2,2,3,8,7,1
3,3,4,9,8,1
4,4,5,10,9,1
5,6,7,12,11,1
1350,1339,1349,1350,0,19
1392,1388,1392,1393,1389,21
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert len(elem_ids) == 7
        assert elem_ids[0] == 1
        assert elem_ids[-1] == 1392

        # Check a quadrilateral element
        assert elem_nodes[0] == [1, 1, 2, 7, 6, 1]

        # Check a triangular element (node4 = 0)
        assert elem_nodes[5] == [1350, 1339, 1349, 1350, 0, 19]

    def test_minimal_element_columns(self, tmp_path):
        """Test with minimal columns (elem_id and 4 nodes only)."""
        csv_file = tmp_path / "elements.csv"
        csv_content = """\
elem_id,node1,node2,node3,node4
1,1,2,7,6
2,2,3,8,7
3,3,4,9,0
"""
        csv_file.write_text(csv_content)

        elem_ids, elem_nodes = iwfm.read_elements_csv(str(csv_file))

        assert len(elem_ids) == 3
        assert len(elem_nodes[0]) == 5  # elem_id + 4 nodes
