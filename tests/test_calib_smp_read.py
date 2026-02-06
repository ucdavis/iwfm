# test_calib_smp_read.py
# Unit tests for calib/smp_read.py - Read PEST SMP file
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


class TestSmpRead:
    """Tests for smp_read function"""

    def create_smp_file(self, tmp_path, observations):
        """Create a mock SMP file.
        
        SMP format: site_name  date  time  value
        
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
        from iwfm.calib.smp_read import smp_read

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '100.5'),
        ])

        result = smp_read(smp_file)

        assert isinstance(result, list)

    def test_returns_list_of_lists(self, tmp_path):
        """Test that function returns list of lists."""
        from iwfm.calib.smp_read import smp_read

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '100.5'),
        ])

        result = smp_read(smp_file)

        assert len(result) == 1
        assert isinstance(result[0], list)

    def test_parses_site_name(self, tmp_path):
        """Test that site name is parsed correctly."""
        from iwfm.calib.smp_read import smp_read

        smp_file = self.create_smp_file(tmp_path, [
            ('MY_WELL_001', '01/15/2020', '0:00:00', '100.5'),
        ])

        result = smp_read(smp_file)

        assert result[0][0] == 'MY_WELL_001'

    def test_parses_date_to_datetime(self, tmp_path):
        """Test that date is parsed to datetime object."""
        from iwfm.calib.smp_read import smp_read

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '100.5'),
        ])

        result = smp_read(smp_file)

        assert isinstance(result[0][1], datetime)
        assert result[0][1].year == 2020
        assert result[0][1].month == 1
        assert result[0][1].day == 15

    def test_parses_value_to_float(self, tmp_path):
        """Test that value is parsed to float."""
        from iwfm.calib.smp_read import smp_read

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '123.456'),
        ])

        result = smp_read(smp_file)

        assert isinstance(result[0][3], float)
        assert abs(result[0][3] - 123.456) < 0.001

    def test_multiple_observations(self, tmp_path):
        """Test with multiple observations."""
        from iwfm.calib.smp_read import smp_read

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '100.0'),
            ('WELL002', '01/16/2020', '0:00:00', '200.0'),
            ('WELL003', '01/17/2020', '0:00:00', '300.0'),
        ])

        result = smp_read(smp_file)

        assert len(result) == 3

    def test_negative_values(self, tmp_path):
        """Test with negative values."""
        from iwfm.calib.smp_read import smp_read

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '0:00:00', '-50.25'),
        ])

        result = smp_read(smp_file)

        assert result[0][3] < 0
        assert abs(result[0][3] - (-50.25)) < 0.001

    def test_preserves_time_string(self, tmp_path):
        """Test that time string is preserved."""
        from iwfm.calib.smp_read import smp_read

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '01/15/2020', '12:30:45', '100.0'),
        ])

        result = smp_read(smp_file)

        assert result[0][2] == '12:30:45'


class TestSmpReadImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import smp_read
        assert callable(smp_read)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.smp_read import smp_read
        assert callable(smp_read)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.smp_read import smp_read
        
        assert smp_read.__doc__ is not None
        assert 'smp' in smp_read.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
