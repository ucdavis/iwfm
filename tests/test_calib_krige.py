# test_calib_krige.py
# Unit tests for calib/krige.py - Spatial interpolation using kriging factors
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


class TestKrige:
    """Tests for krige function"""

    def test_returns_list(self, capsys):
        """Test that function returns a list of kriging factors."""
        from iwfm.calib.krige import krige

        A = [(1, 0.0, 0.0)]
        B = [(1, 1.0, 1.0, 100.0), (2, 2.0, 2.0, 200.0)]

        result = krige(A, B)

        assert isinstance(result, list)

    def test_returns_list_of_lists(self, capsys):
        """Test that function returns a list of lists (one per A point)."""
        from iwfm.calib.krige import krige

        A = [(1, 0.0, 0.0), (2, 1.0, 1.0)]
        B = [(1, 2.0, 2.0, 100.0), (2, 3.0, 3.0, 200.0)]

        result = krige(A, B)

        assert len(result) == 2  # One list per A point
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)

    def test_weights_length_matches_B(self, capsys):
        """Test that each weight list has same length as B."""
        from iwfm.calib.krige import krige

        A = [(1, 0.0, 0.0)]
        B = [(1, 1.0, 1.0, 100.0), (2, 2.0, 2.0, 200.0), (3, 3.0, 3.0, 300.0)]

        result = krige(A, B)

        assert len(result[0]) == 3  # Same as len(B)

    def test_weights_sum_to_one(self, capsys):
        """Test that kriging weights sum to 1.0 (normalized)."""
        from iwfm.calib.krige import krige

        A = [(1, 0.0, 0.0)]
        B = [
            (1, 1.0, 1.0, 100.0),
            (2, 2.0, 2.0, 200.0),
            (3, 3.0, 3.0, 300.0),
        ]

        result = krige(A, B)

        assert np.isclose(sum(result[0]), 1.0)

    def test_closer_points_have_higher_weights(self, capsys):
        """Test that closer B points get higher weights (inverse distance)."""
        from iwfm.calib.krige import krige

        # A point at origin
        A = [(1, 0.0, 0.0)]
        # B points at different distances
        B = [
            (1, 1.0, 0.0, 100.0),   # Distance 1
            (2, 10.0, 0.0, 200.0),  # Distance 10
        ]

        result = krige(A, B)

        # First B point (closer) should have higher weight
        assert result[0][0] > result[0][1]

    def test_equidistant_points_equal_weights(self, capsys):
        """Test that equidistant B points get equal weights."""
        from iwfm.calib.krige import krige

        # A point at origin
        A = [(1, 0.0, 0.0)]
        # B points equidistant from A
        B = [
            (1, 1.0, 0.0, 100.0),   # Distance 1
            (2, 0.0, 1.0, 200.0),   # Distance 1
            (3, -1.0, 0.0, 300.0),  # Distance 1
        ]

        result = krige(A, B)

        # All weights should be equal
        assert np.isclose(result[0][0], result[0][1])
        assert np.isclose(result[0][1], result[0][2])

    def test_multiple_A_points(self, capsys):
        """Test with multiple points in A grid."""
        from iwfm.calib.krige import krige

        A = [
            (1, 0.0, 0.0),
            (2, 5.0, 5.0),
            (3, 10.0, 10.0),
        ]
        B = [
            (1, 1.0, 1.0, 100.0),
            (2, 6.0, 6.0, 200.0),
        ]

        result = krige(A, B)

        assert len(result) == 3  # One list per A point
        # Each A point should have 2 weights (for 2 B points)
        for weights in result:
            assert len(weights) == 2
            assert np.isclose(sum(weights), 1.0)

    def test_single_B_point(self, capsys):
        """Test with single B point (all weight goes to it)."""
        from iwfm.calib.krige import krige

        A = [(1, 0.0, 0.0)]
        B = [(1, 5.0, 5.0, 100.0)]

        result = krige(A, B)

        # Only one B point, so it gets all the weight
        assert len(result[0]) == 1
        assert result[0][0] == 1.0

    def test_many_B_points(self, capsys):
        """Test with many B points."""
        from iwfm.calib.krige import krige

        A = [(1, 0.0, 0.0)]
        B = [(i, float(i), float(i), 100.0) for i in range(1, 51)]  # 50 points

        result = krige(A, B)

        assert len(result[0]) == 50
        assert np.isclose(sum(result[0]), 1.0)

    def test_weights_are_positive(self, capsys):
        """Test that all weights are positive."""
        from iwfm.calib.krige import krige

        A = [(1, 5.0, 5.0)]
        B = [
            (1, 0.0, 0.0, 100.0),
            (2, 10.0, 10.0, 200.0),
            (3, 0.0, 10.0, 300.0),
        ]

        result = krige(A, B)

        for weight in result[0]:
            assert weight > 0

    def test_sample_data_from_module(self, capsys):
        """Test using the sample data defined in the module."""
        from iwfm.calib.krige import krige

        # Sample data from the module
        new_points = [
            (1, 1.0, 2.0),
            (2, 2.0, 3.0),
            (3, 5.0, 4.0),
        ]
        base_points = [
            (1, 2.0, 1.0, 80.0),
            (2, 3.0, 3.0, 120.0),
            (3, 4.0, 6.0, 85.0),
        ]

        result = krige(new_points, base_points)

        assert len(result) == 3
        for weights in result:
            assert len(weights) == 3
            assert np.isclose(sum(weights), 1.0)

    def test_inverse_distance_weighting(self, capsys):
        """Test that weights follow inverse distance relationship."""
        from iwfm.calib.krige import krige

        # A point at origin
        A = [(1, 0.0, 0.0)]
        # B points at distances 1, 2, 4
        B = [
            (1, 1.0, 0.0, 100.0),   # Distance 1
            (2, 2.0, 0.0, 200.0),   # Distance 2
            (3, 4.0, 0.0, 300.0),   # Distance 4
        ]

        result = krige(A, B)

        # Weight ratios should be inversely proportional to distance
        # w1/w2 should be approximately 2 (d2/d1)
        # w1/w3 should be approximately 4 (d3/d1)
        w1, w2, w3 = result[0]
        assert np.isclose(w1 / w2, 2.0, rtol=0.01)
        assert np.isclose(w1 / w3, 4.0, rtol=0.01)

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.krige import krige
        import inspect
        
        sig = inspect.signature(krige)
        params = list(sig.parameters.keys())
        
        assert 'A' in params
        assert 'B' in params


class TestKrigeEdgeCases:
    """Edge case tests for krige function"""

    def test_large_coordinate_values(self, capsys):
        """Test with large coordinate values (e.g., UTM)."""
        from iwfm.calib.krige import krige

        A = [(1, 622426.0, 4296803.0)]
        B = [
            (1, 622426.0, 4296903.0, 100.0),  # 100m away
            (2, 622526.0, 4296803.0, 200.0),  # 100m away
        ]

        result = krige(A, B)

        # Both should have equal weights (equidistant)
        assert np.isclose(result[0][0], result[0][1], rtol=0.01)
        assert np.isclose(sum(result[0]), 1.0)

    def test_small_distances(self, capsys):
        """Test with very small distances."""
        from iwfm.calib.krige import krige

        A = [(1, 0.0, 0.0)]
        B = [
            (1, 0.001, 0.0, 100.0),
            (2, 0.01, 0.0, 200.0),
        ]

        result = krige(A, B)

        # Closer point should have much higher weight
        assert result[0][0] > result[0][1]
        assert np.isclose(sum(result[0]), 1.0)

    def test_negative_coordinates(self, capsys):
        """Test with negative coordinates."""
        from iwfm.calib.krige import krige

        A = [(1, -5.0, -5.0)]
        B = [
            (1, -4.0, -5.0, 100.0),
            (2, -5.0, -4.0, 200.0),
        ]

        result = krige(A, B)

        assert np.isclose(sum(result[0]), 1.0)
        # Equidistant points
        assert np.isclose(result[0][0], result[0][1])

    def test_mixed_positive_negative_coordinates(self, capsys):
        """Test with mixed positive and negative coordinates."""
        from iwfm.calib.krige import krige

        A = [(1, 0.0, 0.0)]
        B = [
            (1, -1.0, 0.0, 100.0),
            (2, 1.0, 0.0, 200.0),
        ]

        result = krige(A, B)

        # Both equidistant from origin
        assert np.isclose(result[0][0], result[0][1])


class TestKrigeInterpolation:
    """Tests for using kriging factors in interpolation"""

    def test_interpolate_value(self, capsys):
        """Test using kriging factors to interpolate a value."""
        from iwfm.calib.krige import krige

        A = [(1, 0.0, 0.0)]
        B = [
            (1, 1.0, 0.0, 100.0),
            (2, 2.0, 0.0, 200.0),
        ]

        result = krige(A, B)
        weights = result[0]
        values = [100.0, 200.0]
        
        # Interpolated value = sum(weight * value)
        interpolated = sum(w * v for w, v in zip(weights, values))
        
        # Should be between min and max values
        assert 100.0 <= interpolated <= 200.0

    def test_interpolation_consistency(self, capsys):
        """Test that interpolation is consistent with inverse distance."""
        from iwfm.calib.krige import krige

        # A point equidistant from two B points with values 100 and 200
        A = [(1, 1.5, 0.0)]
        B = [
            (1, 1.0, 0.0, 100.0),   # Distance 0.5
            (2, 2.0, 0.0, 200.0),   # Distance 0.5
        ]

        result = krige(A, B)
        weights = result[0]
        values = [100.0, 200.0]
        
        interpolated = sum(w * v for w, v in zip(weights, values))
        
        # Equidistant, so should be average of values
        assert np.isclose(interpolated, 150.0)


class TestKrigeImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import krige
        assert callable(krige)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.krige import krige
        assert callable(krige)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.krige import krige
        
        assert krige.__doc__ is not None
        assert 'kriging' in krige.__doc__.lower()

    def test_uses_scipy(self):
        """Test that function uses scipy for distance calculation."""
        import importlib
        module = importlib.import_module('iwfm.calib.krige')
        import inspect

        source = inspect.getsource(module.krige)
        assert 'cdist' in source


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
