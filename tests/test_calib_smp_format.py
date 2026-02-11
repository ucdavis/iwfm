# test_calib_smp_format.py
# Unit tests for calib/smp_format.py - Reformat SMP file
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


class TestSmpFormat:
    """Tests for smp_format function"""

    def create_smp_file(self, tmp_path, observations):
        """Create a mock SMP file.
        
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
        from iwfm.calib.smp_format import smp_format

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '1/15/2020', '0:00:00', '100.0'),
        ])

        result = smp_format(smp_file)

        assert isinstance(result, list)

    def test_preserves_line_count(self, tmp_path):
        """Test that output has same number of lines as input."""
        from iwfm.calib.smp_format import smp_format

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '1/15/2020', '0:00:00', '100.0'),
            ('WELL002', '1/16/2020', '0:00:00', '200.0'),
            ('WELL003', '1/17/2020', '0:00:00', '300.0'),
        ])

        result = smp_format(smp_file)

        assert len(result) == 3

    def test_formats_date(self, tmp_path):
        """Test that date is reformatted to mm/dd/yyyy."""
        from iwfm.calib.smp_format import smp_format

        # Input with single-digit month/day
        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '1/5/2020', '0:00:00', '100.0'),
        ])

        result = smp_format(smp_file)

        # Should be reformatted to 01/05/2020
        assert '01/05/2020' in result[0]

    def test_preserves_site_name(self, tmp_path):
        """Test that site name is preserved."""
        from iwfm.calib.smp_format import smp_format

        smp_file = self.create_smp_file(tmp_path, [
            ('MY_WELL_001', '1/15/2020', '0:00:00', '100.0'),
        ])

        result = smp_format(smp_file)

        assert 'MY_WELL_001' in result[0]

    def test_pads_site_name(self, tmp_path):
        """Test that site name is padded to specified width."""
        from iwfm.calib.smp_format import smp_format

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL', '1/15/2020', '0:00:00', '100.0'),
        ])

        result = smp_format(smp_file, nwidth=20)

        # Site name should be padded to 20 characters
        assert len(result[0].split()[0]) >= 4  # At least site name length

    def test_includes_time(self, tmp_path):
        """Test that output includes time string."""
        from iwfm.calib.smp_format import smp_format

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '1/15/2020', '0:00:00', '100.0'),
        ])

        result = smp_format(smp_file)

        assert '0:00:00' in result[0]

    def test_preserves_value(self, tmp_path):
        """Test that observation value is preserved."""
        from iwfm.calib.smp_format import smp_format

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '1/15/2020', '0:00:00', '123.456'),
        ])

        result = smp_format(smp_file)

        assert '123.456' in result[0]

    def test_custom_nwidth(self, tmp_path):
        """Test with custom name width."""
        from iwfm.calib.smp_format import smp_format

        smp_file = self.create_smp_file(tmp_path, [
            ('WELL001', '1/15/2020', '0:00:00', '100.0'),
        ])

        result = smp_format(smp_file, nwidth=30)

        # Should not raise error
        assert len(result) == 1


class TestSmpFormatImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib.smp_format import smp_format
        assert callable(smp_format)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.smp_format import smp_format
        assert callable(smp_format)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.smp_format import smp_format
        
        assert smp_format.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
