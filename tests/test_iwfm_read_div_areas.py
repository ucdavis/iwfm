#!/usr/bin/env python
# test_iwfm_read_div_areas.py
# Unit tests for iwfm_read_div_areas.py
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

import tempfile
import os


def create_div_spec_file(ndivs, deliv_areas_data, rchg_areas_data):
    """Create IWFM Diversion Specification file for testing.

    Parameters
    ----------
    ndivs : int
        Number of diversions
    deliv_areas_data : list of tuples
        Each tuple: (deliv_id, elements_list)
        elements_list: list of element IDs
    rchg_areas_data : list of tuples
        Each tuple: (rchg_id, elements_list)
        elements_list: list of element IDs

    Returns
    -------
    str
        File contents
    """
    content = "C IWFM Diversion Specification File\n"
    content += "C\n"

    # Number of diversions
    content += f"    {ndivs}                         / NRDV\n"
    content += "C\n"

    # Diversion specifications (skip this section for now, just add placeholder lines)
    for i in range(ndivs):
        content += f"    {i+1}    1    0    1.0    0    0.0    0    0.0    6    {i+1}    0    1.0    0    0\n"

    content += "C\n"
    content += "C Element groups for delivery\n"
    content += "C\n"

    # Number of delivery element groups
    n_delivs = len(deliv_areas_data)
    content += f"     {n_delivs}               / NGRP\n"
    content += "C\n"
    content += "C    ID         NELEM      IELEM\n"
    content += "C\n"

    # Delivery element groups
    for deliv_id, elements in deliv_areas_data:
        n_elems = len(elements)
        # First line: ID, NELEM, first element
        content += f"\t{deliv_id}\t{n_elems}\t{elements[0]}\n"
        # Remaining elements (one per line)
        for elem in elements[1:]:
            content += f"\t\t\t{elem}\n"

    content += "C\n"
    content += "C Recharge zones\n"
    content += "C\n"
    content += "C    ID         NERELS      IERELS     FERELS\n"
    content += "C\n"

    # Recharge zones (one per diversion)
    for rchg_id, elements in rchg_areas_data:
        n_elems = len(elements)
        # First line: ID, NERELS, first element, factor
        content += f"\t{rchg_id}\t{n_elems}\t{elements[0]}\t1\n"
        # Remaining elements (one per line with factor)
        for elem in elements[1:]:
            content += f"\t\t\t{elem}\t1\n"

    return content


class TestIwfmReadDivAreas:
    """Tests for iwfm_read_div_areas function"""

    def test_single_diversion_single_element(self):
        """Test reading single diversion with single element"""
        deliv_areas_data = [
            (1, [100])
        ]
        rchg_areas_data = [
            (1, [100])
        ]

        content = create_div_spec_file(1, deliv_areas_data, rchg_areas_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            # Verify delivery areas
            assert len(deliv_ids) == 1
            assert deliv_ids[0] == 1
            assert len(deliv_areas) == 1
            assert deliv_areas[0] == [100]

            # Verify recharge areas
            assert len(rchg_ids) == 1
            assert rchg_ids[0] == 1
            assert len(rchg_areas) == 1
            assert rchg_areas[0] == [100]

        finally:
            os.unlink(temp_file)

    def test_single_diversion_multiple_elements(self):
        """Test reading single diversion with multiple elements"""
        deliv_areas_data = [
            (1, [100, 101, 102, 103])
        ]
        rchg_areas_data = [
            (1, [100, 101, 102, 103])
        ]

        content = create_div_spec_file(1, deliv_areas_data, rchg_areas_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            # Verify delivery areas
            assert len(deliv_ids) == 1
            assert deliv_ids[0] == 1
            assert deliv_areas[0] == [100, 101, 102, 103]

            # Verify recharge areas
            assert len(rchg_ids) == 1
            assert rchg_ids[0] == 1
            assert rchg_areas[0] == [100, 101, 102, 103]

        finally:
            os.unlink(temp_file)

    def test_multiple_diversions(self):
        """Test reading multiple diversions"""
        deliv_areas_data = [
            (1, [100, 101]),
            (2, [200, 201, 202]),
            (3, [300])
        ]
        rchg_areas_data = [
            (1, [100, 101]),
            (2, [200, 201, 202]),
            (3, [300])
        ]

        content = create_div_spec_file(3, deliv_areas_data, rchg_areas_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            # Verify delivery areas
            assert len(deliv_ids) == 3
            assert deliv_ids == [1, 2, 3]
            assert deliv_areas[0] == [100, 101]
            assert deliv_areas[1] == [200, 201, 202]
            assert deliv_areas[2] == [300]

            # Verify recharge areas
            assert len(rchg_ids) == 3
            assert rchg_ids == [1, 2, 3]
            assert rchg_areas[0] == [100, 101]
            assert rchg_areas[1] == [200, 201, 202]
            assert rchg_areas[2] == [300]

        finally:
            os.unlink(temp_file)

    def test_different_delivery_and_recharge_areas(self):
        """Test when delivery and recharge areas are different"""
        deliv_areas_data = [
            (1, [100, 101, 102]),
            (2, [200, 201])
        ]
        rchg_areas_data = [
            (1, [150, 151]),  # Different elements
            (2, [250, 251, 252, 253])  # Different number of elements
        ]

        content = create_div_spec_file(2, deliv_areas_data, rchg_areas_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            # Verify delivery areas
            assert deliv_areas[0] == [100, 101, 102]
            assert deliv_areas[1] == [200, 201]

            # Verify recharge areas
            assert rchg_areas[0] == [150, 151]
            assert rchg_areas[1] == [250, 251, 252, 253]

        finally:
            os.unlink(temp_file)

    def test_large_element_numbers(self):
        """Test with large element numbers"""
        deliv_areas_data = [
            (1, [1750, 1780, 1808]),
            (2, [1809, 1810])
        ]
        rchg_areas_data = [
            (1, [1750, 1780, 1808]),
            (2, [1809, 1810])
        ]

        content = create_div_spec_file(2, deliv_areas_data, rchg_areas_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            assert deliv_areas[0] == [1750, 1780, 1808]
            assert deliv_areas[1] == [1809, 1810]
            assert rchg_areas[0] == [1750, 1780, 1808]
            assert rchg_areas[1] == [1809, 1810]

        finally:
            os.unlink(temp_file)

    def test_sequential_diversion_ids(self):
        """Test with sequential diversion IDs"""
        deliv_areas_data = [
            (1, [10]),
            (2, [20]),
            (3, [30]),
            (4, [40]),
            (5, [50])
        ]
        rchg_areas_data = [
            (1, [10]),
            (2, [20]),
            (3, [30]),
            (4, [40]),
            (5, [50])
        ]

        content = create_div_spec_file(5, deliv_areas_data, rchg_areas_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            assert deliv_ids == [1, 2, 3, 4, 5]
            assert rchg_ids == [1, 2, 3, 4, 5]
            assert len(deliv_areas) == 5
            assert len(rchg_areas) == 5

        finally:
            os.unlink(temp_file)

    def test_mixed_element_counts(self):
        """Test with varying numbers of elements per diversion"""
        deliv_areas_data = [
            (1, [1, 2]),  # 2 elements
            (2, [7, 11, 12, 18]),  # 4 elements
            (3, [13, 19, 20, 26, 27, 34, 35])  # 7 elements
        ]
        rchg_areas_data = [
            (1, [1, 2]),
            (2, [7, 11, 12, 18]),
            (3, [13, 19, 20, 26, 27, 34, 35])
        ]

        content = create_div_spec_file(3, deliv_areas_data, rchg_areas_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            # Verify element counts
            assert len(deliv_areas[0]) == 2
            assert len(deliv_areas[1]) == 4
            assert len(deliv_areas[2]) == 7

            # Verify specific elements
            assert deliv_areas[0] == [1, 2]
            assert deliv_areas[1] == [7, 11, 12, 18]
            assert deliv_areas[2] == [13, 19, 20, 26, 27, 34, 35]

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Diversion Specification File\n"
        content += "C This is a comment\n"
        content += "c Another comment with lowercase c\n"
        content += "* Comment with asterisk\n"
        content += "# Comment with hash\n"
        content += "    2                         / NRDV\n"
        content += "C Diversion specs\n"
        content += "    1    1    0    1.0    0    0.0    0    0.0    6    1    0    1.0    0    0\n"
        content += "    2    1    0    1.0    0    0.0    0    0.0    6    2    0    1.0    0    0\n"
        content += "C Element groups\n"
        content += "     2               / NGRP\n"
        content += "C More comments\n"
        content += "\t1\t2\t100\n"
        content += "\t\t\t101\n"
        content += "\t2\t3\t200\n"
        content += "\t\t\t201\n"
        content += "\t\t\t202\n"
        content += "C Recharge zones\n"
        content += "\t1\t2\t100\t1\n"
        content += "\t\t\t101\t1\n"
        content += "\t2\t3\t200\t1\n"
        content += "\t\t\t201\t1\n"
        content += "\t\t\t202\t1\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            # Should read correctly despite comment lines
            assert len(deliv_ids) == 2
            assert deliv_areas[0] == [100, 101]
            assert deliv_areas[1] == [200, 201, 202]

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real C2VSimCG file"""
        deliv_areas_data = [
            (1, [1, 2]),
            (2, [7, 11, 12, 18]),
            (3, [7, 11, 12, 18]),
            (4, [1, 2, 5, 6, 8, 9, 14, 15]),
            (5, [1, 7])
        ]
        rchg_areas_data = [
            (1, [1, 2]),
            (2, [7, 11, 12, 18]),
            (3, [7, 11, 12, 18]),
            (4, [1, 2, 5, 6, 8, 9, 14, 15]),
            (5, [1, 7])
        ]

        content = create_div_spec_file(5, deliv_areas_data, rchg_areas_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            # Verify all 5 diversions
            assert len(deliv_ids) == 5
            assert len(deliv_areas) == 5
            assert len(rchg_ids) == 5
            assert len(rchg_areas) == 5

            # Verify specific diversions
            assert deliv_areas[0] == [1, 2]
            assert deliv_areas[1] == [7, 11, 12, 18]
            assert deliv_areas[3] == [1, 2, 5, 6, 8, 9, 14, 15]

            assert rchg_areas[0] == [1, 2]
            assert rchg_areas[1] == [7, 11, 12, 18]
            assert rchg_areas[4] == [1, 7]

        finally:
            os.unlink(temp_file)

    def test_large_number_of_diversions(self):
        """Test with many diversions"""
        # Create 20 diversions
        deliv_areas_data = [(i+1, [i*10, i*10+1]) for i in range(20)]
        rchg_areas_data = [(i+1, [i*10, i*10+1]) for i in range(20)]

        content = create_div_spec_file(20, deliv_areas_data, rchg_areas_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_div_areas import iwfm_read_div_areas

            deliv_ids, deliv_areas, rchg_ids, rchg_areas = iwfm_read_div_areas(temp_file)

            assert len(deliv_ids) == 20
            assert len(deliv_areas) == 20
            assert len(rchg_ids) == 20
            assert len(rchg_areas) == 20

            # Spot check a few
            assert deliv_areas[0] == [0, 1]
            assert deliv_areas[10] == [100, 101]
            assert deliv_areas[19] == [190, 191]

        finally:
            os.unlink(temp_file)
