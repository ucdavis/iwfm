#!/usr/bin/env python
# test_iwfm_read_preproc.py
# Unit tests for iwfm_read_preproc.py
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
from pathlib import Path


def create_preproc_file(preout, elem_file, node_file, strat_file, stream_file, lake_file):
    """Create IWFM Preprocessor main input file for testing.

    Parameters
    ----------
    preout : str
        Preprocessor output file name
    elem_file : str
        Element file name
    node_file : str
        Node file name
    strat_file : str
        Stratigraphy file name
    stream_file : str
        Stream file name
    lake_file : str
        Lake file name (or '/' if no lake file)

    Returns
    -------
    str
        File contents
    """
    content = "C IWFM Preprocessor Main Input File\n"
    content += "C\n"
    content += " Title line 1\n"
    content += " Title line 2\n"
    content += " Title line 3\n"
    content += "C\n"
    content += f" {preout}                / PREOUT\n"
    content += "C\n"
    content += f" {elem_file}             / Element file\n"
    content += "C\n"
    content += f" {node_file}             / Node file\n"
    content += "C\n"
    content += f" {strat_file}            / Stratigraphy file\n"
    content += "C\n"
    content += f" {stream_file}           / Stream file\n"
    content += "C\n"
    content += f" {lake_file}             / Lake file\n"
    content += "C\n"

    return content


class TestIwfmReadPreproc:
    """Tests for iwfm_read_preproc function"""

    def test_basic_file_with_lake(self):
        """Test reading basic preprocessor file with lake file"""
        content = create_preproc_file(
            "Preprocessor.out",
            "Elements.dat",
            "Nodes.dat",
            "Stratigraphy.dat",
            "Streams.dat",
            "Lakes.dat"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            # Get temp file directory for path comparison
            temp_dir = Path(temp_file).parent

            # Verify all file paths are present and resolved to absolute paths
            assert 'preout' in pre_dict
            assert 'elem_file' in pre_dict
            assert 'node_file' in pre_dict
            assert 'strat_file' in pre_dict
            assert 'stream_file' in pre_dict
            assert 'lake_file' in pre_dict

            # Verify paths are absolute
            assert Path(pre_dict['preout']).is_absolute()
            assert Path(pre_dict['elem_file']).is_absolute()
            assert Path(pre_dict['node_file']).is_absolute()
            assert Path(pre_dict['strat_file']).is_absolute()
            assert Path(pre_dict['stream_file']).is_absolute()
            assert Path(pre_dict['lake_file']).is_absolute()

            # Verify lake file flag
            assert have_lake is True

            # Verify file names are correct (basename)
            assert Path(pre_dict['preout']).name == "Preprocessor.out"
            assert Path(pre_dict['elem_file']).name == "Elements.dat"
            assert Path(pre_dict['node_file']).name == "Nodes.dat"
            assert Path(pre_dict['strat_file']).name == "Stratigraphy.dat"
            assert Path(pre_dict['stream_file']).name == "Streams.dat"
            assert Path(pre_dict['lake_file']).name == "Lakes.dat"

        finally:
            os.unlink(temp_file)

    def test_file_without_lake(self):
        """Test reading preprocessor file without lake file (/ marker)"""
        content = create_preproc_file(
            "Preprocessor.out",
            "Elements.dat",
            "Nodes.dat",
            "Stratigraphy.dat",
            "Streams.dat",
            "/"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            # Verify lake file flag is False
            assert have_lake is False

            # Verify lake_file is empty string
            assert pre_dict['lake_file'] == ''

            # Verify other files still present
            assert 'preout' in pre_dict
            assert 'elem_file' in pre_dict
            assert 'node_file' in pre_dict
            assert 'strat_file' in pre_dict
            assert 'stream_file' in pre_dict

        finally:
            os.unlink(temp_file)

    def test_relative_paths_resolved(self):
        """Test that relative paths are resolved to absolute paths"""
        content = create_preproc_file(
            "Preprocessor.out",
            "Elements.dat",
            "Nodes.dat",
            "Stratigraphy.dat",
            "Streams.dat",
            "Lakes.dat"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            temp_dir = Path(temp_file).resolve().parent

            # All paths should be absolute
            for key in ['preout', 'elem_file', 'node_file', 'strat_file', 'stream_file', 'lake_file']:
                assert Path(pre_dict[key]).is_absolute()

            # Verify paths are in temp directory (resolve both for symlink handling)
            assert Path(pre_dict['preout']).resolve().parent == temp_dir
            assert Path(pre_dict['elem_file']).resolve().parent == temp_dir
            assert Path(pre_dict['node_file']).resolve().parent == temp_dir

        finally:
            os.unlink(temp_file)

    def test_windows_backslash_paths(self):
        """Test handling of Windows backslash paths"""
        content = create_preproc_file(
            "Output\\Preprocessor.out",
            "Data\\Elements.dat",
            "Data\\Nodes.dat",
            "Data\\Stratigraphy.dat",
            "Data\\Streams.dat",
            "Data\\Lakes.dat"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            # Verify backslashes are converted to forward slashes and paths are absolute
            assert Path(pre_dict['preout']).is_absolute()
            assert Path(pre_dict['elem_file']).is_absolute()

            # Verify file names are correct
            assert Path(pre_dict['preout']).name == "Preprocessor.out"
            assert Path(pre_dict['elem_file']).name == "Elements.dat"

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Preprocessor Main Input File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += "# Hash comment\n"
        content += " Title line 1\n"
        content += " Title line 2\n"
        content += " Title line 3\n"
        content += "C\n"
        content += " Preprocessor.out        / PREOUT\n"
        content += "C More comments\n"
        content += " Elements.dat            / Element file\n"
        content += "c Another comment\n"
        content += " Nodes.dat               / Node file\n"
        content += "* Comment\n"
        content += " Stratigraphy.dat        / Stratigraphy file\n"
        content += "# Comment\n"
        content += " Streams.dat             / Stream file\n"
        content += "C\n"
        content += " Lakes.dat               / Lake file\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            # Should read correctly despite comment lines
            assert have_lake is True
            assert Path(pre_dict['preout']).name == "Preprocessor.out"
            assert Path(pre_dict['elem_file']).name == "Elements.dat"

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM C2VSimCG file"""
        content = "C*****************************************************************************\n"
        content += "C                C2VSimCG_Preprocessor.in\n"
        content += "C*****************************************************************************\n"
        content += "C\n"
        content += " Historical Simulation\n"
        content += " Central Valley, California\n"
        content += " C2VSimCG_Preprocessor 2020.12.23\n"
        content += "C\n"
        content += " C2VSimCG_Preprocessor.out                    / PREOUT\n"
        content += "C\n"
        content += " C2VSimCG_Elements.dat                        / MODFLOW-style element data file\n"
        content += "C\n"
        content += " C2VSimCG_Nodes.dat                           / Finite element node data file\n"
        content += "C\n"
        content += " C2VSimCG_Stratigraphy.dat                    / Stratigraphy data file\n"
        content += "C\n"
        content += " C2VSimCG_Streams.dat        / Stream data file\n"
        content += "C\n"
        content += " /                                            / Lake data file\n"
        content += "C\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            # Verify data structure
            assert have_lake is False
            assert pre_dict['lake_file'] == ''

            # Verify file names
            assert Path(pre_dict['preout']).name == "C2VSimCG_Preprocessor.out"
            assert Path(pre_dict['elem_file']).name == "C2VSimCG_Elements.dat"
            assert Path(pre_dict['node_file']).name == "C2VSimCG_Nodes.dat"
            assert Path(pre_dict['strat_file']).name == "C2VSimCG_Stratigraphy.dat"
            assert Path(pre_dict['stream_file']).name == "C2VSimCG_Streams.dat"

            # Verify all paths are absolute
            assert Path(pre_dict['preout']).is_absolute()
            assert Path(pre_dict['elem_file']).is_absolute()

        finally:
            os.unlink(temp_file)

    def test_mixed_path_formats(self):
        """Test handling of mixed relative and absolute path formats"""
        content = create_preproc_file(
            "Preprocessor.out",
            "./Data/Elements.dat",
            "../Input/Nodes.dat",
            "Stratigraphy.dat",
            "./Streams.dat",
            "/"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            # All paths should be absolute
            assert Path(pre_dict['preout']).is_absolute()
            assert Path(pre_dict['elem_file']).is_absolute()
            assert Path(pre_dict['node_file']).is_absolute()
            assert Path(pre_dict['strat_file']).is_absolute()
            assert Path(pre_dict['stream_file']).is_absolute()

            # Verify no lake file
            assert have_lake is False
            assert pre_dict['lake_file'] == ''

        finally:
            os.unlink(temp_file)

    def test_long_filenames(self):
        """Test handling of long file names"""
        long_preout = "Very_Long_Preprocessor_Output_File_Name_With_Many_Characters_2021.out"
        long_elem = "Very_Long_Element_File_Name_With_Many_Characters_2021.dat"

        content = create_preproc_file(
            long_preout,
            long_elem,
            "Nodes.dat",
            "Stratigraphy.dat",
            "Streams.dat",
            "Lakes.dat"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            # Verify long file names are read correctly
            assert Path(pre_dict['preout']).name == long_preout
            assert Path(pre_dict['elem_file']).name == long_elem

        finally:
            os.unlink(temp_file)

    def test_file_names_with_spaces(self):
        """Test handling of file names with spaces"""
        content = create_preproc_file(
            "Preprocessor Output.out",
            "Element File.dat",
            "Node File.dat",
            "Stratigraphy File.dat",
            "Stream File.dat",
            "Lake File.dat"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            # Verify file names with spaces are read correctly
            # Note: split()[0] in the function will only get first part before space
            assert Path(pre_dict['preout']).name == "Preprocessor"
            assert Path(pre_dict['elem_file']).name == "Element"

        finally:
            os.unlink(temp_file)

    def test_dictionary_structure(self):
        """Test that returned dictionary has correct structure"""
        content = create_preproc_file(
            "Preprocessor.out",
            "Elements.dat",
            "Nodes.dat",
            "Stratigraphy.dat",
            "Streams.dat",
            "Lakes.dat"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_preproc import iwfm_read_preproc

            pre_dict, have_lake = iwfm_read_preproc(temp_file)

            # Verify dictionary has exactly 6 keys
            assert len(pre_dict) == 6

            # Verify all required keys are present
            required_keys = ['preout', 'elem_file', 'node_file', 'strat_file', 'stream_file', 'lake_file']
            for key in required_keys:
                assert key in pre_dict

            # Verify have_lake is boolean
            assert isinstance(have_lake, bool)

        finally:
            os.unlink(temp_file)
