# test_year.py
# unit test for year() in the iwfm package
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
import iwfm


def test_year_full_year():
    assert iwfm.year("01/02/2020") == 2020


def test_year_two_digit_mapping():
    assert iwfm.year("01/02/75") == 1975
    # Current implementation: > 20 maps to 1900s
    assert iwfm.year("01/02/21") == 1921
    assert iwfm.year("01/02/20") == 2020
    assert iwfm.year("12/31/00") == 2000


