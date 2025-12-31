# test_cfs2afd.py
# unit test for method cfs2afd() in the iwfm package
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


def test_cfs2afd_zero():
    assert iwfm.cfs2afd(0.0) == 0.0


def test_cfs2afd_positive():
    assert iwfm.cfs2afd(1.0) == 1.983
    assert math.isclose(iwfm.cfs2afd(10.0), 19.83, rel_tol=1e-12)


def test_cfs2afd_precision():
    val = iwfm.cfs2afd(123.456)
    assert math.isclose(val, 123.456 * 1.983, rel_tol=1e-12)


