# test_closest_list.py
# Unit tests for the closest_list function in the iwfm package
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

from iwfm.closest_list import closest_list, nearest


class TestClosestListFunctionExists:
    """Test that the closest_list function exists and is callable."""

    def test_closest_list_exists(self):
        """Test that closest_list function exists and is callable."""
        assert closest_list is not None
        assert callable(closest_list)


class TestClosestListBasicFunctionality:
    """Test basic functionality of closest_list."""

    def test_single_point_each_list(self):
        """Test with single point in each list."""
        A = ["1,0.0,0.0"]
        B = ["101,1.0,1.0"]

        result = closest_list(A, B)

        assert len(result) == 1
        # Result should contain items from A followed by items from closest B
        assert result[0][0] == "1"
        assert result[0][1] == "0.0"
        assert result[0][2] == "0.0"
        assert result[0][3] == "101"
        assert result[0][4] == "1.0"
        assert result[0][5] == "1.0"

    def test_multiple_points_in_A(self):
        """Test with multiple points in A, single point in B."""
        A = [
            "1,0.0,0.0",
            "2,5.0,5.0",
            "3,10.0,10.0"
        ]
        B = ["101,2.0,2.0"]

        result = closest_list(A, B)

        assert len(result) == 3
        # All should match to the single B point
        for r in result:
            assert r[3] == "101"

    def test_multiple_points_in_B(self):
        """Test with single point in A, multiple points in B."""
        A = ["1,5.0,5.0"]
        B = [
            "101,0.0,0.0",
            "102,4.0,4.0",  # Closest to (5,5)
            "103,10.0,10.0"
        ]

        result = closest_list(A, B)

        assert len(result) == 1
        # Should match to point 102 which is closest
        assert result[0][3] == "102"

    def test_finds_closest_point(self):
        """Test that the function correctly finds the closest point."""
        A = ["1,0.0,0.0"]
        B = [
            "101,10.0,0.0",   # Distance = 10
            "102,3.0,4.0",    # Distance = 5 (3-4-5 triangle)
            "103,0.0,100.0"   # Distance = 100
        ]

        result = closest_list(A, B)

        # Point 102 at (3,4) is closest to origin (0,0) with distance 5
        assert result[0][3] == "102"


class TestClosestListDistanceCalculation:
    """Test distance calculation in closest_list."""

    def test_exact_match(self):
        """Test when A point exactly matches a B point."""
        A = ["1,5.0,5.0"]
        B = [
            "101,0.0,0.0",
            "102,5.0,5.0",  # Exact match
            "103,10.0,10.0"
        ]

        result = closest_list(A, B)

        # Should match to point 102 (distance = 0)
        assert result[0][3] == "102"

    def test_negative_coordinates(self):
        """Test with negative coordinates."""
        A = ["1,-5.0,-5.0"]
        B = [
            "101,0.0,0.0",
            "102,-4.0,-4.0",  # Closest to (-5,-5)
            "103,10.0,10.0"
        ]

        result = closest_list(A, B)

        # Point 102 should be closest
        assert result[0][3] == "102"

    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative coordinates."""
        A = ["1,1.0,-1.0"]
        B = [
            "101,-10.0,-10.0",
            "102,2.0,-2.0",  # Closest to (1,-1)
            "103,10.0,10.0"
        ]

        result = closest_list(A, B)

        assert result[0][3] == "102"

    def test_large_coordinates(self):
        """Test with large coordinate values."""
        A = ["1,1000000.0,1000000.0"]
        B = [
            "101,0.0,0.0",
            "102,999999.0,999999.0",  # Closest
            "103,2000000.0,2000000.0"
        ]

        result = closest_list(A, B)

        assert result[0][3] == "102"

    def test_small_decimal_coordinates(self):
        """Test with small decimal coordinate values."""
        A = ["1,0.001,0.001"]
        B = [
            "101,0.0,0.0",
            "102,0.002,0.002",  # Closest
            "103,0.1,0.1"
        ]

        result = closest_list(A, B)

        # Point 101 at origin is slightly closer than 102
        # Distance to 101: sqrt(0.001^2 + 0.001^2) = 0.001414
        # Distance to 102: sqrt(0.001^2 + 0.001^2) = 0.001414
        # They're equidistant, so first one (101) should be chosen
        assert result[0][3] == "101"


class TestClosestListReturnFormat:
    """Test the return format of closest_list."""

    def test_return_type_is_list(self):
        """Test that return type is a list."""
        A = ["1,0.0,0.0"]
        B = ["101,1.0,1.0"]

        result = closest_list(A, B)

        assert isinstance(result, list)

    def test_return_length_matches_A(self):
        """Test that return list length matches length of A."""
        A = [
            "1,0.0,0.0",
            "2,1.0,1.0",
            "3,2.0,2.0",
            "4,3.0,3.0",
            "5,4.0,4.0"
        ]
        B = ["101,0.0,0.0"]

        result = closest_list(A, B)

        assert len(result) == len(A)

    def test_result_contains_both_A_and_B_data(self):
        """Test that result contains data from both A and B points."""
        A = ["1,10.0,20.0"]
        B = ["101,15.0,25.0,extra1,extra2"]

        result = closest_list(A, B)

        # Should have A data (3 items) + B data (5 items)
        assert len(result[0]) == 8
        # A data
        assert result[0][0] == "1"
        assert result[0][1] == "10.0"
        assert result[0][2] == "20.0"
        # B data
        assert result[0][3] == "101"
        assert result[0][4] == "15.0"
        assert result[0][5] == "25.0"
        assert result[0][6] == "extra1"
        assert result[0][7] == "extra2"


class TestClosestListMultipleMatches:
    """Test closest_list behavior with multiple points."""

    def test_multiple_A_points_different_closest(self):
        """Test that different A points can match to different B points."""
        A = [
            "1,0.0,0.0",
            "2,10.0,10.0"
        ]
        B = [
            "101,1.0,1.0",   # Closer to point 1
            "102,9.0,9.0"    # Closer to point 2
        ]

        result = closest_list(A, B)

        assert result[0][3] == "101"  # Point 1 matches to 101
        assert result[1][3] == "102"  # Point 2 matches to 102

    def test_multiple_A_points_same_closest(self):
        """Test that multiple A points can match to the same B point."""
        A = [
            "1,4.0,4.0",
            "2,5.0,5.0",
            "3,6.0,6.0"
        ]
        B = [
            "101,0.0,0.0",
            "102,5.0,5.0"  # All A points are closest to this
        ]

        result = closest_list(A, B)

        # All should match to 102
        assert result[0][3] == "102"
        assert result[1][3] == "102"
        assert result[2][3] == "102"


class TestClosestListEdgeCases:
    """Test edge cases for closest_list."""

    def test_empty_A_list(self):
        """Test with empty A list."""
        A = []
        B = ["101,1.0,1.0"]

        result = closest_list(A, B)

        assert result == []

    def test_with_extra_data_in_B(self):
        """Test that extra data in B points is preserved."""
        A = ["1,0.0,0.0"]
        B = ["101,1.0,1.0,value1,value2,value3"]

        result = closest_list(A, B)

        # All B data should be appended
        assert "value1" in result[0]
        assert "value2" in result[0]
        assert "value3" in result[0]

    def test_with_integer_coordinates(self):
        """Test with integer coordinates (as strings)."""
        A = ["1,0,0"]
        B = ["101,1,1"]

        result = closest_list(A, B)

        assert len(result) == 1
        assert result[0][3] == "101"


class TestClosestListVerboseMode:
    """Test verbose mode of closest_list."""

    def test_verbose_false(self):
        """Test that verbose=False works without errors."""
        A = ["1,0.0,0.0"]
        B = ["101,1.0,1.0"]

        # Should not raise any errors
        result = closest_list(A, B, verbose=False)

        assert len(result) == 1

    def test_verbose_true(self):
        """Test that verbose=True works without errors."""
        A = ["1,0.0,0.0"]
        B = ["101,1.0,1.0"]

        # Should not raise any errors
        result = closest_list(A, B, verbose=True)

        assert len(result) == 1


class TestClosestListRealWorldScenarios:
    """Test closest_list with realistic data scenarios."""

    def test_grid_of_points(self):
        """Test matching points on a grid."""
        # A points at corners of a 10x10 square
        A = [
            "1,0.0,0.0",
            "2,10.0,0.0",
            "3,0.0,10.0",
            "4,10.0,10.0"
        ]
        # B points near corners
        B = [
            "101,1.0,1.0",    # Near corner 1
            "102,9.0,1.0",    # Near corner 2
            "103,1.0,9.0",    # Near corner 3
            "104,9.0,9.0"     # Near corner 4
        ]

        result = closest_list(A, B)

        assert result[0][3] == "101"  # Corner 1 -> B point 101
        assert result[1][3] == "102"  # Corner 2 -> B point 102
        assert result[2][3] == "103"  # Corner 3 -> B point 103
        assert result[3][3] == "104"  # Corner 4 -> B point 104

    def test_line_of_points(self):
        """Test matching points along a line."""
        # A points along x-axis
        A = [
            "1,0.0,0.0",
            "2,5.0,0.0",
            "3,10.0,0.0"
        ]
        # B points slightly offset from x-axis
        B = [
            "101,0.0,0.5",
            "102,5.0,0.5",
            "103,10.0,0.5"
        ]

        result = closest_list(A, B)

        # Each A point should match to corresponding B point
        assert result[0][3] == "101"
        assert result[1][3] == "102"
        assert result[2][3] == "103"

    def test_clustered_points(self):
        """Test with clustered points."""
        # A has one cluster around (0,0) and one at (100,100)
        A = [
            "1,0.0,0.0",
            "2,1.0,1.0",
            "3,100.0,100.0",
            "4,101.0,101.0"
        ]
        # B has points near each cluster
        B = [
            "101,0.5,0.5",    # Near first cluster
            "102,100.5,100.5" # Near second cluster
        ]

        result = closest_list(A, B)

        # First two A points should match to 101
        assert result[0][3] == "101"
        assert result[1][3] == "101"
        # Last two A points should match to 102
        assert result[2][3] == "102"
        assert result[3][3] == "102"


class TestNearestFunction:
    """Test the helper nearest() function directly."""

    def test_nearest_basic(self):
        """Test basic nearest function call."""
        a = "1,0.0,0.0"
        B = [
            "101,1.0,0.0",
            "102,0.0,1.0",
            "103,0.5,0.5"  # Closest (distance ~0.707)
        ]

        result = nearest(a, B)

        # Result should contain a's data + closest B's data
        assert result[0] == "1"
        assert result[3] == "103"

    def test_nearest_returns_list(self):
        """Test that nearest returns a list."""
        a = "1,0.0,0.0"
        B = ["101,1.0,1.0"]

        result = nearest(a, B)

        assert isinstance(result, list)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
