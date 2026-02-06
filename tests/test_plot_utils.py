# test_plot_utils.py
# unit tests for plot utility functions in the iwfm package
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

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import numpy as np
import pytest


def _load_fn(module_name, file_name, fn_name):
    base = Path(__file__).resolve().parents[1] / "iwfm" / "plot" / file_name
    spec = spec_from_file_location(module_name, str(base))
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return getattr(mod, fn_name)


get_maxs = _load_fn("get_maxs", "get_maxs.py", "get_maxs")
get_mins = _load_fn("get_mins", "get_mins.py", "get_mins")
flip_y = _load_fn("flip_y", "flip_y.py", "flip_y")
get_XYvalues = _load_fn("get_XYvalues", "get_XYvalues.py", "get_XYvalues")
contour_levels = _load_fn("contour_levels", "contour_levels.py", "contour_levels")


def test_get_maxs_basic():
    data = [[1.5, 2.3, 10.0], [3.2, 1.1, 5.0], [2.8, 4.9, 15.0]]
    maxs = get_maxs(data)
    assert len(maxs) == 3
    # Values are rounded up (ceil)
    assert maxs[0] == 4  # ceil(3.2)
    assert maxs[1] == 5  # ceil(4.9)
    assert maxs[2] == 15  # ceil(15.0)


def test_get_maxs_single_item():
    data = [[100.0, -50.0, 25.5]]
    maxs = get_maxs(data)
    # Values are rounded up (ceil)
    assert maxs == [100, -50, 26]  # ceil values


def test_get_mins_basic():
    data = [[1.5, 2.3, 10.0], [3.2, 1.1, 5.0], [2.8, 4.9, 15.0]]
    mins = get_mins(data)
    assert len(mins) == 3
    # Values are rounded down (floor)
    assert mins[0] == 1  # floor(1.5)
    assert mins[1] == 1  # floor(1.1)
    assert mins[2] == 5  # floor(5.0)


def test_get_mins_single_item():
    data = [[100.0, -50.0, 25.5]]
    mins = get_mins(data)
    # Values are rounded down (floor)
    assert mins == [100, -50, 25]  # floor values


def test_flip_y_modifies_y_coordinate():
    data = [[1.0, 2.0, 10.0], [3.0, 4.0, 20.0]]
    result = flip_y(data)
    assert result[0][1] == -2.0
    assert result[1][1] == -4.0
    assert result[0][0] == 1.0  # x unchanged
    assert result[0][2] == 10.0  # value unchanged


def test_flip_y_modifies_in_place():
    data = [[5.0, 10.0, 100.0]]
    result = flip_y(data)
    assert data is result  # should modify in place
    assert data[0][1] == -10.0


def test_get_XYvalues_extracts_columns():
    data = [[1.0, 2.0, 10.0], [3.0, 4.0, 20.0], [5.0, 6.0, 30.0]]
    X, Y, values = get_XYvalues(data)
    assert isinstance(X, np.ndarray)
    assert isinstance(Y, np.ndarray)
    assert isinstance(values, np.ndarray)
    assert np.array_equal(X, np.array([1.0, 3.0, 5.0]))
    assert np.array_equal(Y, np.array([2.0, 4.0, 6.0]))
    assert np.array_equal(values, np.array([10.0, 20.0, 30.0]))


def test_contour_levels_large_range():
    Z = np.array([[100, 200, 300], [400, 500, 600]])
    levels = contour_levels(Z)
    assert isinstance(levels, np.ndarray)
    assert len(levels) > 0
    assert levels[0] <= Z.min()
    assert levels[-1] >= Z.max()


def test_contour_levels_small_range_uses_linspace():
    Z = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    levels = contour_levels(Z, no_levels=10)
    assert isinstance(levels, np.ndarray)
    assert len(levels) == 10
    assert np.isclose(levels[0], Z.min())
    assert np.isclose(levels[-1], Z.max())


def test_contour_levels_step_size_logic():
    # Range > 500 uses step=50
    Z = np.array([[0], [600]])
    levels = contour_levels(Z)
    step = levels[1] - levels[0] if len(levels) > 1 else None
    if step:
        assert step == 50


def test_data_to_color_with_matplotlib():
    """Test data_to_color function with matplotlib."""
    try:
        data_to_color = _load_fn("data_to_color", "data_to_color.py", "data_to_color")
        
        # Test basic functionality
        rgb = data_to_color(50.0, 0.0, 100.0, colormap='viridis')
        assert isinstance(rgb, tuple)
        assert len(rgb) == 3
        assert all(isinstance(c, int) for c in rgb)
        assert all(0 <= c <= 255 for c in rgb)
        
        # Test with different colormap
        rgb_rainbow = data_to_color(25.0, 0.0, 100.0, colormap='rainbow')
        assert isinstance(rgb_rainbow, tuple)
        assert len(rgb_rainbow) == 3
        assert all(0 <= c <= 255 for c in rgb_rainbow)
        
        # Test edge cases
        rgb_min = data_to_color(0.0, 0.0, 100.0, colormap='viridis')
        rgb_max = data_to_color(100.0, 0.0, 100.0, colormap='viridis')
        assert isinstance(rgb_min, tuple)
        assert isinstance(rgb_max, tuple)
        assert all(0 <= c <= 255 for c in rgb_min)
        assert all(0 <= c <= 255 for c in rgb_max)
        
    except ImportError as e:
        if "matplotlib" in str(e).lower():
            pytest.skip("matplotlib not available - this is an optional dependency")
        else:
            # Re-raise other import errors as they indicate real problems
            raise


def test_data_to_color_normalization():
    """Test data_to_color normalization and different ranges."""
    try:
        data_to_color = _load_fn("data_to_color", "data_to_color.py", "data_to_color")
        
        # Value at min should map to colormap(0)
        rgb_min = data_to_color(0.0, 0.0, 100.0)
        # Value at max should map to colormap(1)
        rgb_max = data_to_color(100.0, 0.0, 100.0)
        # Middle value
        rgb_mid = data_to_color(50.0, 0.0, 100.0)
        
        # All should be valid RGB tuples
        for rgb in [rgb_min, rgb_max, rgb_mid]:
            assert isinstance(rgb, tuple)
            assert len(rgb) == 3
            assert all(isinstance(c, int) for c in rgb)
            assert all(0 <= c <= 255 for c in rgb)
        
        # Test with different range
        rgb_alt = data_to_color(150.0, 100.0, 200.0)  # 50% of range
        assert isinstance(rgb_alt, tuple)
        assert len(rgb_alt) == 3
        assert all(0 <= c <= 255 for c in rgb_alt)
        
        # Test negative ranges
        rgb_neg = data_to_color(-50.0, -100.0, 0.0)  # 50% of range
        assert isinstance(rgb_neg, tuple)
        assert len(rgb_neg) == 3
        assert all(0 <= c <= 255 for c in rgb_neg)
        
    except ImportError as e:
        if "matplotlib" in str(e).lower():
            pytest.skip("matplotlib not available - this is an optional dependency")
        else:
            raise


# --------------------------------------------------------------------------
# Tests for histogram function
# --------------------------------------------------------------------------

def test_histogram_import():
    """Test that histogram can be imported from iwfm.plot."""
    from iwfm.plot import histogram
    assert callable(histogram)


def test_histogram_direct_import():
    """Test direct import from histogram module."""
    from iwfm.plot.histogram import histogram
    assert callable(histogram)


def test_histogram_has_docstring():
    """Test that histogram has documentation."""
    from iwfm.plot.histogram import histogram
    assert histogram.__doc__ is not None


def test_histogram_function_signature():
    """Test that histogram has correct function signature."""
    from iwfm.plot.histogram import histogram
    import inspect

    sig = inspect.signature(histogram)
    params = list(sig.parameters.keys())

    assert 'data' in params
    assert 'name' in params
    assert 'unit' in params
    assert 'file' in params
    assert 'method' in params


def test_histogram_default_method():
    """Test that histogram default method is 'auto'."""
    from iwfm.plot.histogram import histogram
    import inspect

    sig = inspect.signature(histogram)
    assert sig.parameters['method'].default == 'auto'

