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
    """Test the bnds2mask function."""
    # Example input data for the test
    example_bnds = [
        [0, 0],
        [0, 1],
        [1, 1],
        [1, 0]
    ]
    expected_output = "Expected output based on the function's logic"

    # Call the function with the example input
    result = bnds2mask(example_bnds)

    # Assert the result matches the expected output
    assert result == expected_output, f"Expected {expected_output}, but got {result}"