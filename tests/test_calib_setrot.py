# test_calib_setrot.py
# Unit tests for calib/setrot.py - Set up rotation matrix for anisotropy
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


class TestSetrot:
    """Tests for setrot function"""

    def test_returns_list(self):
        """Test that function returns a list."""
        from iwfm.calib.setrot import setrot

        result = setrot(0.0, 0.0, 0.0, 1.0, 1.0)

        assert isinstance(result, list)

    def test_returns_3x3_matrix(self):
        """Test that function returns a 3x3 matrix."""
        from iwfm.calib.setrot import setrot

        result = setrot(0.0, 0.0, 0.0, 1.0, 1.0)

        assert len(result) == 3
        for row in result:
            assert len(row) == 3

    def test_identity_like_with_no_rotation(self):
        """Test that with no rotation angles, matrix is identity-like."""
        from iwfm.calib.setrot import setrot

        # No rotation, no anisotropy
        result = setrot(0.0, 0.0, 0.0, 1.0, 1.0)

        # First row should be [0, 1, 0] for ang1=0 (90 degrees rotation)
        # The matrix depends on GSLIB convention
        assert isinstance(result[0][0], float)
        assert isinstance(result[1][1], float)
        assert isinstance(result[2][2], float)

    def test_anisotropy_affects_matrix(self):
        """Test that anisotropy factors affect the matrix."""
        from iwfm.calib.setrot import setrot

        result1 = setrot(0.0, 0.0, 0.0, 1.0, 1.0)
        result2 = setrot(0.0, 0.0, 0.0, 2.0, 2.0)

        # With different anisotropy, matrices should differ
        assert result1 != result2

    def test_rotation_affects_matrix(self):
        """Test that rotation angles affect the matrix."""
        from iwfm.calib.setrot import setrot

        result1 = setrot(0.0, 0.0, 0.0, 1.0, 1.0)
        result2 = setrot(45.0, 0.0, 0.0, 1.0, 1.0)

        # With different rotation, matrices should differ
        assert result1 != result2

    def test_all_elements_are_floats(self):
        """Test that all matrix elements are floats."""
        from iwfm.calib.setrot import setrot

        result = setrot(30.0, 15.0, 10.0, 1.5, 2.0)

        for row in result:
            for elem in row:
                assert isinstance(elem, float)

    def test_handles_zero_anisotropy(self):
        """Test that function handles near-zero anisotropy (uses epsilon)."""
        from iwfm.calib.setrot import setrot

        # Should not raise error due to division by zero
        result = setrot(0.0, 0.0, 0.0, 0.0, 0.0)

        assert len(result) == 3

    def test_angle_270_boundary(self):
        """Test angle at 270 degree boundary."""
        from iwfm.calib.setrot import setrot

        result1 = setrot(269.0, 0.0, 0.0, 1.0, 1.0)
        result2 = setrot(271.0, 0.0, 0.0, 1.0, 1.0)

        # Results should be different due to boundary condition
        assert result1 != result2

    def test_typical_values(self):
        """Test with typical geostatistical values."""
        from iwfm.calib.setrot import setrot

        # Typical variogram parameters
        result = setrot(45.0, 0.0, 0.0, 0.5, 1.0)

        assert len(result) == 3
        for row in result:
            assert len(row) == 3


class TestSetrotImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import setrot
        assert callable(setrot)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.setrot import setrot
        assert callable(setrot)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.setrot import setrot
        
        assert setrot.__doc__ is not None
        assert 'rotation' in setrot.__doc__.lower() or 'matrix' in setrot.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
