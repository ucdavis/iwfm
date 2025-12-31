# test_date_index.py
# unit test for date_index() in the iwfm package
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


def test_date_index_zero_months_returns_start():
    assert iwfm.date_index(0, "01/15/2020") == "01/15/2020"


def test_date_index_one_month_behaves_as_implemented():
    # Loop starts at 1 and runs to inval-1, so 1 yields no increment
    assert iwfm.date_index(1, "01/15/2020") == "01/15/2020"


def test_date_index_multiple_months_rollover():
    # For 2 months, one increment happens: Dec -> Jan
    # Implementation increments once for inval=2
    assert iwfm.date_index(2, "12/31/2020") == "01/31/2021"


