# test_debug_print_exe_time.py
# Tests for debug/print_exe_time.py - Print execution time between two datetimes
# Copyright (C) 2026 University of California
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

import pytest
from datetime import datetime, timedelta


class TestPrintExeTime:
    """Tests for print_exe_time function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = datetime(2020, 1, 1, 0, 0, 10)
        
        result = print_exe_time(start, end, verbose=0)
        
        assert isinstance(result, str)

    def test_format_seconds_only(self):
        """Test format when duration is less than 1 minute."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = start + timedelta(seconds=12.3)
        
        result = print_exe_time(start, end, verbose=0)
        
        assert "seconds" in result

    def test_format_minutes_and_seconds(self):
        """Test format when duration is more than 1 minute but less than 1 hour."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = start + timedelta(minutes=2, seconds=5)
        
        result = print_exe_time(start, end, verbose=0)
        
        assert "min" in result
        assert "sec" in result

    def test_format_hours_minutes_seconds(self):
        """Test format when duration is 1 hour or more."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = start + timedelta(hours=1, minutes=2, seconds=3)
        
        result = print_exe_time(start, end, verbose=0)
        
        # Should be in hh:mm:ss format
        assert ":" in result
        parts = result.split(':')
        assert len(parts) == 3

    def test_verbose_true_prints(self, capsys):
        """Test that verbose=1 prints to console."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = start + timedelta(seconds=5)
        
        print_exe_time(start, end, verbose=1)
        
        captured = capsys.readouterr()
        assert "Execution time" in captured.out

    def test_verbose_false_no_print(self, capsys):
        """Test that verbose=0 does not print to console."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = start + timedelta(seconds=5)
        
        print_exe_time(start, end, verbose=0)
        
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_zero_duration(self):
        """Test with zero duration (same start and end)."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = start
        
        result = print_exe_time(start, end, verbose=0)
        
        assert "seconds" in result
        assert "0" in result

    def test_fractional_seconds(self):
        """Test with fractional seconds."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = start + timedelta(seconds=5.5)
        
        result = print_exe_time(start, end, verbose=0)
        
        assert "5.5" in result or "5." in result

    def test_exactly_one_minute(self):
        """Test with exactly one minute."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = start + timedelta(minutes=1)
        
        result = print_exe_time(start, end, verbose=0)
        
        assert "1 min" in result

    def test_exactly_one_hour(self):
        """Test with exactly one hour."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = start + timedelta(hours=1)
        
        result = print_exe_time(start, end, verbose=0)
        
        # Should be in hh:mm:ss format
        assert ":" in result


class TestPrintExeTimeImports:
    """Tests for print_exe_time imports."""

    def test_import_from_debug(self):
        """Test import from iwfm.debug."""
        from iwfm.debug import print_exe_time
        assert callable(print_exe_time)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.debug.print_exe_time import print_exe_time
        assert callable(print_exe_time)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.debug.print_exe_time import print_exe_time
        
        assert print_exe_time.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
