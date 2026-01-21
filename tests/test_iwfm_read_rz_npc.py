#!/usr/bin/env python
# test_iwfm_read_rz_npc.py
# Unit tests for iwfm_read_rz_npc.py
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


# NOTE: The iwfm_read_rz_npc function reads a very complex file structure with:
# - Multiple interleaved parameter tables
# - File names scattered throughout the file
# - Dynamic element counting by searching for 'C' markers
# - Calls to iwfm_read_param_table_ints and iwfm_read_param_table_floats
# This makes comprehensive mock-based testing challenging. The tests below
# verify the basic structure and return types using simplified data.


class TestIwfmReadRzNpc:
    """Tests for iwfm_read_rz_npc function"""

    def test_basic_structure_with_real_file(self):
        """Test basic file structure reading with simplified real-world format"""
        # This test uses a simplified version that mimics the real file structure
        content = "C IWFM Non-Ponded Crop Data File\n"
        content += "C\n"
        content += " 2                                 / NCROP\n"
        content += " 1                                  / FLDMD\n"
        content += "C\n"
        content += " GR         / CCODE[ 1]  Grain\n"
        content += " CO         / CCODE[ 2]  Cotton\n"
        content += "C\n"
        content += " Area.dat           / LUFLNP\n"
        content += "C\n"
        content += " 0                                  / NBCROP\n"
        content += "C\n"
        content += "                 / CLWUBUDFL\n"
        content += "                 / CRZBUDFL\n"
        content += "C\n"
        content += " RootDepth.dat      / RZFRACFL\n"
        content += " 1.0                                                     / FACT\n"
        content += "C\n"
        content += "     1      4.0         1        / ROOTCP[ 1]     Grains\n"
        content += "     2      6.0         2        / ROOTCP[ 2]     Cotton\n"
        content += "C\n"
        # Element data - curve numbers
        content += " 0\t50\t47\n"  # IE=0 means all elements use these values
        content += "C\n"
        # ET
        content += " 0\t1\t1\n"
        content += "C\n"
        # Water supply
        content += " 0\t1\t1\n"
        content += "C\n"
        # Irrigation period
        content += " 0\t1\t1\n"
        content += "C\n"
        # Minimum soil moisture file
        content += " MinSoil.dat                / MSFL\n"
        content += " 0\t1\t1\n"
        content += "C\n"
        # Target soil moisture file
        content += " TargetSoil.dat                / TSFL\n"
        content += " 0\t1\t1\n"
        content += "C\n"
        # Return flow fractions
        content += " 0\t1\t1\n"
        content += "C\n"
        # Reuse fractions
        content += " 0\t1\t1\n"
        content += "C\n"
        # Minimum deep percolation file
        content += " MinDeepPerc.dat                / MDFL\n"
        content += "C\n"
        # Initial conditions
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_npc import iwfm_read_rz_npc

            crops, params, files = iwfm_read_rz_npc(temp_file, verbose=False)

            # Verify crops
            assert len(crops) == 2
            assert crops[0] == 'GR'
            assert crops[1] == 'CO'

            # Verify params structure (9 parameter sets)
            assert len(params) == 9
            cn, et, wsp, ip, ms, ts, rf, ru, ic = params

            # Verify files (7 file names)
            assert len(files) == 7
            assert os.path.basename(files[0]) == 'Area.dat'
            assert os.path.basename(files[3]) == 'RootDepth.dat'
            assert os.path.basename(files[4]) == 'MinSoil.dat'
            assert os.path.basename(files[5]) == 'TargetSoil.dat'
            assert os.path.basename(files[6]) == 'MinDeepPerc.dat'

        finally:
            os.unlink(temp_file)

    def test_return_structure(self):
        """Test that function returns correct tuple structure"""
        content = "C IWFM Non-Ponded Crop Data File\n"
        content += " 1                                 / NCROP\n"
        content += " 1                                  / FLDMD\n"
        content += " GR         / CCODE[ 1]\n"
        content += " Area.dat           / LUFLNP\n"
        content += " 0                                  / NBCROP\n"
        content += "                 / CLWUBUDFL\n"
        content += "                 / CRZBUDFL\n"
        content += " RootDepth.dat      / RZFRACFL\n"
        content += " 1.0                                                     / FACT\n"
        content += "     1      4.0         1        / ROOTCP[ 1]\n"
        content += "C\n"
        content += " 0\t50\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " MinSoil.dat                / MSFL\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " TargetSoil.dat                / TSFL\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " MinDeepPerc.dat                / MDFL\n"
        content += "C\n"
        content += " 0\t0.5\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_npc import iwfm_read_rz_npc

            result = iwfm_read_rz_npc(temp_file, verbose=False)

            # Verify return type
            assert isinstance(result, tuple)
            assert len(result) == 3

            crops, params, files = result

            # Verify crops is list
            assert isinstance(crops, list)

            # Verify params is list of 9 elements
            assert isinstance(params, list)
            assert len(params) == 9

            # Verify files is list of 7 elements
            assert isinstance(files, list)
            assert len(files) == 7

        finally:
            os.unlink(temp_file)

    def test_multiple_crops(self):
        """Test reading file with multiple crops"""
        content = "C IWFM Non-Ponded Crop Data File\n"
        content += " 3                                 / NCROP\n"
        content += " 0                                  / FLDMD\n"
        content += " GR         / CCODE[ 1]  Grain\n"
        content += " CO         / CCODE[ 2]  Cotton\n"
        content += " SB         / CCODE[ 3]  Sugar Beets\n"
        content += " Area.dat           / LUFLNP\n"
        content += " 0                                  / NBCROP\n"
        content += "                 / CLWUBUDFL\n"
        content += "                 / CRZBUDFL\n"
        content += " RootDepth.dat      / RZFRACFL\n"
        content += " 1.0                                                     / FACT\n"
        content += "     1      4.0         1        / ROOTCP[ 1]\n"
        content += "     2      6.0         2        / ROOTCP[ 2]\n"
        content += "     3      5.0         3        / ROOTCP[ 3]\n"
        content += "C\n"
        content += " 0\t50\t47\t52\n"
        content += "C\n"
        content += " 0\t1\t1\t1\n"
        content += "C\n"
        content += " 0\t1\t1\t1\n"
        content += "C\n"
        content += " 0\t1\t1\t1\n"
        content += "C\n"
        content += " MinSoil.dat                / MSFL\n"
        content += " 0\t1\t1\t1\n"
        content += "C\n"
        content += " TargetSoil.dat                / TSFL\n"
        content += " 0\t1\t1\t1\n"
        content += "C\n"
        content += " 0\t1\t1\t1\n"
        content += "C\n"
        content += " 0\t1\t1\t1\n"
        content += "C\n"
        content += " MinDeepPerc.dat                / MDFL\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\t0.4\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_npc import iwfm_read_rz_npc

            crops, params, files = iwfm_read_rz_npc(temp_file, verbose=False)

            # Verify crops
            assert len(crops) == 3
            assert crops[0] == 'GR'
            assert crops[1] == 'CO'
            assert crops[2] == 'SB'

        finally:
            os.unlink(temp_file)


    def test_verbose_mode(self):
        """Test verbose mode doesn't affect functionality"""
        content = "C IWFM Non-Ponded Crop Data File\n"
        content += " 1                                 / NCROP\n"
        content += " 1                                  / FLDMD\n"
        content += " GR         / CCODE[ 1]\n"
        content += " Area.dat           / LUFLNP\n"
        content += " 0                                  / NBCROP\n"
        content += "                 / CLWUBUDFL\n"
        content += "                 / CRZBUDFL\n"
        content += " RootDepth.dat      / RZFRACFL\n"
        content += " 1.0                                                     / FACT\n"
        content += "     1      4.0         1        / ROOTCP[ 1]\n"
        content += "C\n"
        content += " 0\t50\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " MinSoil.dat                / MSFL\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " TargetSoil.dat                / TSFL\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " MinDeepPerc.dat                / MDFL\n"
        content += "C\n"
        content += " 0\t0.5\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_npc import iwfm_read_rz_npc

            # Test with verbose=True
            crops, params, files = iwfm_read_rz_npc(temp_file, verbose=True)

            # Verify data is still read correctly
            assert len(crops) == 1
            assert crops[0] == 'GR'

        finally:
            os.unlink(temp_file)

    def test_different_conversion_factor(self):
        """Test with different conversion factor"""
        content = "C IWFM Non-Ponded Crop Data File\n"
        content += " 1                                 / NCROP\n"
        content += " 1                                  / FLDMD\n"
        content += " GR         / CCODE[ 1]\n"
        content += " Area.dat           / LUFLNP\n"
        content += " 0                                  / NBCROP\n"
        content += "                 / CLWUBUDFL\n"
        content += "                 / CRZBUDFL\n"
        content += " RootDepth.dat      / RZFRACFL\n"
        content += " 3.2808                                                  / FACT\n"
        content += "     1      4.0         1        / ROOTCP[ 1]\n"
        content += "C\n"
        content += " 0\t50\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " MinSoil.dat                / MSFL\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " TargetSoil.dat                / TSFL\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " MinDeepPerc.dat                / MDFL\n"
        content += "C\n"
        content += " 0\t0.5\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_npc import iwfm_read_rz_npc

            crops, params, files = iwfm_read_rz_npc(temp_file, verbose=False)

            # Verify data is read correctly with different factor
            assert len(crops) == 1
            assert crops[0] == 'GR'

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Non-Ponded Crop Data File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += " 1                                 / NCROP\n"
        content += "C More comments\n"
        content += " 1                                  / FLDMD\n"
        content += "# Comment\n"
        content += " GR         / CCODE[ 1]\n"
        content += "C\n"
        content += " Area.dat           / LUFLNP\n"
        content += " 0                                  / NBCROP\n"
        content += "C\n"
        content += "                 / CLWUBUDFL\n"
        content += "                 / CRZBUDFL\n"
        content += " RootDepth.dat      / RZFRACFL\n"
        content += " 1.0                                                     / FACT\n"
        content += "     1      4.0         1        / ROOTCP[ 1]\n"
        content += "C\n"
        content += " 0\t50\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " MinSoil.dat                / MSFL\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " TargetSoil.dat                / TSFL\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " 0\t1\n"
        content += "C\n"
        content += " MinDeepPerc.dat                / MDFL\n"
        content += "C\n"
        content += " 0\t0.5\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_npc import iwfm_read_rz_npc

            crops, params, files = iwfm_read_rz_npc(temp_file, verbose=False)

            # Should read correctly despite comment lines
            assert len(crops) == 1
            assert crops[0] == 'GR'

        finally:
            os.unlink(temp_file)
