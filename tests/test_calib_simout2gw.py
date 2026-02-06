#!/usr/bin/env python
# test_calib_simout2gw.py
# Unit tests for calib/simout2gw.py
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
from iwfm.calib.simout2gw import read_gw_params, read_gw_file, replace_params, simout2gw


def create_simout_test_file(nodes_data):
    """Create properly structured SimulationMessages.out test file.

    Parameters
    ----------
    nodes_data : list of tuples
        Each tuple: (node_id, [layer1_params, layer2_params, ...])
        Each layer_params: (pkh, ps, pn, pv, pl)

    Returns
    -------
    str
        File content with proper format
    """
    content = "C SimulationMessages.out test file\n"
    content += "C Header information\n"
    content += "C\n"
    content += "----------------------------------------------------------------------------------------------------\n"
    content += "                              AQUIFER PARAMETER VALUES FOR EACH NODE\n"
    content += "            *** Note: Values Below are After Multiplication by Conversion Factors ***\n"
    content += "----------------------------------------------------------------------------------------------------\n"
    content += "   NODE          PKH                       PS                        PN                        PV                        PL\n"

    # Add node data
    for node_id, layers in nodes_data:
        content += f"  {node_id:5d}"
        for i, (pkh, ps, pn, pv, pl) in enumerate(layers):
            if i == 0:
                # First layer on same line as node number
                content += f"     {pkh:15.13f}         {ps:21.15E}    {pn:21.15E}    {pv:21.15E}         {pl:21.15f}\n"
            else:
                # Subsequent layers on new lines with proper indentation
                content += f"            {pkh:15.13f}         {ps:21.15E}    {pn:21.15E}    {pv:21.15E}         {pl:21.15f}\n"

    content += "\n"  # Empty line to end parameter section
    return content


def create_gw_template_file(nouth=0, noutf=0, param_lines_count=0):
    """Create properly structured Groundwater template file.

    Parameters
    ----------
    nouth : int
        Number of hydrograph output points
    noutf : int
        Number of flow output points
    param_lines_count : int
        Number of parameter lines expected

    Returns
    -------
    str
        File content with proper IWFM groundwater format
    """
    content = "C Groundwater main file\n"
    content += "C IWFM Groundwater Package v4.0\n"
    content += "C\n"

    # Add 20 parameter lines (skipped by skip_ahead(1, lines, 20))
    for i in range(20):
        content += f"     PARAM{i+1}                     / Parameter {i+1}\n"

    # NOUTH line
    content += f"     {nouth}                                          / NOUTH\n"

    # FACTXY, GWHYDOUTFL, and comment (3 lines)
    content += "     3.2808                                     / FACTXY\n"
    content += "     output.out                                 / GWHYDOUTFL\n"
    content += "C--------------------------------------------------------------------------------------------------\n"

    # Skip nouth lines (hydrograph data)
    for i in range(nouth):
        content += f"     {i+1}     0     1     100.0     200.0          WELL_{i+1}\n"

    # NOUTF line
    content += f"     {noutf}                                          / NOUTF\n"

    # Skip 7 more lines
    for i in range(7):
        content += f"     FLOWPARAM{i+1}                     / Flow parameter {i+1}\n"

    # Skip noutf lines (flow data)
    for i in range(noutf):
        content += f"     FLOW_{i+1}     data\n"

    # Parameter section header
    content += "C--------------------------------------------------------------------------------------------------\n"
    content += "C                              AQUIFER PARAMETER VALUES\n"
    content += "C--------------------------------------------------------------------------------------------------\n"

    # Placeholder parameter lines
    for i in range(param_lines_count):
        content += f"  OLD_PARAM_LINE_{i+1}\n"

    return content


class TestReadGwParams:
    """Tests for read_gw_params function"""

    def test_single_node_single_layer(self):
        """Test reading single node with single layer"""
        nodes = [
            (25219, [(10.0, 1.6488448517e-03, 5.0e-02, 0.1, 0.5)])
        ]
        content = create_simout_test_file(nodes)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            gw_params = read_gw_params(temp_file)

            assert len(gw_params) == 1
            assert '25219' in gw_params[0]
            assert '10.0000000000000' in gw_params[0]

        finally:
            os.unlink(temp_file)

    def test_single_node_multiple_layers(self):
        """Test reading single node with multiple layers (6 layers)"""
        nodes = [
            (25219, [
                (10.0, 1.6488448517e-03, 5.0e-02, 0.1, 0.5),
                (7.2216131670, 5.167580249427e-05, 8.0e-02, 2.120725652555e-02, 0.722161316705),
                (10.0, 1.0e-03, 8.0e-02, 1.0e-03, 2.0),
                (10.0, 1.0e-03, 8.0e-02, 1.0e-03, 2.0),
                (1.0, 8.0e-05, 8.0e-02, 1.0e-03, 0.3),
                (1.0, 3.0e-04, 8.0e-02, 5.0e-03, 0.8)
            ])
        ]
        content = create_simout_test_file(nodes)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            gw_params = read_gw_params(temp_file)

            # Should have 6 lines (6 layers)
            assert len(gw_params) == 6
            # First line should have node number
            assert '25219' in gw_params[0]
            # Subsequent lines should be indented
            assert gw_params[1].startswith('            ')

        finally:
            os.unlink(temp_file)

    def test_multiple_nodes(self):
        """Test reading multiple nodes"""
        nodes = [
            (25219, [
                (10.0, 1.6488448517e-03, 5.0e-02, 0.1, 0.5),
                (7.2216131670, 5.167580249427e-05, 8.0e-02, 2.120725652555e-02, 0.722161316705)
            ]),
            (25223, [
                (8.0198789420, 1.697432016859e-03, 5.0e-02, 8.019878942002e-02, 0.400993947100),
                (4.1798015028, 5.551114365933e-05, 8.0e-02, 9.804032789419e-03, 0.417980150279)
            ])
        ]
        content = create_simout_test_file(nodes)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            gw_params = read_gw_params(temp_file)

            # Should have 4 lines total (2 nodes × 2 layers)
            assert len(gw_params) == 4
            # Check node numbers present
            assert '25219' in gw_params[0]
            assert '25223' in gw_params[2]

        finally:
            os.unlink(temp_file)

    def test_parameter_values_format(self):
        """Test that parameter values are read in correct format"""
        nodes = [
            (25219, [(10.0, 1.648844851693743e-03, 5.0e-02, 0.1, 0.5)])
        ]
        content = create_simout_test_file(nodes)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            gw_params = read_gw_params(temp_file)

            # Check that scientific notation is preserved
            assert 'E-' in gw_params[0] or 'e-' in gw_params[0].upper()

        finally:
            os.unlink(temp_file)


class TestReadGwFile:
    """Tests for read_gw_file function"""

    def test_basic_gw_file(self):
        """Test reading basic groundwater file"""
        content = create_gw_template_file(nouth=2, noutf=1, param_lines_count=5)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            gw_data, param_line = read_gw_file(temp_file)

            # Verify data was read
            assert isinstance(gw_data, list)
            assert len(gw_data) > 0

            # Verify param_line is valid
            assert isinstance(param_line, int)
            assert param_line >= 0
            assert param_line < len(gw_data)

        finally:
            os.unlink(temp_file)

    def test_no_hydrographs_no_flows(self):
        """Test reading file with no hydrographs or flows"""
        content = create_gw_template_file(nouth=0, noutf=0, param_lines_count=3)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            gw_data, param_line = read_gw_file(temp_file)

            assert isinstance(gw_data, list)
            assert isinstance(param_line, int)

        finally:
            os.unlink(temp_file)


class TestReplaceParams:
    """Tests for replace_params function"""

    def test_replace_single_line(self):
        """Test replacing single parameter line"""
        gw_params = ["  25219     10.0000000000000         1.648844851693743E-003"]
        gw_data = ["line1", "line2", "OLD_PARAM", "line4"]
        param_line = 2

        result = replace_params(gw_params, gw_data, param_line)

        assert len(result) == 4
        assert result[2] == gw_params[0]
        assert result[0] == "line1"  # Other lines unchanged
        assert result[3] == "line4"

    def test_replace_multiple_lines(self):
        """Test replacing multiple parameter lines"""
        gw_params = [
            "  25219     10.0000000000000         1.648844851693743E-003",
            "            7.2216131670487         5.167580249426959E-005",
            "            10.0000000000000         1.000000000000000E-003"
        ]
        gw_data = ["line1", "line2", "OLD_1", "OLD_2", "OLD_3", "line6"]
        param_line = 2

        result = replace_params(gw_params, gw_data, param_line)

        assert len(result) == 6
        assert result[2] == gw_params[0]
        assert result[3] == gw_params[1]
        assert result[4] == gw_params[2]


class TestSimout2gw:
    """Integration tests for simout2gw function"""

    def test_full_workflow(self):
        """Test complete workflow from simout to gw file"""
        # Create simout file
        nodes = [
            (25219, [(10.0, 1.648844851694e-03, 5.0e-02, 0.1, 0.5)]),
            (25223, [(8.0198789420, 1.697432016859e-03, 5.0e-02, 8.019878942e-02, 0.400993947100)])
        ]
        simout_content = create_simout_test_file(nodes)

        # Create gw template file
        gw_template_content = create_gw_template_file(nouth=0, noutf=0, param_lines_count=2)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(simout_content)
            simout_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(gw_template_content)
            gw_in_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            output_file = f.name

        try:
            # Run simout2gw
            simout2gw(simout_file, gw_in_file, output_file)

            # Verify output file was created
            assert os.path.exists(output_file)

            # Read and verify output
            with open(output_file) as f:
                output_data = f.read()

            # Should contain new parameters from simout file
            assert '25219' in output_data
            assert '25223' in output_data

            # Should contain groundwater file header
            assert 'Groundwater' in output_data

        finally:
            os.unlink(simout_file)
            os.unlink(gw_in_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    @pytest.mark.skip(reason="Large real-world file test - run manually if file exists")
    def test_with_actual_files(self):
        """Test with actual simout2gw test files if they exist"""
        simout_file = '/Volumes/MinEx/Documents/Dropbox/work/Programing/repos/iwfm-py/iwfm-tests/simout2gw/SimulationMessages.out'
        gw_in_file = '/Volumes/MinEx/Documents/Dropbox/work/Programing/repos/iwfm-py/iwfm-tests/simout2gw/C2V-Kern-Subbasin_GW1985.dat'

        if not os.path.exists(simout_file):
            pytest.skip(f"Test file not found: {simout_file}")
        if not os.path.exists(gw_in_file):
            pytest.skip(f"Test file not found: {gw_in_file}")

        # Read parameters
        gw_params = read_gw_params(simout_file)

        # Should have parameter data
        assert isinstance(gw_params, list)
        assert len(gw_params) > 0

        # Verify format
        assert any('NODE' not in line and len(line.split()) > 1 for line in gw_params)

        # Read gw file
        gw_data, param_line = read_gw_file(gw_in_file)

        # Should have data
        assert isinstance(gw_data, list)
        assert len(gw_data) > 0
        assert param_line >= 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
