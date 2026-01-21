#!/usr/bin/env python
# test_iwfm_read_rz_nr.py
# Unit tests for iwfm_read_rz_nr.py
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


class TestIwfmReadRzNr:
    """Tests for iwfm_read_rz_nr function"""

    def test_basic_structure(self):
        """Test reading basic native and riparian vegetation file"""
        content = "C IWFM Native and Riparian Vegetation Data File\n"
        content += "C\n"
        content += " NativeVeg_Area.dat                     / LUFLNVRV\n"
        content += "C\n"
        content += " 1.0                   / FACT\n"
        content += " 5.0                   / ROOTNV\n"
        content += " 5.0                   / ROOTRV\n"
        content += "C\n"
        # Element data - IE=0 means all elements use these values
        content += " 0\t38\t32\t484\t505\t313\n"
        content += "C\n"
        # Initial conditions
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_nr import iwfm_read_rz_nr

            crops, params, files = iwfm_read_rz_nr(temp_file, verbose=False)

            # Verify crops
            assert len(crops) == 2
            assert crops[0] == 'nat_rip'
            assert crops[1] == 'ic'

            # Verify params structure (2 parameter sets)
            assert len(params) == 2

            # Verify files (1 file name)
            assert len(files) == 1
            assert os.path.basename(files[0]) == 'NativeVeg_Area.dat'

        finally:
            os.unlink(temp_file)

    def test_return_structure(self):
        """Test that function returns correct tuple structure"""
        content = "C IWFM Native and Riparian Vegetation Data File\n"
        content += " NativeVeg_Area.dat                     / LUFLNVRV\n"
        content += " 1.0                   / FACT\n"
        content += " 5.0                   / ROOTNV\n"
        content += " 5.0                   / ROOTRV\n"
        content += "C\n"
        content += " 0\t38\t32\t484\t505\t313\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_nr import iwfm_read_rz_nr

            result = iwfm_read_rz_nr(temp_file, verbose=False)

            # Verify return type
            assert isinstance(result, tuple)
            assert len(result) == 3

            crops, params, files = result

            # Verify crops is list of 2 elements
            assert isinstance(crops, list)
            assert len(crops) == 2

            # Verify params is list of 2 elements
            assert isinstance(params, list)
            assert len(params) == 2

            # Verify files is list of 1 element
            assert isinstance(files, list)
            assert len(files) == 1

        finally:
            os.unlink(temp_file)


    def test_different_conversion_factor(self):
        """Test with different conversion factor"""
        content = "C IWFM Native and Riparian Vegetation Data File\n"
        content += " NativeVeg_Area.dat                     / LUFLNVRV\n"
        content += " 3.2808                / FACT\n"
        content += " 5.0                   / ROOTNV\n"
        content += " 5.0                   / ROOTRV\n"
        content += "C\n"
        content += " 0\t38\t32\t484\t505\t313\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_nr import iwfm_read_rz_nr

            crops, params, files = iwfm_read_rz_nr(temp_file, verbose=False)

            # Verify data is read correctly with different factor
            assert len(crops) == 2
            assert crops[0] == 'nat_rip'

        finally:
            os.unlink(temp_file)

    def test_different_rooting_depths(self):
        """Test with different rooting depths"""
        content = "C IWFM Native and Riparian Vegetation Data File\n"
        content += " NativeVeg_Area.dat                     / LUFLNVRV\n"
        content += " 1.0                   / FACT\n"
        content += " 3.0                   / ROOTNV\n"
        content += " 7.0                   / ROOTRV\n"
        content += "C\n"
        content += " 0\t38\t32\t484\t505\t313\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_nr import iwfm_read_rz_nr

            crops, params, files = iwfm_read_rz_nr(temp_file, verbose=False)

            # Verify data is read correctly
            assert len(crops) == 2

        finally:
            os.unlink(temp_file)

    def test_verbose_mode(self):
        """Test verbose mode doesn't affect functionality"""
        content = "C IWFM Native and Riparian Vegetation Data File\n"
        content += " NativeVeg_Area.dat                     / LUFLNVRV\n"
        content += " 1.0                   / FACT\n"
        content += " 5.0                   / ROOTNV\n"
        content += " 5.0                   / ROOTRV\n"
        content += "C\n"
        content += " 0\t38\t32\t484\t505\t313\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_nr import iwfm_read_rz_nr

            # Test with verbose=True
            crops, params, files = iwfm_read_rz_nr(temp_file, verbose=True)

            # Verify data is still read correctly
            assert len(crops) == 2
            assert crops[0] == 'nat_rip'
            assert crops[1] == 'ic'

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Native and Riparian Vegetation Data File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += " NativeVeg_Area.dat                     / LUFLNVRV\n"
        content += "C More comments\n"
        content += " 1.0                   / FACT\n"
        content += "# Comment\n"
        content += " 5.0                   / ROOTNV\n"
        content += "C\n"
        content += " 5.0                   / ROOTRV\n"
        content += "C\n"
        content += " 0\t38\t32\t484\t505\t313\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_nr import iwfm_read_rz_nr

            crops, params, files = iwfm_read_rz_nr(temp_file, verbose=False)

            # Should read correctly despite comment lines
            assert len(crops) == 2
            assert crops[0] == 'nat_rip'

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM C2VSimCG file"""
        content = "C*******************************************************************************\n"
        content += "C                  INTEGRATED WATER FLOW MODEL (IWFM)\n"
        content += "C*******************************************************************************\n"
        content += "C\n"
        content += " RootZone\\C2VSimCG_NativeVeg_Area.dat                     / LUFLNVRV\n"
        content += "C\n"
        content += " 1.0                   / FACT\n"
        content += " 5.0                   / ROOTNV\n"
        content += " 5.0                   / ROOTRV\n"
        content += "C\n"
        content += " 0\t38\t32\t484\t505\t313\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_nr import iwfm_read_rz_nr

            crops, params, files = iwfm_read_rz_nr(temp_file, verbose=False)

            # Verify data structure
            assert len(crops) == 2
            assert crops[0] == 'nat_rip'
            assert crops[1] == 'ic'

            # Verify file name (path is not stripped by the function)
            assert 'C2VSimCG_NativeVeg_Area.dat' in files[0]

        finally:
            os.unlink(temp_file)

    def test_area_file_path_handling(self):
        """Test handling of area file path"""
        content = "C IWFM Native and Riparian Vegetation Data File\n"
        content += " ../Data/NativeVeg_Area.dat                     / LUFLNVRV\n"
        content += " 1.0                   / FACT\n"
        content += " 5.0                   / ROOTNV\n"
        content += " 5.0                   / ROOTRV\n"
        content += "C\n"
        content += " 0\t38\t32\t484\t505\t313\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_nr import iwfm_read_rz_nr

            crops, params, files = iwfm_read_rz_nr(temp_file, verbose=False)

            # Verify file path is read
            assert 'NativeVeg_Area.dat' in files[0]

        finally:
            os.unlink(temp_file)

    def test_zero_stream_node(self):
        """Test handling of zero stream node (no stream access)"""
        content = "C IWFM Native and Riparian Vegetation Data File\n"
        content += " NativeVeg_Area.dat                     / LUFLNVRV\n"
        content += " 1.0                   / FACT\n"
        content += " 5.0                   / ROOTNV\n"
        content += " 5.0                   / ROOTRV\n"
        content += "C\n"
        content += " 0\t45\t40\t484\t505\t0\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_nr import iwfm_read_rz_nr

            crops, params, files = iwfm_read_rz_nr(temp_file, verbose=False)

            # Should read correctly with zero stream nodes
            assert len(crops) == 2

        finally:
            os.unlink(temp_file)
