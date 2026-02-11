# test_debug_exe_time.py
# Tests for debug/exe_time.py - Track and print execution time
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
import time
from datetime import datetime


class TestExeTimeTracker:
    """Tests for ExeTimeTracker class."""

    def test_class_exists(self):
        """Test that ExeTimeTracker class exists."""
        from iwfm.debug.exe_time import ExeTimeTracker
        
        assert ExeTimeTracker is not None

    def test_instantiation(self):
        """Test that ExeTimeTracker can be instantiated."""
        from iwfm.debug.exe_time import ExeTimeTracker
        
        tracker = ExeTimeTracker()
        assert tracker is not None

    def test_start_is_datetime(self):
        """Test that start attribute is a datetime."""
        from iwfm.debug.exe_time import ExeTimeTracker
        
        tracker = ExeTimeTracker()
        assert isinstance(tracker.start, datetime)

    def test_get_start_returns_datetime(self):
        """Test that get_start() returns a datetime."""
        from iwfm.debug.exe_time import ExeTimeTracker
        
        tracker = ExeTimeTracker()
        result = tracker.get_start()
        assert isinstance(result, datetime)

    def test_start_time_is_recent(self):
        """Test that start time is approximately now."""
        from iwfm.debug.exe_time import ExeTimeTracker
        
        before = datetime.now()
        tracker = ExeTimeTracker()
        after = datetime.now()
        
        assert before <= tracker.get_start() <= after


class TestExeTime:
    """Tests for exe_time function."""

    def test_first_call_no_output(self, capsys):
        """Test that first call produces no output (just sets start time)."""
        # Reset the module-level instance
        import iwfm.debug.exe_time as exe_time_module
        exe_time_module._exe_time_instance = None
        
        from iwfm.debug.exe_time import exe_time
        
        exe_time()
        captured = capsys.readouterr()
        
        # First call should not print anything
        assert captured.out == ""

    def test_second_call_prints_elapsed(self, capsys):
        """Test that second call prints elapsed time."""
        # Reset the module-level instance
        import iwfm.debug.exe_time as exe_time_module
        exe_time_module._exe_time_instance = None
        
        from iwfm.debug.exe_time import exe_time
        
        exe_time()  # First call - sets start
        time.sleep(0.01)  # Small delay
        exe_time()  # Second call - prints elapsed
        
        captured = capsys.readouterr()
        assert "Elapsed time" in captured.out

    def test_elapsed_time_format_seconds(self, capsys):
        """Test elapsed time format for short durations (seconds)."""
        import iwfm.debug.exe_time as exe_time_module
        exe_time_module._exe_time_instance = None
        
        from iwfm.debug.exe_time import exe_time
        
        exe_time()
        exe_time()
        
        captured = capsys.readouterr()
        assert "seconds" in captured.out

    def test_multiple_subsequent_calls(self, capsys):
        """Test multiple subsequent calls after reset."""
        import iwfm.debug.exe_time as exe_time_module
        exe_time_module._exe_time_instance = None

        from iwfm.debug.exe_time import exe_time

        capsys.readouterr()  # flush any prior output

        exe_time()  # First call - sets start
        capsys.readouterr()  # clear buffer (should be empty, but guards against ordering)

        exe_time()  # Second call - prints elapsed
        exe_time()  # Third call - prints elapsed

        captured = capsys.readouterr()
        assert captured.out.count("Elapsed time") == 2


class TestExeTimeImports:
    """Tests for exe_time imports."""

    def test_import_from_debug(self):
        """Test import from iwfm.debug."""
        from iwfm.debug import exe_time
        assert callable(exe_time)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.debug.exe_time import exe_time
        assert callable(exe_time)

    def test_import_tracker_class(self):
        """Test importing ExeTimeTracker class."""
        from iwfm.debug.exe_time import ExeTimeTracker
        assert ExeTimeTracker is not None

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.debug.exe_time import exe_time
        
        assert exe_time.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
