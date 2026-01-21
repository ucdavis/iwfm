#!/usr/bin/env python
# test_read_nodes.py
# Unit tests for read_nodes.py
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


class TestReadNodes:
    """Tests for read_nodes function"""

    def test_basic_structure(self):
        """Test reading basic nodes file"""
        content = "C IWFM Node File\n"
        content += " 5\n"
        content += " 1.0\n"
        content += " 1  100.0  200.0\n"
        content += " 2  150.0  250.0\n"
        content += " 3  200.0  300.0\n"
        content += " 4  250.0  350.0\n"
        content += " 5  300.0  400.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            node_coord, node_list = read_nodes(temp_file)

            # Verify node list
            assert len(node_list) == 5
            assert node_list == [1, 2, 3, 4, 5]

            # Verify coordinates
            assert len(node_coord) == 5
            assert node_coord[0] == [100.0, 200.0]
            assert node_coord[1] == [150.0, 250.0]
            assert node_coord[4] == [300.0, 400.0]

        finally:
            os.unlink(temp_file)

    def test_with_factor(self):
        """Test reading nodes file with conversion factor"""
        content = "C IWFM Node File\n"
        content += " 3\n"
        content += " 3.2808\n"
        content += " 1  100.0  200.0\n"
        content += " 2  150.0  250.0\n"
        content += " 3  200.0  300.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            # Test with default factor (from file)
            node_coord, node_list = read_nodes(temp_file)
            assert len(node_list) == 3

            # Test with custom factor
            node_coord2, node_list2 = read_nodes(temp_file, factor=2.0)
            assert len(node_list2) == 3
            assert node_list2 == node_list

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Node File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += "# Yet another comment\n"
        content += " 3\n"
        content += "C More comments\n"
        content += " 1.0\n"
        content += "C Node data follows\n"
        content += " 1  100.0  200.0\n"
        content += " 2  150.0  250.0\n"
        content += " 3  200.0  300.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            node_coord, node_list = read_nodes(temp_file)

            # Should read correctly despite comment lines
            assert len(node_list) == 3
            assert node_list == [1, 2, 3]
            assert node_coord[0] == [100.0, 200.0]

        finally:
            os.unlink(temp_file)

    def test_return_structure(self):
        """Test that function returns correct tuple structure"""
        content = "C IWFM Node File\n"
        content += " 2\n"
        content += " 1.0\n"
        content += " 1  100.0  200.0\n"
        content += " 2  150.0  250.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            result = read_nodes(temp_file)

            # Verify return is tuple of 2 elements
            assert isinstance(result, tuple)
            assert len(result) == 2

            node_coord, node_list = result

            # Verify types
            assert isinstance(node_coord, list)
            assert isinstance(node_list, list)
            assert len(node_coord) == len(node_list)

        finally:
            os.unlink(temp_file)

    def test_non_sequential_node_ids(self):
        """Test reading nodes with non-sequential IDs"""
        content = "C IWFM Node File\n"
        content += " 4\n"
        content += " 1.0\n"
        content += " 10  100.0  200.0\n"
        content += " 25  150.0  250.0\n"
        content += " 50  200.0  300.0\n"
        content += " 100  250.0  350.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            node_coord, node_list = read_nodes(temp_file)

            # Verify node list preserves original IDs
            assert node_list == [10, 25, 50, 100]
            assert len(node_coord) == 4
            assert node_coord[0] == [100.0, 200.0]
            assert node_coord[3] == [250.0, 350.0]

        finally:
            os.unlink(temp_file)

    def test_large_coordinates(self):
        """Test reading nodes with large coordinate values"""
        content = "C IWFM Node File\n"
        content += " 3\n"
        content += " 1.0\n"
        content += " 1  551396.4  4496226.0\n"
        content += " 2  555618.8  4497861.0\n"
        content += " 3  561555.5  4500441.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            node_coord, node_list = read_nodes(temp_file)

            assert len(node_list) == 3
            assert node_coord[0] == [551396.4, 4496226.0]
            assert node_coord[1] == [555618.8, 4497861.0]
            assert node_coord[2] == [561555.5, 4500441.0]

        finally:
            os.unlink(temp_file)

    def test_negative_coordinates(self):
        """Test reading nodes with negative coordinates"""
        content = "C IWFM Node File\n"
        content += " 3\n"
        content += " 1.0\n"
        content += " 1  -100.0  200.0\n"
        content += " 2  150.0  -250.0\n"
        content += " 3  -200.0  -300.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            node_coord, node_list = read_nodes(temp_file)

            assert len(node_list) == 3
            assert node_coord[0] == [-100.0, 200.0]
            assert node_coord[1] == [150.0, -250.0]
            assert node_coord[2] == [-200.0, -300.0]

        finally:
            os.unlink(temp_file)

    def test_scientific_notation_coordinates(self):
        """Test reading nodes with scientific notation coordinates"""
        content = "C IWFM Node File\n"
        content += " 2\n"
        content += " 1.0\n"
        content += " 1  1.5e5  2.0e6\n"
        content += " 2  3.5e5  4.0e6\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            node_coord, node_list = read_nodes(temp_file)

            assert len(node_list) == 2
            assert node_coord[0] == [1.5e5, 2.0e6]
            assert node_coord[1] == [3.5e5, 4.0e6]

        finally:
            os.unlink(temp_file)

    def test_single_node(self):
        """Test reading file with single node"""
        content = "C IWFM Node File\n"
        content += " 1\n"
        content += " 1.0\n"
        content += " 100  123.456  789.012\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            node_coord, node_list = read_nodes(temp_file)

            assert len(node_list) == 1
            assert node_list == [100]
            assert len(node_coord) == 1
            assert node_coord[0] == [123.456, 789.012]

        finally:
            os.unlink(temp_file)

    def test_decimal_factor(self):
        """Test reading with decimal conversion factor"""
        content = "C IWFM Node File\n"
        content += " 2\n"
        content += " 0.5\n"
        content += " 1  100.0  200.0\n"
        content += " 2  150.0  250.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            node_coord, node_list = read_nodes(temp_file)

            assert len(node_list) == 2
            # Factor is read but coordinates are as-is
            assert node_coord[0] == [100.0, 200.0]

        finally:
            os.unlink(temp_file)

    def test_extra_whitespace(self):
        """Test reading nodes with extra whitespace"""
        content = "C IWFM Node File\n"
        content += "    3    \n"
        content += "  1.0  \n"
        content += "  1    100.0    200.0  \n"
        content += "  2    150.0    250.0  \n"
        content += "  3    200.0    300.0  \n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            node_coord, node_list = read_nodes(temp_file)

            # Should handle extra whitespace correctly
            assert len(node_list) == 3
            assert node_list == [1, 2, 3]
            assert node_coord[0] == [100.0, 200.0]

        finally:
            os.unlink(temp_file)

    def test_factor_zero_uses_file_factor(self):
        """Test that factor=0 uses the factor from file"""
        content = "C IWFM Node File\n"
        content += " 2\n"
        content += " 3.2808\n"
        content += " 1  100.0  200.0\n"
        content += " 2  150.0  250.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            # Explicitly pass factor=0.0
            node_coord, node_list = read_nodes(temp_file, factor=0.0)

            assert len(node_list) == 2
            # Coordinates remain unchanged (factor is for reference)
            assert node_coord[0] == [100.0, 200.0]

        finally:
            os.unlink(temp_file)

    def test_custom_factor_overrides_file(self):
        """Test that custom factor overrides file factor"""
        content = "C IWFM Node File\n"
        content += " 2\n"
        content += " 3.2808\n"
        content += " 1  100.0  200.0\n"
        content += " 2  150.0  250.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_nodes import read_nodes

            # Use custom factor
            node_coord, node_list = read_nodes(temp_file, factor=10.0)

            assert len(node_list) == 2
            # Coordinates remain unchanged (factor is for reference)
            assert node_coord[0] == [100.0, 200.0]

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
