#!/usr/bin/env python
# test_igsm_read_chars.py
# Unit tests for igsm_read_chars.py
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


def create_igsm_chars_file(element_chars):
    """Create properly structured IGSM Element Characteristics file for testing.

    IWFM File Format Convention:
    - Comment lines start with 'C', 'c', '*', or '#' in column 1
    - Data lines MUST start with whitespace (space or tab)

    Parameters
    ----------
    element_chars : list of tuples
        Each tuple: (elem_id, rain_station, rain_factor, drainage_node,
                     subregion, elem_subgrp, soil_type)

    Returns
    -------
    str
        File contents
    """
    # Header comments (simplified from real file)
    content = "C IGSM Element Characteristics Data File\n"
    content += "C\n"
    content += "C Element characteristics including rainfall station, factor,\n"
    content += "C drainage node, sub-region, and soil type\n"
    content += "C\n"
    content += "C   IE      - Element number\n"
    content += "C   IRNE    - Rainfall station assigned to element\n"
    content += "C   FRNE    - Rainfall factor\n"
    content += "C   ISTE    - Stream node for drainage\n"
    content += "C   IRGE    - Sub-region number\n"
    content += "C   ISGE    - Sub-element group number\n"
    content += "C   HSOIL   - Hydrologic soil type\n"
    content += "C\n"

    # Data lines - MUST start with whitespace per IWFM convention
    for elem_id, rain_station, rain_factor, drainage_node, subregion, elem_subgrp, soil_type in element_chars:
        content += f"\t{elem_id}\t{rain_station}\t{rain_factor}\t{drainage_node}\t{subregion}\t{elem_subgrp}\t{soil_type}\n"

    return content


class TestIgsmReadChars:
    """Tests for igsm_read_chars function"""

    def test_single_element(self):
        """Test reading single element characteristics"""
        element_chars = [
            (1, 5, 1.0, 207, 14, 1, 2.8)
        ]
        content = create_igsm_chars_file(element_chars)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            # elem_nodes would normally come from elements file
            # For this test, we just need the count
            elem_nodes = [[1, 100, 101, 102]]  # One element with 3 nodes

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify one element was read
            assert len(elem_char) == 1

            # Verify characteristics: [rain_station, rain_factor, drainage_node, subregion, soil_type]
            # Note: elem_subgrp (ISGE) is read but not stored (line 53 in function)
            assert elem_char[0][0] == 5      # rain_station
            assert elem_char[0][1] == 1.0    # rain_factor
            assert elem_char[0][2] == 207    # drainage_node
            assert elem_char[0][3] == 14     # subregion
            assert elem_char[0][4] == 2.8    # soil_type

        finally:
            os.unlink(temp_file)

    def test_multiple_elements(self):
        """Test reading multiple element characteristics"""
        element_chars = [
            (1, 5, 1.00, 207, 14, 1, 2.8),
            (2, 5, 0.96, 207, 14, 1, 2.6),
            (3, 5, 0.92, 207, 14, 1, 2.6),
            (4, 5, 0.89, 207, 14, 1, 2.7),
            (5, 5, 0.84, 207, 14, 1, 3.2)
        ]
        content = create_igsm_chars_file(element_chars)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            elem_nodes = [
                [1, 100, 101, 102],
                [2, 101, 103, 104],
                [3, 103, 105, 106],
                [4, 105, 107, 108],
                [5, 107, 109, 110]
            ]

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify all elements were read
            assert len(elem_char) == 5

            # Verify first element
            assert elem_char[0][0] == 5
            assert elem_char[0][1] == 1.0
            assert elem_char[0][4] == 2.8

            # Verify last element
            assert elem_char[4][0] == 5
            assert elem_char[4][1] == 0.84
            assert elem_char[4][4] == 3.2

        finally:
            os.unlink(temp_file)

    def test_different_rainfall_stations(self):
        """Test elements with different rainfall stations"""
        element_chars = [
            (1, 5, 1.0, 207, 14, 1, 2.8),
            (2, 7, 0.95, 208, 15, 2, 3.0),
            (3, 10, 0.88, 209, 16, 1, 2.5)
        ]
        content = create_igsm_chars_file(element_chars)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            elem_nodes = [
                [1, 100, 101, 102],
                [2, 101, 103, 104],
                [3, 103, 105, 106]
            ]

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify different rainfall stations
            assert elem_char[0][0] == 5
            assert elem_char[1][0] == 7
            assert elem_char[2][0] == 10

        finally:
            os.unlink(temp_file)

    def test_different_drainage_nodes(self):
        """Test elements with different drainage destinations"""
        element_chars = [
            (1, 5, 1.0, 207, 14, 1, 2.8),
            (2, 5, 0.96, 244, 15, 1, 2.6),
            (3, 5, 0.92, 300, 16, 1, 3.0)
        ]
        content = create_igsm_chars_file(element_chars)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            elem_nodes = [
                [1, 100, 101, 102],
                [2, 101, 103, 104],
                [3, 103, 105, 106]
            ]

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify different drainage nodes
            assert elem_char[0][2] == 207
            assert elem_char[1][2] == 244
            assert elem_char[2][2] == 300

        finally:
            os.unlink(temp_file)

    def test_different_subregions(self):
        """Test elements in different sub-regions"""
        element_chars = [
            (1, 5, 1.0, 207, 14, 1, 2.8),
            (2, 5, 0.96, 207, 15, 1, 2.6),
            (3, 5, 0.92, 207, 16, 1, 3.0),
            (4, 5, 0.89, 207, 17, 1, 2.7)
        ]
        content = create_igsm_chars_file(element_chars)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            elem_nodes = [
                [1, 100, 101, 102],
                [2, 101, 103, 104],
                [3, 103, 105, 106],
                [4, 105, 107, 108]
            ]

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify different sub-regions
            assert elem_char[0][3] == 14
            assert elem_char[1][3] == 15
            assert elem_char[2][3] == 16
            assert elem_char[3][3] == 17

        finally:
            os.unlink(temp_file)

    def test_soil_types(self):
        """Test different soil types (A=1, B=2, C=3, D=4)"""
        element_chars = [
            (1, 5, 1.0, 207, 14, 1, 1.0),    # Soil type A
            (2, 5, 0.96, 207, 14, 1, 2.6),   # Soil type B
            (3, 5, 0.92, 207, 14, 1, 3.2),   # Soil type C
            (4, 5, 0.89, 207, 14, 1, 4.0)    # Soil type D
        ]
        content = create_igsm_chars_file(element_chars)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            elem_nodes = [
                [1, 100, 101, 102],
                [2, 101, 103, 104],
                [3, 103, 105, 106],
                [4, 105, 107, 108]
            ]

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify soil types
            assert elem_char[0][4] == 1.0
            assert elem_char[1][4] == 2.6
            assert elem_char[2][4] == 3.2
            assert elem_char[3][4] == 4.0

        finally:
            os.unlink(temp_file)

    def test_rainfall_factors(self):
        """Test various rainfall factors"""
        element_chars = [
            (1, 5, 1.00, 207, 14, 1, 2.8),
            (2, 5, 0.96, 207, 14, 1, 2.6),
            (3, 5, 0.92, 207, 14, 1, 2.6),
            (4, 5, 0.50, 207, 14, 1, 2.7),
            (5, 5, 1.25, 207, 14, 1, 3.0)
        ]
        content = create_igsm_chars_file(element_chars)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            elem_nodes = [
                [1, 100, 101, 102],
                [2, 101, 103, 104],
                [3, 103, 105, 106],
                [4, 105, 107, 108],
                [5, 107, 109, 110]
            ]

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify rainfall factors
            assert elem_char[0][1] == 1.00
            assert elem_char[1][1] == 0.96
            assert elem_char[2][1] == 0.92
            assert elem_char[3][1] == 0.50
            assert elem_char[4][1] == 1.25

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        # Create file with various comment line formats
        content = "C Comment with C\n"
        content += "c Comment with lowercase c\n"
        content += "* Comment with asterisk\n"
        content += "# Comment with hash\n"
        content += "C More comments\n"
        content += "\t1\t5\t1.0\t207\t14\t1\t2.8\n"
        content += "\t2\t5\t0.96\t207\t14\t1\t2.6\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            elem_nodes = [
                [1, 100, 101, 102],
                [2, 101, 103, 104]
            ]

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify data was read correctly despite comment lines
            assert len(elem_char) == 2
            assert elem_char[0][0] == 5
            assert elem_char[1][1] == 0.96

        finally:
            os.unlink(temp_file)

    def test_elem_subgrp_ignored(self):
        """Test that element sub-group (ISGE) is read but not stored"""
        element_chars = [
            (1, 5, 1.0, 207, 14, 99, 2.8),  # ISGE=99 should be ignored
        ]
        content = create_igsm_chars_file(element_chars)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            elem_nodes = [[1, 100, 101, 102]]

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify returned list has 5 items (ISGE not included)
            # [rain_station, rain_factor, drainage_node, subregion, soil_type]
            assert len(elem_char[0]) == 5

            # Values should be: [5, 1.0, 207, 14, 2.8]
            # ISGE (99) is not in the list
            assert elem_char[0] == [5, 1.0, 207, 14, 2.8]

        finally:
            os.unlink(temp_file)

    def test_large_element_set(self):
        """Test reading a larger set of elements"""
        # Create 20 elements with varying characteristics
        element_chars = []
        for i in range(1, 21):
            elem_id = i
            rain_station = 5 if i <= 10 else 7
            rain_factor = 1.0 - (i * 0.01)
            drainage_node = 207 if i <= 10 else 244
            subregion = 14 + (i % 3)
            elem_subgrp = 1
            soil_type = 2.0 + (i % 4) * 0.5
            element_chars.append((elem_id, rain_station, rain_factor,
                                 drainage_node, subregion, elem_subgrp, soil_type))

        content = create_igsm_chars_file(element_chars)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_chars import igsm_read_chars

            elem_nodes = [[i, 100+i, 101+i, 102+i] for i in range(1, 21)]

            elem_char = igsm_read_chars(temp_file, elem_nodes)

            # Verify all 20 elements were read
            assert len(elem_char) == 20

            # Verify first element
            assert elem_char[0][0] == 5      # rain_station
            assert elem_char[0][1] == 0.99   # rain_factor

            # Verify last element
            assert elem_char[19][0] == 7     # rain_station
            assert elem_char[19][2] == 244   # drainage_node

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
