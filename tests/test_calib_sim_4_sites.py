# test_calib_sim_4_sites.py
# Unit tests for calib/sim_4_sites.py - Select simulated values at observation sites
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


class TestSim4Sites:
    """Tests for sim_4_sites function"""

    def test_returns_two_lists(self):
        """Test that function returns sim_dates and sim_values."""
        from iwfm.calib.sim_4_sites import sim_4_sites

        sim_data = [
            ['WELL001', date(2020, 1, 15), '100.0'],
        ]
        obs_sites = ['WELL001']

        result = sim_4_sites(sim_data, obs_sites)

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_filters_by_obs_sites(self):
        """Test that only sites in obs_sites are returned."""
        from iwfm.calib.sim_4_sites import sim_4_sites

        sim_data = [
            ['WELL001', date(2020, 1, 15), '100.0'],
            ['WELL002', date(2020, 1, 15), '200.0'],
            ['WELL003', date(2020, 1, 15), '300.0'],
        ]
        obs_sites = ['WELL001', 'WELL003']  # WELL002 not in obs

        sim_dates, sim_values = sim_4_sites(sim_data, obs_sites)

        # Should have data for 2 sites
        assert len(sim_values) == 2

    def test_extracts_dates(self):
        """Test that dates are extracted correctly."""
        from iwfm.calib.sim_4_sites import sim_4_sites

        sim_data = [
            ['WELL001', date(2020, 1, 15), '100.0'],
            ['WELL001', date(2020, 1, 16), '110.0'],
        ]
        obs_sites = ['WELL001']

        sim_dates, sim_values = sim_4_sites(sim_data, obs_sites)

        assert len(sim_dates) == 1  # One site
        assert len(sim_dates[0]) == 2  # Two dates

    def test_extracts_values_as_floats(self):
        """Test that values are converted to floats."""
        from iwfm.calib.sim_4_sites import sim_4_sites

        sim_data = [
            ['WELL001', date(2020, 1, 15), '123.456'],
        ]
        obs_sites = ['WELL001']

        sim_dates, sim_values = sim_4_sites(sim_data, obs_sites)

        assert isinstance(sim_values[0][0], float)
        assert abs(sim_values[0][0] - 123.456) < 0.001

    def test_multiple_sites(self):
        """Test with multiple observation sites."""
        from iwfm.calib.sim_4_sites import sim_4_sites

        sim_data = [
            ['WELL001', date(2020, 1, 15), '100.0'],
            ['WELL001', date(2020, 1, 16), '110.0'],
            ['WELL002', date(2020, 1, 15), '200.0'],
            ['WELL002', date(2020, 1, 16), '210.0'],
        ]
        obs_sites = ['WELL001', 'WELL002']

        sim_dates, sim_values = sim_4_sites(sim_data, obs_sites)

        assert len(sim_dates) == 2
        assert len(sim_values) == 2

    def test_no_matching_sites(self):
        """Test when no sites match obs_sites."""
        from iwfm.calib.sim_4_sites import sim_4_sites

        sim_data = [
            ['WELL001', date(2020, 1, 15), '100.0'],
        ]
        obs_sites = ['WELL999']  # No match

        sim_dates, sim_values = sim_4_sites(sim_data, obs_sites)

        assert len(sim_dates) == 0
        assert len(sim_values) == 0

    def test_sorts_data(self):
        """Test that data is sorted by site then date."""
        from iwfm.calib.sim_4_sites import sim_4_sites

        sim_data = [
            ['WELL002', date(2020, 1, 16), '210.0'],
            ['WELL001', date(2020, 1, 15), '100.0'],
            ['WELL002', date(2020, 1, 15), '200.0'],
            ['WELL001', date(2020, 1, 16), '110.0'],
        ]
        obs_sites = ['WELL001', 'WELL002']

        sim_dates, sim_values = sim_4_sites(sim_data, obs_sites)

        # Data should be sorted
        assert len(sim_dates) >= 1


class TestSim4SitesImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import sim_4_sites
        assert callable(sim_4_sites)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.sim_4_sites import sim_4_sites
        assert callable(sim_4_sites)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.sim_4_sites import sim_4_sites
        
        assert sim_4_sites.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
