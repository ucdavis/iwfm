#!/usr/bin/env python
# test_iwfm_read_rz_pc.py
# Unit tests for iwfm_read_rz_pc.py
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


class TestIwfmReadRzPc:
    """Tests for iwfm_read_rz_pc function"""

    def test_basic_structure(self):
        """Test reading basic ponded crop file"""
        content = "C IWFM Ponded Crop Data File\n"
        content += "C\n"
        content += " PondedCrop_Area.dat                     / LUFLP\n"
        content += "C\n"
        content += " 0                                                 / NBCROP\n"
        content += "                                                   / CLWUBUDFL\n"
        content += "                                                   / CRZBUDFL\n"
        content += "C\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTRI_NFL\n"
        content += " 2.0                   / ROOTRI_FL\n"
        content += " 2.0                   / ROOTRI_NDC\n"
        content += " 2.0                   / ROOTRF_SL\n"
        content += " 2.0                   / ROOTRF_PR\n"
        content += "C\n"
        # Curve numbers - IE=0 means all elements use these values
        content += " 0\t53\t53\t53\t53\t53\n"
        content += "C\n"
        # ET parameters
        content += " 0\t41\t41\t41\t41\t41\n"
        content += "C\n"
        # Water supply requirement
        content += " 0\t509\t509\t509\t509\t509\n"
        content += "C\n"
        # Irrigation period
        content += " 0\t501\t501\t501\t501\t501\n"
        content += "C\n"
        # Operations input files
        content += " PondingDepth.dat                   / PNDTHFL\n"
        content += " PondingOps.dat                     / FLOWFL\n"
        content += "C\n"
        # Ponding depth column numbers
        content += " 0\t1\t2\t3\t4\t5\n"
        content += "C\n"
        # Application depth column numbers
        content += " 0\t11\n"
        content += "C\n"
        # Return flow fractions
        content += " 0\t312\t312\t312\t312\t312\n"
        content += "C\n"
        # Reuse fractions
        content += " 0\t321\t321\t321\t321\t321\n"
        content += "C\n"
        # Initial conditions
        content += " 0\t0.5\t0.6\t0.7\t0.8\t0.9\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_pc import iwfm_read_rz_pc

            crops, params, files = iwfm_read_rz_pc(temp_file, verbose=False)

            # Verify crops
            assert len(crops) == 5
            assert crops[0] == 'ri_n'
            assert crops[1] == 'ri_f'
            assert crops[2] == 'ri_d'
            assert crops[3] == 'rf_sl'
            assert crops[4] == 'rf_pr'

            # Verify params structure (9 parameter sets)
            assert len(params) == 9

            # Verify files (5 file names)
            assert len(files) == 5
            assert os.path.basename(files[0]) == 'PondedCrop_Area.dat'

        finally:
            os.unlink(temp_file)

    def test_return_structure(self):
        """Test that function returns correct tuple structure"""
        content = "C IWFM Ponded Crop Data File\n"
        content += " PondedCrop_Area.dat                     / LUFLP\n"
        content += " 0                                                 / NBCROP\n"
        content += "                                                   / CLWUBUDFL\n"
        content += "                                                   / CRZBUDFL\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTRI_NFL\n"
        content += " 2.0                   / ROOTRI_FL\n"
        content += " 2.0                   / ROOTRI_NDC\n"
        content += " 2.0                   / ROOTRF_SL\n"
        content += " 2.0                   / ROOTRF_PR\n"
        content += "C\n"
        content += " 0\t53\t53\t53\t53\t53\n"
        content += "C\n"
        content += " 0\t41\t41\t41\t41\t41\n"
        content += "C\n"
        content += " 0\t509\t509\t509\t509\t509\n"
        content += "C\n"
        content += " 0\t501\t501\t501\t501\t501\n"
        content += "C\n"
        content += " PondingDepth.dat                   / PNDTHFL\n"
        content += " PondingOps.dat                     / FLOWFL\n"
        content += "C\n"
        content += " 0\t1\t2\t3\t4\t5\n"
        content += "C\n"
        content += " 0\t11\n"
        content += "C\n"
        content += " 0\t312\t312\t312\t312\t312\n"
        content += "C\n"
        content += " 0\t321\t321\t321\t321\t321\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\t0.7\t0.8\t0.9\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_pc import iwfm_read_rz_pc

            result = iwfm_read_rz_pc(temp_file, verbose=False)

            # Verify return type
            assert isinstance(result, tuple)
            assert len(result) == 3

            crops, params, files = result

            # Verify crops is list of 5 elements
            assert isinstance(crops, list)
            assert len(crops) == 5

            # Verify params is list of 9 elements
            assert isinstance(params, list)
            assert len(params) == 9

            # Verify files is list of 5 elements
            assert isinstance(files, list)
            assert len(files) == 5

        finally:
            os.unlink(temp_file)

    def test_different_conversion_factor(self):
        """Test with different conversion factor"""
        content = "C IWFM Ponded Crop Data File\n"
        content += " PondedCrop_Area.dat                     / LUFLP\n"
        content += " 0                                                 / NBCROP\n"
        content += "                                                   / CLWUBUDFL\n"
        content += "                                                   / CRZBUDFL\n"
        content += " 3.2808                / FACT\n"
        content += " 2.0                   / ROOTRI_NFL\n"
        content += " 2.0                   / ROOTRI_FL\n"
        content += " 2.0                   / ROOTRI_NDC\n"
        content += " 2.0                   / ROOTRF_SL\n"
        content += " 2.0                   / ROOTRF_PR\n"
        content += "C\n"
        content += " 0\t53\t53\t53\t53\t53\n"
        content += "C\n"
        content += " 0\t41\t41\t41\t41\t41\n"
        content += "C\n"
        content += " 0\t509\t509\t509\t509\t509\n"
        content += "C\n"
        content += " 0\t501\t501\t501\t501\t501\n"
        content += "C\n"
        content += " PondingDepth.dat                   / PNDTHFL\n"
        content += " PondingOps.dat                     / FLOWFL\n"
        content += "C\n"
        content += " 0\t1\t2\t3\t4\t5\n"
        content += "C\n"
        content += " 0\t11\n"
        content += "C\n"
        content += " 0\t312\t312\t312\t312\t312\n"
        content += "C\n"
        content += " 0\t321\t321\t321\t321\t321\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\t0.7\t0.8\t0.9\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_pc import iwfm_read_rz_pc

            crops, params, files = iwfm_read_rz_pc(temp_file, verbose=False)

            # Verify data is read correctly with different factor
            assert len(crops) == 5
            assert crops[0] == 'ri_n'

        finally:
            os.unlink(temp_file)

    def test_different_rooting_depths(self):
        """Test with different rooting depths"""
        content = "C IWFM Ponded Crop Data File\n"
        content += " PondedCrop_Area.dat                     / LUFLP\n"
        content += " 0                                                 / NBCROP\n"
        content += "                                                   / CLWUBUDFL\n"
        content += "                                                   / CRZBUDFL\n"
        content += " 1.0                   / FACT\n"
        content += " 1.5                   / ROOTRI_NFL\n"
        content += " 2.0                   / ROOTRI_FL\n"
        content += " 2.5                   / ROOTRI_NDC\n"
        content += " 3.0                   / ROOTRF_SL\n"
        content += " 3.5                   / ROOTRF_PR\n"
        content += "C\n"
        content += " 0\t53\t53\t53\t53\t53\n"
        content += "C\n"
        content += " 0\t41\t41\t41\t41\t41\n"
        content += "C\n"
        content += " 0\t509\t509\t509\t509\t509\n"
        content += "C\n"
        content += " 0\t501\t501\t501\t501\t501\n"
        content += "C\n"
        content += " PondingDepth.dat                   / PNDTHFL\n"
        content += " PondingOps.dat                     / FLOWFL\n"
        content += "C\n"
        content += " 0\t1\t2\t3\t4\t5\n"
        content += "C\n"
        content += " 0\t11\n"
        content += "C\n"
        content += " 0\t312\t312\t312\t312\t312\n"
        content += "C\n"
        content += " 0\t321\t321\t321\t321\t321\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\t0.7\t0.8\t0.9\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_pc import iwfm_read_rz_pc

            crops, params, files = iwfm_read_rz_pc(temp_file, verbose=False)

            # Verify data is read correctly
            assert len(crops) == 5

        finally:
            os.unlink(temp_file)

    def test_verbose_mode(self):
        """Test verbose mode doesn't affect functionality"""
        content = "C IWFM Ponded Crop Data File\n"
        content += " PondedCrop_Area.dat                     / LUFLP\n"
        content += " 0                                                 / NBCROP\n"
        content += "                                                   / CLWUBUDFL\n"
        content += "                                                   / CRZBUDFL\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTRI_NFL\n"
        content += " 2.0                   / ROOTRI_FL\n"
        content += " 2.0                   / ROOTRI_NDC\n"
        content += " 2.0                   / ROOTRF_SL\n"
        content += " 2.0                   / ROOTRF_PR\n"
        content += "C\n"
        content += " 0\t53\t53\t53\t53\t53\n"
        content += "C\n"
        content += " 0\t41\t41\t41\t41\t41\n"
        content += "C\n"
        content += " 0\t509\t509\t509\t509\t509\n"
        content += "C\n"
        content += " 0\t501\t501\t501\t501\t501\n"
        content += "C\n"
        content += " PondingDepth.dat                   / PNDTHFL\n"
        content += " PondingOps.dat                     / FLOWFL\n"
        content += "C\n"
        content += " 0\t1\t2\t3\t4\t5\n"
        content += "C\n"
        content += " 0\t11\n"
        content += "C\n"
        content += " 0\t312\t312\t312\t312\t312\n"
        content += "C\n"
        content += " 0\t321\t321\t321\t321\t321\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\t0.7\t0.8\t0.9\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_pc import iwfm_read_rz_pc

            # Test with verbose=True
            crops, params, files = iwfm_read_rz_pc(temp_file, verbose=True)

            # Verify data is still read correctly
            assert len(crops) == 5
            assert crops[0] == 'ri_n'
            assert crops[1] == 'ri_f'
            assert crops[2] == 'ri_d'
            assert crops[3] == 'rf_sl'
            assert crops[4] == 'rf_pr'

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Ponded Crop Data File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += " PondedCrop_Area.dat                     / LUFLP\n"
        content += "C More comments\n"
        content += " 0                                                 / NBCROP\n"
        content += "# Comment\n"
        content += "                                                   / CLWUBUDFL\n"
        content += "C\n"
        content += "                                                   / CRZBUDFL\n"
        content += " 1.0                   / FACT\n"
        content += "C\n"
        content += " 2.0                   / ROOTRI_NFL\n"
        content += " 2.0                   / ROOTRI_FL\n"
        content += " 2.0                   / ROOTRI_NDC\n"
        content += " 2.0                   / ROOTRF_SL\n"
        content += " 2.0                   / ROOTRF_PR\n"
        content += "C\n"
        content += " 0\t53\t53\t53\t53\t53\n"
        content += "C\n"
        content += " 0\t41\t41\t41\t41\t41\n"
        content += "C\n"
        content += " 0\t509\t509\t509\t509\t509\n"
        content += "C\n"
        content += " 0\t501\t501\t501\t501\t501\n"
        content += "C\n"
        content += " PondingDepth.dat                   / PNDTHFL\n"
        content += " PondingOps.dat                     / FLOWFL\n"
        content += "C\n"
        content += " 0\t1\t2\t3\t4\t5\n"
        content += "C\n"
        content += " 0\t11\n"
        content += "C\n"
        content += " 0\t312\t312\t312\t312\t312\n"
        content += "C\n"
        content += " 0\t321\t321\t321\t321\t321\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\t0.7\t0.8\t0.9\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_pc import iwfm_read_rz_pc

            crops, params, files = iwfm_read_rz_pc(temp_file, verbose=False)

            # Should read correctly despite comment lines
            assert len(crops) == 5
            assert crops[0] == 'ri_n'

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM C2VSimCG file"""
        content = "C*******************************************************************************\n"
        content += "C                  INTEGRATED WATER FLOW MODEL (IWFM)\n"
        content += "C*******************************************************************************\n"
        content += "C\n"
        content += " RootZone\\C2VSimCG_PondedCrop_Area.dat                     / LUFLP\n"
        content += "C\n"
        content += " 0                                                 / NBCROP\n"
        content += "                                                        / CLWUBUDFL\n"
        content += "                                                        / CRZBUDFL\n"
        content += "C\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTRI_NFL\n"
        content += " 2.0                   / ROOTRI_FL\n"
        content += " 2.0                   / ROOTRI_NDC\n"
        content += " 2.0                   / ROOTRF_SL\n"
        content += " 2.0                   / ROOTRF_PR\n"
        content += "C\n"
        content += " 0\t53\t53\t53\t53\t53\n"
        content += "C\n"
        content += " 0\t41\t41\t41\t41\t41\n"
        content += "C\n"
        content += " 0\t509\t509\t509\t509\t509\n"
        content += "C\n"
        content += " 0\t501\t501\t501\t501\t501\n"
        content += "C\n"
        content += " RootZone\\PondingDepth.dat                   / PNDTHFL\n"
        content += " RootZone\\PondingOps.dat                     / FLOWFL\n"
        content += "C\n"
        content += " 0\t1\t2\t3\t4\t5\n"
        content += "C\n"
        content += " 0\t11\n"
        content += "C\n"
        content += " 0\t312\t312\t312\t312\t312\n"
        content += "C\n"
        content += " 0\t321\t321\t321\t321\t321\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\t0.7\t0.8\t0.9\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_pc import iwfm_read_rz_pc

            crops, params, files = iwfm_read_rz_pc(temp_file, verbose=False)

            # Verify data structure
            assert len(crops) == 5
            assert crops[0] == 'ri_n'
            assert crops[1] == 'ri_f'
            assert crops[2] == 'ri_d'
            assert crops[3] == 'rf_sl'
            assert crops[4] == 'rf_pr'

            # Verify file names (path is not stripped by the function)
            assert 'C2VSimCG_PondedCrop_Area.dat' in files[0]

        finally:
            os.unlink(temp_file)

    def test_area_file_path_handling(self):
        """Test handling of area file path"""
        content = "C IWFM Ponded Crop Data File\n"
        content += " ../Data/PondedCrop_Area.dat                     / LUFLP\n"
        content += " 0                                                 / NBCROP\n"
        content += "                                                   / CLWUBUDFL\n"
        content += "                                                   / CRZBUDFL\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTRI_NFL\n"
        content += " 2.0                   / ROOTRI_FL\n"
        content += " 2.0                   / ROOTRI_NDC\n"
        content += " 2.0                   / ROOTRF_SL\n"
        content += " 2.0                   / ROOTRF_PR\n"
        content += "C\n"
        content += " 0\t53\t53\t53\t53\t53\n"
        content += "C\n"
        content += " 0\t41\t41\t41\t41\t41\n"
        content += "C\n"
        content += " 0\t509\t509\t509\t509\t509\n"
        content += "C\n"
        content += " 0\t501\t501\t501\t501\t501\n"
        content += "C\n"
        content += " PondingDepth.dat                   / PNDTHFL\n"
        content += " PondingOps.dat                     / FLOWFL\n"
        content += "C\n"
        content += " 0\t1\t2\t3\t4\t5\n"
        content += "C\n"
        content += " 0\t11\n"
        content += "C\n"
        content += " 0\t312\t312\t312\t312\t312\n"
        content += "C\n"
        content += " 0\t321\t321\t321\t321\t321\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\t0.7\t0.8\t0.9\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_pc import iwfm_read_rz_pc

            crops, params, files = iwfm_read_rz_pc(temp_file, verbose=False)

            # Verify file path is read
            assert 'PondedCrop_Area.dat' in files[0]

        finally:
            os.unlink(temp_file)

    def test_crop_types(self):
        """Test that all 5 ponded crop types are returned"""
        content = "C IWFM Ponded Crop Data File\n"
        content += " PondedCrop_Area.dat                     / LUFLP\n"
        content += " 0                                                 / NBCROP\n"
        content += "                                                   / CLWUBUDFL\n"
        content += "                                                   / CRZBUDFL\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTRI_NFL\n"
        content += " 2.0                   / ROOTRI_FL\n"
        content += " 2.0                   / ROOTRI_NDC\n"
        content += " 2.0                   / ROOTRF_SL\n"
        content += " 2.0                   / ROOTRF_PR\n"
        content += "C\n"
        content += " 0\t53\t53\t53\t53\t53\n"
        content += "C\n"
        content += " 0\t41\t41\t41\t41\t41\n"
        content += "C\n"
        content += " 0\t509\t509\t509\t509\t509\n"
        content += "C\n"
        content += " 0\t501\t501\t501\t501\t501\n"
        content += "C\n"
        content += " PondingDepth.dat                   / PNDTHFL\n"
        content += " PondingOps.dat                     / FLOWFL\n"
        content += "C\n"
        content += " 0\t1\t2\t3\t4\t5\n"
        content += "C\n"
        content += " 0\t11\n"
        content += "C\n"
        content += " 0\t312\t312\t312\t312\t312\n"
        content += "C\n"
        content += " 0\t321\t321\t321\t321\t321\n"
        content += "C\n"
        content += " 0\t0.5\t0.6\t0.7\t0.8\t0.9\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_pc import iwfm_read_rz_pc

            crops, params, files = iwfm_read_rz_pc(temp_file, verbose=False)

            # Verify all 5 crop types
            assert crops == ['ri_n', 'ri_f', 'ri_d', 'rf_sl', 'rf_pr']

        finally:
            os.unlink(temp_file)
