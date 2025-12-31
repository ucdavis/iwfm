# test_distence.py
# unit test for distance() in the iwfm package
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
import math

import iwfm


def test_distance_zero():
    assert iwfm.distance((0.0, 0.0), (0.0, 0.0)) == 0.0


def test_distance_axis_aligned():
    assert iwfm.distance((0.0, 0.0), (3.0, 0.0)) == 3.0
    assert iwfm.distance((0.0, 0.0), (0.0, 4.0)) == 4.0


def test_distance_pythagorean():
    assert iwfm.distance((0.0, 0.0), (3.0, 4.0)) == 5.0


def test_distance_non_integer():
    d = iwfm.distance((1.2, -3.4), (5.6, 7.8))
    assert math.isclose(d, math.hypot(5.6 - 1.2, 7.8 - (-3.4)), rel_tol=1e-12)


