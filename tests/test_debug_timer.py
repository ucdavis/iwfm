# test_debug_timer.py 
# Test debug/timer function decorator for timing execution
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


def test_timer_imports():
    '''Test that timer imports wraps from functools (verifies fix).'''
    # This verifies the fix: added 'from functools import wraps'
    from iwfm.debug.timer import wraps

    assert wraps is not None


def test_timer_decorator_basic():
    '''Test basic functionality of timer decorator.'''
    from iwfm.debug.timer import timer

    @timer
    def sample_function():
        return "test"

    result = sample_function()

    assert result == "test"


def test_timer_decorator_with_arguments():
    '''Test timer decorator with function that takes arguments.'''
    from iwfm.debug.timer import timer

    @timer
    def add_numbers(a, b):
        return a + b

    result = add_numbers(5, 3)

    assert result == 8


def test_timer_decorator_with_kwargs():
    '''Test timer decorator with keyword arguments.'''
    from iwfm.debug.timer import timer

    @timer
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")

    assert result == "Hi, Alice!"


def test_timer_decorator_preserves_function_name():
    '''Test that timer decorator preserves function name (uses functools.wraps).'''
    from iwfm.debug.timer import timer

    @timer
    def my_function():
        '''My function docstring'''
        pass

    # wraps decorator should preserve name and docstring
    assert my_function.__name__ == 'my_function'
    assert 'My function docstring' in my_function.__doc__


def test_timer_decorator_measures_time(capsys):
    '''Test that timer decorator actually measures and prints time.'''
    from iwfm.debug.timer import timer

    @timer
    def slow_function():
        time.sleep(0.01)  # Sleep for 10ms
        return "done"

    result = slow_function()

    captured = capsys.readouterr()
    assert result == "done"
    # Should print elapsed time
    assert 'slow_function' in captured.out or 'Elapsed' in captured.out or captured.out != ''


def test_timer_decorator_with_exception():
    '''Test timer decorator when decorated function raises exception.'''
    from iwfm.debug.timer import timer

    @timer
    def failing_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError, match="Test error"):
        failing_function()


def test_timer_decorator_multiple_calls():
    '''Test timer decorator with multiple function calls.'''
    from iwfm.debug.timer import timer

    call_count = 0

    @timer
    def increment():
        nonlocal call_count
        call_count += 1
        return call_count

    assert increment() == 1
    assert increment() == 2
    assert increment() == 3


def test_timer_uses_wraps():
    '''Test that timer uses functools.wraps (verifies fix).'''
    from iwfm.debug import timer
    import inspect

    source = inspect.getsource(timer)
    assert '@wraps(function)' in source or 'wraps(function)' in source
