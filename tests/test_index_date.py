# test_index_date.py
# unit test for index_date() in the iwfm package
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


def test_index_date_same_date_zero():
    assert iwfm.index_date("10/01/1984", start_date="10/01/1984") == 0


def test_index_date_simple_forward():
    # Returns number of days between dates (datetime difference)
    assert iwfm.index_date("10/02/1984", start_date="10/01/1984") == 1


def test_index_date_across_years():
    # Rough check using implementation (365-day years + simple leap handling)
    days = iwfm.index_date("01/01/1986", start_date="10/01/1984")
    assert isinstance(days, int)
    assert days > 400


