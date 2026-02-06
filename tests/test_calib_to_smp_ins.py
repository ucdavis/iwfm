# test_calib_to_smp_ins.py
# Unit tests for calib/to_smp_ins.py - Write SMP and INS file lines
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


class TestToSmpIns:
    """Tests for to_smp_ins function"""

    def test_returns_two_strings(self):
        """Test that function returns smp and ins strings."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = 100.5
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        assert isinstance(smp, str)
        assert isinstance(ins, str)

    def test_smp_contains_site_name(self):
        """Test that SMP string contains site name."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'MY_WELL_001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = 100.5
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        assert 'MY_WELL_001' in smp

    def test_smp_contains_date(self):
        """Test that SMP string contains formatted date."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = 100.5
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        assert '01/15/2020' in smp

    def test_smp_contains_time(self):
        """Test that SMP string contains time."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = 100.5
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        assert '0:00:00' in smp

    def test_smp_contains_value(self):
        """Test that SMP string contains observation value."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = 123.456789
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        # Value should be rounded to 6 decimal places
        assert '123.456789' in smp

    def test_ins_contains_site_name(self):
        """Test that INS string contains site name."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = 100.5
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        assert 'WELL001' in ins

    def test_ins_contains_timestep(self):
        """Test that INS string contains timestep."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = 100.5
        ts = 42

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        # Timestep should be zero-padded to 3 digits
        assert '_042]' in ins or '_42]' in ins

    def test_ins_format_L1(self):
        """Test that INS string starts with L1."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = 100.5
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        assert ins.startswith('L1')

    def test_ins_contains_column_positions(self):
        """Test that INS string contains column positions."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = 100.5
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        assert '42:70' in ins

    def test_different_dates(self):
        """Test with different dates."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2025, 12, 31)
        obs_val = 100.5
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        assert '12/31/2025' in smp

    def test_negative_value(self):
        """Test with negative observation value."""
        from iwfm.calib.to_smp_ins import to_smp_ins

        obs_site = 'WELL001'
        obs_dt = datetime(2020, 1, 15)
        obs_val = -50.25
        ts = 1

        smp, ins = to_smp_ins(obs_site, obs_dt, obs_val, ts)

        assert '-50.25' in smp


class TestToSmpInsImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import to_smp_ins
        assert callable(to_smp_ins)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.to_smp_ins import to_smp_ins
        assert callable(to_smp_ins)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.to_smp_ins import to_smp_ins
        
        assert to_smp_ins.__doc__ is not None
        assert 'smp' in to_smp_ins.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
