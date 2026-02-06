# test_write_2_dat.py
# Unit tests for write_2_dat.py - Write 3D array to fixed-width DAT files
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
from datetime import datetime
import os


class TestWrite2Dat:
    """Tests for write_2_dat function"""

    def test_basic_functionality(self, tmp_path):
        """Test basic functionality with simple data."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        # 2 crops, 3 elements, 2 time steps
        data = [
            [[10.0, 20.0], [11.0, 21.0], [12.0, 22.0]],  # crop 1
            [[30.0, 40.0], [31.0, 41.0], [32.0, 42.0]],  # crop 2
        ]
        crop_list = ['Crop1', 'Crop2']
        elem_list = [1, 2, 3]
        no_time_steps = 2
        date_list = [datetime(2020, 1, 1), datetime(2021, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        # Check files were created
        assert os.path.exists(f'{file_base}_1.dat')
        assert os.path.exists(f'{file_base}_2.dat')

    def test_creates_correct_number_of_files(self, tmp_path):
        """Test that correct number of files are created based on crop_list."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        # 5 crops
        data = [[[1.0]], [[2.0]], [[3.0]], [[4.0]], [[5.0]]]
        crop_list = ['C1', 'C2', 'C3', 'C4', 'C5']
        elem_list = [1]
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        for i in range(1, 6):
            assert os.path.exists(f'{file_base}_{i}.dat')

    def test_header_format(self, tmp_path):
        """Test that header row contains WYr and years with spacing."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        data = [[[10.0, 20.0, 30.0]]]
        crop_list = ['Crop1']
        elem_list = [1]
        no_time_steps = 3
        date_list = [datetime(2018, 1, 1), datetime(2019, 1, 1), datetime(2020, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.dat', 'r') as f:
            header = f.readline()

        # Header should contain WYr and years
        assert 'WYr' in header
        assert '2018' in header
        assert '2019' in header
        assert '2020' in header

    def test_fixed_width_element_format(self, tmp_path):
        """Test that element numbers are formatted with fixed width (6 digits)."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        data = [[[100.0], [200.0]]]
        crop_list = ['Crop1']
        elem_list = [1, 999]
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.dat', 'r') as f:
            lines = f.readlines()

        # Element 1 should be right-justified in 6 characters
        assert lines[1].startswith('     1 ')
        # Element 999 should be right-justified in 6 characters
        assert lines[2].startswith('   999 ')

    def test_fixed_width_data_format(self, tmp_path):
        """Test that data values are formatted with fixed width (20.4f)."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        data = [[[123.4567]]]
        crop_list = ['Crop1']
        elem_list = [1]
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.dat', 'r') as f:
            lines = f.readlines()

        # Data should be formatted with 4 decimal places
        assert '123.4567' in lines[1]

    def test_multiple_crops_different_data(self, tmp_path):
        """Test that each crop file contains correct data."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        data = [
            [[111.1111]],  # crop 1
            [[222.2222]],  # crop 2
        ]
        crop_list = ['Crop1', 'Crop2']
        elem_list = [1]
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        # Check crop 1 file
        with open(f'{file_base}_1.dat', 'r') as f:
            content = f.read()
        assert '111.1111' in content

        # Check crop 2 file
        with open(f'{file_base}_2.dat', 'r') as f:
            content = f.read()
        assert '222.2222' in content

    def test_single_element_single_timestep(self, tmp_path):
        """Test minimal case with single element and timestep."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        data = [[[42.0]]]
        crop_list = ['OnlyCrop']
        elem_list = [99]
        no_time_steps = 1
        date_list = [datetime(2025, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.dat', 'r') as f:
            lines = f.readlines()

        assert len(lines) == 2  # header + 1 data row
        assert '2025' in lines[0]
        assert '42.0' in lines[1]

    def test_many_elements(self, tmp_path):
        """Test with many elements."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        num_elems = 100
        data = [[[float(i)] for i in range(num_elems)]]
        crop_list = ['Crop1']
        elem_list = list(range(1, num_elems + 1))
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.dat', 'r') as f:
            lines = f.readlines()

        # Header + 100 data rows
        assert len(lines) == 101

    def test_large_element_numbers(self, tmp_path):
        """Test with large element numbers."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        data = [[[1.0], [2.0], [3.0]]]
        crop_list = ['Crop1']
        elem_list = [100000, 200000, 999999]  # Large 6-digit numbers
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.dat', 'r') as f:
            lines = f.readlines()

        assert '100000' in lines[1]
        assert '200000' in lines[2]
        assert '999999' in lines[3]

    def test_negative_values(self, tmp_path):
        """Test with negative data values."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        data = [[[-123.4567, -0.0001]]]
        crop_list = ['Crop1']
        elem_list = [1]
        no_time_steps = 2
        date_list = [datetime(2020, 1, 1), datetime(2021, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.dat', 'r') as f:
            content = f.read()

        assert '-123.4567' in content

    def test_zero_values(self, tmp_path):
        """Test with zero data values."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        data = [[[0.0, 0.0]]]
        crop_list = ['Crop1']
        elem_list = [1]
        no_time_steps = 2
        date_list = [datetime(2020, 1, 1), datetime(2021, 1, 1)]

        write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.dat', 'r') as f:
            content = f.read()

        assert '0.0000' in content

    def test_return_value(self, tmp_path):
        """Test that function returns None."""
        from iwfm.write_2_dat import write_2_dat

        file_base = str(tmp_path / 'test_output')
        
        data = [[[1.0]]]
        crop_list = ['Crop1']
        elem_list = [1]
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        result = write_2_dat(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        assert result is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
