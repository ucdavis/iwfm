# test_calib_params2gw.py
# Unit tests for calib/params2gw.py - Read/write parameter values to IWFM Groundwater file
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


class TestWriteGwFile:
    """Tests for write_gw_file function"""

    def create_mock_gw_lines(self, num_nodes=3, num_layers=2):
        """Create mock groundwater file lines for testing write_gw_file."""
        lines = []
        
        # Initial comment block
        lines.append('C  IWFM Groundwater File')
        lines.append('C  Test file for unit testing')
        
        # File names and units (non-comment)
        lines.append('  groundwater.bin')
        lines.append('  FEET')
        
        # Comment block
        lines.append('C  KDEB section')
        
        # KDEB line (non-comment)
        lines.append('  0')
        
        # Comment block
        lines.append('C  Hydrograph information section')
        
        # Hydrograph info (non-comment)
        lines.append('  5')
        lines.append('  hydrographs.out')
        
        # Comment block
        lines.append('C  Hydrograph lines section')
        
        # Hydrograph lines (non-comment)
        lines.append('  1  100  1  WELL_001')
        lines.append('  2  200  1  WELL_002')
        
        # Comment block
        lines.append('C  Face flow control section')
        
        # Face flow control (non-comment)
        lines.append('  0')
        
        # Comment block
        lines.append('C  NGROUP section')
        
        # NGROUP line (non-comment)
        lines.append('  1')
        
        # Comment block
        lines.append('C  Factors section')
        
        # Factors line (non-comment) - will be replaced
        lines.append('  1.0  1.0  1.0  1.0  1.0  1.0')
        
        # Comment block
        lines.append('C  Time units section')
        
        # Time units (non-comment)
        lines.append('  DAY')
        
        # Comment block before parameters
        lines.append('C  Parameter values section')
        lines.append('C  ID  PKH  PS  PN  PV  PL')
        
        # Parameter lines (non-comment) - will be replaced
        for n in range(1, num_nodes + 1):
            for l in range(num_layers):
                if l == 0:
                    lines.append(f'  {n}  10.0  1.0E-05  0.15  1.0E-06  10.0')
                else:
                    lines.append(f'      10.0  1.0E-05  0.15  1.0E-06  10.0')
        
        # Trailing comment
        lines.append('C  End of file')
        
        return lines

    def create_mock_parvals_d(self, num_nodes=3, num_layers=2):
        """Create mock parameter values dictionary."""
        parvals_d = {}
        for n in range(1, num_nodes + 1):
            for l in range(1, num_layers + 1):
                key = f'{n}_{l}'
                # [PKH, PS, PN, PV, PL]
                parvals_d[key] = [10.0, 1.0e-05, 0.15, 1.0e-06, 10.0]
        return parvals_d

    def create_mock_parvals(self, num_nodes=3, num_layers=2, value=20.0):
        """Create mock new parameter values.
        
        Structure: parvals[param_type][layer][node]
        param_types: PKH, PS, PN, PV, PL (5 types)
        """
        parvals = []
        for ptype in range(5):  # 5 parameter types
            ptype_vals = []
            for layer in range(num_layers):
                layer_vals = [value * (ptype + 1)] * num_nodes
                ptype_vals.append(layer_vals)
            parvals.append(ptype_vals)
        return parvals

    def test_creates_output_file(self, tmp_path):
        """Test that output file is created."""
        from iwfm.calib.params2gw import write_gw_file

        gw_lines = self.create_mock_gw_lines()
        parvals_d = self.create_mock_parvals_d()
        parvals = self.create_mock_parvals()
        parnodes = [1, 2, 3]
        factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        outfile = str(tmp_path / 'output_gw.dat')

        write_gw_file(outfile, gw_lines, 2, parnodes, parvals, factors, parvals_d)

        assert os.path.exists(outfile)

    def test_output_file_has_content(self, tmp_path):
        """Test that output file has content."""
        from iwfm.calib.params2gw import write_gw_file

        gw_lines = self.create_mock_gw_lines()
        parvals_d = self.create_mock_parvals_d()
        parvals = self.create_mock_parvals()
        parnodes = [1, 2, 3]
        factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        outfile = str(tmp_path / 'output_gw.dat')

        write_gw_file(outfile, gw_lines, 2, parnodes, parvals, factors, parvals_d)

        assert os.path.getsize(outfile) > 0

    def test_writes_factors(self, tmp_path):
        """Test that factors are written to output file."""
        from iwfm.calib.params2gw import write_gw_file

        gw_lines = self.create_mock_gw_lines()
        parvals_d = self.create_mock_parvals_d()
        parvals = self.create_mock_parvals()
        parnodes = [1, 2, 3]
        factors = [2.5, 3.5, 4.5, 5.5, 6.5, 7.5]  # Distinctive values
        outfile = str(tmp_path / 'output_gw.dat')

        write_gw_file(outfile, gw_lines, 2, parnodes, parvals, factors, parvals_d)

        with open(outfile, 'r') as f:
            content = f.read()

        # Check that factors are in the file
        assert '2.5' in content
        assert '7.5' in content

    def test_uses_default_values_when_negative(self, tmp_path):
        """Test that default values from parvals_d are used when parvals < 0."""
        from iwfm.calib.params2gw import write_gw_file

        gw_lines = self.create_mock_gw_lines(num_nodes=1, num_layers=1)
        parvals_d = self.create_mock_parvals_d(num_nodes=1, num_layers=1)
        # Set default PKH to distinctive value
        parvals_d['1_1'][0] = 999.0
        
        # Create parvals with negative PKH (should use default)
        parvals = []
        for ptype in range(5):
            if ptype == 0:  # PKH is negative
                parvals.append([[-1.0]])
            else:
                parvals.append([[50.0]])
        
        parnodes = [1]
        factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        outfile = str(tmp_path / 'output_gw.dat')

        write_gw_file(outfile, gw_lines, 1, parnodes, parvals, factors, parvals_d)

        with open(outfile, 'r') as f:
            content = f.read()

        # Should use default value 999.0 for PKH
        assert '999.0' in content

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.params2gw import write_gw_file
        import inspect
        
        sig = inspect.signature(write_gw_file)
        params = list(sig.parameters.keys())
        
        assert 'outfile' in params
        assert 'gw_lines' in params
        assert 'nlay' in params
        assert 'parnodes' in params
        assert 'parvals' in params
        assert 'fp' in params
        assert 'parvals_d' in params
        assert 'verbose' in params


class TestReadGwFileStructure:
    """Tests for read_gw_file function structure (without running full function)."""

    def test_function_exists(self):
        """Test that read_gw_file function exists."""
        from iwfm.calib.params2gw import read_gw_file
        assert callable(read_gw_file)

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.params2gw import read_gw_file
        import inspect
        
        sig = inspect.signature(read_gw_file)
        params = list(sig.parameters.keys())
        
        assert 'gw_file' in params
        assert 'verbose' in params

    def test_verbose_default_false(self):
        """Test that verbose parameter defaults to False."""
        from iwfm.calib.params2gw import read_gw_file
        import inspect
        
        sig = inspect.signature(read_gw_file)
        
        assert sig.parameters['verbose'].default == False

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.params2gw import read_gw_file
        
        assert read_gw_file.__doc__ is not None
        assert 'factors' in read_gw_file.__doc__


class TestReadParamsStructure:
    """Tests for read_params function structure (without running - uses input())."""

    def test_function_exists(self):
        """Test that read_params function exists."""
        from iwfm.calib.params2gw import read_params
        assert callable(read_params)

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.params2gw import read_params
        import inspect
        
        sig = inspect.signature(read_params)
        params = list(sig.parameters.keys())
        
        assert 'param_types' in params
        assert 'verbose' in params

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.params2gw import read_params
        
        assert read_params.__doc__ is not None


class TestParams2GwImports:
    """Tests for module imports."""

    def test_import_read_gw_file(self):
        """Test import of read_gw_file."""
        from iwfm.calib.params2gw import read_gw_file
        assert callable(read_gw_file)

    def test_import_read_params(self):
        """Test import of read_params."""
        from iwfm.calib.params2gw import read_params
        assert callable(read_params)

    def test_import_write_gw_file(self):
        """Test import of write_gw_file."""
        from iwfm.calib.params2gw import write_gw_file
        assert callable(write_gw_file)

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import params2gw
        assert hasattr(params2gw, 'read_gw_file')
        assert hasattr(params2gw, 'read_params')
        assert hasattr(params2gw, 'write_gw_file')


class TestWriteGwFileEdgeCases:
    """Edge case tests for write_gw_file."""

    def create_minimal_gw_lines(self):
        """Create minimal groundwater file lines."""
        lines = []
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
        lines.append('  1.0  1.0  1.0  1.0  1.0  1.0')
        lines.append('C  Comment')
        lines.append('  time_units')
        lines.append('C  Comment')
        lines.append('  1  10.0  1E-5  0.15  1E-6  10.0')
        lines.append('C  End')
        return lines

    def test_single_node_single_layer(self, tmp_path):
        """Test with single node and single layer."""
        from iwfm.calib.params2gw import write_gw_file

        gw_lines = self.create_minimal_gw_lines()
        parvals_d = {'1_1': [10.0, 1e-5, 0.15, 1e-6, 10.0]}
        parvals = [[[20.0]], [[2e-5]], [[0.20]], [[2e-6]], [[20.0]]]
        parnodes = [1]
        factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        outfile = str(tmp_path / 'output.dat')

        write_gw_file(outfile, gw_lines, 1, parnodes, parvals, factors, parvals_d)

        assert os.path.exists(outfile)

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output (currently write_gw_file doesn't print anything)."""
        from iwfm.calib.params2gw import write_gw_file

        gw_lines = self.create_minimal_gw_lines()
        parvals_d = {'1_1': [10.0, 1e-5, 0.15, 1e-6, 10.0]}
        parvals = [[[20.0]], [[2e-5]], [[0.20]], [[2e-6]], [[20.0]]]
        parnodes = [1]
        factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        outfile = str(tmp_path / 'output.dat')

        # Should not raise error with verbose=True
        write_gw_file(outfile, gw_lines, 1, parnodes, parvals, factors, parvals_d, verbose=True)

        assert os.path.exists(outfile)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
