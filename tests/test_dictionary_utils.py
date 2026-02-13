# test_dictionary_utils.py
# unit test for dictionary methods in the iwfm package
# Copyright (C) 2025 University of California
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
"""Tests for dictionary utility functions in the iwfm package."""

import tempfile
import os
import iwfm


class TestFile2Dict:
    """Test the file2dict function."""
    
    def create_temp_file(self, content):
        """Helper to create temporary file with content."""
        fd, path = tempfile.mkstemp(text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)
            return path
        except:
            os.close(fd)
            raise
    
    def test_file2dict_basic(self):
        """Test basic file to dictionary conversion."""
        content = "key1\tval1\nkey2\tval2\nkey3\tval3"
        file_path = self.create_temp_file(content)
        try:
            result = iwfm.file2dict(file_path)
            expected = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
            assert result == expected
        finally:
            os.unlink(file_path)
    
    def test_file2dict_comma_separated(self):
        """Test with comma-separated values."""
        content = "key1,val1\nkey2,val2\nkey3,val3"
        file_path = self.create_temp_file(content)
        try:
            result = iwfm.file2dict(file_path)
            expected = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
            assert result == expected
        finally:
            os.unlink(file_path)
    
    def test_file2dict_numeric_conversion(self):
        """Test with type conversion."""
        content = "1\t10\n2\t20\n3\t30"
        file_path = self.create_temp_file(content)
        try:
            result = iwfm.file2dict(file_path, key_type=int, val_type=int)
            expected = {1: 10, 2: 20, 3: 30}
            assert result == expected
        finally:
            os.unlink(file_path)
    
    def test_file2dict_custom_fields(self):
        """Test with custom key and value fields."""
        content = "ignore\tkey1\tval1\nignore\tkey2\tval2"
        file_path = self.create_temp_file(content)
        try:
            result = iwfm.file2dict(file_path, key_field=1, val_field=2)
            expected = {'key1': 'val1', 'key2': 'val2'}
            assert result == expected
        finally:
            os.unlink(file_path)
    
    def test_file2dict_skip_header(self):
        """Test with header line to skip."""
        content = "HEADER_KEY\tHEADER_VAL\nkey1\tval1\nkey2\tval2"
        file_path = self.create_temp_file(content)
        try:
            result = iwfm.file2dict(file_path, skip=1)
            expected = {'key1': 'val1', 'key2': 'val2'}
            assert result == expected
        finally:
            os.unlink(file_path)
    
    def test_file2dict_mixed_separators(self):
        """Test with mixed separators (semicolon, asterisk)."""
        content = "key1;val1\nkey2*val2\nkey3\tval3"
        file_path = self.create_temp_file(content)
        try:
            result = iwfm.file2dict(file_path)
            expected = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
            assert result == expected
        finally:
            os.unlink(file_path)
    
    def test_file2dict_error_handling(self):
        """Test error handling for malformed lines."""
        content = "key1\tval1\nmalformed_line\nkey2\tval2"
        file_path = self.create_temp_file(content)
        try:
            # Should continue processing despite malformed line
            result = iwfm.file2dict(file_path)
            # The malformed line should be skipped
            expected = {'key1': 'val1', 'key2': 'val2'}
            assert result == expected
        finally:
            os.unlink(file_path)


class TestHydDict:
    """Test the hyd_dict function."""
    
    def create_temp_groundwater_file(self):
        """Helper to create a temporary groundwater.dat file."""
        content = """C Groundwater.dat file
C 
C Comment lines
C
C More comments
C Number of hydrographs (skip 20 lines as per function)
C 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
20
5
C
C More header
C 
C column layer x y well_name
1 1 1 100.0 200.0 WELL_01
2 2 1 150.0 250.0 WELL_02
3 3 1 200.0 300.0 WELL_03
4 4 2 250.0 350.0 WELL_04
5 5 2 300.0 400.0 WELL_05"""
        
        fd, path = tempfile.mkstemp(text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)
            return path
        except:
            os.close(fd)
            raise
    
    def test_hyd_dict_basic(self):
        """Test basic hydrograph dictionary creation."""
        file_path = self.create_temp_groundwater_file()
        try:
            result = iwfm.hyd_dict(file_path)
            
            # Check structure - should have 5 wells
            assert len(result) == 5
            
            # Check specific well data
            assert 'well_01' in result
            well_01_data = result['well_01']
            assert well_01_data[0] == 1    # column number
            assert well_01_data[1] == 100.0  # x coordinate
            assert well_01_data[2] == 200.0  # y coordinate
            assert well_01_data[3] == 1    # model layer
            assert well_01_data[4] == 'well_01'  # well name
            
            # Check another well
            assert 'well_04' in result
            well_04_data = result['well_04']
            assert well_04_data[0] == 4
            assert well_04_data[1] == 250.0
            assert well_04_data[2] == 350.0
            assert well_04_data[3] == 2
            assert well_04_data[4] == 'well_04'
            
        finally:
            os.unlink(file_path)