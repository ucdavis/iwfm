# test_calib_ppk2fac_trans.py
# Unit tests for calib/ppk2fac_trans.py - Translate sequential to actual node numbers
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


class TestPpk2FacTrans:
    """Tests for ppk2fac_trans function"""

    def create_factors_file(self, tmp_path, pp_file_name, num_nodes, num_params, node_ids):
        """Create a mock ppk2fac factors file.
        
        Format:
        - Line 1: pilot points file name
        - Line 2: number of nodes
        - Line 3: number of parameters (pilot points)
        - Next num_params lines: parameter names
        - Then for each node: 3 lines of factor data
        """
        factors_file = tmp_path / 'factors.fac'
        
        lines = []
        lines.append(pp_file_name)
        lines.append(f'          {num_nodes}')
        lines.append(f'          {num_params}')
        
        # Parameter names
        for i in range(num_params):
            lines.append(f'PP{i+1:03d}')
        
        # Node factor lines (3 lines per node)
        for node_id in node_ids:
            lines.append(f'          {node_id}           1           3  0.0000000E+00          1 0.5')
            lines.append(f'          2 0.3           3 0.2')
            lines.append(f'')  # Empty line or continuation
        
        factors_file.write_text('\n'.join(lines))
        return str(factors_file)

    def create_trans_file(self, tmp_path, translations):
        """Create a translation file.
        
        Format: sequential_id  actual_id
        
        Parameters
        ----------
        translations : list of tuples
            Each tuple is (sequential_id, actual_id)
        """
        trans_file = tmp_path / 'trans.dat'
        
        lines = []
        for seq_id, actual_id in translations:
            lines.append(f'{seq_id}  {actual_id}')
        
        trans_file.write_text('\n'.join(lines))
        return str(trans_file)

    def test_creates_output_file(self, tmp_path):
        """Test that output file is created."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans

        factors_file = self.create_factors_file(
            tmp_path, 'pp.dat', num_nodes=2, num_params=3, node_ids=[1, 2]
        )
        trans_file = self.create_trans_file(tmp_path, [('1', '101'), ('2', '102')])
        out_file = str(tmp_path / 'output.fac')

        ppk2fac_trans(factors_file, trans_file, out_file)

        assert os.path.exists(out_file)

    def test_output_file_has_content(self, tmp_path):
        """Test that output file has content."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans

        factors_file = self.create_factors_file(
            tmp_path, 'pp.dat', num_nodes=2, num_params=3, node_ids=[1, 2]
        )
        trans_file = self.create_trans_file(tmp_path, [('1', '101'), ('2', '102')])
        out_file = str(tmp_path / 'output.fac')

        ppk2fac_trans(factors_file, trans_file, out_file)

        assert os.path.getsize(out_file) > 0

    def test_translates_node_ids(self, tmp_path):
        """Test that sequential node IDs are translated to actual IDs."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans

        factors_file = self.create_factors_file(
            tmp_path, 'pp.dat', num_nodes=2, num_params=3, node_ids=[1, 2]
        )
        trans_file = self.create_trans_file(tmp_path, [('1', '999'), ('2', '888')])
        out_file = str(tmp_path / 'output.fac')

        ppk2fac_trans(factors_file, trans_file, out_file)

        with open(out_file, 'r') as f:
            content = f.read()

        # Should contain translated IDs
        assert '999' in content
        assert '888' in content

    def test_preserves_header(self, tmp_path):
        """Test that header information is preserved."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans

        factors_file = self.create_factors_file(
            tmp_path, 'my_pilot_points.dat', num_nodes=1, num_params=3, node_ids=[1]
        )
        trans_file = self.create_trans_file(tmp_path, [('1', '101')])
        out_file = str(tmp_path / 'output.fac')

        ppk2fac_trans(factors_file, trans_file, out_file)

        with open(out_file, 'r') as f:
            content = f.read()

        assert 'my_pilot_points.dat' in content

    def test_preserves_parameter_names(self, tmp_path):
        """Test that parameter names are preserved."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans

        factors_file = self.create_factors_file(
            tmp_path, 'pp.dat', num_nodes=1, num_params=3, node_ids=[1]
        )
        trans_file = self.create_trans_file(tmp_path, [('1', '101')])
        out_file = str(tmp_path / 'output.fac')

        ppk2fac_trans(factors_file, trans_file, out_file)

        with open(out_file, 'r') as f:
            content = f.read()

        assert 'PP001' in content
        assert 'PP002' in content
        assert 'PP003' in content

    def test_skips_comment_lines(self, tmp_path):
        """Test that comment lines are skipped in input files."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans

        # Create factors file with comments
        factors_file = tmp_path / 'factors.fac'
        content = """# Comment line
pp.dat
          1
          3
PP001
PP002
PP003
          1           1           3  0.0000000E+00          1 0.5
          2 0.3           3 0.2

"""
        factors_file.write_text(content)

        # Create trans file with comments
        trans_file = tmp_path / 'trans.dat'
        trans_content = """# Comment
C Another comment
1  101
"""
        trans_file.write_text(trans_content)

        out_file = str(tmp_path / 'output.fac')

        ppk2fac_trans(str(factors_file), str(trans_file), out_file)

        assert os.path.exists(out_file)

    def test_many_nodes(self, tmp_path):
        """Test with many nodes."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans

        num_nodes = 50
        node_ids = list(range(1, num_nodes + 1))
        translations = [(str(i), str(i + 1000)) for i in node_ids]

        factors_file = self.create_factors_file(
            tmp_path, 'pp.dat', num_nodes=num_nodes, num_params=3, node_ids=node_ids
        )
        trans_file = self.create_trans_file(tmp_path, translations)
        out_file = str(tmp_path / 'output.fac')

        ppk2fac_trans(factors_file, trans_file, out_file)

        assert os.path.exists(out_file)

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans

        factors_file = self.create_factors_file(
            tmp_path, 'pp.dat', num_nodes=1, num_params=3, node_ids=[1]
        )
        trans_file = self.create_trans_file(tmp_path, [('1', '101')])
        out_file = str(tmp_path / 'output.fac')

        ppk2fac_trans(factors_file, trans_file, out_file, verbose=True)

        captured = capsys.readouterr()
        assert 'Read' in captured.out
        assert 'Wrote' in captured.out

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans
        import inspect
        
        sig = inspect.signature(ppk2fac_trans)
        params = list(sig.parameters.keys())
        
        assert 'factors_file' in params
        assert 'trans_file' in params
        assert 'out_file' in params
        assert 'verbose' in params

    def test_verbose_default_false(self):
        """Test that verbose parameter defaults to False."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans
        import inspect
        
        sig = inspect.signature(ppk2fac_trans)
        
        assert sig.parameters['verbose'].default == False


class TestPpk2FacTransImports:
    """Tests for module imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import ppk2fac_trans
        assert callable(ppk2fac_trans)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans
        assert callable(ppk2fac_trans)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.ppk2fac_trans import ppk2fac_trans
        
        assert ppk2fac_trans.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
