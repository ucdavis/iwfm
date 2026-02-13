# test_text_and_dss_date.py
# unit test for text_date() and dss_date() in the iwfm package
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


def test_dss_date_regular_hour():
    dt = datetime(2020, 1, 2, 15, 7)
    assert iwfm.dss_date(dt) == "01/02/2020_15:07"


def test_dss_date_midnight_is_24():
    dt = datetime(2020, 1, 2, 0, 0)
    assert iwfm.dss_date(dt) == "01/02/2020_24:00"


