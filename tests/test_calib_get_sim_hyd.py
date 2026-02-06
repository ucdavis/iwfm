# test_calib_get_sim_hyd.py
# Unit tests for calib/get_sim_hyd.py - Get simulated hydrograph values
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
from datetime import datetime


class TestGetSimHyd:
    """Tests for get_sim_hyd function"""

    def create_sim_hyd_file(self, tmp_path, dates_values):
        """Create a mock simulation hydrograph file.
        
        Parameters
        ----------
        dates_values : list of tuples
            Each tuple is (date_string, value1, value2, ...)
        """
        hyd_file = tmp_path / 'sim_hyd.out'
        lines = []
        # Header line (will be skipped)
        lines.append('# Simulation hydrograph output')
        # Data lines: date followed by values
        for row in dates_values:
            lines.append('  '.join(str(x) for x in row))
        hyd_file.write_text('\n'.join(lines))
        return str(hyd_file)

    def test_returns_two_items(self, tmp_path):
        """Test that function returns sim_hyd and dates."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('01/15/2020', 100.0, 200.0),
        ])
        start_date = datetime(2020, 1, 1)

        result = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_sim_hyd_is_list_of_arrays(self, tmp_path):
        """Test that sim_hyd is a list of numpy arrays."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('01/15/2020', 100.0, 200.0),
            ('01/16/2020', 110.0, 210.0),
        ])
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert isinstance(sim_hyd, list)
        assert len(sim_hyd) == 2
        assert isinstance(sim_hyd[0], np.ndarray)
        assert isinstance(sim_hyd[1], np.ndarray)

    def test_dates_is_list_of_days(self, tmp_path):
        """Test that dates is a list of days since start."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('01/11/2020', 100.0),  # 10 days after start
            ('01/21/2020', 110.0),  # 20 days after start
        ])
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert isinstance(dates, list)
        assert len(dates) == 2
        assert dates[0] == 10
        assert dates[1] == 20

    def test_values_extracted_correctly(self, tmp_path):
        """Test that simulation values are extracted correctly."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('01/15/2020', 100.5, 200.5, 300.5),
        ])
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert len(sim_hyd[0]) == 3
        assert sim_hyd[0][0] == 100.5
        assert sim_hyd[0][1] == 200.5
        assert sim_hyd[0][2] == 300.5

    def test_multiple_timesteps(self, tmp_path):
        """Test with multiple time steps."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('01/01/2020', 100.0, 200.0),
            ('02/01/2020', 110.0, 210.0),
            ('03/01/2020', 120.0, 220.0),
            ('04/01/2020', 130.0, 230.0),
        ])
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert len(sim_hyd) == 4
        assert len(dates) == 4

    def test_many_columns(self, tmp_path):
        """Test with many value columns (many sites)."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        # 20 sites
        values = [float(i) for i in range(1, 21)]
        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('01/15/2020', *values),
        ])
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert len(sim_hyd[0]) == 20

    def test_skips_header_lines(self, tmp_path):
        """Test that non-date header lines are skipped."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = tmp_path / 'sim_hyd.out'
        lines = [
            '# Header comment 1',
            '# Header comment 2',
            'SITE_A    SITE_B    SITE_C',
            '01/15/2020  100.0  200.0  300.0',
            '01/16/2020  110.0  210.0  310.0',
        ]
        hyd_file.write_text('\n'.join(lines))
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', str(hyd_file), start_date)

        # Should only get the 2 data lines
        assert len(sim_hyd) == 2
        assert len(dates) == 2

    def test_single_timestep(self, tmp_path):
        """Test with single time step."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('06/15/2020', 999.9),
        ])
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert len(sim_hyd) == 1
        assert len(dates) == 1
        assert sim_hyd[0][0] == 999.9

    def test_negative_values(self, tmp_path):
        """Test with negative simulation values."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('01/15/2020', -50.5, -100.25),
        ])
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert sim_hyd[0][0] == -50.5
        assert sim_hyd[0][1] == -100.25

    def test_zero_values(self, tmp_path):
        """Test with zero values."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('01/15/2020', 0.0, 0.0, 0.0),
        ])
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert all(v == 0.0 for v in sim_hyd[0])

    def test_large_values(self, tmp_path):
        """Test with large values."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('01/15/2020', 1e10, 1e-10),
        ])
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        assert sim_hyd[0][0] == 1e10
        assert sim_hyd[0][1] == 1e-10

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd
        import inspect
        
        sig = inspect.signature(get_sim_hyd)
        params = list(sig.parameters.keys())
        
        assert 'nt' in params
        assert 'file_name' in params
        assert 'start_date' in params


class TestGetSimHydDateHandling:
    """Tests for date handling in get_sim_hyd."""

    def create_sim_hyd_file(self, tmp_path, dates_values):
        """Create simulation hydrograph file."""
        hyd_file = tmp_path / 'sim_hyd.out'
        lines = ['# Header']
        for row in dates_values:
            lines.append('  '.join(str(x) for x in row))
        hyd_file.write_text('\n'.join(lines))
        return str(hyd_file)

    def test_date_truncation(self, tmp_path):
        """Test that date string is truncated to first 10 characters."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        # Date with time component that should be truncated
        hyd_file = tmp_path / 'sim_hyd.out'
        lines = [
            '# Header',
            '01/15/2020_24:00  100.0',  # Has _24:00 suffix
        ]
        hyd_file.write_text('\n'.join(lines))
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', str(hyd_file), start_date)

        # Should successfully parse date
        assert len(dates) == 1
        assert dates[0] == 14  # January 15 is 14 days after January 1

    def test_days_from_different_start_date(self, tmp_path):
        """Test days calculation with different start date."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd

        hyd_file = self.create_sim_hyd_file(tmp_path, [
            ('03/01/2020', 100.0),
        ])
        # Start from beginning of year
        start_date = datetime(2020, 1, 1)

        sim_hyd, dates = get_sim_hyd('Groundwater', hyd_file, start_date)

        # March 1, 2020 is day 60 (2020 is leap year: 31 Jan + 29 Feb = 60)
        assert dates[0] == 60


class TestGetSimHydImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import get_sim_hyd
        assert callable(get_sim_hyd)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd
        assert callable(get_sim_hyd)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.get_sim_hyd import get_sim_hyd
        
        assert get_sim_hyd.__doc__ is not None
        assert 'sim_hyd' in get_sim_hyd.__doc__
        assert 'dates' in get_sim_hyd.__doc__


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
