# test_calib_sim_obs_list.py
# Unit tests for calib/sim_obs_list.py - Calculate simulated equivalents for observations
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


class TestSimObsList:
    """Tests for sim_obs_list function"""

    def test_returns_list(self):
        """Test that function returns a list."""
        from iwfm.calib.sim_obs_list import sim_obs_list

        obs = [
            ['WELL001', datetime(2020, 1, 15), '0:00:00', 100.0],
        ]
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        gwhyd_sim = [
            [95.0, 105.0],   # values at first date
            [100.0, 110.0],  # values at second date
        ]
        dates = [datetime(2020, 1, 10), datetime(2020, 1, 20)]

        result = sim_obs_list(obs, well_dict, gwhyd_sim, dates)

        assert isinstance(result, list)

    def test_calculates_simulated_equivalent(self):
        """Test that simulated equivalent is calculated."""
        from iwfm.calib.sim_obs_list import sim_obs_list

        obs = [
            ['WELL001', datetime(2020, 1, 15), '0:00:00', 100.0],
        ]
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        gwhyd_sim = [
            [90.0],   # value at 1/10
            [110.0],  # value at 1/20
        ]
        dates = [datetime(2020, 1, 10), datetime(2020, 1, 20)]

        result = sim_obs_list(obs, well_dict, gwhyd_sim, dates)

        # Should have one result
        assert len(result) == 1
        # Simulated value should be interpolated (midpoint = 100)
        assert abs(result[0][3] - 100.0) < 1.0

    def test_calculates_difference(self):
        """Test that difference (obs - sim) is calculated."""
        from iwfm.calib.sim_obs_list import sim_obs_list

        obs = [
            ['WELL001', datetime(2020, 1, 15), '0:00:00', 105.0],
        ]
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        gwhyd_sim = [
            [100.0],
            [100.0],
        ]
        dates = [datetime(2020, 1, 10), datetime(2020, 1, 20)]

        result = sim_obs_list(obs, well_dict, gwhyd_sim, dates)

        # Difference should be obs - sim = 105 - 100 = 5
        assert abs(result[0][4] - 5.0) < 0.1

    def test_filters_by_well_dict(self):
        """Test that only wells in well_dict are processed."""
        from iwfm.calib.sim_obs_list import sim_obs_list

        obs = [
            ['WELL001', datetime(2020, 1, 15), '0:00:00', 100.0],
            ['WELL002', datetime(2020, 1, 15), '0:00:00', 200.0],  # Not in dict
        ]
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        gwhyd_sim = [
            [95.0],
            [105.0],
        ]
        dates = [datetime(2020, 1, 10), datetime(2020, 1, 20)]

        result = sim_obs_list(obs, well_dict, gwhyd_sim, dates)

        # Should only have WELL001
        assert len(result) == 1
        assert result[0][0] == 'WELL001'

    def test_filters_by_date_range(self):
        """Test that observations outside date range are excluded."""
        from iwfm.calib.sim_obs_list import sim_obs_list

        obs = [
            ['WELL001', datetime(2020, 1, 15), '0:00:00', 100.0],  # In range
            ['WELL001', datetime(2019, 1, 15), '0:00:00', 90.0],   # Before range
            ['WELL001', datetime(2021, 1, 15), '0:00:00', 110.0],  # After range
        ]
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        gwhyd_sim = [
            [95.0],
            [105.0],
        ]
        dates = [datetime(2020, 1, 10), datetime(2020, 1, 20)]

        result = sim_obs_list(obs, well_dict, gwhyd_sim, dates)

        # Should only have one result (in range)
        assert len(result) == 1

    def test_multiple_observations(self):
        """Test with multiple observations."""
        from iwfm.calib.sim_obs_list import sim_obs_list

        obs = [
            ['WELL001', datetime(2020, 1, 12), '0:00:00', 100.0],
            ['WELL001', datetime(2020, 1, 15), '0:00:00', 102.0],
            ['WELL001', datetime(2020, 1, 18), '0:00:00', 104.0],
        ]
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        gwhyd_sim = [
            [90.0],
            [110.0],
        ]
        dates = [datetime(2020, 1, 10), datetime(2020, 1, 20)]

        result = sim_obs_list(obs, well_dict, gwhyd_sim, dates)

        assert len(result) == 3

    def test_output_format(self):
        """Test that output has correct format."""
        from iwfm.calib.sim_obs_list import sim_obs_list

        obs = [
            ['WELL001', datetime(2020, 1, 15), '0:00:00', 100.0],
        ]
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        gwhyd_sim = [
            [95.0],
            [105.0],
        ]
        dates = [datetime(2020, 1, 10), datetime(2020, 1, 20)]

        result = sim_obs_list(obs, well_dict, gwhyd_sim, dates)

        # Output format: [obs_name, date_str, obs_meas, sim_equiv, difference]
        assert len(result[0]) == 5
        assert result[0][0] == 'WELL001'  # Name
        assert '01/15/2020' in result[0][1]  # Date string


class TestSimObsListImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib.sim_obs_list import sim_obs_list
        assert callable(sim_obs_list)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.sim_obs_list import sim_obs_list
        assert callable(sim_obs_list)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.sim_obs_list import sim_obs_list
        
        assert sim_obs_list.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
