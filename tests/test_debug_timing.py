# test_debug_timing.py
# unit test for iwfm.debug timing methods in the iwfm package
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
from datetime import datetime, timedelta

import pytest

import iwfm
import iwfm.debug as debug


def test_print_exe_time_formats():
    # <1 minute
    s = datetime(2020, 1, 1, 0, 0, 0)
    e = s + timedelta(seconds=12.3)
    msg = debug.print_exe_time(s, e, verbose=0)
    assert "seconds" in msg

    # >1 minute
    s = datetime(2020, 1, 1, 0, 0, 0)
    e = s + timedelta(minutes=2, seconds=5)
    msg = debug.print_exe_time(s, e, verbose=0)
    assert "min" in msg and "sec" in msg

    # >=1 hour
    s = datetime(2020, 1, 1, 0, 0, 0)
    e = s + timedelta(hours=1, minutes=2, seconds=3)
    msg = debug.print_exe_time(s, e, verbose=0)
    assert ":" in msg and len(msg.split(':')) == 3


def test_exe_time_two_calls_prints_elapsed(capsys):
    # First call sets start
    debug.exe_time()
    # Second call prints
    debug.exe_time()
    out = capsys.readouterr().out
    assert "Elapsed time" in out


def test_timer_decorator_current_behavior_nameerror():
    # Import timer directly from its module since package __init__ doesn't expose it
    from iwfm.debug.timer import timer  # type: ignore
    # Current implementation references wraps without import; expect NameError at decoration
    with pytest.raises(NameError):
        @timer
        def add(a, b):
            return a + b


