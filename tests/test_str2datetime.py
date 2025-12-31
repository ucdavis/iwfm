# test_str2datetime.py
# unit test for str2datetime() in the iwfm package
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
from datetime import datetime

import iwfm


def test_str2datetime_full_year():
    d = iwfm.str2datetime("01/02/2020")
    assert isinstance(d, datetime)
    assert d == datetime(2020, 1, 2)


def test_str2datetime_two_digit_year_behaves_as_implemented():
    # Current implementation treats YY literally as AD year YY
    d = iwfm.str2datetime("12/31/20")
    assert d == datetime(20, 12, 31)


