# test_calib_obs_smp.py
# Unit tests for calib/obs_smp.py - Return observation bore sample info
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


class TestObsSmp:
    """Tests for obs_smp function"""

    def test_returns_three_items(self):
        """Test that function returns obs_data, obs_sites, missing."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = ['SITE_001  01/15/2020  0:00:00  100.0']
        sim_sites = ['SITE_001']

        result = obs_smp(obs_lines, sim_sites)

        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_obs_data_structure(self):
        """Test that obs_data contains [site, date, date_string]."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = ['SITE_001  01/15/2020  0:00:00  100.0']
        sim_sites = ['SITE_001']

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert len(obs_data) == 1
        assert obs_data[0][0] == 'SITE_001'  # site name
        assert isinstance(obs_data[0][1], date)  # date object
        assert obs_data[0][2] == '01/15/2020'  # date string

    def test_filters_by_sim_sites(self):
        """Test that only observations for sites in sim_sites are returned."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'SITE_001  01/15/2020  0:00:00  100.0',
            'SITE_002  01/16/2020  0:00:00  200.0',
            'SITE_003  01/17/2020  0:00:00  300.0',
        ]
        sim_sites = ['SITE_001', 'SITE_003']  # SITE_002 not in sim

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        # Should only have SITE_001 and SITE_003
        sites_in_data = [d[0] for d in obs_data]
        assert 'SITE_001' in sites_in_data
        assert 'SITE_003' in sites_in_data
        assert 'SITE_002' not in sites_in_data

    def test_obs_sites_unique(self):
        """Test that obs_sites contains unique site names."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'SITE_001  01/15/2020  0:00:00  100.0',
            'SITE_001  01/16/2020  0:00:00  110.0',  # Same site
            'SITE_001  01/17/2020  0:00:00  120.0',  # Same site
        ]
        sim_sites = ['SITE_001']

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert len(obs_sites) == 1
        assert obs_sites[0] == 'SITE_001'

    def test_missing_contains_unmatched_sites(self):
        """Test that missing contains observation sites not in sim_sites."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'SITE_001  01/15/2020  0:00:00  100.0',
            'SITE_002  01/16/2020  0:00:00  200.0',
            'SITE_003  01/17/2020  0:00:00  300.0',
        ]
        sim_sites = ['SITE_001']  # Only SITE_001 in sim

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert 'SITE_002' in missing
        assert 'SITE_003' in missing
        assert 'SITE_001' not in missing

    def test_missing_unique(self):
        """Test that missing contains unique site names."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'SITE_002  01/15/2020  0:00:00  100.0',
            'SITE_002  01/16/2020  0:00:00  110.0',  # Same site
            'SITE_002  01/17/2020  0:00:00  120.0',  # Same site
        ]
        sim_sites = ['SITE_001']  # SITE_002 not in sim

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert missing.count('SITE_002') == 1

    def test_obs_data_sorted_by_site_and_date(self):
        """Test that obs_data is sorted by site then date."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'SITE_B  01/20/2020  0:00:00  200.0',
            'SITE_A  01/15/2020  0:00:00  100.0',
            'SITE_A  01/10/2020  0:00:00  50.0',
        ]
        sim_sites = ['SITE_A', 'SITE_B']

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        # Should be sorted: SITE_A first (by date), then SITE_B
        assert obs_data[0][0] == 'SITE_A'
        assert obs_data[1][0] == 'SITE_A'
        assert obs_data[2][0] == 'SITE_B'
        # SITE_A dates should be in order
        assert obs_data[0][1] < obs_data[1][1]

    def test_obs_sites_sorted(self):
        """Test that obs_sites list is sorted."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'ZEBRA  01/15/2020  0:00:00  100.0',
            'ALPHA  01/16/2020  0:00:00  200.0',
            'MIKE  01/17/2020  0:00:00  300.0',
        ]
        sim_sites = ['ZEBRA', 'ALPHA', 'MIKE']

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert obs_sites == sorted(obs_sites)

    def test_date_parsing(self):
        """Test that dates are parsed correctly."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = ['SITE_001  12/25/2020  0:00:00  100.0']
        sim_sites = ['SITE_001']

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert obs_data[0][1].year == 2020
        assert obs_data[0][1].month == 12
        assert obs_data[0][1].day == 25

    def test_empty_obs_lines(self):
        """Test with empty observation lines."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = []
        sim_sites = ['SITE_001']

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert obs_data == []
        assert obs_sites == []
        assert missing == []

    def test_empty_sim_sites(self):
        """Test with empty simulation sites."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'SITE_001  01/15/2020  0:00:00  100.0',
            'SITE_002  01/16/2020  0:00:00  200.0',
        ]
        sim_sites = []

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert obs_data == []
        assert obs_sites == []
        assert 'SITE_001' in missing
        assert 'SITE_002' in missing

    def test_all_sites_match(self):
        """Test when all observation sites are in sim_sites."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'SITE_001  01/15/2020  0:00:00  100.0',
            'SITE_002  01/16/2020  0:00:00  200.0',
        ]
        sim_sites = ['SITE_001', 'SITE_002', 'SITE_003']

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert len(obs_data) == 2
        assert len(obs_sites) == 2
        assert missing == []

    def test_no_sites_match(self):
        """Test when no observation sites are in sim_sites."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'SITE_001  01/15/2020  0:00:00  100.0',
            'SITE_002  01/16/2020  0:00:00  200.0',
        ]
        sim_sites = ['SITE_X', 'SITE_Y', 'SITE_Z']

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert obs_data == []
        assert obs_sites == []
        assert 'SITE_001' in missing
        assert 'SITE_002' in missing

    def test_multiple_observations_per_site(self):
        """Test with multiple observations per site."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            'SITE_001  01/15/2020  0:00:00  100.0',
            'SITE_001  02/15/2020  0:00:00  110.0',
            'SITE_001  03/15/2020  0:00:00  120.0',
            'SITE_002  01/15/2020  0:00:00  200.0',
        ]
        sim_sites = ['SITE_001', 'SITE_002']

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        # Should have 4 observations
        assert len(obs_data) == 4
        # But only 2 unique sites
        assert len(obs_sites) == 2

    def test_many_observations(self):
        """Test with many observations."""
        from iwfm.calib.obs_smp import obs_smp

        obs_lines = [
            f'SITE_{i % 10:03d}  01/{(i % 28) + 1:02d}/2020  0:00:00  {100.0 + i}'
            for i in range(100)
        ]
        sim_sites = [f'SITE_{i:03d}' for i in range(10)]

        obs_data, obs_sites, missing = obs_smp(obs_lines, sim_sites)

        assert len(obs_data) == 100
        assert len(obs_sites) == 10

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.obs_smp import obs_smp
        import inspect
        
        sig = inspect.signature(obs_smp)
        params = list(sig.parameters.keys())
        
        assert 'obs_lines' in params
        assert 'sim_sites' in params


class TestObsSmpImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import obs_smp
        assert callable(obs_smp)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.obs_smp import obs_smp
        assert callable(obs_smp)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.obs_smp import obs_smp
        
        assert obs_smp.__doc__ is not None
        assert 'obs_data' in obs_smp.__doc__
        assert 'obs_sites' in obs_smp.__doc__
        assert 'missing' in obs_smp.__doc__


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
