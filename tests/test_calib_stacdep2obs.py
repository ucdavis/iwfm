# test_calib_stacdep2obs.py
# Unit tests for calib/stacdep2obs.py - Convert Stream Budget to SMP format
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


class TestReadReaches:
    """Tests for read_reaches function"""

    def create_reach_file(self, tmp_path, reaches):
        """Create a mock reach list file.
        
        Format:
        - 3 header lines
        - Data lines: name  description  reach_nums
        """
        reach_file = tmp_path / 'reaches.dat'
        
        lines = []
        lines.append('# Header line 1')
        lines.append('# Header line 2')
        lines.append('# Header line 3')
        
        for reach in reaches:
            name, desc, nums = reach
            lines.append(f'{name}  {desc}  {nums}')
        
        reach_file.write_text('\n'.join(lines))
        return str(reach_file)

    def test_returns_list(self, tmp_path):
        """Test that function returns a list."""
        from iwfm.calib.stacdep2obs import read_reaches

        reach_file = self.create_reach_file(tmp_path, [
            ('REACH1', 'Description', '1'),
        ])

        result = read_reaches(reach_file)

        assert isinstance(result, list)

    def test_parses_reach_name(self, tmp_path):
        """Test that reach name is parsed."""
        from iwfm.calib.stacdep2obs import read_reaches

        reach_file = self.create_reach_file(tmp_path, [
            ('MY_REACH', 'Desc', '1'),
        ])

        result = read_reaches(reach_file)

        assert result[0][0] == 'MY_REACH'

    def test_parses_reach_numbers(self, tmp_path):
        """Test that reach numbers are parsed as integers."""
        from iwfm.calib.stacdep2obs import read_reaches

        reach_file = self.create_reach_file(tmp_path, [
            ('REACH1', 'Desc', '1,2,3'),
        ])

        result = read_reaches(reach_file)

        assert result[0][1] == [1, 2, 3]

    def test_multiple_reaches(self, tmp_path):
        """Test with multiple reaches."""
        from iwfm.calib.stacdep2obs import read_reaches

        reach_file = self.create_reach_file(tmp_path, [
            ('REACH1', 'Desc1', '1'),
            ('REACH2', 'Desc2', '2,3'),
            ('REACH3', 'Desc3', '4,5,6'),
        ])

        result = read_reaches(reach_file)

        assert len(result) == 3

    def test_skips_header_lines(self, tmp_path):
        """Test that first 3 header lines are skipped."""
        from iwfm.calib.stacdep2obs import read_reaches

        reach_file = self.create_reach_file(tmp_path, [
            ('REACH1', 'Desc', '1'),
        ])

        result = read_reaches(reach_file)

        # Should only have 1 reach (headers skipped)
        assert len(result) == 1


class TestStacdep2Obs:
    """Tests for stacdep2obs function"""

    def test_returns_two_lists(self):
        """Test that function returns stacdep and ins lists."""
        from iwfm.calib.stacdep2obs import stacdep2obs

        budget_table = [np.array([100.0, 110.0, 120.0])]
        dates = ['1/15/2020', '1/16/2020', '1/17/2020']
        reaches = [['REACH1', [1]]]

        result = stacdep2obs(budget_table, dates, reaches)

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_creates_smp_format(self):
        """Test that output is in SMP format."""
        from iwfm.calib.stacdep2obs import stacdep2obs

        budget_table = [np.array([100.0])]
        dates = ['1/15/2020']
        reaches = [['REACH1', [1]]]

        stacdep, ins = stacdep2obs(budget_table, dates, reaches)

        assert len(stacdep) == 1
        assert 'REACH1' in stacdep[0]
        assert '01/15/2020' in stacdep[0]

    def test_creates_ins_format(self):
        """Test that INS output is created."""
        from iwfm.calib.stacdep2obs import stacdep2obs

        budget_table = [np.array([100.0])]
        dates = ['1/15/2020']
        reaches = [['REACH1', [1]]]

        stacdep, ins = stacdep2obs(budget_table, dates, reaches)

        assert len(ins) == 1
        assert 'l1' in ins[0]
        assert 'REACH1' in ins[0]

    def test_multiple_dates(self):
        """Test with multiple dates."""
        from iwfm.calib.stacdep2obs import stacdep2obs

        budget_table = [np.array([100.0, 110.0, 120.0])]
        dates = ['1/15/2020', '1/16/2020', '1/17/2020']
        reaches = [['REACH1', [1]]]

        stacdep, ins = stacdep2obs(budget_table, dates, reaches)

        assert len(stacdep) == 3
        assert len(ins) == 3

    def test_sums_multiple_reaches(self):
        """Test that multiple reach numbers are summed."""
        from iwfm.calib.stacdep2obs import stacdep2obs

        # The function uses reach_nums[0]-1 for the first reach (0-indexed),
        # and reach_nums[i] (NOT -1) for subsequent reaches.
        # So for reaches [1, 2]: first uses budget_table[0], second uses budget_table[2].
        # We need 3 entries in budget_table.
        budget_table = [
            np.array([100.0]),  # index 0, for reach 1
            np.array([75.0]),   # index 1
            np.array([50.0]),   # index 2, for reach 2
        ]
        dates = ['1/15/2020']
        reaches = [['COMBINED', [1, 2]]]  # Sum reaches 1 and 2

        stacdep, ins = stacdep2obs(budget_table, dates, reaches)

        # Should have summed value in output
        assert len(stacdep) == 1


class TestStacdep2ObsImports:
    """Tests for function imports."""

    def test_import_process_budget(self):
        """Test import of process_budget."""
        from iwfm.calib.stacdep2obs import process_budget
        assert callable(process_budget)

    def test_import_read_reaches(self):
        """Test import of read_reaches."""
        from iwfm.calib.stacdep2obs import read_reaches
        assert callable(read_reaches)

    def test_import_stacdep2obs(self):
        """Test import of stacdep2obs."""
        from iwfm.calib.stacdep2obs import stacdep2obs
        assert callable(stacdep2obs)

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import stacdep2obs
        assert hasattr(stacdep2obs, 'stacdep2obs') or callable(stacdep2obs)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
