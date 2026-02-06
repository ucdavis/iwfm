# test_write_2_csv.py
# Unit tests for write_2_csv.py - Write 3D array to CSV files
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


class TestWrite2Csv:
    """Tests for write_2_csv function"""

    def test_basic_functionality(self, tmp_path):
        """Test basic functionality with simple data."""
        from iwfm.write_2_csv import write_2_csv

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

        write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        # Check files were created
        assert os.path.exists(f'{file_base}_1.csv')
        assert os.path.exists(f'{file_base}_2.csv')

    def test_creates_correct_number_of_files(self, tmp_path):
        """Test that correct number of files are created based on crop_list."""
        from iwfm.write_2_csv import write_2_csv

        file_base = str(tmp_path / 'test_output')
        
        # 4 crops
        data = [
            [[1.0]], [[2.0]], [[3.0]], [[4.0]]
        ]
        crop_list = ['C1', 'C2', 'C3', 'C4']
        elem_list = [1]
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        for i in range(1, 5):
            assert os.path.exists(f'{file_base}_{i}.csv')

    def test_header_format(self, tmp_path):
        """Test that header row contains WYr and years."""
        from iwfm.write_2_csv import write_2_csv

        file_base = str(tmp_path / 'test_output')
        
        data = [[[10.0, 20.0, 30.0]]]
        crop_list = ['Crop1']
        elem_list = [1]
        no_time_steps = 3
        date_list = [datetime(2018, 1, 1), datetime(2019, 1, 1), datetime(2020, 1, 1)]

        write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.csv', 'r') as f:
            header = f.readline().strip()

        assert header == 'WYr,2018,2019,2020'

    def test_data_rows_format(self, tmp_path):
        """Test that data rows contain element number and values."""
        from iwfm.write_2_csv import write_2_csv

        file_base = str(tmp_path / 'test_output')
        
        data = [[[100.5, 200.5], [101.5, 201.5]]]
        crop_list = ['Crop1']
        elem_list = [10, 20]
        no_time_steps = 2
        date_list = [datetime(2020, 1, 1), datetime(2021, 1, 1)]

        write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.csv', 'r') as f:
            lines = f.readlines()

        # Check data rows (skip header)
        assert lines[1].strip() == '10,100.5,200.5'
        assert lines[2].strip() == '20,101.5,201.5'

    def test_multiple_crops_different_data(self, tmp_path):
        """Test that each crop file contains correct data."""
        from iwfm.write_2_csv import write_2_csv

        file_base = str(tmp_path / 'test_output')
        
        data = [
            [[1.1, 1.2]],  # crop 1
            [[2.1, 2.2]],  # crop 2
        ]
        crop_list = ['Crop1', 'Crop2']
        elem_list = [1]
        no_time_steps = 2
        date_list = [datetime(2020, 1, 1), datetime(2021, 1, 1)]

        write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        # Check crop 1 file
        with open(f'{file_base}_1.csv', 'r') as f:
            lines = f.readlines()
        assert '1.1' in lines[1] and '1.2' in lines[1]

        # Check crop 2 file
        with open(f'{file_base}_2.csv', 'r') as f:
            lines = f.readlines()
        assert '2.1' in lines[1] and '2.2' in lines[1]

    def test_single_element_single_timestep(self, tmp_path):
        """Test minimal case with single element and timestep."""
        from iwfm.write_2_csv import write_2_csv

        file_base = str(tmp_path / 'test_output')
        
        data = [[[42.0]]]
        crop_list = ['OnlyCrop']
        elem_list = [99]
        no_time_steps = 1
        date_list = [datetime(2025, 1, 1)]

        write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.csv', 'r') as f:
            lines = f.readlines()

        assert lines[0].strip() == 'WYr,2025'
        assert lines[1].strip() == '99,42.0'

    def test_many_elements(self, tmp_path):
        """Test with many elements."""
        from iwfm.write_2_csv import write_2_csv

        file_base = str(tmp_path / 'test_output')
        
        num_elems = 100
        data = [[[float(i)] for i in range(num_elems)]]
        crop_list = ['Crop1']
        elem_list = list(range(1, num_elems + 1))
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.csv', 'r') as f:
            lines = f.readlines()

        # Header + 100 data rows
        assert len(lines) == 101

    def test_many_timesteps(self, tmp_path):
        """Test with many time steps."""
        from iwfm.write_2_csv import write_2_csv

        file_base = str(tmp_path / 'test_output')
        
        num_steps = 50
        data = [[[float(i) for i in range(num_steps)]]]
        crop_list = ['Crop1']
        elem_list = [1]
        no_time_steps = num_steps
        date_list = [datetime(1970 + i, 1, 1) for i in range(num_steps)]

        write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.csv', 'r') as f:
            header = f.readline().strip()

        # Header should have WYr + 50 years
        parts = header.split(',')
        assert len(parts) == 51  # WYr + 50 years

    def test_float_precision(self, tmp_path):
        """Test that float values are written correctly."""
        from iwfm.write_2_csv import write_2_csv

        file_base = str(tmp_path / 'test_output')
        
        data = [[[123.456789, 0.001, 999999.99]]]
        crop_list = ['Crop1']
        elem_list = [1]
        no_time_steps = 3
        date_list = [datetime(2020, 1, 1), datetime(2021, 1, 1), datetime(2022, 1, 1)]

        write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        with open(f'{file_base}_1.csv', 'r') as f:
            lines = f.readlines()

        # Values should be present (exact format depends on float conversion)
        data_line = lines[1]
        assert '123.456789' in data_line
        assert '0.001' in data_line
        assert '999999.99' in data_line

    def test_return_value(self, tmp_path):
        """Test that function returns None."""
        from iwfm.write_2_csv import write_2_csv

        file_base = str(tmp_path / 'test_output')
        
        data = [[[1.0]]]
        crop_list = ['Crop1']
        elem_list = [1]
        no_time_steps = 1
        date_list = [datetime(2020, 1, 1)]

        result = write_2_csv(file_base, data, crop_list, elem_list, no_time_steps, date_list)

        assert result is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
