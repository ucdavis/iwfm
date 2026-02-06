#!/usr/bin/env python
# test_iwfm_read_strat.py
# Unit tests for iwfm_read_strat.py
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


class TestIwfmReadStrat:
    """Tests for iwfm_read_strat function"""

    def test_basic_structure_4_layers(self):
        """Test reading basic stratigraphy file with 4 layers"""
        content = "C IWFM Stratigraphy File\n"
        content += "C\n"
        content += " 4                             /NL\n"
        content += " 1.0                           /FACT\n"
        content += "C\n"
        content += "C      ID   Elev   A1    L1    A2    L2    A3    L3    A4    L4\n"
        content += " 1  576.95  0.00  113.69  0.00  106.37  0.00  152.80  0.00  50.00\n"
        content += " 2  683.75  0.00  176.92  0.00  119.59  0.00  116.60  0.00  50.00\n"
        content += " 3  712.80  0.00  190.84  0.00  121.52  0.00  101.99  0.00  50.00\n"
        content += "C\n"

        # Node coordinates (x, y) for 3 nodes
        node_coords = [(100.0, 200.0), (150.0, 250.0), (200.0, 300.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # Verify return types
            assert isinstance(strat, list)
            assert isinstance(nlayers, int)

            # Verify number of layers
            assert nlayers == 4

            # Verify number of nodes
            assert len(strat) == 3

            # Verify structure of first node
            # Each node should have: [ID, Elev, A1, L1, A2, L2, A3, L3, A4, L4]
            # That's 1 + 1 + (4 layers * 2) = 10 values
            assert len(strat[0]) == 10
            assert strat[0][0] == 1  # Node ID
            assert strat[0][1] == 576.95  # Elevation

        finally:
            os.unlink(temp_file)

    def test_basic_structure_2_layers(self):
        """Test reading stratigraphy file with 2 layers"""
        content = "C IWFM Stratigraphy File\n"
        content += " 2                             /NL\n"
        content += " 1.0                           /FACT\n"
        content += "C\n"
        content += " 1  500.0  0.0  100.0  0.0  50.0\n"
        content += " 2  550.0  0.0  120.0  0.0  60.0\n"

        node_coords = [(100.0, 200.0), (150.0, 250.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # Verify number of layers
            assert nlayers == 2

            # Verify number of nodes
            assert len(strat) == 2

            # Each node should have: [ID, Elev, A1, L1, A2, L2]
            # That's 1 + 1 + (2 layers * 2) = 6 values
            assert len(strat[0]) == 6

        finally:
            os.unlink(temp_file)

    def test_conversion_factor(self):
        """Test with different conversion factor"""
        content = "C IWFM Stratigraphy File\n"
        content += " 2                             /NL\n"
        content += " 3.2808                        /FACT\n"
        content += "C\n"
        content += " 1  500.0  0.0  100.0  0.0  50.0\n"
        content += " 2  550.0  0.0  120.0  0.0  60.0\n"

        node_coords = [(100.0, 200.0), (150.0, 250.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # Verify conversion factor is applied
            # Elevation should be multiplied by factor
            assert abs(strat[0][1] - (500.0 * 3.2808)) < 0.01
            assert abs(strat[0][3] - (100.0 * 3.2808)) < 0.01

        finally:
            os.unlink(temp_file)

    def test_return_structure(self):
        """Test that function returns correct tuple structure"""
        content = "C IWFM Stratigraphy File\n"
        content += " 3                             /NL\n"
        content += " 1.0                           /FACT\n"
        content += " 1  500.0  0.0  100.0  0.0  80.0  0.0  60.0\n"

        node_coords = [(100.0, 200.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            result = iwfm_read_strat(temp_file, node_coords)

            # Verify return is tuple of 2 elements
            assert isinstance(result, tuple)
            assert len(result) == 2

            strat, nlayers = result

            # Verify types
            assert isinstance(strat, list)
            assert isinstance(nlayers, int)

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Stratigraphy File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += " 2                             /NL\n"
        content += "# Comment\n"
        content += " 1.0                           /FACT\n"
        content += "C More comments\n"
        content += " 1  500.0  0.0  100.0  0.0  50.0\n"
        content += " 2  550.0  0.0  120.0  0.0  60.0\n"

        node_coords = [(100.0, 200.0), (150.0, 250.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # Should read correctly despite comment lines
            assert nlayers == 2
            assert len(strat) == 2

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM C2VSimCG file"""
        content = "C*******************************************************************************\n"
        content += "C                  INTEGRATED WATER FLOW MODEL (IWFM)\n"
        content += "C*******************************************************************************\n"
        content += "C\n"
        content += " 4                             /NL\n"
        content += " 1.0                           /FACT\n"
        content += "C\n"
        content += "C      ID   Elev   A1    L1    A2    L2    A3    L3    A4    L4\n"
        content += " 1  576.95  0.00  113.69  0.00  106.37  0.00  152.80  0.00  50.00\n"
        content += " 2  683.75  0.00  176.92  0.00  119.59  0.00  116.60  0.00  50.00\n"
        content += " 3  712.80  0.00  190.84  0.00  121.52  0.00  101.99  0.00  50.00\n"

        node_coords = [(100.0, 200.0), (150.0, 250.0), (200.0, 300.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # Verify data structure
            assert nlayers == 4
            assert len(strat) == 3
            assert strat[0][0] == 1
            assert strat[0][1] == 576.95

        finally:
            os.unlink(temp_file)

    def test_single_node(self):
        """Test with single node"""
        content = "C IWFM Stratigraphy File\n"
        content += " 2                             /NL\n"
        content += " 1.0                           /FACT\n"
        content += " 1  500.0  0.0  100.0  0.0  50.0\n"

        node_coords = [(100.0, 200.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # Verify single node is read correctly
            assert len(strat) == 1
            assert strat[0][0] == 1

        finally:
            os.unlink(temp_file)

    def test_multiple_nodes(self):
        """Test with multiple nodes"""
        content = "C IWFM Stratigraphy File\n"
        content += " 2                             /NL\n"
        content += " 1.0                           /FACT\n"
        content += " 1  500.0  0.0  100.0  0.0  50.0\n"
        content += " 2  550.0  0.0  120.0  0.0  60.0\n"
        content += " 3  600.0  0.0  140.0  0.0  70.0\n"
        content += " 4  650.0  0.0  160.0  0.0  80.0\n"
        content += " 5  700.0  0.0  180.0  0.0  90.0\n"

        node_coords = [(100.0, 200.0), (150.0, 250.0), (200.0, 300.0),
                      (250.0, 350.0), (300.0, 400.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # Verify all nodes are read
            assert len(strat) == 5
            assert strat[0][0] == 1
            assert strat[4][0] == 5

        finally:
            os.unlink(temp_file)

    def test_layer_count_calculation(self):
        """Test that layer count is calculated correctly from data"""
        content = "C IWFM Stratigraphy File\n"
        content += " 3                             /NL\n"
        content += " 1.0                           /FACT\n"
        content += " 1  500.0  0.0  100.0  0.0  80.0  0.0  60.0\n"

        node_coords = [(100.0, 200.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # nlayers = (len(strat[0]) - 1) / 2
            # len(strat[0]) = 1 (ID) + 1 (Elev) + 3*2 (layers) = 8
            # nlayers = (8 - 1) / 2 = 3.5 rounded to int = 3
            assert nlayers == 3

        finally:
            os.unlink(temp_file)

    def test_aquifer_and_aquitard_thicknesses(self):
        """Test that aquifer and aquitard thicknesses are read correctly"""
        content = "C IWFM Stratigraphy File\n"
        content += " 2                             /NL\n"
        content += " 1.0                           /FACT\n"
        content += " 1  500.0  10.0  100.0  20.0  50.0\n"

        node_coords = [(100.0, 200.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # Verify structure: [ID, Elev, A1, L1, A2, L2]
            assert strat[0][0] == 1      # ID
            assert strat[0][1] == 500.0  # Elevation
            assert strat[0][2] == 10.0   # Aquitard thickness layer 1
            assert strat[0][3] == 100.0  # Aquifer thickness layer 1
            assert strat[0][4] == 20.0   # Aquitard thickness layer 2
            assert strat[0][5] == 50.0   # Aquifer thickness layer 2

        finally:
            os.unlink(temp_file)

    def test_zero_aquitard_thickness(self):
        """Test handling of zero aquitard thickness"""
        content = "C IWFM Stratigraphy File\n"
        content += " 2                             /NL\n"
        content += " 1.0                           /FACT\n"
        content += " 1  500.0  0.0  100.0  0.0  50.0\n"

        node_coords = [(100.0, 200.0)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_strat import iwfm_read_strat

            strat, nlayers = iwfm_read_strat(temp_file, node_coords)

            # Verify zero aquitard thicknesses
            assert strat[0][2] == 0.0   # Aquitard thickness layer 1 is zero
            assert strat[0][4] == 0.0   # Aquitard thickness layer 2 is zero

        finally:
            os.unlink(temp_file)
