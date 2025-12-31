# test_date2text.py
# unit test for date2text() in the iwfm package
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


def test_date2text_basic():
    assert iwfm.date2text(1, 1, 2020) == "01/01/2020"
    assert iwfm.date2text(9, 9, 1999) == "09/09/1999"
    assert iwfm.date2text(10, 10, 2001) == "10/10/2001"


def test_date2text_zero_padding():
    assert iwfm.date2text(3, 4, 2021) == "04/03/2021"


def test_date2text_two_digit_years():
    # y < 20 -> 2000 + y
    assert iwfm.date2text(5, 6, 5) == "06/05/2005"
    # 20 <= y < 100 -> 1900 + y
    assert iwfm.date2text(7, 8, 75) == "08/07/1975"


