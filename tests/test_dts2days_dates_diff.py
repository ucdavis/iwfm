# test_dts2days_dates_diff.py
# unit test for dts2days() and dates_diff() in the iwfm package
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


def test_dts2days_single_datetime():
    start = datetime(2020, 1, 1)
    d = datetime(2020, 1, 11)
    assert iwfm.dts2days(d, start) == 10


def test_dts2days_list_of_datetimes():
    start = datetime(2020, 1, 1)
    dates = [datetime(2020, 1, 1), datetime(2020, 1, 2), datetime(2020, 1, 11)]
    assert iwfm.dts2days(dates, start) == [0, 1, 10]


def test_dates_diff_absolute_days():
    a = datetime(2020, 1, 1)
    b = datetime(2020, 1, 11)
    assert iwfm.dates_diff(a, b) == 10
    assert iwfm.dates_diff(b, a) == 10


