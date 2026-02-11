# test_calib_sim_smp.py
# Unit tests for calib/sim_smp.py - Process SMP file lines into observation data
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
from datetime import date


class TestSimSmp:
    """Tests for sim_smp function"""

    def test_returns_two_lists(self):
        """Test that function returns sim_data and sim_sites."""
        from iwfm.calib.sim_smp import sim_smp

        smp_list = [
            'WELL001  01/15/2020  0:00:00  100.0',
        ]

        result = sim_smp(smp_list)

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_parses_site_name(self):
        """Test that site name is parsed correctly."""
        from iwfm.calib.sim_smp import sim_smp

        smp_list = [
            'MY_WELL_001  01/15/2020  0:00:00  100.0',
        ]

        sim_data, sim_sites = sim_smp(smp_list)

        assert sim_data[0][0] == 'MY_WELL_001'
        assert 'MY_WELL_001' in sim_sites

    def test_parses_date(self):
        """Test that date is parsed to date object."""
        from iwfm.calib.sim_smp import sim_smp

        smp_list = [
            'WELL001  12/25/2020  0:00:00  100.0',
        ]

        sim_data, sim_sites = sim_smp(smp_list)

        assert isinstance(sim_data[0][1], date)
        assert sim_data[0][1].year == 2020
        assert sim_data[0][1].month == 12
        assert sim_data[0][1].day == 25

    def test_parses_value(self):
        """Test that value is parsed."""
        from iwfm.calib.sim_smp import sim_smp

        smp_list = [
            'WELL001  01/15/2020  0:00:00  123.456',
        ]

        sim_data, sim_sites = sim_smp(smp_list)

        assert sim_data[0][2] == '123.456'

    def test_multiple_observations(self):
        """Test with multiple observations."""
        from iwfm.calib.sim_smp import sim_smp

        smp_list = [
            'WELL001  01/15/2020  0:00:00  100.0',
            'WELL002  01/16/2020  0:00:00  200.0',
            'WELL003  01/17/2020  0:00:00  300.0',
        ]

        sim_data, sim_sites = sim_smp(smp_list)

        assert len(sim_data) == 3
        assert len(sim_sites) == 3

    def test_unique_sites(self):
        """Test that sim_sites contains unique site names."""
        from iwfm.calib.sim_smp import sim_smp

        smp_list = [
            'WELL001  01/15/2020  0:00:00  100.0',
            'WELL001  01/16/2020  0:00:00  110.0',
            'WELL001  01/17/2020  0:00:00  120.0',
        ]

        sim_data, sim_sites = sim_smp(smp_list)

        assert len(sim_data) == 3
        assert len(sim_sites) == 1  # Only one unique site

    def test_sorts_data(self):
        """Test that data is sorted by site then date."""
        from iwfm.calib.sim_smp import sim_smp

        smp_list = [
            'WELL002  01/15/2020  0:00:00  200.0',
            'WELL001  01/16/2020  0:00:00  110.0',
            'WELL001  01/15/2020  0:00:00  100.0',
        ]

        sim_data, sim_sites = sim_smp(smp_list)

        # Should be sorted by site, then date
        assert sim_data[0][0] == 'WELL001'
        assert sim_data[1][0] == 'WELL001'
        assert sim_data[2][0] == 'WELL002'

    def test_sorts_sites(self):
        """Test that sim_sites list is sorted."""
        from iwfm.calib.sim_smp import sim_smp

        smp_list = [
            'ZEBRA  01/15/2020  0:00:00  100.0',
            'ALPHA  01/15/2020  0:00:00  200.0',
            'MIKE  01/15/2020  0:00:00  300.0',
        ]

        sim_data, sim_sites = sim_smp(smp_list)

        assert sim_sites == sorted(sim_sites)

    def test_skips_short_lines(self):
        """Test that lines with single-char site names are skipped.

        sim_smp skips lines where len(item[0]) <= 1.
        """
        from iwfm.calib.sim_smp import sim_smp

        smp_list = [
            'WELL001  01/15/2020  0:00:00  100.0',
            'X  01/16/2020  0:00:00  200.0',  # Single char - skipped by len > 1 check
        ]

        sim_data, sim_sites = sim_smp(smp_list)

        # Only WELL001 should be processed; 'X' is skipped (len <= 1)
        assert len(sim_data) == 1


class TestSimSmpImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import sim_smp
        assert callable(sim_smp)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.sim_smp import sim_smp
        assert callable(sim_smp)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.sim_smp import sim_smp
        
        assert sim_smp.__doc__ is not None
        assert 'smp' in sim_smp.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
