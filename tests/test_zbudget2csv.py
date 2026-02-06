# test_zbudget2csv.py
# Unit tests for zbudget2csv.py - Write IWFM ZBudget data to CSV file
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
import pandas as pd
from datetime import datetime
import os


class TestZbudget2Csv:
    """Tests for zbudget2csv function"""

    def create_mock_dataframe(self, num_rows=3, num_cols=5):
        """Helper to create a mock zbudget dataframe with datetime index."""
        dates = [datetime(2020, 1, 1) + pd.Timedelta(days=i*30) for i in range(num_rows)]
        data = {f'col_{i}': [float(i * 10 + j) for j in range(num_rows)] for i in range(1, num_cols)}
        df = pd.DataFrame(data)
        df.insert(0, 'Time', dates)
        return df

    def test_basic_functionality(self, tmp_path):
        """Test basic functionality with ROOT ZONE budget type."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test_zbudget.csv')
        
        zone_names = ['Zone_A', 'Zone_B']
        column_headers = [
            [['Time', 'Inflow', 'Outflow', 'Storage', 'Error']],
            [['Time', 'Inflow', 'Outflow', 'Storage', 'Error']],
        ]
        zone_values = [
            self.create_mock_dataframe(num_rows=3, num_cols=5),
            self.create_mock_dataframe(num_rows=3, num_cols=5),
        ]
        # ROOT ZONE type (not GROUNDWATER, so no column removal)
        titles = [
            ['Title Line 1', 'ROOT ZONE BUDGET for Zone 1'],
            ['Title Line 1', 'ROOT ZONE BUDGET for Zone 2'],
        ]
        zone_list = [1, 2]
        zone_extent_ids = {'horizontal': 0, 'vertical': 0}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles, 
                   zone_list, zone_extent_ids)

        assert os.path.exists(outfile)

    def test_output_file_created(self, tmp_path):
        """Test that output file is created."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'output.csv')
        
        zone_names = ['TestZone']
        column_headers = [[['Time', 'Value1', 'Value2']]]
        zone_values = [self.create_mock_dataframe(num_rows=2, num_cols=3)]
        titles = [['Title', 'LAND AND WATER USE BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        assert os.path.exists(outfile)
        assert os.path.getsize(outfile) > 0

    def test_header_format(self, tmp_path):
        """Test that CSV header contains ZoneNo, ZoneName, and column headers."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        zone_names = ['Zone_1']
        column_headers = [[['Time', 'Precipitation', 'ET', 'Runoff']]]
        zone_values = [self.create_mock_dataframe(num_rows=2, num_cols=4)]
        titles = [['Title', 'UNSATURATED ZONE BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            header = f.readline().strip()

        assert header.startswith('ZoneNo,ZoneName,')
        assert 'Time' in header
        assert 'Precipitation' in header
        assert 'ET' in header
        assert 'Runoff' in header

    def test_data_rows_contain_zone_info(self, tmp_path):
        """Test that data rows contain zone number and zone name."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        zone_names = ['Sacramento_Valley', 'San_Joaquin']
        column_headers = [
            [['Time', 'Value']],
            [['Time', 'Value']],
        ]
        zone_values = [
            self.create_mock_dataframe(num_rows=2, num_cols=2),
            self.create_mock_dataframe(num_rows=2, num_cols=2),
        ]
        titles = [
            ['Title', 'LAND USE BUDGET'],
            ['Title', 'LAND USE BUDGET'],
        ]
        zone_list = [10, 20]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        # Check zone info in data rows
        content = ''.join(lines[1:])  # Skip header
        assert '10,Sacramento_Valley' in content
        assert '20,San_Joaquin' in content

    def test_date_formatting(self, tmp_path):
        """Test that dates are formatted as MM/DD/YYYY."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        # Create dataframe with specific dates
        df = pd.DataFrame({
            'Time': [datetime(2020, 1, 15), datetime(2020, 6, 30), datetime(2020, 12, 31)],
            'Value': [1.0, 2.0, 3.0],
        })
        
        zone_names = ['Zone1']
        column_headers = [[['Time', 'Value']]]
        zone_values = [df]
        titles = [['Title', 'ROOT ZONE BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            content = f.read()

        assert '01/15/2020' in content
        assert '06/30/2020' in content
        assert '12/31/2020' in content

    def test_multiple_zones(self, tmp_path):
        """Test with multiple zones."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        num_zones = 5
        zone_names = [f'Zone_{i}' for i in range(num_zones)]
        column_headers = [[['Time', 'Val1', 'Val2']]] * num_zones
        zone_values = [self.create_mock_dataframe(num_rows=3, num_cols=3) for _ in range(num_zones)]
        titles = [['Title', 'LAND BUDGET']] * num_zones
        zone_list = list(range(1, num_zones + 1))
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        # Header + (5 zones * 3 rows each) = 16 lines
        assert len(lines) == 16

    def test_single_zone_single_row(self, tmp_path):
        """Test minimal case with single zone and single time step."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        df = pd.DataFrame({
            'Time': [datetime(2020, 9, 30)],
            'Storage': [1000.0],
        })
        
        zone_names = ['OnlyZone']
        column_headers = [[['Time', 'Storage']]]
        zone_values = [df]
        titles = [['Title', 'UNSATURATED BUDGET']]
        zone_list = [99]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        assert len(lines) == 2  # header + 1 data row
        assert '99,OnlyZone' in lines[1]
        assert '1000.0' in lines[1]

    def test_many_time_steps(self, tmp_path):
        """Test with many time steps."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        num_rows = 100
        zone_names = ['Zone1']
        column_headers = [[['Time', 'Value']]]
        zone_values = [self.create_mock_dataframe(num_rows=num_rows, num_cols=2)]
        titles = [['Title', 'ROOT ZONE BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        assert len(lines) == 101  # header + 100 data rows

    def test_negative_values(self, tmp_path):
        """Test with negative values."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        df = pd.DataFrame({
            'Time': [datetime(2020, 1, 1)],
            'Inflow': [100.5],
            'Outflow': [-50.25],
            'Net': [-150.75],
        })
        
        zone_names = ['Zone1']
        column_headers = [[['Time', 'Inflow', 'Outflow', 'Net']]]
        zone_values = [df]
        titles = [['Title', 'LAND BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            content = f.read()

        assert '-50.25' in content
        assert '-150.75' in content

    def test_csv_comma_separated(self, tmp_path):
        """Test that output is properly comma-separated."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        df = pd.DataFrame({
            'Time': [datetime(2020, 1, 1)],
            'A': [1.0],
            'B': [2.0],
            'C': [3.0],
        })
        
        zone_names = ['Zone1']
        column_headers = [[['Time', 'A', 'B', 'C']]]
        zone_values = [df]
        titles = [['Title', 'ROOT BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            data_line = f.readlines()[1]

        # Should have commas separating: ZoneNo, ZoneName, Time, A, B, C
        assert data_line.count(',') >= 5

    def test_return_value(self, tmp_path):
        """Test that function returns None."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        zone_names = ['Zone1']
        column_headers = [[['Time', 'Value']]]
        zone_values = [self.create_mock_dataframe(num_rows=1, num_cols=2)]
        titles = [['Title', 'LAND BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        result = zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                            zone_list, zone_extent_ids)

        assert result is None


class TestZbudget2CsvGroundwater:
    """Tests for zbudget2csv with GROUNDWATER budget type (column removal)."""

    def create_groundwater_dataframe(self, num_rows=3):
        """Create a mock GROUNDWATER zbudget dataframe with many columns.
        
        GROUNDWATER budgets have inter-zone flow columns (21 to n-2) that 
        should be removed.
        """
        dates = [datetime(2020, 1, 1) + pd.Timedelta(days=i*30) for i in range(num_rows)]
        
        # Create 30 columns: Time + 20 standard cols + 7 interzone + 2 final cols
        data = {'Time': dates}
        for i in range(1, 21):
            data[f'StdCol_{i}'] = [float(i * 10 + j) for j in range(num_rows)]
        for i in range(7):
            data[f'InterZone_{i}'] = [float(100 + i + j) for j in range(num_rows)]
        data['FinalCol_1'] = [float(200 + j) for j in range(num_rows)]
        data['FinalCol_2'] = [float(300 + j) for j in range(num_rows)]
        
        return pd.DataFrame(data)

    def create_groundwater_headers(self):
        """Create headers matching the groundwater dataframe."""
        headers = ['Time']
        for i in range(1, 21):
            headers.append(f'StdCol_{i}')
        for i in range(7):
            headers.append(f'InterZone_{i}')
        headers.append('FinalCol_1')
        headers.append('FinalCol_2')
        return headers

    def test_groundwater_type_detected(self, tmp_path):
        """Test that GROUNDWATER type is correctly detected from titles."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        zone_names = ['Zone1']
        column_headers = [[self.create_groundwater_headers()]]
        zone_values = [self.create_groundwater_dataframe(num_rows=2)]
        titles = [['Title Line 1', 'GROUNDWATER BUDGET for Subregion 1']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        assert os.path.exists(outfile)

    def test_groundwater_interzone_columns_removed_from_header(self, tmp_path):
        """Test that inter-zone columns (21 to n-2) are removed from header."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        zone_names = ['Zone1']
        column_headers = [[self.create_groundwater_headers()]]
        zone_values = [self.create_groundwater_dataframe(num_rows=2)]
        titles = [['Title', 'GROUNDWATER BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            header = f.readline()

        # Inter-zone columns should NOT be in header
        assert 'InterZone_0' not in header
        assert 'InterZone_6' not in header
        
        # Standard and final columns should still be present
        assert 'StdCol_1' in header
        assert 'StdCol_20' in header
        assert 'FinalCol_1' in header
        assert 'FinalCol_2' in header

    def test_groundwater_interzone_columns_removed_from_data(self, tmp_path):
        """Test that inter-zone columns are removed from data rows."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        zone_names = ['Zone1']
        column_headers = [[self.create_groundwater_headers()]]
        zone_values = [self.create_groundwater_dataframe(num_rows=1)]
        titles = [['Title', 'GROUNDWATER BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            lines = f.readlines()
            header_cols = lines[0].strip().split(',')
            data_cols = lines[1].strip().split(',')

        # Data row should have same number of columns as header
        assert len(data_cols) == len(header_cols)

    def test_groundwater_multiple_zones(self, tmp_path):
        """Test GROUNDWATER with multiple zones."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        num_zones = 3
        zone_names = [f'Subregion_{i}' for i in range(num_zones)]
        column_headers = [[self.create_groundwater_headers()]] * num_zones
        zone_values = [self.create_groundwater_dataframe(num_rows=2) for _ in range(num_zones)]
        titles = [['Title', 'GROUNDWATER BUDGET']] * num_zones
        zone_list = [1, 2, 3]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        # Header + (3 zones * 2 rows) = 7 lines
        assert len(lines) == 7

    def test_non_groundwater_no_column_removal(self, tmp_path):
        """Test that non-GROUNDWATER types don't have columns removed."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        # Use same structure but with ROOT ZONE type
        zone_names = ['Zone1']
        headers = self.create_groundwater_headers()
        column_headers = [[headers]]
        zone_values = [self.create_groundwater_dataframe(num_rows=1)]
        titles = [['Title', 'ROOT ZONE BUDGET']]  # Not GROUNDWATER
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            header = f.readline()

        # All columns should be present including inter-zone
        assert 'InterZone_0' in header
        assert 'InterZone_6' in header


class TestZbudget2CsvEdgeCases:
    """Edge case tests for zbudget2csv function."""

    def test_empty_zone_names(self, tmp_path):
        """Test with empty zone list."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        zone_names = []
        column_headers = [[['Time', 'Value']]]
        zone_values = []
        titles = []
        zone_list = []
        zone_extent_ids = {}

        # Should handle empty zones gracefully
        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        # Should have only header
        assert len(lines) == 1

    def test_special_characters_in_zone_name(self, tmp_path):
        """Test zone names with special characters."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        df = pd.DataFrame({
            'Time': [datetime(2020, 1, 1)],
            'Value': [100.0],
        })
        
        zone_names = ['Zone_With_Underscores', 'Zone-With-Dashes']
        column_headers = [[['Time', 'Value']]] * 2
        zone_values = [df.copy(), df.copy()]
        titles = [['Title', 'LAND BUDGET']] * 2
        zone_list = [1, 2]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            content = f.read()

        assert 'Zone_With_Underscores' in content
        assert 'Zone-With-Dashes' in content

    def test_large_numeric_values(self, tmp_path):
        """Test with large numeric values."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile = str(tmp_path / 'test.csv')
        
        df = pd.DataFrame({
            'Time': [datetime(2020, 1, 1)],
            'LargeValue': [123456789.123456],
            'SmallValue': [0.000001],
        })
        
        zone_names = ['Zone1']
        column_headers = [[['Time', 'LargeValue', 'SmallValue']]]
        zone_values = [df]
        titles = [['Title', 'ROOT BUDGET']]
        zone_list = [1]
        zone_extent_ids = {}

        zbudget2csv(outfile, zone_names, column_headers, zone_values, titles,
                   zone_list, zone_extent_ids)

        with open(outfile, 'r') as f:
            content = f.read()

        # Values should be present (exact format may vary)
        assert '123456789' in content

    def test_zone_extent_ids_not_used(self, tmp_path):
        """Test that zone_extent_ids parameter doesn't affect output."""
        from iwfm.zbudget2csv import zbudget2csv

        outfile1 = str(tmp_path / 'test1.csv')
        outfile2 = str(tmp_path / 'test2.csv')
        
        df = pd.DataFrame({
            'Time': [datetime(2020, 1, 1)],
            'Value': [100.0],
        })
        
        zone_names = ['Zone1']
        column_headers = [[['Time', 'Value']]]
        zone_values = [df]
        titles = [['Title', 'LAND BUDGET']]
        zone_list = [1]

        # Write with different zone_extent_ids
        zbudget2csv(outfile1, zone_names, column_headers, [df.copy()], titles,
                   zone_list, {'horizontal': 0, 'vertical': 0})
        zbudget2csv(outfile2, zone_names, column_headers, [df.copy()], titles,
                   zone_list, {'horizontal': 1, 'vertical': 1})

        with open(outfile1, 'r') as f1, open(outfile2, 'r') as f2:
            content1 = f1.read()
            content2 = f2.read()

        # Output should be identical
        assert content1 == content2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
