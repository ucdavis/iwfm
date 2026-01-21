#!/usr/bin/env python
# test_iwfm_read_sim_file.py
# Unit tests for iwfm_read_sim_file.py
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


class TestIwfmReadSimFile:
    """Tests for iwfm_read_sim_file function"""

    def test_basic_structure_with_lake(self):
        """Test reading basic simulation file with lake component"""
        content = "C IWFM Simulation Main File\n"
        content += "C\n"
        content += "C Title Lines\n"
        content += " Historical Simulation, Water Years 1922-2015\n"
        content += " Central Valley, California\n"
        content += " Simulation v.R383\n"
        content += "C\n"
        content += " PreprocessorOut.bin                      / 1: PREPROCESSOR OUTPUT\n"
        content += " Groundwater.dat  / 2: GROUNDWATER COMPONENT\n"
        content += " Streams.dat                      / 3: STREAM COMPONENT\n"
        content += " Lake.dat                      / 4: LAKE COMPONENT\n"
        content += " RootZone.dat                    / 5: ROOT ZONE COMPONENT\n"
        content += " SWatersheds.dat                          / 6: SMALL WATERSHED COMPONENT\n"
        content += " Unsat.dat                                / 7: UNSATURATED ZONE COMPONENT\n"
        content += " IrrFrac.dat                              / 8: IRRIGATION FRACTIONS\n"
        content += " SupplyAdj.dat                            / 9: SUPPLY ADJUSTMENT\n"
        content += " Precip.dat                               /10: PRECIPITATION\n"
        content += " ET.dat                                   /11: EVAPOTRANSPIRATION\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            sim_dict, have_lake = iwfm_read_sim_file(temp_file)

            # Verify return type
            assert isinstance(sim_dict, dict)
            assert isinstance(have_lake, bool)

            # Verify lake is present
            assert have_lake is True

            # Verify dictionary contents
            assert 'preout' in sim_dict
            assert 'gw_file' in sim_dict
            assert 'stream_file' in sim_dict
            assert 'lake_file' in sim_dict
            assert 'root_file' in sim_dict
            assert 'swshed_file' in sim_dict
            assert 'unsat_file' in sim_dict
            assert 'precip_file' in sim_dict
            assert 'et_file' in sim_dict

            # Verify file names
            assert sim_dict['preout'] == 'PreprocessorOut.bin'
            assert sim_dict['gw_file'] == 'Groundwater.dat'
            assert sim_dict['stream_file'] == 'Streams.dat'
            assert sim_dict['lake_file'] == 'Lake.dat'
            assert sim_dict['root_file'] == 'RootZone.dat'
            assert sim_dict['swshed_file'] == 'SWatersheds.dat'
            assert sim_dict['unsat_file'] == 'Unsat.dat'
            assert sim_dict['precip_file'] == 'Precip.dat'
            assert sim_dict['et_file'] == 'ET.dat'

        finally:
            os.unlink(temp_file)

    def test_basic_structure_without_lake(self):
        """Test reading simulation file without lake component"""
        content = "C IWFM Simulation Main File\n"
        content += " Simulation Title\n"
        content += " Central Valley\n"
        content += " Version 1.0\n"
        content += "C\n"
        content += " PreprocessorOut.bin                      / 1: PREPROCESSOR OUTPUT\n"
        content += " Groundwater.dat  / 2: GROUNDWATER COMPONENT\n"
        content += " Streams.dat                      / 3: STREAM COMPONENT\n"
        content += "                                                     / 4: LAKE COMPONENT\n"
        content += " RootZone.dat                    / 5: ROOT ZONE COMPONENT\n"
        content += " SWatersheds.dat                          / 6: SMALL WATERSHED COMPONENT\n"
        content += " Unsat.dat                                / 7: UNSATURATED ZONE COMPONENT\n"
        content += " IrrFrac.dat                              / 8: IRRIGATION FRACTIONS\n"
        content += " SupplyAdj.dat                            / 9: SUPPLY ADJUSTMENT\n"
        content += " Precip.dat                               /10: PRECIPITATION\n"
        content += " ET.dat                                   /11: EVAPOTRANSPIRATION\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            sim_dict, have_lake = iwfm_read_sim_file(temp_file)

            # Verify lake is not present
            assert have_lake is False

            # Verify lake file is empty string
            assert sim_dict['lake_file'] == ''

            # Verify other files are still present
            assert sim_dict['preout'] == 'PreprocessorOut.bin'
            assert sim_dict['gw_file'] == 'Groundwater.dat'

        finally:
            os.unlink(temp_file)

    def test_return_structure(self):
        """Test that function returns correct structure"""
        content = "C IWFM Simulation Main File\n"
        content += " Title Line 1\n"
        content += " Title Line 2\n"
        content += " Title Line 3\n"
        content += " PreprocessorOut.bin                      / 1: PREPROCESSOR OUTPUT\n"
        content += " Groundwater.dat  / 2: GROUNDWATER COMPONENT\n"
        content += " Streams.dat                      / 3: STREAM COMPONENT\n"
        content += " Lake.dat                      / 4: LAKE COMPONENT\n"
        content += " RootZone.dat                    / 5: ROOT ZONE COMPONENT\n"
        content += " SWatersheds.dat                          / 6: SMALL WATERSHED COMPONENT\n"
        content += " Unsat.dat                                / 7: UNSATURATED ZONE COMPONENT\n"
        content += " IrrFrac.dat                              / 8: IRRIGATION FRACTIONS\n"
        content += " SupplyAdj.dat                            / 9: SUPPLY ADJUSTMENT\n"
        content += " Precip.dat                               /10: PRECIPITATION\n"
        content += " ET.dat                                   /11: EVAPOTRANSPIRATION\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            result = iwfm_read_sim_file(temp_file)

            # Verify return is tuple of 2 elements
            assert isinstance(result, tuple)
            assert len(result) == 2

            sim_dict, have_lake = result

            # Verify types
            assert isinstance(sim_dict, dict)
            assert isinstance(have_lake, bool)

            # Verify dictionary has all required keys
            required_keys = ['preout', 'gw_file', 'stream_file', 'lake_file',
                           'root_file', 'swshed_file', 'unsat_file', 'precip_file', 'et_file']
            for key in required_keys:
                assert key in sim_dict

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Simulation Main File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += " Title Line 1\n"
        content += " Title Line 2\n"
        content += " Title Line 3\n"
        content += "C More comments\n"
        content += " PreprocessorOut.bin                      / 1: PREPROCESSOR OUTPUT\n"
        content += "# Comment\n"
        content += " Groundwater.dat  / 2: GROUNDWATER COMPONENT\n"
        content += "C\n"
        content += " Streams.dat                      / 3: STREAM COMPONENT\n"
        content += " Lake.dat                      / 4: LAKE COMPONENT\n"
        content += " RootZone.dat                    / 5: ROOT ZONE COMPONENT\n"
        content += " SWatersheds.dat                          / 6: SMALL WATERSHED COMPONENT\n"
        content += " Unsat.dat                                / 7: UNSATURATED ZONE COMPONENT\n"
        content += " IrrFrac.dat                              / 8: IRRIGATION FRACTIONS\n"
        content += " SupplyAdj.dat                            / 9: SUPPLY ADJUSTMENT\n"
        content += " Precip.dat                               /10: PRECIPITATION\n"
        content += " ET.dat                                   /11: EVAPOTRANSPIRATION\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            sim_dict, have_lake = iwfm_read_sim_file(temp_file)

            # Should read correctly despite comment lines
            assert sim_dict['preout'] == 'PreprocessorOut.bin'
            assert sim_dict['gw_file'] == 'Groundwater.dat'

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM C2VSimCG file"""
        content = "C*******************************************************************************\n"
        content += "C                  INTEGRATED WATER FLOW MODEL (IWFM)\n"
        content += "C*******************************************************************************\n"
        content += "C\n"
        content += " Historical Simulation, Water Years 1922-2015\n"
        content += " Central Valley, California\n"
        content += " Simulation v.R383-2015-CG 2016.09.26\n"
        content += "C\n"
        content += " C2VSimCG_PreprocessorOut.bin                      / 1: BINARY INPUT GENERATED BY PRE-PROCESSOR\n"
        content += " Groundwater\\C2VSimCG_Groundwater.dat  / 2: GROUNDWATER COMPONENT MAIN FILE\n"
        content += " Streams\\C2VSimCG_Streams.dat                      / 3: STREAM COMPONENT MAIN FILE\n"
        content += "                                                     / 4: LAKE COMPONENT MAIN FILE\n"
        content += " RootZone\\C2VSimCG_RootZone.dat                    / 5: ROOT ZONE COMPONENT MAIN FILE\n"
        content += " C2VSimCG_SWatersheds.dat                          / 6: SMALL WATERSHED COMPONENT MAIN FILE\n"
        content += " C2VSimCG_Unsat.dat                                / 7: UNSATURATED ZONE COMPONENT MAIN FILE\n"
        content += " C2VSimCG_IrrFrac.dat                              / 8: IRRIGATION FRACTIONS DATA FILE\n"
        content += " C2VSimCG_SupplyAdj.dat                            / 9: SUPPLY ADJUSTMENT SPECIFICATION DATA FILE\n"
        content += " C2VSimCG_Precip.dat                               /10: PRECIPITATION DATA FILE\n"
        content += " C2VSimCG_ET.dat                                   /11: EVAPOTRANSPIRATION DATA FILE\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            sim_dict, have_lake = iwfm_read_sim_file(temp_file)

            # Verify data structure
            assert have_lake is False
            assert sim_dict['preout'] == 'C2VSimCG_PreprocessorOut.bin'
            assert 'C2VSimCG_Groundwater.dat' in sim_dict['gw_file']
            assert 'C2VSimCG_Streams.dat' in sim_dict['stream_file']
            assert sim_dict['lake_file'] == ''
            assert 'C2VSimCG_RootZone.dat' in sim_dict['root_file']

        finally:
            os.unlink(temp_file)

    def test_file_paths_with_directories(self):
        """Test handling of file paths with directory prefixes"""
        content = "C IWFM Simulation Main File\n"
        content += " Simulation Title\n"
        content += " Central Valley\n"
        content += " Version 1.0\n"
        content += " PreprocessorOut.bin                      / 1: PREPROCESSOR OUTPUT\n"
        content += " Groundwater/GW.dat  / 2: GROUNDWATER COMPONENT\n"
        content += " Streams/Stream.dat                      / 3: STREAM COMPONENT\n"
        content += " Lakes/Lake.dat                      / 4: LAKE COMPONENT\n"
        content += " RootZone/RZ.dat                    / 5: ROOT ZONE COMPONENT\n"
        content += " SWatersheds.dat                          / 6: SMALL WATERSHED COMPONENT\n"
        content += " Unsat.dat                                / 7: UNSATURATED ZONE COMPONENT\n"
        content += " IrrFrac.dat                              / 8: IRRIGATION FRACTIONS\n"
        content += " SupplyAdj.dat                            / 9: SUPPLY ADJUSTMENT\n"
        content += " Precip.dat                               /10: PRECIPITATION\n"
        content += " ET.dat                                   /11: EVAPOTRANSPIRATION\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            sim_dict, have_lake = iwfm_read_sim_file(temp_file)

            # Verify file paths include directory prefixes
            assert 'GW.dat' in sim_dict['gw_file']
            assert 'Stream.dat' in sim_dict['stream_file']
            assert 'Lake.dat' in sim_dict['lake_file']
            assert 'RZ.dat' in sim_dict['root_file']

        finally:
            os.unlink(temp_file)

    def test_windows_backslash_paths(self):
        """Test handling of Windows backslash paths"""
        content = "C IWFM Simulation Main File\n"
        content += " Simulation Title\n"
        content += " Central Valley\n"
        content += " Version 1.0\n"
        content += " PreprocessorOut.bin                      / 1: PREPROCESSOR OUTPUT\n"
        content += " Groundwater\\GW.dat  / 2: GROUNDWATER COMPONENT\n"
        content += " Streams\\Stream.dat                      / 3: STREAM COMPONENT\n"
        content += " Lakes\\Lake.dat                      / 4: LAKE COMPONENT\n"
        content += " RootZone\\RZ.dat                    / 5: ROOT ZONE COMPONENT\n"
        content += " SWatersheds.dat                          / 6: SMALL WATERSHED COMPONENT\n"
        content += " Unsat.dat                                / 7: UNSATURATED ZONE COMPONENT\n"
        content += " IrrFrac.dat                              / 8: IRRIGATION FRACTIONS\n"
        content += " SupplyAdj.dat                            / 9: SUPPLY ADJUSTMENT\n"
        content += " Precip.dat                               /10: PRECIPITATION\n"
        content += " ET.dat                                   /11: EVAPOTRANSPIRATION\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            sim_dict, have_lake = iwfm_read_sim_file(temp_file)

            # Verify file paths are read correctly with backslashes
            assert 'GW.dat' in sim_dict['gw_file']
            assert 'Stream.dat' in sim_dict['stream_file']
            assert 'Lake.dat' in sim_dict['lake_file']

        finally:
            os.unlink(temp_file)

    def test_all_required_files_present(self):
        """Test that all 9 required file entries are returned"""
        content = "C IWFM Simulation Main File\n"
        content += " Title 1\n"
        content += " Title 2\n"
        content += " Title 3\n"
        content += " file1.bin                      / 1: PREPROCESSOR OUTPUT\n"
        content += " file2.dat  / 2: GROUNDWATER COMPONENT\n"
        content += " file3.dat                      / 3: STREAM COMPONENT\n"
        content += " file4.dat                      / 4: LAKE COMPONENT\n"
        content += " file5.dat                    / 5: ROOT ZONE COMPONENT\n"
        content += " file6.dat                          / 6: SMALL WATERSHED COMPONENT\n"
        content += " file7.dat                                / 7: UNSATURATED ZONE COMPONENT\n"
        content += " file8.dat                              / 8: IRRIGATION FRACTIONS\n"
        content += " file9.dat                            / 9: SUPPLY ADJUSTMENT\n"
        content += " file10.dat                               /10: PRECIPITATION\n"
        content += " file11.dat                                   /11: EVAPOTRANSPIRATION\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            sim_dict, have_lake = iwfm_read_sim_file(temp_file)

            # Verify all 9 keys are present
            assert len(sim_dict) == 9
            assert sim_dict['preout'] == 'file1.bin'
            assert sim_dict['gw_file'] == 'file2.dat'
            assert sim_dict['stream_file'] == 'file3.dat'
            assert sim_dict['lake_file'] == 'file4.dat'
            assert sim_dict['root_file'] == 'file5.dat'
            assert sim_dict['swshed_file'] == 'file6.dat'
            assert sim_dict['unsat_file'] == 'file7.dat'
            assert sim_dict['precip_file'] == 'file10.dat'
            assert sim_dict['et_file'] == 'file11.dat'

        finally:
            os.unlink(temp_file)

    def test_have_lake_flag_with_lake(self):
        """Test that have_lake flag is True when lake file is present"""
        content = "C IWFM Simulation Main File\n"
        content += " Title\n"
        content += " Title\n"
        content += " Title\n"
        content += " PreprocessorOut.bin / 1\n"
        content += " Groundwater.dat / 2\n"
        content += " Streams.dat / 3\n"
        content += " Lake.dat / 4\n"
        content += " RootZone.dat / 5\n"
        content += " SWatersheds.dat / 6\n"
        content += " Unsat.dat / 7\n"
        content += " IrrFrac.dat / 8\n"
        content += " SupplyAdj.dat / 9\n"
        content += " Precip.dat /10\n"
        content += " ET.dat /11\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            sim_dict, have_lake = iwfm_read_sim_file(temp_file)

            assert have_lake is True
            assert sim_dict['lake_file'] == 'Lake.dat'

        finally:
            os.unlink(temp_file)

    def test_have_lake_flag_without_lake(self):
        """Test that have_lake flag is False when lake file line starts with /"""
        content = "C IWFM Simulation Main File\n"
        content += " Title\n"
        content += " Title\n"
        content += " Title\n"
        content += " PreprocessorOut.bin / 1\n"
        content += " Groundwater.dat / 2\n"
        content += " Streams.dat / 3\n"
        content += " / 4: LAKE COMPONENT (NOT USED)\n"
        content += " RootZone.dat / 5\n"
        content += " SWatersheds.dat / 6\n"
        content += " Unsat.dat / 7\n"
        content += " IrrFrac.dat / 8\n"
        content += " SupplyAdj.dat / 9\n"
        content += " Precip.dat /10\n"
        content += " ET.dat /11\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_sim_file import iwfm_read_sim_file

            sim_dict, have_lake = iwfm_read_sim_file(temp_file)

            assert have_lake is False
            assert sim_dict['lake_file'] == ''

        finally:
            os.unlink(temp_file)
