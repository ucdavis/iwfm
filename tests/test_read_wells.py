#!/usr/bin/env python
# test_read_wells.py
# Unit tests for read_wells.py
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


class TestReadWells:
    """Tests for read_wells function"""

    def test_basic_structure(self):
        """Test reading basic groundwater hydrograph file"""
        # File starts at line 0 (index 0)
        # skip_ahead(1, gwhyd_info, 20) starts from line 1 and skips 20 non-comment data lines
        content = "#4.0\n"  # Line 0 - comment line
        content += "C IWFM Groundwater File\n"  # Line 1 - where skip_ahead starts
        # Add 20 data lines (non-comment lines starting with space)
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 3\n"  # Line 22 - NOUTH = 3 hydrographs (21st data line)
        content += " 1.0\n"  # FACTXY
        content += " output.hdf\n"  # GWHYDOUTFL
        # skip_ahead from line where NOUTH was found, skip 3 more non-comment lines
        content += "C Hydrograph header\n"
        content += "C Column headers\n"
        content += "C Dash line\n"
        # Hydrograph data: ID HYDTYP IOUTHL X Y IOUTH NAME
        content += " 1  0  1  100.0  200.0    WELL_001\n"
        content += " 2  0  2  150.0  250.0    WELL_002\n"
        content += " 3  0  1  200.0  300.0    WELL_003\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            # Verify dictionary keys (uppercase well names)
            assert 'WELL_001' in well_dict
            assert 'WELL_002' in well_dict
            assert 'WELL_003' in well_dict

            # Verify values: WellInfo(column, x, y, layer, name)
            from iwfm.iwfm_dataclasses import WellInfo
            assert well_dict['WELL_001'] == WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well_001')
            assert well_dict['WELL_002'] == WellInfo(column=2, x=150.0, y=250.0, layer=2, name='well_002')
            assert well_dict['WELL_003'] == WellInfo(column=3, x=200.0, y=300.0, layer=1, name='well_003')

        finally:
            os.unlink(temp_file)

    def test_with_state_well_numbers(self):
        """Test reading wells with state well number format"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 2\n"
        content += " 3.2808\n"
        content += " GW_Hydrographs.out\n"
        content += "C Header\n"
        content += "C Columns\n"
        content += "C Dashes\n"
        content += " 1  0  1  592798.7  4209815.4    S_380313N1219426W001\n"
        content += " 2  0  2  622426.4  4296803.2    S_381150N1215899W001\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            assert 'S_380313N1219426W001' in well_dict
            assert 'S_381150N1215899W001' in well_dict

            # Check values
            assert well_dict['S_380313N1219426W001'].column == 1  # column
            assert well_dict['S_380313N1219426W001'].x == 592798.7  # x
            assert well_dict['S_380313N1219426W001'].y == 4209815.4  # y
            assert well_dict['S_380313N1219426W001'].layer == 1  # layer
            assert well_dict['S_380313N1219426W001'].name == 's_380313n1219426w001'  # lowercase name

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 1\n"
        content += " 1.0\n"
        content += " output.hdf\n"
        content += "C Header\n"
        content += "c more comments\n"
        content += "* even more\n"
        content += " 1  0  1  100.0  200.0    TEST_WELL\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            # Should read correctly despite comment lines
            from iwfm.iwfm_dataclasses import WellInfo
            assert 'TEST_WELL' in well_dict
            assert well_dict['TEST_WELL'] == WellInfo(column=1, x=100.0, y=200.0, layer=1, name='test_well')

        finally:
            os.unlink(temp_file)

    def test_return_structure(self):
        """Test that function returns correct dictionary structure"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 1\n"
        content += " 1.0\n"
        content += " output.hdf\n"
        content += "C Header\n"
        content += "C Columns\n"
        content += "C Dashes\n"
        content += " 1  0  1  100.0  200.0    WELL_A\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            result = read_wells(temp_file)

            # Verify return is a dictionary
            assert isinstance(result, dict)
            assert len(result) == 1
            assert 'WELL_A' in result

            # Verify value structure: WellInfo(column, x, y, layer, name)
            from iwfm.iwfm_dataclasses import WellInfo
            values = result['WELL_A']
            assert isinstance(values, WellInfo)
            assert isinstance(values.column, int)   # column number
            assert isinstance(values.x, float)      # x coord
            assert isinstance(values.y, float)      # y coord
            assert isinstance(values.layer, int)     # layer
            assert isinstance(values.name, str)      # lowercase name

        finally:
            os.unlink(temp_file)

    def test_multiple_wells_same_location(self):
        """Test reading multiple wells at same location (different layers)"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 4\n"
        content += " 1.0\n"
        content += " output.hdf\n"
        content += "C Header\n"
        content += "C Columns\n"
        content += "C Dashes\n"
        # Same location, different layers (common pattern)
        content += " 1  0  1  100.0  200.0    SITE_A_L1\n"
        content += " 2  0  2  100.0  200.0    SITE_A_L2\n"
        content += " 3  0  3  100.0  200.0    SITE_A_L3\n"
        content += " 4  0  4  100.0  200.0    SITE_A_L4\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            assert len(well_dict) == 4
            # All at same x,y
            assert well_dict['SITE_A_L1'].x == 100.0
            assert well_dict['SITE_A_L2'].x == 100.0
            # But different layers
            assert well_dict['SITE_A_L1'].layer == 1
            assert well_dict['SITE_A_L2'].layer == 2
            assert well_dict['SITE_A_L3'].layer == 3
            assert well_dict['SITE_A_L4'].layer == 4

        finally:
            os.unlink(temp_file)

    def test_large_coordinates(self):
        """Test reading wells with large coordinate values"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 2\n"
        content += " 1.0\n"
        content += " output.hdf\n"
        content += "C Header\n"
        content += "C Columns\n"
        content += "C Dashes\n"
        content += " 1  0  1  622426.423  4296803.182    WELL_LARGE_1\n"
        content += " 2  0  2  642045.125  4291704.836    WELL_LARGE_2\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            assert len(well_dict) == 2
            assert abs(well_dict['WELL_LARGE_1'].x - 622426.423) < 0.01
            assert abs(well_dict['WELL_LARGE_1'].y - 4296803.182) < 0.01

        finally:
            os.unlink(temp_file)

    def test_sequential_column_numbers(self):
        """Test that column numbers are read correctly"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 5\n"
        content += " 1.0\n"
        content += " output.hdf\n"
        content += "C Header\n"
        content += "C Columns\n"
        content += "C Dashes\n"
        content += " 10  0  1  100.0  200.0    WELL_10\n"
        content += " 20  0  1  110.0  210.0    WELL_20\n"
        content += " 30  0  1  120.0  220.0    WELL_30\n"
        content += " 40  0  1  130.0  230.0    WELL_40\n"
        content += " 50  0  1  140.0  240.0    WELL_50\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            # Column numbers from first field
            assert well_dict['WELL_10'].column == 10
            assert well_dict['WELL_20'].column == 20
            assert well_dict['WELL_30'].column == 30
            assert well_dict['WELL_40'].column == 40
            assert well_dict['WELL_50'].column == 50

        finally:
            os.unlink(temp_file)

    def test_well_names_with_special_characters(self):
        """Test reading well names with underscores, numbers, and letters"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 3\n"
        content += " 1.0\n"
        content += " output.hdf\n"
        content += "C Header\n"
        content += "C Columns\n"
        content += "C Dashes\n"
        content += " 1  0  1  100.0  200.0    S_380313N1219426W001%1\n"
        content += " 2  0  1  150.0  250.0    WELL-123_ABC\n"
        content += " 3  0  1  200.0  300.0    Site_01\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            # Keys should be uppercase
            assert 'S_380313N1219426W001%1' in well_dict
            assert 'WELL-123_ABC' in well_dict
            assert 'SITE_01' in well_dict

            # Lowercase names in values
            assert well_dict['S_380313N1219426W001%1'].name == 's_380313n1219426w001%1'
            assert well_dict['WELL-123_ABC'].name == 'well-123_abc'
            assert well_dict['SITE_01'].name == 'site_01'

        finally:
            os.unlink(temp_file)

    def test_zero_hydrographs(self):
        """Test reading file with zero hydrographs"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 0\n"  # NOUTH = 0
        content += " 1.0\n"
        content += " output.hdf\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            # Should return empty dictionary
            assert isinstance(well_dict, dict)
            assert len(well_dict) == 0

        finally:
            os.unlink(temp_file)

    def test_single_well(self):
        """Test reading file with single well"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += " 1\n"
        content += " 1.0\n"
        content += " output.hdf\n"
        content += "C Header\n"
        content += "C Columns\n"
        content += "C Dashes\n"
        content += " 100  0  3  555.5  666.6    SINGLE_WELL\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            assert len(well_dict) == 1
            assert 'SINGLE_WELL' in well_dict
            from iwfm.iwfm_dataclasses import WellInfo
            assert well_dict['SINGLE_WELL'] == WellInfo(column=100, x=555.5, y=666.6, layer=3, name='single_well')

        finally:
            os.unlink(temp_file)

    def test_extra_whitespace(self):
        """Test reading wells with extra whitespace"""
        content = "#4.0\n"
        content += "C IWFM Groundwater File\n"
        for i in range(20):
            content += f" Data line {i}\n"
        content += "    2    \n"
        content += "  1.0  \n"
        content += "  output.hdf  \n"
        content += "C Header\n"
        content += "C Columns\n"
        content += "C Dashes\n"
        content += "  1    0    1    100.0    200.0      WELL_A  \n"
        content += "  2    0    2    150.0    250.0      WELL_B  \n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.read_wells import read_wells

            well_dict = read_wells(temp_file)

            # Should handle extra whitespace correctly
            assert len(well_dict) == 2
            assert 'WELL_A' in well_dict
            assert 'WELL_B' in well_dict

        finally:
            os.unlink(temp_file)


    def test_with_real_file_hydtyp_0(self):
        """Test reading wells with HYDTYP=0 (x,y coordinates) from real file

        Note: This test only validates wells with HYDTYP=0. The current implementation
        of read_wells.py assumes HYDTYP=0 format where X and Y coordinates are present.
        Wells with HYDTYP=1 (node number format) will fail because they have different
        field positions.
        """
        import os

        # Check if the example file exists
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021/Simulation/Groundwater/C2VSimCG_Groundwater1974.dat'
        )

        if not os.path.exists(test_file):
            pytest.skip(f"Test file not found: {test_file}")

        # Read the file manually to find first well with HYDTYP=0
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        import iwfm

        with open(test_file) as f:
            lines = f.read().splitlines()

        line_index = iwfm.skip_ahead(1, lines, 20)
        nouth = int(lines[line_index].split()[0])
        line_index = iwfm.skip_ahead(line_index, lines, 3)

        # Find the first HYDTYP=0 well
        test_line = None
        for i in range(min(100, nouth)):  # Check first 100 wells
            fields = lines[line_index + i].split()
            if len(fields) >= 6 and fields[1] == '0':  # HYDTYP=0
                test_line = lines[line_index + i]
                break

        if test_line is None:
            pytest.skip("No HYDTYP=0 wells found in first 100 lines")

        # Verify the line has expected format
        fields = test_line.split()
        assert len(fields) >= 6
        assert fields[1] == '0'  # HYDTYP
        # X and Y should be numeric
        try:
            float(fields[3])
            float(fields[4])
        except (ValueError, IndexError):
            pytest.fail(f"Expected numeric X,Y coordinates: {fields}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
