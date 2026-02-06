# test_calib_read_gw_file.py
# Unit tests for calib/read_gw_file.py - Read IWFM Groundwater file parameters
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


class TestReadGwFile:
    """Tests for read_gw_file function"""

    def create_gw_file(self, tmp_path, num_nodes=3, num_layers=2, factors=None):
        """Create a mock IWFM Groundwater file.
        
        The file structure follows IWFM format with:
        - Initial lines (skipped, start at line 10)
        - Comment blocks and data sections
        - Scaling factors line
        - Parameter values for each node/layer
        """
        if factors is None:
            factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            
        gw_file = tmp_path / 'groundwater.dat'
        
        lines = []
        
        # Lines 0-9 (first 10 lines - skipped)
        for i in range(10):
            lines.append(f'C  Header line {i}')
        
        # Comment block
        lines.append('C  File names section')
        lines.append('C  -------------------')
        
        # File names and units (non-comment)
        lines.append('  groundwater.bin')
        lines.append('  FEET')
        
        # Comment block
        lines.append('C  KDEB section')
        
        # KDEB line (non-comment)
        lines.append('  0')
        
        # Comment block
        lines.append('C  Hydrograph information')
        
        # Hydrograph info (non-comment)
        lines.append('  5')
        lines.append('  hydrographs.out')
        
        # Comment block
        lines.append('C  Hydrograph output locations')
        
        # Hydrograph lines (non-comment)
        lines.append('  1  100  1  WELL_001')
        lines.append('  2  200  1  WELL_002')
        
        # Comment block
        lines.append('C  Face flow control')
        
        # Face flow control (non-comment)
        lines.append('  0')
        
        # Comment block
        lines.append('C  NGROUP section')
        
        # NGROUP line (non-comment)
        lines.append('  1')
        
        # Comment block
        lines.append('C  Scaling factors')
        
        # Factors line (non-comment) - THIS IS WHAT WE READ
        factors_str = '  ' + '  '.join(str(f) for f in factors)
        lines.append(factors_str)
        
        # Comment block
        lines.append('C  Time units')
        
        # Time units (non-comment)
        lines.append('  DAY')
        
        # Comment block before parameters
        lines.append('C  Parameter values')
        lines.append('C  Node  PKH  PS  PN  PV  PL')
        
        # Parameter lines (non-comment)
        # Format: node_id (first layer only), then PKH, PS, PN, PV, PL
        for n in range(1, num_nodes + 1):
            for l in range(num_layers):
                pkh = 10.0 + n
                ps = 1.0e-05 * n
                pn = 0.15 + n * 0.01
                pv = 1.0e-06 * n
                pl = 10.0 + n
                if l == 0:
                    lines.append(f'  {n}  {pkh:.4f}  {ps:.3E}  {pn:.3f}  {pv:.3E}  {pl:.4f}')
                else:
                    lines.append(f'      {pkh:.4f}  {ps:.3E}  {pn:.3f}  {pv:.3E}  {pl:.4f}')
        
        # Trailing comment
        lines.append('C  End of groundwater file')
        
        gw_file.write_text('\n'.join(lines))
        return str(gw_file)

    def test_returns_three_items(self, tmp_path):
        """Test that function returns gw_lines, factors, parvals_d."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        result = read_gw_file(gw_file, nlay=2, keys_file=keys_file, dict_file=dict_file)

        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_gw_lines_is_list(self, tmp_path):
        """Test that gw_lines is a list of strings."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        gw_lines, factors, parvals_d = read_gw_file(
            gw_file, nlay=2, keys_file=keys_file, dict_file=dict_file
        )

        assert isinstance(gw_lines, list)
        assert all(isinstance(line, str) for line in gw_lines)

    def test_factors_is_list_of_floats(self, tmp_path):
        """Test that factors is a list of floats."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        gw_lines, factors, parvals_d = read_gw_file(
            gw_file, nlay=2, keys_file=keys_file, dict_file=dict_file
        )

        assert isinstance(factors, list)
        assert all(isinstance(f, float) for f in factors)

    def test_reads_factors_correctly(self, tmp_path):
        """Test that scaling factors are read correctly."""
        from iwfm.calib.read_gw_file import read_gw_file

        expected_factors = [2.5, 3.5, 4.5, 5.5, 6.5, 7.5]
        gw_file = self.create_gw_file(tmp_path, factors=expected_factors)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        gw_lines, factors, parvals_d = read_gw_file(
            gw_file, nlay=2, keys_file=keys_file, dict_file=dict_file
        )

        assert len(factors) == 6
        for i, expected in enumerate(expected_factors):
            assert abs(factors[i] - expected) < 0.01

    def test_parvals_d_is_dictionary(self, tmp_path):
        """Test that parvals_d is a dictionary."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        gw_lines, factors, parvals_d = read_gw_file(
            gw_file, nlay=2, keys_file=keys_file, dict_file=dict_file
        )

        assert isinstance(parvals_d, dict)

    def test_parvals_d_keys_format(self, tmp_path):
        """Test that parvals_d keys have format 'node_layer'."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path, num_nodes=3, num_layers=2)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        gw_lines, factors, parvals_d = read_gw_file(
            gw_file, nlay=2, keys_file=keys_file, dict_file=dict_file
        )

        # Check that keys follow 'node_layer' format
        for key in parvals_d.keys():
            parts = key.split('_')
            assert len(parts) == 2
            assert parts[0].isdigit()  # node number
            assert parts[1].isdigit()  # layer number

    def test_parvals_d_values_are_lists(self, tmp_path):
        """Test that parvals_d values are lists of parameters."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        gw_lines, factors, parvals_d = read_gw_file(
            gw_file, nlay=2, keys_file=keys_file, dict_file=dict_file
        )

        for key, values in parvals_d.items():
            assert isinstance(values, list)
            assert all(isinstance(v, float) for v in values)

    def test_creates_keys_file(self, tmp_path):
        """Test that keys output file is created."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path)
        keys_file = str(tmp_path / 'my_keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        read_gw_file(gw_file, nlay=2, keys_file=keys_file, dict_file=dict_file)

        assert os.path.exists(keys_file)

    def test_creates_dict_file(self, tmp_path):
        """Test that dictionary output file is created."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'my_dict.txt')

        read_gw_file(gw_file, nlay=2, keys_file=keys_file, dict_file=dict_file)

        assert os.path.exists(dict_file)

    def test_single_layer(self, tmp_path):
        """Test with single layer."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path, num_nodes=3, num_layers=1)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        gw_lines, factors, parvals_d = read_gw_file(
            gw_file, nlay=1, keys_file=keys_file, dict_file=dict_file
        )

        # Should have 3 entries (one per node)
        assert len(parvals_d) == 3
        # All keys should end with '_1'
        for key in parvals_d.keys():
            assert key.endswith('_1')

    def test_multiple_layers(self, tmp_path):
        """Test with multiple layers."""
        from iwfm.calib.read_gw_file import read_gw_file

        gw_file = self.create_gw_file(tmp_path, num_nodes=2, num_layers=3)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        gw_lines, factors, parvals_d = read_gw_file(
            gw_file, nlay=3, keys_file=keys_file, dict_file=dict_file
        )

        # Should have 2 nodes * 3 layers = 6 entries
        assert len(parvals_d) == 6

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.read_gw_file import read_gw_file
        import inspect
        
        sig = inspect.signature(read_gw_file)
        params = list(sig.parameters.keys())
        
        assert 'gw_file' in params
        assert 'nlay' in params
        assert 'keys_file' in params
        assert 'dict_file' in params
        assert 'verbose' in params

    def test_default_parameter_values(self):
        """Test default parameter values."""
        from iwfm.calib.read_gw_file import read_gw_file
        import inspect
        
        sig = inspect.signature(read_gw_file)
        
        assert sig.parameters['keys_file'].default == 'parvals_keys.txt'
        assert sig.parameters['dict_file'].default == 'parvals_d.txt'
        assert sig.parameters['verbose'].default == False


class TestReadGwFileEdgeCases:
    """Edge case tests for read_gw_file"""

    def create_minimal_gw_file(self, tmp_path, factors, params):
        """Create a minimal groundwater file for testing."""
        gw_file = tmp_path / 'gw.dat'
        
        lines = []
        # 10 header lines
        for i in range(10):
            lines.append(f'C  Line {i}')
        
        # Minimal structure
        lines.append('C  Comment')
        lines.append('  data')
        lines.append('C  Comment')
        lines.append('  KDEB')
        lines.append('C  Comment')
        lines.append('  hyd_info')
        lines.append('C  Comment')
        lines.append('  hyd_line')
        lines.append('C  Comment')
        lines.append('  face_flow')
        lines.append('C  Comment')
        lines.append('  NGROUP')
        lines.append('C  Comment')
        lines.append('  ' + '  '.join(str(f) for f in factors))
        lines.append('C  Comment')
        lines.append('  time_units')
        lines.append('C  Comment')
        
        # Parameters
        for param_line in params:
            lines.append(param_line)
        
        lines.append('C  End')
        
        gw_file.write_text('\n'.join(lines))
        return str(gw_file)

    def test_many_nodes(self, tmp_path):
        """Test with many nodes."""
        from iwfm.calib.read_gw_file import read_gw_file

        factors = [1.0] * 6
        params = []
        num_nodes = 100
        for n in range(1, num_nodes + 1):
            params.append(f'  {n}  10.0  1E-5  0.15  1E-6  10.0')

        gw_file = self.create_minimal_gw_file(tmp_path, factors, params)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        gw_lines, factors_out, parvals_d = read_gw_file(
            gw_file, nlay=1, keys_file=keys_file, dict_file=dict_file
        )

        assert len(parvals_d) == num_nodes

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output."""
        from iwfm.calib.read_gw_file import read_gw_file

        factors = [1.0] * 6
        params = ['  1  10.0  1E-5  0.15  1E-6  10.0']

        gw_file = self.create_minimal_gw_file(tmp_path, factors, params)
        keys_file = str(tmp_path / 'keys.txt')
        dict_file = str(tmp_path / 'dict.txt')

        read_gw_file(gw_file, nlay=1, keys_file=keys_file, dict_file=dict_file, verbose=True)

        captured = capsys.readouterr()
        assert 'Read' in captured.out


class TestReadGwFileImports:
    """Tests for module imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import read_gw_file
        assert callable(read_gw_file)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.read_gw_file import read_gw_file
        assert callable(read_gw_file)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.read_gw_file import read_gw_file
        
        assert read_gw_file.__doc__ is not None
        assert 'factors' in read_gw_file.__doc__
        assert 'params' in read_gw_file.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
