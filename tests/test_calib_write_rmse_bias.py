# test_calib_write_rmse_bias.py
# Unit tests for calib/write_rmse_bias.py - Write RMSE and bias values to file
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


class TestWriteRmseBias:
    """Tests for write_rmse_bias function"""

    def test_creates_output_file(self, tmp_path):
        """Test that output file is created."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias

        output_file = str(tmp_path / 'stats.txt')
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        well_names = ['WELL001']
        rmse = [5.0]
        bias = [2.0]
        count = [10]

        write_rmse_bias(output_file, well_dict, well_names, rmse, bias, count)

        assert os.path.exists(output_file)

    def test_writes_header(self, tmp_path):
        """Test that header is written."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias

        output_file = str(tmp_path / 'stats.txt')
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        well_names = ['WELL001']
        rmse = [5.0]
        bias = [2.0]
        count = [10]

        write_rmse_bias(output_file, well_dict, well_names, rmse, bias, count)

        with open(output_file, 'r') as f:
            header = f.readline()

        assert 'ID' in header
        assert 'Well Name' in header
        assert 'X' in header
        assert 'Y' in header
        assert 'Layer' in header
        assert 'RMSE' in header
        assert 'Bias' in header
        assert 'Count' in header

    def test_writes_well_data(self, tmp_path):
        """Test that well data is written."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias

        output_file = str(tmp_path / 'stats.txt')
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=123.45, y=678.90, layer=2, name='well001')}
        well_names = ['WELL001']
        rmse = [5.5]
        bias = [2.25]
        count = [15]

        write_rmse_bias(output_file, well_dict, well_names, rmse, bias, count)

        with open(output_file, 'r') as f:
            content = f.read()

        assert 'WELL001' in content
        assert '123.45' in content
        assert '678.9' in content
        assert '5.5' in content
        assert '2.25' in content
        assert '15' in content

    def test_multiple_wells(self, tmp_path):
        """Test with multiple wells."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias

        output_file = str(tmp_path / 'stats.txt')
        from iwfm.dataclasses import WellInfo
        well_dict = {
            'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001'),
            'WELL002': WellInfo(column=2, x=150.0, y=250.0, layer=2, name='well002'),
            'WELL003': WellInfo(column=3, x=200.0, y=300.0, layer=1, name='well003'),
        }
        well_names = ['WELL001', 'WELL002', 'WELL003']
        rmse = [5.0, 6.0, 7.0]
        bias = [1.0, 2.0, 3.0]
        count = [10, 20, 30]

        write_rmse_bias(output_file, well_dict, well_names, rmse, bias, count)

        with open(output_file, 'r') as f:
            lines = f.readlines()

        # Should have header + 3 data lines
        assert len(lines) == 4

    def test_skips_missing_wells(self, tmp_path):
        """Test that wells not in well_dict are skipped."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias

        output_file = str(tmp_path / 'stats.txt')
        from iwfm.dataclasses import WellInfo
        well_dict = {
            'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001'),
            # WELL002 is missing from dict
        }
        well_names = ['WELL001', 'WELL002']
        rmse = [5.0, 6.0]
        bias = [1.0, 2.0]
        count = [10, 20]

        write_rmse_bias(output_file, well_dict, well_names, rmse, bias, count)

        with open(output_file, 'r') as f:
            content = f.read()

        assert 'WELL001' in content
        # WELL002 should not be in output (not in well_dict)

    def test_negative_bias(self, tmp_path):
        """Test with negative bias values."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias

        output_file = str(tmp_path / 'stats.txt')
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001')}
        well_names = ['WELL001']
        rmse = [5.0]
        bias = [-3.5]
        count = [10]

        write_rmse_bias(output_file, well_dict, well_names, rmse, bias, count)

        with open(output_file, 'r') as f:
            content = f.read()

        assert '-3.5' in content

    def test_rounds_values(self, tmp_path):
        """Test that values are rounded to 2 decimal places."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias

        output_file = str(tmp_path / 'stats.txt')
        from iwfm.dataclasses import WellInfo
        well_dict = {'WELL001': WellInfo(column=1, x=100.123456, y=200.654321, layer=1, name='well001')}
        well_names = ['WELL001']
        rmse = [5.12345]
        bias = [2.98765]
        count = [10]

        write_rmse_bias(output_file, well_dict, well_names, rmse, bias, count)

        with open(output_file, 'r') as f:
            content = f.read()

        assert '100.12' in content
        assert '200.65' in content
        assert '5.12' in content
        assert '2.99' in content

    def test_incremental_id(self, tmp_path):
        """Test that IDs are incremental (1-based)."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias

        output_file = str(tmp_path / 'stats.txt')
        from iwfm.dataclasses import WellInfo
        well_dict = {
            'WELL001': WellInfo(column=1, x=100.0, y=200.0, layer=1, name='well001'),
            'WELL002': WellInfo(column=2, x=150.0, y=250.0, layer=2, name='well002'),
        }
        well_names = ['WELL001', 'WELL002']
        rmse = [5.0, 6.0]
        bias = [1.0, 2.0]
        count = [10, 20]

        write_rmse_bias(output_file, well_dict, well_names, rmse, bias, count)

        with open(output_file, 'r') as f:
            lines = f.readlines()

        # First data line should have ID=1, second should have ID=2
        assert lines[1].startswith('1\t')
        assert lines[2].startswith('2\t')


class TestWriteRmseBiasImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import write_rmse_bias
        assert callable(write_rmse_bias)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias
        assert callable(write_rmse_bias)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.write_rmse_bias import write_rmse_bias
        
        assert write_rmse_bias.__doc__ is not None
        assert 'rmse' in write_rmse_bias.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
