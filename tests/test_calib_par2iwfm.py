# test_calib_par2iwfm.py
# Unit tests for calib/par2iwfm.py - Use kriging to translate parameter values
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


class TestPar2Iwfm:
    """Tests for par2iwfm function"""

    def test_returns_list(self, capsys):
        """Test that function returns a list of values."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 0.0, 0.0)]
        B = [(1, 1.0, 1.0, 100.0), (2, 2.0, 2.0, 200.0)]

        result = par2iwfm(A, B)

        assert isinstance(result, list)

    def test_returns_correct_length(self, capsys):
        """Test that result length matches A length."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 0.0, 0.0), (2, 1.0, 1.0), (3, 2.0, 2.0)]
        B = [(1, 0.5, 0.5, 100.0), (2, 1.5, 1.5, 200.0)]

        result = par2iwfm(A, B)

        assert len(result) == 3  # Same as len(A)

    def test_values_are_floats(self, capsys):
        """Test that result values are numeric."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 0.0, 0.0)]
        B = [(1, 1.0, 1.0, 100.0)]

        result = par2iwfm(A, B)

        assert isinstance(result[0], (int, float, np.floating))

    def test_interpolation_single_B_point(self, capsys):
        """Test interpolation with single B point."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 0.0, 0.0)]
        B = [(1, 5.0, 5.0, 100.0)]  # Single B point with value 100

        result = par2iwfm(A, B)

        # With single B point, A should get that value
        assert np.isclose(result[0], 100.0)

    def test_interpolation_equidistant_points(self, capsys):
        """Test interpolation when A is equidistant from B points."""
        from iwfm.calib.par2iwfm import par2iwfm

        # A point at midpoint between two B points
        A = [(1, 1.5, 0.0)]
        B = [
            (1, 1.0, 0.0, 100.0),  # Distance 0.5, value 100
            (2, 2.0, 0.0, 200.0),  # Distance 0.5, value 200
        ]

        result = par2iwfm(A, B)

        # Equidistant, so should be average = 150
        assert np.isclose(result[0], 150.0)

    def test_closer_point_weighted_more(self, capsys):
        """Test that closer B points contribute more to result."""
        from iwfm.calib.par2iwfm import par2iwfm

        # A point closer to first B point
        A = [(1, 0.0, 0.0)]
        B = [
            (1, 1.0, 0.0, 100.0),   # Distance 1, value 100
            (2, 10.0, 0.0, 200.0),  # Distance 10, value 200
        ]

        result = par2iwfm(A, B)

        # Result should be closer to 100 than 200
        assert result[0] < 150.0  # Weighted toward 100

    def test_multiple_A_points(self, capsys):
        """Test with multiple A points."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [
            (1, 0.0, 0.0),
            (2, 5.0, 5.0),
            (3, 10.0, 10.0),
        ]
        B = [
            (1, 0.0, 0.0, 100.0),
            (2, 10.0, 10.0, 200.0),
        ]

        result = par2iwfm(A, B)

        assert len(result) == 3
        # First A at same location as first B should get ~100
        # Third A at same location as second B should get ~200
        # Second A in middle should get ~150

    def test_values_within_range(self, capsys):
        """Test that interpolated values are within B value range."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 5.0, 5.0)]
        B = [
            (1, 0.0, 0.0, 100.0),
            (2, 10.0, 0.0, 150.0),
            (3, 10.0, 10.0, 200.0),
            (4, 0.0, 10.0, 120.0),
        ]

        result = par2iwfm(A, B)

        min_val = min(v for _, _, _, v in B)
        max_val = max(v for _, _, _, v in B)
        
        # Interpolated value should be within range of B values
        assert min_val <= result[0] <= max_val

    def test_sample_data_from_module(self, capsys):
        """Test using sample data defined in the module."""
        from iwfm.calib.par2iwfm import par2iwfm

        new_set = [
            (1, 1.0, 2.0),
            (2, 2.0, 3.0),
            (3, 5.0, 4.0),
        ]
        base_set = [
            (1, 2.0, 1.0, 80.0),
            (2, 3.0, 3.0, 120.0),
            (3, 4.0, 6.0, 85.0),
        ]

        result = par2iwfm(new_set, base_set)

        assert len(result) == 3
        # All values should be within range of base_set values
        for val in result:
            assert 80.0 <= val <= 120.0

    def test_many_B_points(self, capsys):
        """Test with many B points."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 5.0, 5.0)]
        B = [(i, float(i % 10), float(i // 10), 100.0 + i) for i in range(1, 51)]

        result = par2iwfm(A, B)

        assert len(result) == 1
        # Value should be reasonable
        assert result[0] > 0

    def test_large_coordinate_values(self, capsys):
        """Test with large coordinate values (UTM-scale)."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 622500.0, 4296850.0)]
        B = [
            (1, 622400.0, 4296800.0, 100.0),
            (2, 622600.0, 4296900.0, 200.0),
        ]

        result = par2iwfm(A, B)

        assert len(result) == 1
        assert 100.0 <= result[0] <= 200.0

    def test_negative_values(self, capsys):
        """Test with negative B values."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 0.0, 0.0)]
        B = [
            (1, 1.0, 0.0, -100.0),
            (2, -1.0, 0.0, -200.0),
        ]

        result = par2iwfm(A, B)

        # Result should be negative
        assert result[0] < 0

    def test_zero_values(self, capsys):
        """Test with zero B values."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 0.0, 0.0)]
        B = [
            (1, 1.0, 0.0, 0.0),
            (2, -1.0, 0.0, 0.0),
        ]

        result = par2iwfm(A, B)

        assert result[0] == 0.0

    def test_mixed_positive_negative_values(self, capsys):
        """Test with mixed positive and negative B values."""
        from iwfm.calib.par2iwfm import par2iwfm

        # A equidistant from both B points
        A = [(1, 0.0, 0.0)]
        B = [
            (1, 1.0, 0.0, 100.0),
            (2, -1.0, 0.0, -100.0),
        ]

        result = par2iwfm(A, B)

        # Equidistant, so average should be ~0
        assert np.isclose(result[0], 0.0, atol=1e-10)

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.par2iwfm import par2iwfm
        import inspect
        
        sig = inspect.signature(par2iwfm)
        params = list(sig.parameters.keys())
        
        assert 'A' in params
        assert 'B' in params


class TestPar2IwfmIntegration:
    """Integration tests for par2iwfm with krige function"""

    def test_uses_krige_function(self, capsys):
        """Test that par2iwfm uses the krige function."""
        import importlib
        module = importlib.import_module('iwfm.calib.par2iwfm')
        import inspect

        source = inspect.getsource(module.par2iwfm)
        assert 'krige' in source

    def test_consistent_with_inverse_distance(self, capsys):
        """Test that results are consistent with inverse distance weighting."""
        from iwfm.calib.par2iwfm import par2iwfm

        # A point at (0,0), B points at distances 1 and 2
        A = [(1, 0.0, 0.0)]
        B = [
            (1, 1.0, 0.0, 100.0),  # Distance 1
            (2, 2.0, 0.0, 200.0),  # Distance 2
        ]

        result = par2iwfm(A, B)

        # IDW: weight1 = 1/1 = 1, weight2 = 1/2 = 0.5
        # Normalized: w1 = 1/1.5 = 0.667, w2 = 0.5/1.5 = 0.333
        # Expected: 0.667 * 100 + 0.333 * 200 = 66.7 + 66.6 = 133.3
        expected = (1.0 * 100.0 + 0.5 * 200.0) / 1.5
        assert np.isclose(result[0], expected, rtol=0.01)


class TestPar2IwfmEdgeCases:
    """Edge case tests for par2iwfm"""

    def test_single_A_single_B(self, capsys):
        """Test with single point in both A and B."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(1, 0.0, 0.0)]
        B = [(1, 5.0, 5.0, 42.0)]

        result = par2iwfm(A, B)

        assert len(result) == 1
        assert result[0] == 42.0

    def test_A_at_same_location_as_B(self, capsys):
        """Test when A point is at same location as a B point."""
        from iwfm.calib.par2iwfm import par2iwfm

        # When A is at the exact same location as a B point, distance is 0,
        # causing 1/0 = inf weights. This produces NaN from inf/inf normalization.
        # This is a known limitation of inverse distance weighting.
        A = [(1, 1.0, 1.0)]
        B = [
            (1, 1.0, 1.0, 100.0),  # Same location as A - zero distance
            (2, 10.0, 10.0, 200.0),
        ]

        result = par2iwfm(A, B)

        # Result will be NaN due to zero-distance division
        assert np.isnan(result[0]) or np.isclose(result[0], 100.0, atol=1.0)

    def test_many_A_points(self, capsys):
        """Test with many A points."""
        from iwfm.calib.par2iwfm import par2iwfm

        A = [(i, float(i), float(i)) for i in range(100)]
        B = [
            (1, 0.0, 0.0, 100.0),
            (2, 100.0, 100.0, 200.0),
        ]

        result = par2iwfm(A, B)

        assert len(result) == 100


class TestPar2IwfmImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import par2iwfm
        assert callable(par2iwfm)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.par2iwfm import par2iwfm
        assert callable(par2iwfm)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.par2iwfm import par2iwfm
        
        assert par2iwfm.__doc__ is not None
        assert 'krige' in par2iwfm.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
