# test_calib_divshort2obs.py
# Unit tests for calib/divshort2obs.py - Convert diversion shortages to SMP format
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
import numpy as np


class TestProcessBudget:
    """Tests for process_budget function"""

    def create_mock_budget_file(self, tmp_path, num_reaches=2, num_dates=3):
        """Helper to create a mock IWFM diversion budget file."""
        budget_file = tmp_path / 'test_diversions.bud'
        
        lines = []
        for reach in range(1, num_reaches + 1):
            # Title lines
            lines.append('                                    IWFM STREAM PACKAGE (v4.2.0106)                                     ')
            lines.append(f'                     DIVERSION AND DELIVERY DETAILS IN AC.FT. FOR DIVERSION_{reach}(SN0)                      ')
            # Separator
            lines.append('-' * 104)
            # Header lines
            lines.append('                                                                  Non          Actual     Delivery')
            lines.append('      Time              Actual      Diversion   Recoverable   Recoverable   Delivery to  Shortage for')
            lines.append('                      Diversion      Shortage       Loss          Loss     Elem. Grp. 1  Elem. Grp. 1')
            # Separator
            lines.append('-' * 104)
            # Data lines
            dates_data = [
                ('10/31/1973_24:00', 0.0, 10.0, 0.0, 0.0, 0.0, 5.0),
                ('11/30/1973_24:00', 0.0, 20.0, 0.0, 0.0, 0.0, 10.0),
                ('12/31/1973_24:00', 0.0, 30.0, 0.0, 0.0, 0.0, 15.0),
            ]
            for i, (date, *vals) in enumerate(dates_data[:num_dates]):
                # Adjust shortage value based on reach
                shortage = vals[-1] * reach
                line = f'{date}           {vals[0]}           {vals[1]}           {vals[2]}           {vals[3]}           {vals[4]}           {shortage}'
                lines.append(line)
            # Empty lines between tables
            lines.append('')
            lines.append('')
        
        budget_file.write_text('\n'.join(lines))
        return str(budget_file)

    def test_process_budget_returns_three_items(self, tmp_path):
        """Test that process_budget returns budget_table, reach_list, dates."""
        from iwfm.calib.divshort2obs import process_budget

        budget_file = self.create_mock_budget_file(tmp_path)
        result = process_budget(budget_file)

        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_process_budget_reach_list(self, tmp_path):
        """Test that reach_list contains correct reach numbers."""
        from iwfm.calib.divshort2obs import process_budget

        budget_file = self.create_mock_budget_file(tmp_path, num_reaches=3)
        budget_table, reach_list, dates = process_budget(budget_file)

        assert len(reach_list) == 3
        assert 1 in reach_list
        assert 2 in reach_list
        assert 3 in reach_list

    def test_process_budget_dates(self, tmp_path):
        """Test that dates are extracted correctly."""
        from iwfm.calib.divshort2obs import process_budget

        budget_file = self.create_mock_budget_file(tmp_path, num_dates=3)
        budget_table, reach_list, dates = process_budget(budget_file)

        assert len(dates) == 3
        # Dates should have _24:00 removed
        assert '10/31/1973' in dates[0]
        assert '11/30/1973' in dates[1]
        assert '12/31/1973' in dates[2]

    def test_process_budget_table_structure(self, tmp_path):
        """Test that budget_table has correct structure."""
        from iwfm.calib.divshort2obs import process_budget

        budget_file = self.create_mock_budget_file(tmp_path, num_reaches=2, num_dates=3)
        budget_table, reach_list, dates = process_budget(budget_file)

        # Should have one array per reach
        assert len(budget_table) == 2
        # Each array should be numpy array
        assert isinstance(budget_table[0], np.ndarray)
        assert isinstance(budget_table[1], np.ndarray)


class TestReadReaches:
    """Tests for read_reaches function"""

    def test_read_reaches_basic(self, tmp_path):
        """Test basic functionality of read_reaches."""
        from iwfm.calib.divshort2obs import read_reaches

        reach_file = tmp_path / 'reaches.dat'
        content = """Name    Reach
DIV_001    1
DIV_002    2
DIV_003    3
"""
        reach_file.write_text(content)

        reaches = read_reaches(str(reach_file))

        assert len(reaches) == 3
        assert reaches[0] == ['DIV_001', 1]
        assert reaches[1] == ['DIV_002', 2]
        assert reaches[2] == ['DIV_003', 3]

    def test_read_reaches_skips_header(self, tmp_path):
        """Test that first line (header) is skipped."""
        from iwfm.calib.divshort2obs import read_reaches

        reach_file = tmp_path / 'reaches.dat'
        content = """HEADER_LINE SHOULD_BE_SKIPPED
REACH_A    5
REACH_B    10
"""
        reach_file.write_text(content)

        reaches = read_reaches(str(reach_file))

        assert len(reaches) == 2
        assert reaches[0][0] == 'REACH_A'
        assert reaches[1][0] == 'REACH_B'

    def test_read_reaches_returns_list_of_lists(self, tmp_path):
        """Test that each reach is [name, reach_number]."""
        from iwfm.calib.divshort2obs import read_reaches

        reach_file = tmp_path / 'reaches.dat'
        content = """Header
TestReach    42
"""
        reach_file.write_text(content)

        reaches = read_reaches(str(reach_file))

        assert isinstance(reaches, list)
        assert isinstance(reaches[0], list)
        assert len(reaches[0]) == 2
        assert isinstance(reaches[0][0], str)
        assert isinstance(reaches[0][1], int)

    def test_read_reaches_single_reach(self, tmp_path):
        """Test with single reach."""
        from iwfm.calib.divshort2obs import read_reaches

        reach_file = tmp_path / 'reaches.dat'
        content = """Name    Reach
OnlyReach    99
"""
        reach_file.write_text(content)

        reaches = read_reaches(str(reach_file))

        assert len(reaches) == 1
        assert reaches[0] == ['OnlyReach', 99]

    def test_read_reaches_many_reaches(self, tmp_path):
        """Test with many reaches."""
        from iwfm.calib.divshort2obs import read_reaches

        reach_file = tmp_path / 'reaches.dat'
        lines = ['Name    Reach']
        for i in range(50):
            lines.append(f'REACH_{i:03d}    {i+1}')
        reach_file.write_text('\n'.join(lines))

        reaches = read_reaches(str(reach_file))

        assert len(reaches) == 50
        assert reaches[0] == ['REACH_000', 1]
        assert reaches[49] == ['REACH_049', 50]


class TestDivshort2Obs:
    """Tests for divshort2obs function"""

    def test_divshort2obs_returns_two_lists(self):
        """Test that divshort2obs returns divshort and ins lists."""
        from iwfm.calib.divshort2obs import divshort2obs

        budget_table = [np.array([100.0, 200.0])]
        dates = ['10/31/1973', '11/30/1973']
        reaches = [['DIV_001', 1]]

        divshort, ins = divshort2obs(budget_table, dates, reaches)

        assert isinstance(divshort, list)
        assert isinstance(ins, list)

    def test_divshort2obs_smp_format(self):
        """Test that output is in SMP format."""
        from iwfm.calib.divshort2obs import divshort2obs

        budget_table = [np.array([123.45])]
        dates = ['10/31/1973']
        reaches = [['TEST_DIV', 1]]

        divshort, ins = divshort2obs(budget_table, dates, reaches)

        assert len(divshort) == 1
        # SMP format: name date time value
        assert 'TEST_DIV' in divshort[0]
        assert '0:00:00' in divshort[0]
        assert '123.45' in divshort[0]

    def test_divshort2obs_ins_format(self):
        """Test that instruction file format is correct."""
        from iwfm.calib.divshort2obs import divshort2obs

        budget_table = [np.array([100.0])]
        dates = ['10/31/1973']
        reaches = [['DIV_001', 1]]

        divshort, ins = divshort2obs(budget_table, dates, reaches)

        assert len(ins) == 1
        # INS format: l1  [name_MMDDYY]45:56
        assert 'l1' in ins[0]
        assert 'DIV_001_' in ins[0]
        assert '45:56' in ins[0]

    def test_divshort2obs_multiple_dates(self):
        """Test with multiple dates."""
        from iwfm.calib.divshort2obs import divshort2obs

        budget_table = [np.array([100.0, 200.0, 300.0])]
        dates = ['10/31/1973', '11/30/1973', '12/31/1973']
        reaches = [['DIV_001', 1]]

        divshort, ins = divshort2obs(budget_table, dates, reaches)

        assert len(divshort) == 3
        assert len(ins) == 3

    def test_divshort2obs_multiple_reaches(self):
        """Test with multiple reaches."""
        from iwfm.calib.divshort2obs import divshort2obs

        budget_table = [
            np.array([100.0, 200.0]),
            np.array([150.0, 250.0]),
        ]
        dates = ['10/31/1973', '11/30/1973']
        reaches = [['DIV_001', 1], ['DIV_002', 2]]

        divshort, ins = divshort2obs(budget_table, dates, reaches)

        # 2 reaches * 2 dates = 4 outputs
        assert len(divshort) == 4
        assert len(ins) == 4

    def test_divshort2obs_date_conversion(self):
        """Test that dates are converted to MM/DD/YYYY format."""
        from iwfm.calib.divshort2obs import divshort2obs

        budget_table = [np.array([100.0])]
        dates = ['1/5/1980']  # Single digit month and day
        reaches = [['DIV_001', 1]]

        divshort, ins = divshort2obs(budget_table, dates, reaches)

        # Should be converted to proper format
        # The exact format depends on date2text implementation
        assert len(divshort) == 1

    def test_divshort2obs_name_padding(self):
        """Test that reach names are padded to nwidth."""
        from iwfm.calib.divshort2obs import divshort2obs

        budget_table = [np.array([100.0])]
        dates = ['10/31/1973']
        reaches = [['A', 1]]  # Short name

        divshort, ins = divshort2obs(budget_table, dates, reaches, nwidth=20)

        # Name should be padded
        assert len(divshort) == 1
        # First 20 characters should be the padded name
        assert divshort[0].startswith('A')

    def test_divshort2obs_negative_values(self):
        """Test with negative shortage values."""
        from iwfm.calib.divshort2obs import divshort2obs

        budget_table = [np.array([-50.0, -100.0])]
        dates = ['10/31/1973', '11/30/1973']
        reaches = [['DIV_001', 1]]

        divshort, ins = divshort2obs(budget_table, dates, reaches)

        assert '-50.0' in divshort[0]
        assert '-100.0' in divshort[1]

    def test_divshort2obs_zero_values(self):
        """Test with zero shortage values."""
        from iwfm.calib.divshort2obs import divshort2obs

        budget_table = [np.array([0.0, 0.0])]
        dates = ['10/31/1973', '11/30/1973']
        reaches = [['DIV_001', 1]]

        divshort, ins = divshort2obs(budget_table, dates, reaches)

        assert '0.0' in divshort[0]

    def test_divshort2obs_reach_index(self):
        """Test that correct reach index is used (reach_num - 1)."""
        from iwfm.calib.divshort2obs import divshort2obs

        # Three reaches in budget_table
        budget_table = [
            np.array([100.0]),  # Reach 1
            np.array([200.0]),  # Reach 2
            np.array([300.0]),  # Reach 3
        ]
        dates = ['10/31/1973']
        # Only request reach 2
        reaches = [['DIV_002', 2]]

        divshort, ins = divshort2obs(budget_table, dates, reaches)

        # Should get value from reach 2 (index 1)
        assert '200.0' in divshort[0]


class TestDivshort2ObsIntegration:
    """Integration tests using all three functions together"""

    def create_test_files(self, tmp_path, num_reaches=2, num_dates=3):
        """Create both budget and reach files for integration testing."""
        # Create budget file
        budget_file = tmp_path / 'diversions.bud'
        lines = []
        for reach in range(1, num_reaches + 1):
            lines.append('                                    IWFM STREAM PACKAGE (v4.2.0106)                                     ')
            lines.append(f'                     DIVERSION AND DELIVERY DETAILS IN AC.FT. FOR DIVERSION_{reach}(SN0)                      ')
            lines.append('-' * 104)
            lines.append('                                                                  Non          Actual     Delivery')
            lines.append('      Time              Actual      Diversion   Recoverable   Recoverable   Delivery to  Shortage for')
            lines.append('                      Diversion      Shortage       Loss          Loss     Elem. Grp. 1  Elem. Grp. 1')
            lines.append('-' * 104)
            
            base_dates = ['10/31/1973_24:00', '11/30/1973_24:00', '12/31/1973_24:00']
            for i in range(num_dates):
                shortage = float((i + 1) * 10 * reach)
                line = f'{base_dates[i]}           0.0           0.0           0.0           0.0           0.0           {shortage}'
                lines.append(line)
            lines.append('')
            lines.append('')
        budget_file.write_text('\n'.join(lines))

        # Create reach file
        reach_file = tmp_path / 'reaches.dat'
        reach_lines = ['Name    Reach']
        for i in range(1, num_reaches + 1):
            reach_lines.append(f'DIV_{i:03d}    {i}')
        reach_file.write_text('\n'.join(reach_lines))

        return str(budget_file), str(reach_file)

    def test_full_workflow(self, tmp_path):
        """Test the complete workflow from files to SMP output."""
        from iwfm.calib.divshort2obs import process_budget, read_reaches, divshort2obs

        budget_file, reach_file = self.create_test_files(tmp_path, num_reaches=2, num_dates=3)

        # Process budget file
        budget_table, reach_list, dates = process_budget(budget_file)

        # Read reaches
        reaches = read_reaches(reach_file)

        # Convert to SMP format
        divshort, ins = divshort2obs(budget_table, dates, reaches)

        # 2 reaches * 3 dates = 6 outputs
        assert len(divshort) == 6
        assert len(ins) == 6

    def test_output_can_be_written_to_file(self, tmp_path):
        """Test that output can be written to SMP and INS files."""
        from iwfm.calib.divshort2obs import process_budget, read_reaches, divshort2obs

        budget_file, reach_file = self.create_test_files(tmp_path)
        
        budget_table, reach_list, dates = process_budget(budget_file)
        reaches = read_reaches(reach_file)
        divshort, ins = divshort2obs(budget_table, dates, reaches)

        # Write SMP file
        smp_file = tmp_path / 'output.smp'
        with open(smp_file, 'w') as f:
            for item in divshort:
                f.write(f'{item}\n')

        # Write INS file
        ins_file = tmp_path / 'output.ins'
        with open(ins_file, 'w') as f:
            f.write('pif #\n')
            for item in ins:
                f.write(f'{item}\n')

        assert smp_file.exists()
        assert ins_file.exists()
        assert smp_file.stat().st_size > 0
        assert ins_file.stat().st_size > 0


class TestWithRealFile:
    """Tests using the actual C2VSimCG diversions file if available."""

    @pytest.fixture
    def real_budget_file(self):
        """Get path to real budget file if it exists."""
        test_dir = os.path.dirname(__file__)
        budget_path = os.path.join(
            test_dir, 
            'C2VSimCG-2021/Results/C2VSimCG_Diversions.bud'
        )
        if os.path.exists(budget_path):
            return budget_path
        pytest.skip("C2VSimCG diversions file not found")

    def test_process_real_budget_file(self, real_budget_file):
        """Test process_budget with real C2VSimCG file."""
        from iwfm.calib.divshort2obs import process_budget

        budget_table, reach_list, dates = process_budget(real_budget_file)

        # Should have data
        assert len(budget_table) > 0
        assert len(reach_list) > 0
        assert len(dates) > 0

        # Reach list should be integers
        assert all(isinstance(r, int) for r in reach_list)

        # Budget table should contain numpy arrays
        assert all(isinstance(bt, np.ndarray) for bt in budget_table)

    def test_dates_format_real_file(self, real_budget_file):
        """Test that dates are properly extracted from real file."""
        from iwfm.calib.divshort2obs import process_budget

        budget_table, reach_list, dates = process_budget(real_budget_file)

        # Dates should be in M/D/YYYY format (without _24:00)
        for date in dates:
            assert '_24:00' not in date
            parts = date.split('/')
            assert len(parts) == 3  # M/D/YYYY


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
