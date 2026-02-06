# test_calib_get_obs_hyd.py
# Unit tests for calib/get_obs_hyd.py - Read observation SMP file
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


class TestGetObsHyd:
    """Tests for get_obs_hyd function"""

    def create_obs_file(self, tmp_path, observations):
        """Create a mock observation SMP file.
        
        Parameters
        ----------
        observations : list of tuples
            Each tuple is (site_name, date_string, optional_extra...)
        """
        obs_file = tmp_path / 'observations.smp'
        lines = []
        for obs in observations:
            lines.append('  '.join(str(x) for x in obs))
        obs_file.write_text('\n'.join(lines))
        return str(obs_file)

    def test_returns_two_items(self, tmp_path):
        """Test that function returns obs_sites and obs_data."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        obs_file = self.create_obs_file(tmp_path, [
            ('SITE_001', '01/15/2020'),
        ])
        start_date = datetime(2020, 1, 1)

        result = get_obs_hyd(obs_file, start_date)

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_obs_sites_is_list(self, tmp_path):
        """Test that obs_sites is a list of site names."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        obs_file = self.create_obs_file(tmp_path, [
            ('SITE_A', '01/15/2020'),
            ('SITE_B', '01/20/2020'),
        ])
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        assert isinstance(obs_sites, list)
        assert 'SITE_A' in obs_sites
        assert 'SITE_B' in obs_sites

    def test_obs_data_structure(self, tmp_path):
        """Test that obs_data contains [site, days, datetime]."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        obs_file = self.create_obs_file(tmp_path, [
            ('SITE_001', '01/15/2020'),
        ])
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        assert len(obs_data) == 1
        assert len(obs_data[0]) == 3
        assert obs_data[0][0] == 'SITE_001'  # site name
        assert isinstance(obs_data[0][1], (int, float))  # days since start
        assert isinstance(obs_data[0][2], datetime)  # datetime object

    def test_days_since_start_calculation(self, tmp_path):
        """Test that days since start_date is calculated correctly."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        obs_file = self.create_obs_file(tmp_path, [
            ('SITE_001', '01/11/2020'),  # 10 days after start
        ])
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        # January 11 is 10 days after January 1
        assert obs_data[0][1] == 10

    def test_unique_sites(self, tmp_path):
        """Test that obs_sites contains unique site names."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        obs_file = self.create_obs_file(tmp_path, [
            ('SITE_A', '01/15/2020'),
            ('SITE_A', '01/20/2020'),  # Same site, different date
            ('SITE_B', '01/25/2020'),
        ])
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        assert len(obs_sites) == 2  # Only unique sites
        assert obs_sites.count('SITE_A') == 1

    def test_all_observations_in_data(self, tmp_path):
        """Test that all observations are included in obs_data."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        obs_file = self.create_obs_file(tmp_path, [
            ('SITE_A', '01/15/2020'),
            ('SITE_A', '01/20/2020'),
            ('SITE_B', '01/25/2020'),
        ])
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        assert len(obs_data) == 3  # All observations

    def test_data_sorted_by_site_and_days(self, tmp_path):
        """Test that obs_data is sorted by site name then days."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        # Create observations in random order
        obs_file = self.create_obs_file(tmp_path, [
            ('SITE_B', '01/25/2020'),
            ('SITE_A', '01/20/2020'),
            ('SITE_A', '01/15/2020'),
        ])
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        # Should be sorted: SITE_A first (by date), then SITE_B
        assert obs_data[0][0] == 'SITE_A'
        assert obs_data[1][0] == 'SITE_A'
        assert obs_data[2][0] == 'SITE_B'
        # SITE_A dates should be in order
        assert obs_data[0][1] < obs_data[1][1]

    def test_sites_sorted(self, tmp_path):
        """Test that obs_sites list is sorted."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        obs_file = self.create_obs_file(tmp_path, [
            ('ZEBRA', '01/15/2020'),
            ('ALPHA', '01/20/2020'),
            ('MIKE', '01/25/2020'),
        ])
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        assert obs_sites == sorted(obs_sites)

    def test_single_observation(self, tmp_path):
        """Test with single observation."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        obs_file = self.create_obs_file(tmp_path, [
            ('ONLY_SITE', '06/15/2020'),
        ])
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        assert len(obs_sites) == 1
        assert len(obs_data) == 1
        assert obs_sites[0] == 'ONLY_SITE'

    def test_many_observations(self, tmp_path):
        """Test with many observations."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        observations = []
        for i in range(100):
            site = f'SITE_{i % 10:02d}'
            day = (i % 28) + 1
            observations.append((site, f'01/{day:02d}/2020'))
        
        obs_file = self.create_obs_file(tmp_path, observations)
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        assert len(obs_sites) == 10  # 10 unique sites
        assert len(obs_data) == 100  # All observations

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd
        import inspect
        
        sig = inspect.signature(get_obs_hyd)
        params = list(sig.parameters.keys())
        
        assert 'obs_file' in params
        assert 'start_date' in params


class TestGetObsHydDateFormats:
    """Tests for date handling in get_obs_hyd."""

    def create_obs_file(self, tmp_path, observations):
        """Create observation file."""
        obs_file = tmp_path / 'obs.smp'
        lines = ['  '.join(str(x) for x in obs) for obs in observations]
        obs_file.write_text('\n'.join(lines))
        return str(obs_file)

    def test_mm_dd_yyyy_format(self, tmp_path):
        """Test MM/DD/YYYY date format."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd

        obs_file = self.create_obs_file(tmp_path, [
            ('SITE', '12/25/2020'),
        ])
        start_date = datetime(2020, 1, 1)

        obs_sites, obs_data = get_obs_hyd(obs_file, start_date)

        # December 25 is day 359 (or 360 in leap year 2020)
        assert obs_data[0][2].month == 12
        assert obs_data[0][2].day == 25
        assert obs_data[0][2].year == 2020


class TestGetObsHydImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import get_obs_hyd
        assert callable(get_obs_hyd)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd
        assert callable(get_obs_hyd)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.get_obs_hyd import get_obs_hyd
        
        assert get_obs_hyd.__doc__ is not None
        assert 'obs_sites' in get_obs_hyd.__doc__
        assert 'obs_data' in get_obs_hyd.__doc__


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
