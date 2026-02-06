# test_calib_ppk2fac.py
# Unit tests for calib/ppk2fac.py - Calculate IDW factors from pilot points to nodes
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
import numpy as np
import os


class TestReadPpFile:
    """Tests for read_pp_file function"""

    def create_pp_file(self, tmp_path, pilot_points):
        """Create a mock pilot points file.
        
        Parameters
        ----------
        pilot_points : list of tuples
            Each tuple is (id, x, y)
        """
        pp_file = tmp_path / 'pilot_points.dat'
        lines = []
        for pp in pilot_points:
            pp_id, x, y = pp
            lines.append(f'{pp_id}  {x}  {y}')
        pp_file.write_text('\n'.join(lines))
        return str(pp_file)

    def test_returns_two_items(self, tmp_path):
        """Test that function returns pp_coord and pp_list."""
        from iwfm.calib.ppk2fac import read_pp_file

        pp_file = self.create_pp_file(tmp_path, [
            ('PP001', 100.0, 200.0),
        ])

        result = read_pp_file(pp_file)

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_pp_coord_is_numpy_array(self, tmp_path):
        """Test that pp_coord is a numpy array."""
        from iwfm.calib.ppk2fac import read_pp_file

        pp_file = self.create_pp_file(tmp_path, [
            ('PP001', 100.0, 200.0),
        ])

        pp_coord, pp_list = read_pp_file(pp_file)

        assert isinstance(pp_coord, np.ndarray)

    def test_pp_list_contains_ids(self, tmp_path):
        """Test that pp_list contains pilot point IDs."""
        from iwfm.calib.ppk2fac import read_pp_file

        pp_file = self.create_pp_file(tmp_path, [
            ('PP001', 100.0, 200.0),
            ('PP002', 300.0, 400.0),
        ])

        pp_coord, pp_list = read_pp_file(pp_file)

        assert 'PP001' in pp_list
        assert 'PP002' in pp_list

    def test_coordinates_extracted_correctly(self, tmp_path):
        """Test that coordinates are extracted correctly."""
        from iwfm.calib.ppk2fac import read_pp_file

        pp_file = self.create_pp_file(tmp_path, [
            ('PP001', 123.45, 678.90),
        ])

        pp_coord, pp_list = read_pp_file(pp_file)

        assert np.isclose(pp_coord[0, 0], 123.45)
        assert np.isclose(pp_coord[0, 1], 678.90)

    def test_skips_comment_lines(self, tmp_path):
        """Test that lines starting with # are skipped."""
        from iwfm.calib.ppk2fac import read_pp_file

        pp_file = tmp_path / 'pp.dat'
        content = """# This is a comment
# Another comment
PP001  100.0  200.0
PP002  300.0  400.0
"""
        pp_file.write_text(content)

        pp_coord, pp_list = read_pp_file(str(pp_file))

        assert len(pp_list) == 2

    def test_multiple_pilot_points(self, tmp_path):
        """Test with multiple pilot points."""
        from iwfm.calib.ppk2fac import read_pp_file

        pilot_points = [(f'PP{i:03d}', float(i * 100), float(i * 200)) for i in range(10)]
        pp_file = self.create_pp_file(tmp_path, pilot_points)

        pp_coord, pp_list = read_pp_file(pp_file)

        assert len(pp_list) == 10
        assert pp_coord.shape == (10, 2)


class TestPar2FacIdw2:
    """Tests for par2fac_idw2 function"""

    def test_returns_two_lists(self):
        """Test that function returns ppoints and weights."""
        from iwfm.calib.ppk2fac import par2fac_idw2

        pp_coord = np.array([
            [0.0, 0.0],
            [10.0, 0.0],
            [0.0, 10.0],
            [10.0, 10.0],
        ])
        node_coord = np.array([[5.0, 5.0]])

        ppoints, weights = par2fac_idw2(pp_coord, node_coord)

        assert isinstance(ppoints, list)
        assert isinstance(weights, list)

    def test_returns_correct_length(self):
        """Test that result length matches number of nodes."""
        from iwfm.calib.ppk2fac import par2fac_idw2

        pp_coord = np.array([
            [0.0, 0.0],
            [10.0, 0.0],
            [0.0, 10.0],
            [10.0, 10.0],
        ])
        node_coord = np.array([
            [5.0, 5.0],
            [2.0, 2.0],
            [8.0, 8.0],
        ])

        ppoints, weights = par2fac_idw2(pp_coord, node_coord)

        assert len(ppoints) == 3
        assert len(weights) == 3

    def test_n_ppoints_returned(self):
        """Test that n_ppoints pilot points are returned per node."""
        from iwfm.calib.ppk2fac import par2fac_idw2

        pp_coord = np.array([
            [0.0, 0.0],
            [10.0, 0.0],
            [0.0, 10.0],
            [10.0, 10.0],
            [5.0, 5.0],
        ])
        node_coord = np.array([[2.0, 2.0]])

        ppoints, weights = par2fac_idw2(pp_coord, node_coord, n_ppoints=3)

        assert len(ppoints[0]) == 3
        assert len(weights[0]) == 3

    def test_weights_sum_to_one(self):
        """Test that weights are normalized to sum to 1."""
        from iwfm.calib.ppk2fac import par2fac_idw2

        pp_coord = np.array([
            [0.0, 0.0],
            [10.0, 0.0],
            [0.0, 10.0],
            [10.0, 10.0],
        ])
        node_coord = np.array([[5.0, 5.0]])

        ppoints, weights = par2fac_idw2(pp_coord, node_coord)

        assert np.isclose(sum(weights[0]), 1.0)

    def test_closer_points_have_higher_weights(self):
        """Test that closer pilot points get higher weights."""
        from iwfm.calib.ppk2fac import par2fac_idw2

        pp_coord = np.array([
            [1.0, 0.0],   # Close to node
            [10.0, 0.0],  # Far from node
            [100.0, 0.0], # Very far from node
        ])
        node_coord = np.array([[0.0, 0.0]])

        ppoints, weights = par2fac_idw2(pp_coord, node_coord, n_ppoints=3)

        # Closest point (index 0) should have highest weight
        assert weights[0][0] > weights[0][1]
        assert weights[0][1] > weights[0][2]

    def test_ppoints_are_zero_indexed(self):
        """Test that pilot point indices are zero-indexed."""
        from iwfm.calib.ppk2fac import par2fac_idw2

        pp_coord = np.array([
            [0.0, 0.0],
            [10.0, 0.0],
            [0.0, 10.0],
        ])
        node_coord = np.array([[0.0, 0.0]])  # At first pilot point

        ppoints, weights = par2fac_idw2(pp_coord, node_coord, n_ppoints=3)

        # Indices should be 0, 1, or 2
        for pp in ppoints[0]:
            assert 0 <= pp <= 2

    def test_inverse_distance_squared(self):
        """Test that weights follow inverse distance squared."""
        from iwfm.calib.ppk2fac import par2fac_idw2

        # Node at origin, pilot points at distances 1 and 2
        pp_coord = np.array([
            [1.0, 0.0],   # Distance 1
            [2.0, 0.0],   # Distance 2
            [4.0, 0.0],   # Distance 4
        ])
        node_coord = np.array([[0.0, 0.0]])

        ppoints, weights = par2fac_idw2(pp_coord, node_coord, n_ppoints=3)

        # Weights should be proportional to 1/d²
        # 1/1² = 1, 1/2² = 0.25, 1/4² = 0.0625
        # Normalized: 1/1.3125 ≈ 0.762, 0.25/1.3125 ≈ 0.190, 0.0625/1.3125 ≈ 0.048
        w1, w2, w3 = weights[0][0], weights[0][1], weights[0][2]
        
        # Ratio w1/w2 should be (1/1²)/(1/2²) = 4
        assert np.isclose(w1 / w2, 4.0, rtol=0.01)


class TestWriteFactors:
    """Tests for write_factors function"""

    def test_creates_output_file(self, tmp_path):
        """Test that output file is created."""
        from iwfm.calib.ppk2fac import write_factors

        outfile = str(tmp_path / 'factors.out')
        pp_file = 'pilot_points.dat'
        pp_list = ['PP001', 'PP002', 'PP003']
        node_list = [1, 2]
        ppoints = [[0, 1, 2], [1, 2, 0]]
        weights = [[0.5, 0.3, 0.2], [0.4, 0.4, 0.2]]

        write_factors(outfile, pp_file, pp_list, node_list, ppoints, weights, verbose=False)

        assert os.path.exists(outfile)

    def test_writes_header_info(self, tmp_path):
        """Test that header information is written."""
        from iwfm.calib.ppk2fac import write_factors

        outfile = str(tmp_path / 'factors.out')
        pp_file = 'my_pilot_points.dat'
        pp_list = ['PP001', 'PP002', 'PP003']
        node_list = [1]
        ppoints = [[0, 1, 2]]
        weights = [[0.5, 0.3, 0.2]]

        write_factors(outfile, pp_file, pp_list, node_list, ppoints, weights, verbose=False)

        with open(outfile, 'r') as f:
            content = f.read()

        assert 'my_pilot_points.dat' in content

    def test_writes_pilot_point_count(self, tmp_path):
        """Test that pilot point count is written."""
        from iwfm.calib.ppk2fac import write_factors

        outfile = str(tmp_path / 'factors.out')
        pp_list = ['PP001', 'PP002', 'PP003', 'PP004', 'PP005']
        node_list = [1]
        ppoints = [[0, 1, 2]]
        weights = [[0.5, 0.3, 0.2]]

        write_factors(outfile, 'pp.dat', pp_list, node_list, ppoints, weights, verbose=False)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        # Third line should have pilot point count
        assert '5' in lines[2]

    def test_returns_count(self, tmp_path):
        """Test that function returns count of nodes written."""
        from iwfm.calib.ppk2fac import write_factors

        outfile = str(tmp_path / 'factors.out')
        pp_list = ['PP001', 'PP002', 'PP003']
        node_list = [1, 2, 3, 4, 5]
        ppoints = [[0, 1, 2]] * 5
        weights = [[0.5, 0.3, 0.2]] * 5

        count = write_factors(outfile, 'pp.dat', pp_list, node_list, ppoints, weights, verbose=False)

        assert count == 5


class TestPpk2FacImports:
    """Tests for module imports."""

    def test_import_read_pp_file(self):
        """Test import of read_pp_file."""
        from iwfm.calib.ppk2fac import read_pp_file
        assert callable(read_pp_file)

    def test_import_par2fac_idw2(self):
        """Test import of par2fac_idw2."""
        from iwfm.calib.ppk2fac import par2fac_idw2
        assert callable(par2fac_idw2)

    def test_import_write_factors(self):
        """Test import of write_factors."""
        from iwfm.calib.ppk2fac import write_factors
        assert callable(write_factors)

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import ppk2fac
        assert hasattr(ppk2fac, 'read_pp_file')
        assert hasattr(ppk2fac, 'par2fac_idw2')
        assert hasattr(ppk2fac, 'write_factors')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
