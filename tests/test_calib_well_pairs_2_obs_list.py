# test_calib_well_pairs_2_obs_list.py
# Unit tests for calib/well_pairs_2_obs_list.py - Process well pairs for head differences
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
import os


class TestWellPairs2ObsList:
    """Tests for well_pairs_2_obs_list function"""

    def create_well_pair_file(self, tmp_path, pairs):
        """Create a mock well pairs CSV file.
        
        Format: PairNo,WellName1,WellName2
        """
        pair_file = tmp_path / 'well_pairs.csv'
        
        lines = ['PairNo,WellName1,WellName2']
        for pair in pairs:
            lines.append(','.join(str(x) for x in pair))
        
        pair_file.write_text('\n'.join(lines))
        return str(pair_file)

    def create_obs_file(self, tmp_path, observations):
        """Create a mock observations CSV file.
        
        Format: WELL_NAME,MSMT_DATE,WSE
        """
        obs_file = tmp_path / 'observations.csv'
        
        lines = ['WELL_NAME,MSMT_DATE,WSE']
        for obs in observations:
            lines.append(','.join(str(x) for x in obs))
        
        obs_file.write_text('\n'.join(lines))
        return str(obs_file)

    def test_returns_three_values(self, tmp_path):
        """Test that function returns well_count, obs_count, output_file."""
        from iwfm.calib.well_pairs_2_obs_list import well_pairs_2_obs_list

        pair_file = self.create_well_pair_file(tmp_path, [
            (1, 'WELL_A', 'WELL_B'),
        ])
        obs_file = self.create_obs_file(tmp_path, [
            ('WELL_A', '01/15/2020', '100.0'),
            ('WELL_B', '01/15/2020', '95.0'),
        ])

        result = well_pairs_2_obs_list(pair_file, obs_file)

        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_counts_well_pairs(self, tmp_path):
        """Test that well pair count is returned."""
        from iwfm.calib.well_pairs_2_obs_list import well_pairs_2_obs_list

        pair_file = self.create_well_pair_file(tmp_path, [
            (1, 'WELL_A', 'WELL_B'),
            (2, 'WELL_C', 'WELL_D'),
            (3, 'WELL_E', 'WELL_F'),
        ])
        obs_file = self.create_obs_file(tmp_path, [
            ('WELL_A', '01/15/2020', '100.0'),
            ('WELL_B', '01/15/2020', '95.0'),
        ])

        well_count, obs_count, output_file = well_pairs_2_obs_list(pair_file, obs_file)

        assert well_count == 3

    def test_creates_output_file(self, tmp_path):
        """Test that output file is created."""
        from iwfm.calib.well_pairs_2_obs_list import well_pairs_2_obs_list

        pair_file = self.create_well_pair_file(tmp_path, [
            (1, 'WELL_A', 'WELL_B'),
        ])
        obs_file = self.create_obs_file(tmp_path, [
            ('WELL_A', '01/15/2020', '100.0'),
            ('WELL_B', '01/15/2020', '95.0'),
        ])

        well_count, obs_count, output_file = well_pairs_2_obs_list(pair_file, obs_file)

        assert os.path.exists(output_file)

    def test_matches_observations_within_window(self, tmp_path):
        """Test that observations within date window are matched."""
        from iwfm.calib.well_pairs_2_obs_list import well_pairs_2_obs_list

        pair_file = self.create_well_pair_file(tmp_path, [
            (1, 'WELL_A', 'WELL_B'),
        ])
        obs_file = self.create_obs_file(tmp_path, [
            ('WELL_A', '01/15/2020', '100.0'),
            ('WELL_B', '01/20/2020', '95.0'),  # 5 days apart (within default 15)
        ])

        well_count, obs_count, output_file = well_pairs_2_obs_list(pair_file, obs_file, days=15)

        assert obs_count >= 1

    def test_custom_days_window(self, tmp_path):
        """Test with custom days window."""
        from iwfm.calib.well_pairs_2_obs_list import well_pairs_2_obs_list

        pair_file = self.create_well_pair_file(tmp_path, [
            (1, 'WELL_A', 'WELL_B'),
        ])
        obs_file = self.create_obs_file(tmp_path, [
            ('WELL_A', '01/15/2020', '100.0'),
            ('WELL_B', '01/25/2020', '95.0'),  # 10 days apart
        ])

        # With 5-day window, should not match
        well_count, obs_count1, _ = well_pairs_2_obs_list(pair_file, obs_file, days=5)
        
        # With 15-day window, should match
        well_count, obs_count2, _ = well_pairs_2_obs_list(pair_file, obs_file, days=15)

        assert obs_count1 <= obs_count2

    def test_no_matching_observations(self, tmp_path):
        """Test when no observations match."""
        from iwfm.calib.well_pairs_2_obs_list import well_pairs_2_obs_list

        pair_file = self.create_well_pair_file(tmp_path, [
            (1, 'WELL_A', 'WELL_B'),
        ])
        obs_file = self.create_obs_file(tmp_path, [
            ('WELL_X', '01/15/2020', '100.0'),  # Different wells
            ('WELL_Y', '01/15/2020', '95.0'),
        ])

        well_count, obs_count, output_file = well_pairs_2_obs_list(pair_file, obs_file)

        assert obs_count == 0

    def test_output_filename_convention(self, tmp_path):
        """Test that output filename follows convention."""
        from iwfm.calib.well_pairs_2_obs_list import well_pairs_2_obs_list

        pair_file = self.create_well_pair_file(tmp_path, [
            (1, 'WELL_A', 'WELL_B'),
        ])
        obs_file = self.create_obs_file(tmp_path, [
            ('WELL_A', '01/15/2020', '100.0'),
            ('WELL_B', '01/15/2020', '95.0'),
        ])

        well_count, obs_count, output_file = well_pairs_2_obs_list(pair_file, obs_file)

        # Output should be input with _headfiff.csv
        assert '_headfiff.csv' in output_file


class TestWellPairs2ObsListImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import well_pairs_2_obs_list
        assert callable(well_pairs_2_obs_list)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.well_pairs_2_obs_list import well_pairs_2_obs_list
        assert callable(well_pairs_2_obs_list)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.well_pairs_2_obs_list import well_pairs_2_obs_list
        
        assert well_pairs_2_obs_list.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
