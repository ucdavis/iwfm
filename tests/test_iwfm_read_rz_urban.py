#!/usr/bin/env python
# test_iwfm_read_rz_urban.py
# Unit tests for iwfm_read_rz_urban.py
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


class TestIwfmReadRzUrban:
    """Tests for iwfm_read_rz_urban function"""

    def test_basic_structure(self):
        """Test reading basic urban data file"""
        content = "C IWFM Urban Data File\n"
        content += "C\n"
        content += " Urban_Area.dat              / LUFLU\n"
        content += "C\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTURB\n"
        content += "C\n"
        content += " Urban_Population.dat          / POPULFL\n"
        content += " Urban_PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " Urban_WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        # Urban parameters - IE=0 means all elements use these values
        content += " 0\t0.62\t58\t6\t6\t-1\t463\t6\t6\t1\n"
        content += "C\n"
        # Initial conditions
        content += " 0\t0.5\t0.19\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            crops, params, files = iwfm_read_rz_urban(temp_file)

            # Verify crops
            assert len(crops) == 2
            assert crops[0] == 'urban'
            assert crops[1] == 'ic'

            # Verify params structure (2 parameter sets: urban params and ic)
            assert len(params) == 2

            # Verify files (4 file names)
            assert len(files) == 4
            assert os.path.basename(files[0]) == 'Urban_Area.dat'
            assert os.path.basename(files[1]) == 'Urban_Population.dat'
            assert os.path.basename(files[2]) == 'Urban_PerCapWaterUse.dat'
            assert os.path.basename(files[3]) == 'Urban_WaterUseSpecs.dat'

        finally:
            os.unlink(temp_file)

    def test_return_structure(self):
        """Test that function returns correct tuple structure"""
        content = "C IWFM Urban Data File\n"
        content += " Urban_Area.dat              / LUFLU\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTURB\n"
        content += " Urban_Population.dat          / POPULFL\n"
        content += " Urban_PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " Urban_WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        content += " 0\t0.62\t58\t6\t6\t-1\t463\t6\t6\t1\n"
        content += "C\n"
        content += " 0\t0.5\t0.19\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            result = iwfm_read_rz_urban(temp_file)

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

            # Verify files is list of 4 elements
            assert isinstance(files, list)
            assert len(files) == 4

        finally:
            os.unlink(temp_file)

    def test_different_conversion_factor(self):
        """Test with different conversion factor"""
        content = "C IWFM Urban Data File\n"
        content += " Urban_Area.dat              / LUFLU\n"
        content += " 3.2808                / FACT\n"
        content += " 2.0                   / ROOTURB\n"
        content += " Urban_Population.dat          / POPULFL\n"
        content += " Urban_PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " Urban_WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        content += " 0\t0.62\t58\t6\t6\t-1\t463\t6\t6\t1\n"
        content += "C\n"
        content += " 0\t0.5\t0.19\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            crops, params, files = iwfm_read_rz_urban(temp_file)

            # Verify data is read correctly with different factor
            assert len(crops) == 2
            assert crops[0] == 'urban'

        finally:
            os.unlink(temp_file)

    def test_different_rooting_depth(self):
        """Test with different rooting depth"""
        content = "C IWFM Urban Data File\n"
        content += " Urban_Area.dat              / LUFLU\n"
        content += " 1.0                   / FACT\n"
        content += " 3.5                   / ROOTURB\n"
        content += " Urban_Population.dat          / POPULFL\n"
        content += " Urban_PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " Urban_WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        content += " 0\t0.62\t58\t6\t6\t-1\t463\t6\t6\t1\n"
        content += "C\n"
        content += " 0\t0.5\t0.19\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            crops, params, files = iwfm_read_rz_urban(temp_file)

            # Verify data is read correctly
            assert len(crops) == 2

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Urban Data File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += " Urban_Area.dat              / LUFLU\n"
        content += "C More comments\n"
        content += " 1.0                   / FACT\n"
        content += "# Comment\n"
        content += " 2.0                   / ROOTURB\n"
        content += "C\n"
        content += " Urban_Population.dat          / POPULFL\n"
        content += " Urban_PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " Urban_WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        content += " 0\t0.62\t58\t6\t6\t-1\t463\t6\t6\t1\n"
        content += "C\n"
        content += " 0\t0.5\t0.19\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            crops, params, files = iwfm_read_rz_urban(temp_file)

            # Should read correctly despite comment lines
            assert len(crops) == 2
            assert crops[0] == 'urban'

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM C2VSimCG file"""
        content = "C*******************************************************************************\n"
        content += "C                  INTEGRATED WATER FLOW MODEL (IWFM)\n"
        content += "C*******************************************************************************\n"
        content += "C\n"
        content += " RootZone\\C2VSimCG_Urban_Area.dat              / LUFLU\n"
        content += "C\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTURB\n"
        content += "C\n"
        content += " RootZone\\C2VSimCG_Urban_Population.dat          / POPULFL\n"
        content += " RootZone\\C2VSimCG_Urban_PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " RootZone\\C2VSimCG_Urban_WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        content += " 0\t0.62\t58\t6\t6\t-1\t463\t6\t6\t1\n"
        content += "C\n"
        content += " 0\t0.5\t0.19344\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            crops, params, files = iwfm_read_rz_urban(temp_file)

            # Verify data structure
            assert len(crops) == 2
            assert crops[0] == 'urban'
            assert crops[1] == 'ic'

            # Verify file names (path is not stripped by the function)
            assert 'C2VSimCG_Urban_Area.dat' in files[0]
            assert 'C2VSimCG_Urban_Population.dat' in files[1]

        finally:
            os.unlink(temp_file)

    def test_area_file_path_handling(self):
        """Test handling of area file path"""
        content = "C IWFM Urban Data File\n"
        content += " ../Data/Urban_Area.dat              / LUFLU\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTURB\n"
        content += " Urban_Population.dat          / POPULFL\n"
        content += " Urban_PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " Urban_WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        content += " 0\t0.62\t58\t6\t6\t-1\t463\t6\t6\t1\n"
        content += "C\n"
        content += " 0\t0.5\t0.19\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            crops, params, files = iwfm_read_rz_urban(temp_file)

            # Verify file path is read
            assert 'Urban_Area.dat' in files[0]

        finally:
            os.unlink(temp_file)

    def test_different_urban_parameters(self):
        """Test with different urban parameter values"""
        content = "C IWFM Urban Data File\n"
        content += " Urban_Area.dat              / LUFLU\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTURB\n"
        content += " Urban_Population.dat          / POPULFL\n"
        content += " Urban_PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " Urban_WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        # Different parameter values: PERV=0.5, CNURB=60, etc.
        content += " 0\t0.5\t60\t10\t10\t-1.0\t500\t8\t8\t2\n"
        content += "C\n"
        content += " 0\t0.6\t0.22\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            crops, params, files = iwfm_read_rz_urban(temp_file)

            # Verify data is read correctly
            assert len(crops) == 2
            assert len(params) == 2

        finally:
            os.unlink(temp_file)

    def test_crop_type(self):
        """Test that urban crop type is returned"""
        content = "C IWFM Urban Data File\n"
        content += " Urban_Area.dat              / LUFLU\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTURB\n"
        content += " Urban_Population.dat          / POPULFL\n"
        content += " Urban_PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " Urban_WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        content += " 0\t0.62\t58\t6\t6\t-1\t463\t6\t6\t1\n"
        content += "C\n"
        content += " 0\t0.5\t0.19\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            crops, params, files = iwfm_read_rz_urban(temp_file)

            # Verify crop types
            assert crops == ['urban', 'ic']

        finally:
            os.unlink(temp_file)

    def test_all_file_names_returned(self):
        """Test that all 4 file names are returned"""
        content = "C IWFM Urban Data File\n"
        content += " Area.dat              / LUFLU\n"
        content += " 1.0                   / FACT\n"
        content += " 2.0                   / ROOTURB\n"
        content += " Population.dat          / POPULFL\n"
        content += " PerCapWaterUse.dat      / WTRUSEFL\n"
        content += " WaterUseSpecs.dat       / URBSPECFL\n"
        content += "C\n"
        content += " 0\t0.62\t58\t6\t6\t-1\t463\t6\t6\t1\n"
        content += "C\n"
        content += " 0\t0.5\t0.19\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_rz_urban import iwfm_read_rz_urban

            crops, params, files = iwfm_read_rz_urban(temp_file)

            # Verify all 4 file names
            assert len(files) == 4
            assert 'Area.dat' in files[0]
            assert 'Population.dat' in files[1]
            assert 'PerCapWaterUse.dat' in files[2]
            assert 'WaterUseSpecs.dat' in files[3]

        finally:
            os.unlink(temp_file)
