#!/usr/bin/env python
# test_igsm_read_lake.py
# Unit tests for igsm_read_lake.py
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


def create_igsm_lake_file(nlakes, lakes_data):
    """Create properly structured IGSM Lake file for testing.

    IWFM File Format Convention:
    - Comment lines start with 'C', 'c', '*', or '#' in column 1
    - Data lines MUST start with whitespace (space or tab)

    Parameters
    ----------
    nlakes : int
        Number of lakes
    lakes_data : list of tuples
        Each tuple: (lake_id, max_elev, next_lake, elements_data)
        elements_data: list of tuples (element_id, area)

    Returns
    -------
    str
        File contents
    """
    # Header comments (simplified from real file)
    content = "C IGSM Lake Configuration Data File\n"
    content += "C\n"
    content += "C Lakes with maximum elevation, downstream connections,\n"
    content += "C and element areas\n"
    content += "C\n"

    # Number of lakes
    content += f"    {nlakes}                           /NLAKE\n"
    content += "C\n"

    # Lake data - MUST start with whitespace per IWFM convention
    for lake_id, max_elev, next_lake, elements_data in lakes_data:
        nelem = len(elements_data)

        # First line: Lake ID, max elevation, next lake, number of elements, first element info
        elem_id, area = elements_data[0]
        content += f"      {lake_id}         {max_elev}     {next_lake}          {nelem}            {elem_id}        {area}\n"

        # Remaining elements (each on its own line)
        for elem_id, area in elements_data[1:]:
            content += f"                                                   {elem_id}        {area}\n"

    # Add end marker (the code will try to read one more line after last element)
    content += "C End of file\n"

    return content


class TestIgsmReadLake:
    """Tests for igsm_read_lake function"""

    def test_single_lake_single_element(self):
        """Test reading single lake with single element"""
        lakes_data = [
            (1, 515.0, 0, [(100, 1.0)])  # Lake 1, max_elev=515, no downstream, 1 element
        ]
        content = create_igsm_lake_file(1, lakes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify one lake was read
            assert len(lakes) == 1
            assert len(lake_elems) == 1

            # Verify lake properties: [lake_id, max_elev, next, nelem]
            assert lakes[0][0] == 1       # lake_id
            assert lakes[0][1] == 515.0   # max_elev
            assert lakes[0][2] == 0       # next (no downstream lake)
            assert lakes[0][3] == 1       # nelem

            # Verify lake element: [lake_id, element_id, area]
            assert lake_elems[0][0] == 1    # lake_id
            assert lake_elems[0][1] == 100  # element_id
            assert lake_elems[0][2] == 1.0  # area

        finally:
            os.unlink(temp_file)

    def test_single_lake_multiple_elements(self):
        """Test reading single lake with multiple elements"""
        lakes_data = [
            (1, 515.0, 0, [
                (1580, 1.0),
                (1581, 1.0),
                (1633, 1.0),
                (1634, 1.0),
                (1635, 1.0)
            ])
        ]
        content = create_igsm_lake_file(1, lakes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify one lake was read
            assert len(lakes) == 1
            assert len(lake_elems) == 5

            # Verify lake properties
            assert lakes[0][0] == 1       # lake_id
            assert lakes[0][1] == 515.0   # max_elev
            assert lakes[0][2] == 0       # next
            assert lakes[0][3] == 5       # nelem

            # Verify all elements belong to lake 1
            for elem in lake_elems:
                assert elem[0] == 1  # All belong to lake 1

            # Verify element IDs
            assert lake_elems[0][1] == 1580
            assert lake_elems[1][1] == 1581
            assert lake_elems[2][1] == 1633
            assert lake_elems[3][1] == 1634
            assert lake_elems[4][1] == 1635

            # Verify all areas are 1.0
            for elem in lake_elems:
                assert elem[2] == 1.0

        finally:
            os.unlink(temp_file)

    def test_multiple_lakes(self):
        """Test reading multiple lakes"""
        lakes_data = [
            (1, 515.0, 2, [
                (100, 1.0),
                (101, 1.0)
            ]),
            (2, 510.0, 0, [
                (200, 1.0),
                (201, 1.0),
                (202, 1.0)
            ]),
            (3, 520.0, 1, [
                (300, 0.8)
            ])
        ]
        content = create_igsm_lake_file(3, lakes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify three lakes were read
            assert len(lakes) == 3
            assert len(lake_elems) == 6  # 2 + 3 + 1 elements

            # Verify lake 1
            assert lakes[0] == [1, 515.0, 2, 2]

            # Verify lake 2
            assert lakes[1] == [2, 510.0, 0, 3]

            # Verify lake 3
            assert lakes[2] == [3, 520.0, 1, 1]

            # Verify elements for lake 1
            lake1_elems = [e for e in lake_elems if e[0] == 1]
            assert len(lake1_elems) == 2
            assert lake1_elems[0][1] == 100
            assert lake1_elems[1][1] == 101

            # Verify elements for lake 2
            lake2_elems = [e for e in lake_elems if e[0] == 2]
            assert len(lake2_elems) == 3

            # Verify elements for lake 3
            lake3_elems = [e for e in lake_elems if e[0] == 3]
            assert len(lake3_elems) == 1
            assert lake3_elems[0][2] == 0.8  # Fractional area

        finally:
            os.unlink(temp_file)

    def test_lake_with_downstream_connection(self):
        """Test lakes with downstream connections"""
        lakes_data = [
            (1, 520.0, 2, [(100, 1.0)]),  # Lake 1 flows to Lake 2
            (2, 515.0, 3, [(200, 1.0)]),  # Lake 2 flows to Lake 3
            (3, 510.0, 0, [(300, 1.0)])   # Lake 3 has no downstream
        ]
        content = create_igsm_lake_file(3, lakes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify downstream connections
            assert lakes[0][2] == 2  # Lake 1 -> Lake 2
            assert lakes[1][2] == 3  # Lake 2 -> Lake 3
            assert lakes[2][2] == 0  # Lake 3 -> None

        finally:
            os.unlink(temp_file)

    def test_fractional_areas(self):
        """Test elements with fractional areas"""
        lakes_data = [
            (1, 515.0, 0, [
                (100, 1.0),
                (101, 0.75),
                (102, 0.5),
                (103, 0.25)
            ])
        ]
        content = create_igsm_lake_file(1, lakes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify fractional areas
            assert lake_elems[0][2] == 1.0
            assert lake_elems[1][2] == 0.75
            assert lake_elems[2][2] == 0.5
            assert lake_elems[3][2] == 0.25

        finally:
            os.unlink(temp_file)

    def test_different_max_elevations(self):
        """Test lakes with different maximum elevations"""
        lakes_data = [
            (1, 515.0, 0, [(100, 1.0)]),
            (2, 520.5, 0, [(200, 1.0)]),
            (3, 505.25, 0, [(300, 1.0)])
        ]
        content = create_igsm_lake_file(3, lakes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify different elevations
            assert lakes[0][1] == 515.0
            assert lakes[1][1] == 520.5
            assert lakes[2][1] == 505.25

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        # Create file with various comment formats
        content = "C Comment with C\n"
        content += "c Comment with lowercase c\n"
        content += "* Comment with asterisk\n"
        content += "# Comment with hash\n"
        content += "    2                           /NLAKE\n"
        content += "C More comments\n"
        content += "      1         515.0     0          2            100        1.0\n"
        content += "                                                   101        1.0\n"
        content += "      2         520.0     0          1            200        0.8\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify data was read correctly despite comment lines
            assert len(lakes) == 2
            assert len(lake_elems) == 3
            assert lakes[0][0] == 1
            assert lakes[1][0] == 2

        finally:
            os.unlink(temp_file)

    def test_lake_element_correspondence(self):
        """Test that lake_elems and lakes correspond correctly"""
        lakes_data = [
            (1, 515.0, 0, [
                (100, 1.0),
                (101, 1.0)
            ]),
            (2, 520.0, 0, [
                (200, 1.0),
                (201, 1.0),
                (202, 1.0)
            ])
        ]
        content = create_igsm_lake_file(2, lakes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify lake 1 has correct number of elements
            lake1_count = lakes[0][3]  # nelem for lake 1
            lake1_elems = [e for e in lake_elems if e[0] == 1]
            assert len(lake1_elems) == lake1_count
            assert lake1_count == 2

            # Verify lake 2 has correct number of elements
            lake2_count = lakes[1][3]  # nelem for lake 2
            lake2_elems = [e for e in lake_elems if e[0] == 2]
            assert len(lake2_elems) == lake2_count
            assert lake2_count == 3

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IGSM file"""
        lakes_data = [
            (1, 515.0, 0, [
                (1580, 1.0),
                (1581, 1.0),
                (1633, 1.0),
                (1634, 1.0),
                (1635, 1.0),
                (1684, 1.0),
                (1685, 1.0),
                (1686, 1.0),
                (1736, 1.0),
                (1738, 1.0),
                (1739, 1.0),
                (1740, 1.0),
                (1741, 1.0),
                (1742, 1.0),
                (1745, 1.0),
                (1793, 1.0),
                (1794, 1.0),
                (1795, 1.0),
                (1797, 1.0),
                (1844, 1.0)
            ])
        ]
        content = create_igsm_lake_file(1, lakes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify lake properties
            assert len(lakes) == 1
            assert lakes[0][0] == 1       # lake_id
            assert lakes[0][1] == 515.0   # max_elev
            assert lakes[0][2] == 0       # next
            assert lakes[0][3] == 20      # nelem

            # Verify all 20 elements
            assert len(lake_elems) == 20

            # Verify first and last elements
            assert lake_elems[0][1] == 1580
            assert lake_elems[19][1] == 1844

            # All areas should be 1.0
            for elem in lake_elems:
                assert elem[2] == 1.0

        finally:
            os.unlink(temp_file)

    def test_non_sequential_lake_ids(self):
        """Test lakes with non-sequential IDs"""
        lakes_data = [
            (5, 515.0, 0, [(100, 1.0)]),
            (10, 520.0, 0, [(200, 1.0)]),
            (2, 525.0, 0, [(300, 1.0)])
        ]
        content = create_igsm_lake_file(3, lakes_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_lake import igsm_read_lake

            lake_elems, lakes = igsm_read_lake(temp_file)

            # Verify lake IDs are preserved
            assert lakes[0][0] == 5
            assert lakes[1][0] == 10
            assert lakes[2][0] == 2

            # Verify element associations
            assert lake_elems[0][0] == 5
            assert lake_elems[1][0] == 10
            assert lake_elems[2][0] == 2

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
