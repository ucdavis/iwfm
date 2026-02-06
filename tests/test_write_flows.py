# test_write_flows.py
# Unit tests for write_flows.py - Write flow data to CSV file
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
import os


class TestWriteFlows:
    """Tests for write_flows function"""

    def test_basic_functionality(self, tmp_path):
        """Test basic functionality with simple data."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'test_output.dat')
        file_type = '_flows'
        
        # table: columns of data (will be transposed)
        table = [
            ['2020-01', '2020-02', '2020-03'],  # dates
            [100.0, 110.0, 120.0],              # values col 1
            [200.0, 210.0, 220.0],              # values col 2
        ]
        # site_info: header rows (will be transposed)
        site_info = [
            ['Date', 'Site1', 'Site2'],
            ['', 'cfs', 'cfs'],
        ]

        write_flows(data_file_base, file_type, table, site_info, verbose=False)

        expected_file = str(tmp_path / 'test_output_flows.csv')
        assert os.path.exists(expected_file)

    def test_output_filename_construction(self, tmp_path):
        """Test that output filename is correctly constructed."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'mydata.txt')
        file_type = '_monthly'
        
        table = [['2020-01'], [100.0]]
        site_info = [['Date', 'Site1']]

        write_flows(data_file_base, file_type, table, site_info, verbose=False)

        expected_file = str(tmp_path / 'mydata_monthly.csv')
        assert os.path.exists(expected_file)

    def test_header_rows_transposed(self, tmp_path):
        """Test that site_info is transposed correctly into header rows."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'test.dat')
        file_type = '_test'
        
        table = [['2020-01'], [100.0], [200.0]]
        # 2 header info rows, 3 columns
        site_info = [
            ['Date', 'Site_A', 'Site_B'],
            ['', 'Units_A', 'Units_B'],
        ]

        write_flows(data_file_base, file_type, table, site_info, verbose=False)

        with open(str(tmp_path / 'test_test.csv'), 'r') as f:
            lines = f.readlines()

        # First two lines should be transposed site_info
        # After transpose: each row is one column of original site_info
        assert 'Date' in lines[0]
        assert 'Site_A' in lines[1]
        assert 'Site_B' in lines[2]

    def test_data_rows_transposed(self, tmp_path):
        """Test that table data is transposed correctly into rows."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'test.dat')
        file_type = '_test'
        
        # 3 columns, 2 rows of data
        table = [
            ['2020-01', '2020-02'],  # dates
            [100.0, 110.0],          # Site1 values
            [200.0, 210.0],          # Site2 values
        ]
        site_info = [['Date', 'Site1', 'Site2']]

        write_flows(data_file_base, file_type, table, site_info, verbose=False)

        with open(str(tmp_path / 'test_test.csv'), 'r') as f:
            lines = f.readlines()

        # After site_info (1 row transposed to 3 lines), data starts
        # Each line is a transposed column from table
        # Line with 2020-01, 100.0, 200.0 and line with 2020-02, 110.0, 210.0
        content = ''.join(lines)
        assert '2020-01' in content
        assert '2020-02' in content
        assert '100.0' in content or '100' in content
        assert '200.0' in content or '200' in content

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output displays write information."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'test.dat')
        file_type = '_test'
        
        table = [
            ['2020-01', '2020-02', '2020-03'],
            [100.0, 110.0, 120.0],
        ]
        site_info = [['Date', 'Site1']]

        write_flows(data_file_base, file_type, table, site_info, verbose=True)

        captured = capsys.readouterr()
        assert 'Wrote' in captured.out
        assert 'cols' in captured.out
        assert 'rows' in captured.out

    def test_single_column_single_row(self, tmp_path):
        """Test minimal case with single column and row."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'test.dat')
        file_type = '_test'
        
        table = [['value1']]
        site_info = [['Header1']]

        write_flows(data_file_base, file_type, table, site_info, verbose=False)

        expected_file = str(tmp_path / 'test_test.csv')
        assert os.path.exists(expected_file)
        
        with open(expected_file, 'r') as f:
            content = f.read()
        
        assert 'Header1' in content
        assert 'value1' in content

    def test_many_columns(self, tmp_path):
        """Test with many columns of data."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'test.dat')
        file_type = '_test'
        
        num_cols = 50
        table = [[f'val_{i}'] for i in range(num_cols)]
        site_info = [[f'Col_{i}' for i in range(num_cols)]]

        write_flows(data_file_base, file_type, table, site_info, verbose=False)

        expected_file = str(tmp_path / 'test_test.csv')
        with open(expected_file, 'r') as f:
            lines = f.readlines()

        # site_info transposed: 50 lines (one per column)
        # table transposed: 1 line (one row of data)
        assert len(lines) == 51

    def test_many_rows(self, tmp_path):
        """Test with many rows of data."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'test.dat')
        file_type = '_test'
        
        num_rows = 100
        table = [[f'date_{i}' for i in range(num_rows)]]
        site_info = [['Date']]

        write_flows(data_file_base, file_type, table, site_info, verbose=False)

        expected_file = str(tmp_path / 'test_test.csv')
        with open(expected_file, 'r') as f:
            lines = f.readlines()

        # 1 header line + 100 data rows (transposed)
        assert len(lines) == 101

    def test_numeric_values(self, tmp_path):
        """Test with various numeric values."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'test.dat')
        file_type = '_test'
        
        table = [
            ['2020-01'],
            [123.456],
            [-50.0],
            [0.0],
            [999999.99],
        ]
        site_info = [['Date', 'Site1', 'Site2', 'Site3', 'Site4']]

        write_flows(data_file_base, file_type, table, site_info, verbose=False)

        expected_file = str(tmp_path / 'test_test.csv')
        with open(expected_file, 'r') as f:
            content = f.read()

        assert '123.456' in content
        assert '-50' in content
        assert '999999.99' in content

    def test_file_type_variations(self, tmp_path):
        """Test different file_type values."""
        from iwfm.write_flows import write_flows

        table = [['val']]
        site_info = [['Header']]

        # Test various file_type strings
        file_types = ['_daily', '_monthly', '_annual', '_raw', '']
        
        for ft in file_types:
            data_file_base = str(tmp_path / f'test{ft}.dat')
            write_flows(data_file_base, ft, table, site_info, verbose=False)
            
            expected_file = str(tmp_path / f'test{ft}{ft}.csv')
            assert os.path.exists(expected_file), f"File not created for file_type='{ft}'"

    def test_return_value(self, tmp_path):
        """Test that function returns None."""
        from iwfm.write_flows import write_flows

        data_file_base = str(tmp_path / 'test.dat')
        file_type = '_test'
        table = [['val']]
        site_info = [['Header']]

        result = write_flows(data_file_base, file_type, table, site_info, verbose=False)

        assert result is None

    def test_csv_format(self, tmp_path):
        """Test that output is valid CSV format."""
        from iwfm.write_flows import write_flows
        import csv

        data_file_base = str(tmp_path / 'test.dat')
        file_type = '_test'
        
        table = [
            ['2020-01', '2020-02'],
            [100.0, 110.0],
            [200.0, 210.0],
        ]
        site_info = [['Date', 'Site1', 'Site2']]

        write_flows(data_file_base, file_type, table, site_info, verbose=False)

        expected_file = str(tmp_path / 'test_test.csv')
        
        # Should be readable as valid CSV
        with open(expected_file, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        assert len(rows) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
