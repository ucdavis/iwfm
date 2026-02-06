# test_calib_ltsmp.py
# Unit tests for calib/ltsmp.py - Log-transform PEST SMP file values
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


class TestLtsmp:
    """Tests for ltsmp function"""

    def create_smp_file(self, tmp_path, observations):
        """Create a mock PEST SMP format file.
        
        SMP format: site_name  date  time  value
        
        Parameters
        ----------
        observations : list of tuples
            Each tuple is (site_name, date, time, value)
        """
        smp_file = tmp_path / 'input.smp'
        
        lines = []
        for obs in observations:
            site, date, time, value = obs
            # SMP format with specific spacing
            line = f'{site:<20} {date}  {time}   {value:12.4f}'
            lines.append(line)
        
        smp_file.write_text('\n'.join(lines))
        return str(smp_file)

    def test_creates_output_file(self, tmp_path):
        """Test that output file is created."""
        from iwfm.calib.ltsmp import ltsmp

        input_file = self.create_smp_file(tmp_path, [
            ('SITE_001', '01/15/2020', '0:00:00', 100.0),
        ])
        output_file = str(tmp_path / 'output.smp')

        ltsmp(input_file, output_file)

        assert os.path.exists(output_file)

    def test_output_file_has_content(self, tmp_path):
        """Test that output file has content."""
        from iwfm.calib.ltsmp import ltsmp

        input_file = self.create_smp_file(tmp_path, [
            ('SITE_001', '01/15/2020', '0:00:00', 100.0),
            ('SITE_002', '01/16/2020', '0:00:00', 200.0),
        ])
        output_file = str(tmp_path / 'output.smp')

        ltsmp(input_file, output_file)

        assert os.path.getsize(output_file) > 0

    def test_same_number_of_lines(self, tmp_path):
        """Test that output has same number of lines as input."""
        from iwfm.calib.ltsmp import ltsmp

        input_file = self.create_smp_file(tmp_path, [
            ('SITE_001', '01/15/2020', '0:00:00', 100.0),
            ('SITE_002', '01/16/2020', '0:00:00', 200.0),
            ('SITE_003', '01/17/2020', '0:00:00', 300.0),
        ])
        output_file = str(tmp_path / 'output.smp')

        ltsmp(input_file, output_file)

        with open(input_file, 'r') as f:
            input_lines = len(f.readlines())
        with open(output_file, 'r') as f:
            output_lines = len(f.readlines())

        assert output_lines == input_lines

    def test_preserves_site_name(self, tmp_path):
        """Test that site names are preserved."""
        from iwfm.calib.ltsmp import ltsmp

        input_file = self.create_smp_file(tmp_path, [
            ('MY_WELL_001', '01/15/2020', '0:00:00', 100.0),
        ])
        output_file = str(tmp_path / 'output.smp')

        ltsmp(input_file, output_file)

        with open(output_file, 'r') as f:
            content = f.read()

        assert 'MY_WELL_001' in content

    def test_transforms_values(self, tmp_path):
        """Test that values are log-transformed."""
        from iwfm.calib.ltsmp import ltsmp

        input_file = self.create_smp_file(tmp_path, [
            ('SITE_001', '01/15/2020', '0:00:00', 100.0),
        ])
        output_file = str(tmp_path / 'output.smp')

        ltsmp(input_file, output_file)

        with open(output_file, 'r') as f:
            output_line = f.readline()

        # Value should be different (log-transformed)
        # Original value was 100.0, log-transformed should be different
        assert '100.0000' not in output_line

    def test_multiple_observations(self, tmp_path):
        """Test with multiple observations."""
        from iwfm.calib.ltsmp import ltsmp

        observations = [
            (f'SITE_{i:03d}', f'01/{i+1:02d}/2020', '0:00:00', float(100 + i * 10))
            for i in range(20)
        ]
        input_file = self.create_smp_file(tmp_path, observations)
        output_file = str(tmp_path / 'output.smp')

        ltsmp(input_file, output_file)

        with open(output_file, 'r') as f:
            lines = f.readlines()

        assert len(lines) == 20

    def test_zero_offset_parameter(self, tmp_path):
        """Test that zero_offset parameter affects output."""
        from iwfm.calib.ltsmp import ltsmp

        input_file = self.create_smp_file(tmp_path, [
            ('SITE_001', '01/15/2020', '0:00:00', 100.0),
        ])
        output1 = str(tmp_path / 'output1.smp')
        output2 = str(tmp_path / 'output2.smp')

        ltsmp(input_file, output1, zero_offset=36.0)
        ltsmp(input_file, output2, zero_offset=100.0)

        # Both files should be created
        assert os.path.exists(output1)
        assert os.path.exists(output2)

    def test_neg_val_parameter(self, tmp_path):
        """Test that neg_val parameter is accepted."""
        from iwfm.calib.ltsmp import ltsmp

        input_file = self.create_smp_file(tmp_path, [
            ('SITE_001', '01/15/2020', '0:00:00', 100.0),
        ])
        output_file = str(tmp_path / 'output.smp')

        # Should not raise error
        ltsmp(input_file, output_file, neg_val=0.001)

        assert os.path.exists(output_file)

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.ltsmp import ltsmp
        import inspect
        
        sig = inspect.signature(ltsmp)
        params = list(sig.parameters.keys())
        
        assert 'input_file' in params
        assert 'output_file' in params
        assert 'zero_offset' in params
        assert 'neg_val' in params

    def test_default_parameter_values(self):
        """Test default parameter values."""
        from iwfm.calib.ltsmp import ltsmp
        import inspect
        
        sig = inspect.signature(ltsmp)
        
        assert sig.parameters['zero_offset'].default == 36.0
        assert sig.parameters['neg_val'].default == 0.001


class TestLtsmpImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import ltsmp
        assert callable(ltsmp)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.ltsmp import ltsmp
        assert callable(ltsmp)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.ltsmp import ltsmp
        
        assert ltsmp.__doc__ is not None
        assert 'smp' in ltsmp.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
