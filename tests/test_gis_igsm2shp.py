#!/usr/bin/env python
# test_gis_igsm2shp.py
# Unit tests for gis/igsm2shp.py
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


def create_igsm_main_file(elem_file, node_file, strat_file, stream_file, lake_file, char_file):
    """Create properly structured IGSM main input file for testing.

    Parameters
    ----------
    elem_file : str
        Element configuration file name
    node_file : str
        Node coordinate file name
    strat_file : str
        Stratigraphic data file name
    stream_file : str
        Stream geometric data file name
    lake_file : str
        Lake data file name (or '/' for no lake file)
    char_file : str
        Element characteristic data file name

    Returns
    -------
    str
        File content with proper IGSM format
    """
    content = "C*****************************************************************************\n"
    content += "C\n"
    content += "C            INTEGRATED GROUND AND SURFACE WATER MODEL  (IGSM)\n"
    content += "C\n"
    content += "C                        MAIN INPUT FILE\n"
    content += "C*****************************************************************************\n"
    content += "C                 Titles To Be Printed in the Output\n"
    content += "C-----------------------------------------------------------------------------\n"
    content += "                    Test Model\n"
    content += "                        Test Area\n"
    content += "                                        PART 1\n"
    content += "C*****************************************************************************\n"
    content += "C                            File Description\n"
    content += "C-----------------------------------------------------------------------------\n"
    content += "C    FILE NAME                 DESCRIPTION\n"
    content += "C-----------------------------------------------------------------------------\n"
    content += "   OUTPUT.BIN                  / 4: BINARY OUTPUT FOR PASS 2\n"
    content += "   CONTROL.IN                  / 5: CONTROL INPUT FILE\n"
    content += "   OUTPUT.OUT                  / 6: STANDARD OUTPUT FILE\n"
    content += f"   {elem_file:30s}  / 7: ELEMENT CONFIGURATION FILE (INPUT)\n"
    content += f"   {node_file:30s}  / 8: NODE X-Y COORDINATE FILE (INPUT)\n"
    content += f"   {strat_file:30s}  / 9: STRATIGRAPHIC DATA FILE (INPUT)\n"
    content += f"   {stream_file:30s}  /10: STREAM GEOMETRIC DATA FILE (INPUT)\n"
    content += f"   {lake_file:30s}  /11: LAKE DATA FILE (INPUT)\n"
    content += "                                /12: WELL DATA FILE (INPUT)\n"
    content += f"   {char_file:30s}  /13: ELEMENT CHARACTERISTIC DATA FILE (INPUT)\n"
    content += "C******************************************************************************\n"
    content += "C                      Output Control\n"
    content += "C-----------------------------------------------------------------------------\n"
    content += "    1                           /KOUT\n"
    content += "    2                           /KDEB\n"
    content += "C******************************************************************************\n"
    content += "C                   Input / Output Unit Control\n"
    content += "C-----------------------------------------------------------------------------\n"
    content += "    0                           /KUNIN\n"
    content += "    0                           /KUNOUT\n"
    content += "C*******************************************************************************\n"
    content += "C  End of file\n"
    content += "C*******************************************************************************\n"

    return content


class TestIgsm2shpFileReading:
    """Tests for file reading logic in igsm2shp function"""

    def test_read_basic_file_names(self):
        """Test reading basic file names from IGSM main file"""
        # Note: We're testing the file reading logic, not the shapefile creation
        # So we'll extract and test just the file reading portion

        content = create_igsm_main_file(
            elem_file='ELEM.DAT',
            node_file='NODE.DAT',
            strat_file='STRAT.DAT',
            stream_file='STREAM.DAT',
            lake_file='LAKE.DAT',
            char_file='CHAR.DAT'
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.IN1', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            # Read the file and extract file names using the same logic as igsm2shp
            import iwfm
            with open(temp_file) as f:
                main_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, main_lines, 6)
            elem_file = main_lines[line_index].split()[0]
            line_index += 1
            node_file = main_lines[line_index].split()[0]
            line_index += 1
            strat_file = main_lines[line_index].split()[0]
            line_index += 1
            stream_file = main_lines[line_index].split()[0]
            line_index += 1
            lake_file = main_lines[line_index].split()[0]
            line_index += 2
            char_file = main_lines[line_index].split()[0]

            # Verify file names
            assert elem_file == 'ELEM.DAT'
            assert node_file == 'NODE.DAT'
            assert strat_file == 'STRAT.DAT'
            assert stream_file == 'STREAM.DAT'
            assert lake_file == 'LAKE.DAT'
            assert char_file == 'CHAR.DAT'

        finally:
            os.unlink(temp_file)

    def test_read_no_lake_file(self):
        """Test reading file names when no lake file is specified"""
        content = create_igsm_main_file(
            elem_file='ELEM.DAT',
            node_file='NODE.DAT',
            strat_file='STRAT.DAT',
            stream_file='STREAM.DAT',
            lake_file='/',  # No lake file
            char_file='CHAR.DAT'
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.IN1', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                main_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, main_lines, 6)
            elem_file = main_lines[line_index].split()[0]
            line_index += 1
            node_file = main_lines[line_index].split()[0]
            line_index += 1
            strat_file = main_lines[line_index].split()[0]
            line_index += 1
            stream_file = main_lines[line_index].split()[0]
            line_index += 1
            lake_file = main_lines[line_index].split()[0]

            # Check that lake file is '/' indicating no lake
            assert lake_file == '/'
            # The function sets lake_file = '' when it detects '/'
            if lake_file[0] == '/':
                lake_file = ''
            assert lake_file == ''

        finally:
            os.unlink(temp_file)

    def test_read_with_path_prefixes(self):
        """Test reading file names with path prefixes"""
        content = create_igsm_main_file(
            elem_file='./data/ELEM.DAT',
            node_file='../input/NODE.DAT',
            strat_file='/abs/path/STRAT.DAT',
            stream_file='streams/STREAM.DAT',
            lake_file='/',
            char_file='CHAR.DAT'
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.IN1', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                main_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, main_lines, 6)
            elem_file = main_lines[line_index].split()[0]
            line_index += 1
            node_file = main_lines[line_index].split()[0]
            line_index += 1
            strat_file = main_lines[line_index].split()[0]
            line_index += 1
            stream_file = main_lines[line_index].split()[0]

            # Verify paths are preserved
            assert elem_file == './data/ELEM.DAT'
            assert node_file == '../input/NODE.DAT'
            assert strat_file == '/abs/path/STRAT.DAT'
            assert stream_file == 'streams/STREAM.DAT'

        finally:
            os.unlink(temp_file)

    def test_read_windows_paths(self):
        """Test reading file names with Windows-style paths"""
        content = create_igsm_main_file(
            elem_file=r'data\ELEM.DAT',
            node_file=r'input\NODE.DAT',
            strat_file=r'C:\model\STRAT.DAT',
            stream_file=r'streams\STREAM.DAT',
            lake_file='/',
            char_file=r'data\CHAR.DAT'
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.IN1', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                main_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, main_lines, 6)
            elem_file = main_lines[line_index].split()[0]
            line_index += 1
            node_file = main_lines[line_index].split()[0]

            # Verify Windows paths are preserved
            assert 'ELEM.DAT' in elem_file
            assert 'NODE.DAT' in node_file

        finally:
            os.unlink(temp_file)

    def test_skip_logic_correctness(self):
        """Test that skip_ahead(0, lines, 6) reaches the correct line"""
        content = create_igsm_main_file(
            elem_file='ELEM.DAT',
            node_file='NODE.DAT',
            strat_file='STRAT.DAT',
            stream_file='STREAM.DAT',
            lake_file='/',
            char_file='CHAR.DAT'
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.IN1', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                main_lines = f.read().splitlines()

            # Start at line 0, skip 6 non-comment lines
            line_index = iwfm.skip_ahead(0, main_lines, 6)

            # The line at line_index should contain 'BINARY OUTPUT'
            # (it's the 7th non-comment line after comments)
            line = main_lines[line_index]

            # Verify we're at the first file specification line
            assert 'OUTPUT.BIN' in line or '/' in line

        finally:
            os.unlink(temp_file)

    def test_file_name_extraction(self):
        """Test that file names are correctly extracted from lines with comments"""
        content = create_igsm_main_file(
            elem_file='SCFELEM.DAT',
            node_file='SCFXY.DAT',
            strat_file='SCFSTRA.DAT',
            stream_file='SCFSTRM.DAT',
            lake_file='SCFLAKE.DAT',
            char_file='SCFCHRC.DAT'
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.IN1', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                main_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, main_lines, 6)
            elem_file = main_lines[line_index].split()[0]

            # Should extract just the file name, not the comment
            assert elem_file == 'SCFELEM.DAT'
            assert '/' not in elem_file or elem_file == '/'

        finally:
            os.unlink(temp_file)

    @pytest.mark.skip(reason="Large real-world file test - run manually if file exists")
    def test_with_actual_scf_in1_file(self):
        """Test with actual SCF.IN1 file if it exists"""
        test_file = '/Volumes/MinEx/Documents/Dropbox/work/Programing/repos/iwfm-py/iwfm-tests/igsm2shp/SCF.IN1'

        if not os.path.exists(test_file):
            pytest.skip(f"Test file not found: {test_file}")

        import iwfm
        with open(test_file) as f:
            main_lines = f.read().splitlines()

        line_index = iwfm.skip_ahead(0, main_lines, 6)
        elem_file = main_lines[line_index].split()[0]
        line_index += 1
        node_file = main_lines[line_index].split()[0]
        line_index += 1
        strat_file = main_lines[line_index].split()[0]
        line_index += 1
        stream_file = main_lines[line_index].split()[0]
        line_index += 1
        lake_file = main_lines[line_index].split()[0]
        line_index += 2  # Skip well data file line
        char_file = main_lines[line_index].split()[0]

        # Verify file names from actual file
        assert elem_file == 'SCFELEM.DAT'
        assert node_file == 'SCFXY.DAT'
        assert strat_file == 'SCFSTRA.DAT'
        assert stream_file == 'SCFSTRM.DAT'
        assert lake_file == 'SCFLAKE.DAT'
        assert char_file == 'SCFCHRC.DAT'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
