# test_bnds2mask.py
# unit test for bnds2mask function
# Copyright (C) 2025 University of California
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

from iwfm.bnds2mask import bnds2mask

def test_bnds2mask():
    """Test the bnds2mask function.

    bnds2mask(bnds_d, coords) takes:
    - bnds_d: list of boundary node IDs (integers)
    - coords: list of [node_id, x, y]
    Returns a list of (x, y) tuples forming a closed polygon.
    """
    # Boundary node IDs in order
    bnds_d = [1, 2, 3, 4]

    # Node coordinates: [node_id, x, y]
    coords = [
        [1, 0.0, 0.0],
        [2, 1.0, 0.0],
        [3, 1.0, 1.0],
        [4, 0.0, 1.0],
    ]

    result = bnds2mask(bnds_d, coords)

    # Result should be a closed polygon (5 points: 4 nodes + closing point)
    assert len(result) == 5
    assert result[0] == (0.0, 0.0)
    assert result[1] == (1.0, 0.0)
    assert result[2] == (1.0, 1.0)
    assert result[3] == (0.0, 1.0)
    assert result[4] == result[0]  # polygon is closed