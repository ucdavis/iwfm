# test_calib_hyds_missed.py
# Unit tests for calib/hyds_missed.py - Compare lists and find missing sites
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


class TestHydsMissed:
    """Tests for hyds_missed function"""

    def test_returns_two_lists(self):
        """Test that function returns sim_miss and obs_miss."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = ['A', 'B', 'C']
        obs_sites = ['B', 'C', 'D']

        result = hyds_missed(sim_sites, obs_sites)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)

    def test_sim_miss_contains_sites_not_in_obs(self):
        """Test that sim_miss contains simulation sites not in observation sites."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = ['A', 'B', 'C', 'D']
        obs_sites = ['B', 'C']

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        # A and D are in sim but not obs
        assert 'A' in sim_miss
        assert 'D' in sim_miss
        assert 'B' not in sim_miss
        assert 'C' not in sim_miss

    def test_obs_miss_contains_sites_not_in_sim(self):
        """Test that obs_miss contains observation sites not in simulation sites."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = ['A', 'B']
        obs_sites = ['B', 'C', 'D', 'E']

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        # C, D, E are in obs but not sim
        assert 'C' in obs_miss
        assert 'D' in obs_miss
        assert 'E' in obs_miss
        assert 'B' not in obs_miss

    def test_no_missing_sites(self):
        """Test when all sites are in both lists."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = ['A', 'B', 'C']
        obs_sites = ['A', 'B', 'C']

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        assert sim_miss == []
        assert obs_miss == []

    def test_all_sites_missing(self):
        """Test when no sites are in common."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = ['A', 'B', 'C']
        obs_sites = ['X', 'Y', 'Z']

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        assert set(sim_miss) == {'A', 'B', 'C'}
        assert set(obs_miss) == {'X', 'Y', 'Z'}

    def test_empty_sim_sites(self):
        """Test with empty simulation sites list."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = []
        obs_sites = ['A', 'B', 'C']

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        assert sim_miss == []
        assert set(obs_miss) == {'A', 'B', 'C'}

    def test_empty_obs_sites(self):
        """Test with empty observation sites list."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = ['A', 'B', 'C']
        obs_sites = []

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        assert set(sim_miss) == {'A', 'B', 'C'}
        assert obs_miss == []

    def test_both_empty(self):
        """Test with both lists empty."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = []
        obs_sites = []

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        assert sim_miss == []
        assert obs_miss == []

    def test_single_site_lists(self):
        """Test with single site in each list."""
        from iwfm.calib.hyds_missed import hyds_missed

        # Same site
        sim_miss, obs_miss = hyds_missed(['A'], ['A'])
        assert sim_miss == []
        assert obs_miss == []

        # Different sites
        sim_miss, obs_miss = hyds_missed(['A'], ['B'])
        assert 'A' in sim_miss
        assert 'B' in obs_miss

    def test_duplicates_in_lists(self):
        """Test that duplicates are handled (set conversion removes them)."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = ['A', 'A', 'B', 'B', 'C']
        obs_sites = ['B', 'C', 'C', 'D']

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        # A is in sim but not obs (duplicates don't matter)
        assert 'A' in sim_miss
        # D is in obs but not sim
        assert 'D' in obs_miss

    def test_large_lists(self):
        """Test with large lists."""
        from iwfm.calib.hyds_missed import hyds_missed

        # 1000 sim sites, 800 obs sites with 500 overlap
        sim_sites = [f'SIM_{i:04d}' for i in range(1000)]
        obs_sites = [f'SIM_{i:04d}' for i in range(500, 1300)]  # 500-1299

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        # Sites 0-499 are in sim but not obs
        assert len(sim_miss) == 500
        # Sites 1000-1299 are in obs but not sim
        assert len(obs_miss) == 300

    def test_typical_well_names(self):
        """Test with typical well name formats."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = [
            'WELL_001',
            'WELL_002',
            'WELL_003',
            'S_380313N1219426W001',
        ]
        obs_sites = [
            'WELL_002',
            'WELL_003',
            'WELL_004',
            'S_381150N1215899W001',
        ]

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        # WELL_001 and state well number in sim but not obs
        assert 'WELL_001' in sim_miss
        assert 'S_380313N1219426W001' in sim_miss
        
        # WELL_004 and state well number in obs but not sim
        assert 'WELL_004' in obs_miss
        assert 'S_381150N1215899W001' in obs_miss

    def test_case_sensitive(self):
        """Test that comparison is case-sensitive."""
        from iwfm.calib.hyds_missed import hyds_missed

        sim_sites = ['Well_A', 'WELL_A', 'well_a']
        obs_sites = ['WELL_A']

        sim_miss, obs_miss = hyds_missed(sim_sites, obs_sites)

        # Well_A and well_a are different from WELL_A
        assert 'Well_A' in sim_miss
        assert 'well_a' in sim_miss
        assert 'WELL_A' not in sim_miss

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.hyds_missed import hyds_missed
        import inspect
        
        sig = inspect.signature(hyds_missed)
        params = list(sig.parameters.keys())
        
        assert 'sim_sites' in params
        assert 'obs_sites' in params


class TestItemsNotInSecondList:
    """Tests for items_not_in_second_list helper function"""

    def test_basic_functionality(self):
        """Test basic functionality."""
        from iwfm.calib.hyds_missed import items_not_in_second_list

        list1 = ['A', 'B', 'C', 'D']
        list2 = ['B', 'C', 'E']

        result = items_not_in_second_list(list1, list2)

        # A and D are in list1 but not list2
        assert set(result) == {'A', 'D'}

    def test_returns_list(self):
        """Test that function returns a list."""
        from iwfm.calib.hyds_missed import items_not_in_second_list

        result = items_not_in_second_list(['A'], ['B'])

        assert isinstance(result, list)

    def test_empty_first_list(self):
        """Test with empty first list."""
        from iwfm.calib.hyds_missed import items_not_in_second_list

        result = items_not_in_second_list([], ['A', 'B'])

        assert result == []

    def test_empty_second_list(self):
        """Test with empty second list."""
        from iwfm.calib.hyds_missed import items_not_in_second_list

        result = items_not_in_second_list(['A', 'B'], [])

        assert set(result) == {'A', 'B'}

    def test_identical_lists(self):
        """Test with identical lists."""
        from iwfm.calib.hyds_missed import items_not_in_second_list

        result = items_not_in_second_list(['A', 'B', 'C'], ['A', 'B', 'C'])

        assert result == []

    def test_uses_set_difference(self):
        """Test that function uses efficient set difference."""
        from iwfm.calib import hyds_missed as module
        import inspect
        
        source = inspect.getsource(module.items_not_in_second_list)
        
        # Should use set operations
        assert 'set(' in source
        assert 'set1 - set2' in source or 'difference' in source


class TestHydsMissedImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import hyds_missed
        assert callable(hyds_missed)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.hyds_missed import hyds_missed
        assert callable(hyds_missed)

    def test_import_helper_function(self):
        """Test import of helper function."""
        from iwfm.calib.hyds_missed import items_not_in_second_list
        assert callable(items_not_in_second_list)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.hyds_missed import hyds_missed
        
        assert hyds_missed.__doc__ is not None
        assert 'sim_miss' in hyds_missed.__doc__
        assert 'obs_miss' in hyds_missed.__doc__


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
