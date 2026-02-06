# test_calib_smp_avg.py
# Unit tests for calib/smp_avg.py - Average SMP observation values by site
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


class TestSmpAvg:
    """Tests for smp_avg function"""

    def create_smp_file(self, tmp_path, observations):
        """Create a mock SMP file.
        
        Parameters
        ----------
        observations : list of tuples
            Each tuple is (site_name, date_str, time_str, value)
        """
        smp_file = tmp_path / 'test.smp'
        lines = []
        for obs in observations:
            site, date_str, time_str, value = obs
            lines.append(f'{site}  {date_str}  {time_str}  {value}')
        smp_file.write_text('\n'.join(lines))
        return str(smp_file)

    def test_returns_list(self, tmp_path):
        """Test that function returns a list."""
        from iwfm.calib.smp_avg import smp_avg

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '100.0'),
        ])

        result = smp_avg(smp_file)

        assert isinstance(result, list)

    def test_calculates_average_single_site(self, tmp_path):
        """Test that average is calculated for single site."""
        from iwfm.calib.smp_avg import smp_avg

        # Three observations: 100, 110, 120 -> average = 110
        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '100.0'),
            ('WELL001', '01/16/2020', '0:00:00', '110.0'),
            ('WELL001', '01/17/2020', '0:00:00', '120.0'),
        ])

        result = smp_avg(smp_file)

        # All three lines should have the same average value
        assert len(result) == 3
        for line in result:
            assert '110.0' in line

    def test_calculates_average_multiple_sites(self, tmp_path):
        """Test that average is calculated for multiple sites."""
        from iwfm.calib.smp_avg import smp_avg

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '100.0'),
            ('WELL001', '01/16/2020', '0:00:00', '200.0'),  # avg = 150
            ('WELL002', '01/15/2020', '0:00:00', '50.0'),
            ('WELL002', '01/16/2020', '0:00:00', '60.0'),   # avg = 55
        ])

        result = smp_avg(smp_file)

        assert len(result) == 4

    def test_preserves_line_count(self, tmp_path):
        """Test that output has same number of lines as input."""
        from iwfm.calib.smp_avg import smp_avg

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '100.0'),
            ('WELL001', '01/16/2020', '0:00:00', '110.0'),
            ('WELL002', '01/15/2020', '0:00:00', '200.0'),
        ])

        result = smp_avg(smp_file)

        assert len(result) == 3

    def test_single_observation(self, tmp_path):
        """Test with single observation (average = value)."""
        from iwfm.calib.smp_avg import smp_avg

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '123.456'),
        ])

        result = smp_avg(smp_file)

        assert len(result) == 1
        assert '123.456' in result[0]

    def test_preserves_site_name(self, tmp_path):
        """Test that site name is preserved in output."""
        from iwfm.calib.smp_avg import smp_avg

        smp_file = self.create_smp_file(tmp_path, [
            ('MY_WELL_001', '01/15/2020', '0:00:00', '100.0'),
        ])

        result = smp_avg(smp_file)

        assert 'MY_WELL_001' in result[0]

    def test_preserves_date(self, tmp_path):
        """Test that date is preserved in output."""
        from iwfm.calib.smp_avg import smp_avg

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '12/25/2020', '0:00:00', '100.0'),
        ])

        result = smp_avg(smp_file)

        assert '12/25/2020' in result[0]


class TestNameIndex:
    """Tests for name_index helper function"""

    def test_finds_matching_name(self):
        """Test that function finds matching name."""
        from iwfm.calib.smp_avg import name_index

        names_list = [['WELL001', 'data'], ['WELL002', 'data'], ['WELL003', 'data']]
        
        result = name_index(names_list, 'WELL002')

        assert 1 in result

    def test_returns_empty_for_no_match(self):
        """Test that function returns empty list for no match."""
        from iwfm.calib.smp_avg import name_index

        names_list = [['WELL001', 'data'], ['WELL002', 'data']]
        
        result = name_index(names_list, 'WELL999')

        assert result == []

    def test_finds_multiple_matches(self):
        """Test that function finds multiple matches."""
        from iwfm.calib.smp_avg import name_index

        names_list = [['WELL001', 'data'], ['WELL001', 'data2'], ['WELL002', 'data']]
        
        result = name_index(names_list, 'WELL001')

        assert len(result) == 2
        assert 0 in result
        assert 1 in result


class TestSmpAvgImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import smp_avg
        assert callable(smp_avg)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.smp_avg import smp_avg
        assert callable(smp_avg)

    def test_import_name_index(self):
        """Test import of helper function."""
        from iwfm.calib.smp_avg import name_index
        assert callable(name_index)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.smp_avg import smp_avg
        
        assert smp_avg.__doc__ is not None
        assert 'average' in smp_avg.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
