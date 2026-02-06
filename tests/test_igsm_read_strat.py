#!/usr/bin/env python
# test_igsm_read_strat.py
# Unit tests for igsm_read_strat.py
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


def create_igsm_strat_file(nlayers, strat_data):
    """Create properly structured IGSM Stratigraphy file for testing.

    IWFM File Format Convention:
    - Comment lines start with 'C', 'c', '*', or '#' in column 1
    - Data lines MUST start with whitespace (space or tab)

    Parameters
    ----------
    nlayers : int
        Number of aquifer layers
    strat_data : list of tuples
        Each tuple: (node_id, elevation, aquiclude1_thickness, aquifer1_thickness,
                     aquiclude2_thickness, aquifer2_thickness, ...)
        Format: node_id, elevation, then pairs of (aquiclude_thickness, aquifer_thickness)

    Returns
    -------
    str
        File contents
    """
    # Header comments (simplified from real file)
    content = "C IGSM Stratigraphy Data File\n"
    content += "C\n"
    content += "C Ground surface elevation and layer thicknesses at each node\n"
    content += "C\n"

    # Number of layers
    content += f"    {nlayers}                           /NL\n"
    content += "C\n"

    # Stratigraphy data - MUST start with whitespace per IWFM convention
    for data in strat_data:
        # Convert tuple to tab-separated string
        # Format: node_id elevation w1 w2 w3 w4 ... (where w = thickness values)
        line_parts = [str(int(data[0])), str(int(data[1]))]  # node_id, elevation
        for thickness in data[2:]:
            line_parts.append(str(int(thickness)))
        content += "\t" + "\t".join(line_parts) + "\n"

    return content


class TestIgsmReadStrat:
    """Tests for igsm_read_strat function"""

    def test_single_node_single_layer(self):
        """Test reading single node with single aquifer layer"""
        # For 1 layer: elevation, aquiclude1, aquifer1
        strat_data = [
            (1, 190, 0, 120)  # node 1: elev=190, no aquiclude, aquifer=120
        ]
        content = create_igsm_strat_file(1, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            # node_coords would normally come from nodes file
            # For this test, we just need the count
            node_coords = [[1, 0.0, 0.0]]  # One node

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify one node was read
            assert len(strat) == 1

            # Verify number of layers
            assert nlayers == 1

            # Verify stratigraphy: [node_id, elevation, aquiclude1, aquifer1]
            assert strat[0][0] == 1      # node_id
            assert strat[0][1] == 190.0  # elevation
            assert strat[0][2] == 0.0    # aquiclude1 thickness
            assert strat[0][3] == 120.0  # aquifer1 thickness

        finally:
            os.unlink(temp_file)

    def test_single_node_multiple_layers(self):
        """Test reading single node with multiple aquifer layers"""
        # For 4 layers: elevation, aq1, a1, aq2, a2, aq3, a3, aq4, a4
        # where aq = aquiclude, a = aquifer
        strat_data = [
            (1, 190, 0, 0, 0, 120, 0, 0, 0, 0)
            # node 1: elev=190, layers 1-4 with only layer 2 having aquifer thickness
        ]
        content = create_igsm_strat_file(4, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [[1, 0.0, 0.0]]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify number of layers
            assert nlayers == 4

            # Verify stratigraphy data
            assert len(strat[0]) == 10  # node_id + elevation + 4*2 layer values
            assert strat[0][0] == 1
            assert strat[0][1] == 190.0

            # Check layer 2 aquifer thickness (position 5: aquifer2)
            assert strat[0][5] == 120.0

        finally:
            os.unlink(temp_file)

    def test_multiple_nodes(self):
        """Test reading multiple nodes"""
        # 2 layers per node
        strat_data = [
            (1, 190, 0, 0, 0, 120),
            (2, 164, 0, 35, 0, 200),
            (3, 152, 0, 35, 0, 290),
            (4, 142, 0, 45, 0, 450)
        ]
        content = create_igsm_strat_file(2, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [
                [1, 0.0, 0.0],
                [2, 10.0, 0.0],
                [3, 20.0, 0.0],
                [4, 30.0, 0.0]
            ]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify all nodes were read
            assert len(strat) == 4
            assert nlayers == 2

            # Verify node IDs
            assert strat[0][0] == 1
            assert strat[1][0] == 2
            assert strat[2][0] == 3
            assert strat[3][0] == 4

            # Verify elevations
            assert strat[0][1] == 190.0
            assert strat[1][1] == 164.0
            assert strat[2][1] == 152.0
            assert strat[3][1] == 142.0

            # Verify layer 2 aquifer thicknesses
            assert strat[0][5] == 120.0
            assert strat[1][5] == 200.0
            assert strat[2][5] == 290.0
            assert strat[3][5] == 450.0

        finally:
            os.unlink(temp_file)

    def test_layer_count_calculation(self):
        """Test that nlayers is calculated correctly"""
        # Formula: nlayers = (len(strat[0]) - 1) / 2
        # For 3 layers: 1 node_id + 1 elevation + 6 layer values = 8 total
        # nlayers = (8 - 1) / 2 = 3.5... should be 3
        strat_data = [
            (1, 190, 0, 100, 0, 200, 0, 300)
            # 3 aquifer layers with thicknesses 100, 200, 300
        ]
        content = create_igsm_strat_file(3, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [[1, 0.0, 0.0]]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify layer count
            assert nlayers == 3
            assert len(strat[0]) == 8  # 1 + 1 + 3*2

        finally:
            os.unlink(temp_file)

    def test_varying_elevations(self):
        """Test nodes with varying ground surface elevations"""
        strat_data = [
            (1, 190, 0, 120),
            (2, 164, 0, 200),
            (3, 152, 0, 290),
            (4, 142, 0, 450)
        ]
        content = create_igsm_strat_file(1, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [[i+1, 0.0, 0.0] for i in range(4)]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify decreasing elevations
            assert strat[0][1] == 190.0
            assert strat[1][1] == 164.0
            assert strat[2][1] == 152.0
            assert strat[3][1] == 142.0

        finally:
            os.unlink(temp_file)

    def test_aquiclude_thicknesses(self):
        """Test that aquiclude thicknesses are read correctly"""
        # Include some non-zero aquiclude values
        strat_data = [
            (1, 190, 10, 100, 20, 200)
            # Layer 1: aquiclude=10, aquifer=100
            # Layer 2: aquiclude=20, aquifer=200
        ]
        content = create_igsm_strat_file(2, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [[1, 0.0, 0.0]]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify aquiclude thicknesses
            assert strat[0][2] == 10.0   # aquiclude 1
            assert strat[0][3] == 100.0  # aquifer 1
            assert strat[0][4] == 20.0   # aquiclude 2
            assert strat[0][5] == 200.0  # aquifer 2

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        # Create file with various comment formats
        content = "C Comment with C\n"
        content += "c Comment with lowercase c\n"
        content += "* Comment with asterisk\n"
        content += "# Comment with hash\n"
        content += "    2                           /NL\n"
        content += "C More comments\n"
        content += "\t1\t190\t0\t100\t0\t200\n"
        content += "\t2\t164\t0\t120\t0\t250\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [[1, 0.0, 0.0], [2, 10.0, 0.0]]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify data was read correctly despite comment lines
            assert len(strat) == 2
            assert nlayers == 2
            assert strat[0][0] == 1
            assert strat[1][0] == 2

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IGSM file"""
        # Real file has 4 layers
        strat_data = [
            (1, 190, 0, 0, 0, 120, 0, 0, 0, 0),
            (2, 164, 0, 35, 0, 200, 0, 0, 0, 0),
            (3, 152, 0, 35, 0, 290, 0, 0, 0, 0),
            (4, 142, 0, 45, 0, 450, 0, 0, 0, 0),
            (5, 135, 0, 50, 0, 550, 0, 0, 0, 0)
        ]
        content = create_igsm_strat_file(4, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [[i+1, 0.0, 0.0] for i in range(5)]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify layer count
            assert nlayers == 4

            # Verify all nodes
            assert len(strat) == 5

            # Verify first node
            assert strat[0][0] == 1
            assert strat[0][1] == 190.0

            # Verify last node
            assert strat[4][0] == 5
            assert strat[4][1] == 135.0
            assert strat[4][5] == 550.0  # layer 2 aquifer thickness

        finally:
            os.unlink(temp_file)

    def test_strat_data_structure(self):
        """Test that stratigraphy data structure is correct"""
        strat_data = [
            (1, 100, 5, 50, 10, 100, 15, 150)
            # 3 layers with varying thicknesses
        ]
        content = create_igsm_strat_file(3, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [[1, 0.0, 0.0]]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify structure: [node_id, elevation, aq1, a1, aq2, a2, aq3, a3]
            assert len(strat[0]) == 8
            assert strat[0] == [1, 100.0, 5.0, 50.0, 10.0, 100.0, 15.0, 150.0]

        finally:
            os.unlink(temp_file)

    def test_non_sequential_node_ids(self):
        """Test nodes with non-sequential IDs"""
        strat_data = [
            (10, 190, 0, 120),
            (25, 164, 0, 200),
            (100, 152, 0, 290)
        ]
        content = create_igsm_strat_file(1, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [[10, 0.0, 0.0], [25, 0.0, 0.0], [100, 0.0, 0.0]]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify node IDs are preserved
            assert strat[0][0] == 10
            assert strat[1][0] == 25
            assert strat[2][0] == 100

        finally:
            os.unlink(temp_file)

    def test_zero_thickness_layers(self):
        """Test handling of zero-thickness aquicludes (indicates leakance used)"""
        strat_data = [
            (1, 190, 0, 100, 0, 200, 0, 300)
            # All aquicludes have zero thickness
        ]
        content = create_igsm_strat_file(3, strat_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.igsm_read_strat import igsm_read_strat

            node_coords = [[1, 0.0, 0.0]]

            strat, nlayers = igsm_read_strat(temp_file, node_coords)

            # Verify zero aquiclude thicknesses
            assert strat[0][2] == 0.0  # aquiclude 1
            assert strat[0][4] == 0.0  # aquiclude 2
            assert strat[0][6] == 0.0  # aquiclude 3

            # Verify non-zero aquifer thicknesses
            assert strat[0][3] == 100.0  # aquifer 1
            assert strat[0][5] == 200.0  # aquifer 2
            assert strat[0][7] == 300.0  # aquifer 3

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
