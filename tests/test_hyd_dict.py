#!/usr/bin/env python
# test_hyd_dict.py
# Unit tests for hyd_dict.py
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


def create_groundwater_file(nouth, hydrograph_data):
    """Create properly structured IWFM groundwater file for testing.

    IWFM File Format Convention:
    - Comment lines start with 'C', 'c', '*', or '#' in column 1
    - Data lines MUST start with whitespace (space or tab)

    The hyd_dict function calls:
    1. skip_ahead(1, lines, 20) to skip 20 non-comment lines and reach NOUTH
    2. skip_ahead(line_index, lines, 2) to skip 2 more lines after NOUTH

    Parameters
    ----------
    nouth : int
        Number of hydrographs to be printed
    hydrograph_data : list of tuples
        Each tuple: (id, hydtyp, layer, x, y, node, name)

    Returns
    -------
    str
        File contents
    """
    # Version and header comments
    content = "C Groundwater Component Main Data File\n"
    content += "C IWFM Groundwater Package v4.0\n"
    content += "C\n"

    # Add 20 parameter lines (these are skipped by skip_ahead(1, lines, 20))
    for i in range(20):
        content += f"     PARAM{i+1}                     / Parameter {i+1}\n"

    # NOUTH line (21st non-comment line, where skip_ahead lands)
    content += f"     {nouth}                          / NOUTH\n"

    # After NOUTH, skip_ahead(line_index, lines, 3) skips 3 non-comment lines:
    # NOUTH, FACTXY, and GWHYDOUTFL
    content += "     3.2808                           / FACTXY\n"
    content += "     output.hyd                       / GWHYDOUTFL\n"

    # Comment header before hydrograph data (automatically skipped by skip_ahead)
    content += "C--------------------------------------------------------------------------------------------------\n"
    content += "C  Hydrograph location specifications\n"
    content += "C--------------------------------------------------------------------------------------------------\n"

    # Hydrograph data (consecutive non-comment lines)

    for id, hydtyp, layer, x, y, node, name in hydrograph_data:
        # Format: ID HYDTYP LAYER X Y [NODE] NAME
        # All lines MUST start with whitespace per IWFM convention
        if hydtyp == 0:
            # X-Y coordinates: ID\tHYDTYP\tLAYER\tX\tY\t\tNAME
            # The double tab before NAME (\t\t) represents empty node field
            # When split(), this becomes 6 fields: [ID, HYDTYP, LAYER, X, Y, NAME]
            content += f"    {id}\t{hydtyp}\t{layer}\t{x:.4f}\t{y:.4f}\t\t{name}\n"
        else:
            # Node number: ID\tHYDTYP\tLAYER\t\t\tNODE\tNAME
            # The three tabs represent empty X and Y fields
            # When split(), this becomes 5 fields: [ID, HYDTYP, LAYER, NODE, NAME]
            content += f"    {id}\t{hydtyp}\t{layer}\t\t\t{node}\t{name}\n"

    return content


class TestHydDictFileReading:
    """Tests for file reading logic in hyd_dict function"""

    def test_single_hydrograph(self):
        """Test reading single hydrograph with X-Y coordinates"""
        hydrographs = [
            (1, 0, 1, 592798.7048, 4209815.426, None, "Well_001")
        ]
        content = create_groundwater_file(1, hydrographs)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.hyd_dict import hyd_dict
            well_dict = hyd_dict(temp_file)

            # Verify dictionary has one entry
            assert len(well_dict) == 1
            assert "well_001" in well_dict

            # Verify well info: [column, x, y, layer, name]
            info = well_dict["well_001"]
            assert info[0] == 1  # column number
            assert abs(info[1] - 592798.7048) < 0.01  # x
            assert abs(info[2] - 4209815.426) < 0.01  # y
            assert info[3] == 1  # layer
            assert info[4] == "well_001"  # name

        finally:
            os.unlink(temp_file)

    def test_multiple_hydrographs(self):
        """Test reading multiple hydrographs"""
        hydrographs = [
            (1, 0, 1, 592798.7048, 4209815.426, None, "Well_001"),
            (2, 0, 2, 622426.4231, 4296803.182, None, "Well_002"),
            (3, 0, 3, 588091.0913, 4223057.566, None, "Well_003")
        ]
        content = create_groundwater_file(3, hydrographs)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.hyd_dict import hyd_dict
            well_dict = hyd_dict(temp_file)

            # Verify all hydrographs are in dictionary
            assert len(well_dict) == 3
            assert "well_001" in well_dict
            assert "well_002" in well_dict
            assert "well_003" in well_dict

        finally:
            os.unlink(temp_file)

    def test_hydrograph_with_node_number(self):
        """Test reading hydrograph specified by node number (HYDTYP=1)"""
        hydrographs = [
            (1, 1, 1, None, None, 1304, "Node_1304")
        ]
        content = create_groundwater_file(1, hydrographs)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.hyd_dict import hyd_dict
            well_dict = hyd_dict(temp_file)

            assert len(well_dict) == 1
            assert "node_1304" in well_dict

            info = well_dict["node_1304"]
            assert info[0] == 1  # column
            assert info[1] == 0.0  # x (not available for node format)
            assert info[2] == 0.0  # y (not available for node format)
            assert info[3] == 1  # layer
            assert info[4] == "node_1304"  # name

        finally:
            os.unlink(temp_file)

    def test_mixed_coordinate_types(self):
        """Test reading mix of X-Y coordinates and node numbers"""
        hydrographs = [
            (1, 0, 1, 592798.7048, 4209815.426, None, "Well_XY"),
            (2, 1, 2, None, None, 1304, "Well_Node")
        ]
        content = create_groundwater_file(2, hydrographs)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.hyd_dict import hyd_dict
            well_dict = hyd_dict(temp_file)

            assert len(well_dict) == 2
            assert "well_xy" in well_dict
            assert "well_node" in well_dict

            # Verify X-Y coordinate well
            xy_info = well_dict["well_xy"]
            assert xy_info[0] == 1  # column
            assert abs(xy_info[1] - 592798.7048) < 0.01  # x
            assert abs(xy_info[2] - 4209815.426) < 0.01  # y
            assert xy_info[3] == 1  # layer

            # Verify node number well
            node_info = well_dict["well_node"]
            assert node_info[0] == 2  # column
            assert node_info[1] == 0.0  # x (not available)
            assert node_info[2] == 0.0  # y (not available)
            assert node_info[3] == 2  # layer

        finally:
            os.unlink(temp_file)

    def test_different_layers(self):
        """Test hydrographs in different model layers"""
        hydrographs = [
            (1, 0, 1, 592798.7048, 4209815.426, None, "Layer1_Well"),
            (2, 0, 2, 592798.7048, 4209815.426, None, "Layer2_Well"),
            (3, 0, 3, 592798.7048, 4209815.426, None, "Layer3_Well"),
            (4, 0, 4, 592798.7048, 4209815.426, None, "Layer4_Well")
        ]
        content = create_groundwater_file(4, hydrographs)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.hyd_dict import hyd_dict
            well_dict = hyd_dict(temp_file)

            assert len(well_dict) == 4

            # Verify layers are correctly assigned
            assert well_dict["layer1_well"][3] == 1
            assert well_dict["layer2_well"][3] == 2
            assert well_dict["layer3_well"][3] == 3
            assert well_dict["layer4_well"][3] == 4

        finally:
            os.unlink(temp_file)

    def test_column_numbering(self):
        """Test that column numbers (ID) are correctly assigned"""
        hydrographs = [
            (5, 0, 1, 592798.7048, 4209815.426, None, "Col5"),
            (10, 0, 1, 622426.4231, 4296803.182, None, "Col10"),
            (15, 0, 1, 588091.0913, 4223057.566, None, "Col15")
        ]
        content = create_groundwater_file(3, hydrographs)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.hyd_dict import hyd_dict
            well_dict = hyd_dict(temp_file)

            # Verify column numbers match ID field
            assert well_dict["col5"][0] == 5
            assert well_dict["col10"][0] == 10
            assert well_dict["col15"][0] == 15

        finally:
            os.unlink(temp_file)

    def test_well_name_case_insensitive(self):
        """Test that well names are stored in lowercase"""
        hydrographs = [
            (1, 0, 1, 592798.7048, 4209815.426, None, "UPPERCASE_WELL"),
            (2, 0, 1, 622426.4231, 4296803.182, None, "MixedCase_Well"),
            (3, 0, 1, 588091.0913, 4223057.566, None, "lowercase_well")
        ]
        content = create_groundwater_file(3, hydrographs)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.hyd_dict import hyd_dict
            well_dict = hyd_dict(temp_file)

            # All names should be lowercase
            assert "uppercase_well" in well_dict
            assert "mixedcase_well" in well_dict
            assert "lowercase_well" in well_dict

            # Verify stored names are also lowercase
            assert well_dict["uppercase_well"][4] == "uppercase_well"
            assert well_dict["mixedcase_well"][4] == "mixedcase_well"

        finally:
            os.unlink(temp_file)

    def test_nouth_zero(self):
        """Test file with NOUTH = 0 (no hydrographs)"""
        content = create_groundwater_file(0, [])

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.hyd_dict import hyd_dict
            well_dict = hyd_dict(temp_file)

            # Dictionary should be empty
            assert len(well_dict) == 0

        finally:
            os.unlink(temp_file)

    def test_coordinate_precision(self):
        """Test that coordinates are stored with proper precision"""
        hydrographs = [
            (1, 0, 1, 592798.7048, 4209815.426, None, "Precise_Well")
        ]
        content = create_groundwater_file(1, hydrographs)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.hyd_dict import hyd_dict
            well_dict = hyd_dict(temp_file)

            info = well_dict["precise_well"]
            # Coordinates should be within floating point precision
            assert abs(info[1] - 592798.7048) < 1e-6
            assert abs(info[2] - 4209815.426) < 1e-6

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
