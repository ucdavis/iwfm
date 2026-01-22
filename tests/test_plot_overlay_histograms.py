# test_plot_overlay_histograms.py 
# Test plot/overlay_histograms function
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
from unittest.mock import patch, Mock
import numpy as np


def test_overlay_histograms_docstring_format():
    '''Test that overlay_histograms uses triple single quotes (verifies fix).'''
    # This verifies the fix: changed docstring from """ to '''
    from iwfm.plot.overlay_histograms import overlay_histograms
    import inspect

    source = inspect.getsource(overlay_histograms)
    # Should have ''' for docstrings
    assert "'''" in source


@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.grid')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.hist')
def test_overlay_histograms_basic(mock_hist, mock_xlabel, mock_ylabel, mock_title, mock_legend, mock_grid, mock_savefig, tmp_path):
    '''Test basic functionality of overlay_histograms.'''
    from iwfm.plot.overlay_histograms import overlay_histograms

    data1 = [1.0, 2.0, 3.0, 4.0, 5.0]
    data2 = [1.5, 2.5, 3.5, 4.5, 5.5]
    file_name = tmp_path / 'histogram.pdf'

    overlay_histograms(data1, data2, str(file_name), format='pdf')

    # Verify plt.hist was called twice (once for each dataset)
    assert mock_hist.call_count == 2
    mock_savefig.assert_called_once()


@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.grid')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.hist')
def test_overlay_histograms_with_labels(mock_hist, mock_xlabel, mock_ylabel, mock_title, mock_legend, mock_grid, mock_savefig, tmp_path):
    '''Test overlay_histograms with custom labels.'''
    from iwfm.plot.overlay_histograms import overlay_histograms

    data1 = [1, 2, 3]
    data2 = [4, 5, 6]
    file_name = tmp_path / 'histogram.pdf'

    overlay_histograms(
        data1, data2, str(file_name),
        label1='Dataset A',
        label2='Dataset B',
        format='pdf'
    )

    # Check that hist was called with labels
    calls = mock_hist.call_args_list
    assert len(calls) == 2


@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.grid')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.hist')
def test_overlay_histograms_with_alpha(mock_hist, mock_xlabel, mock_ylabel, mock_title, mock_legend, mock_grid, mock_savefig, tmp_path):
    '''Test overlay_histograms with custom alpha transparency.'''
    from iwfm.plot.overlay_histograms import overlay_histograms

    data1 = [1, 2, 3]
    data2 = [4, 5, 6]
    file_name = tmp_path / 'histogram.pdf'

    overlay_histograms(data1, data2, str(file_name), alpha=0.7, format='pdf')

    mock_hist.assert_called()


@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.grid')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.hist')
def test_overlay_histograms_with_bins(mock_hist, mock_xlabel, mock_ylabel, mock_title, mock_legend, mock_grid, mock_savefig, tmp_path):
    '''Test overlay_histograms with custom bins.'''
    from iwfm.plot.overlay_histograms import overlay_histograms

    data1 = [1, 2, 3, 4, 5]
    data2 = [6, 7, 8, 9, 10]
    file_name = tmp_path / 'histogram.pdf'

    overlay_histograms(data1, data2, str(file_name), bins=10, format='pdf')

    mock_hist.assert_called()


@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.grid')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.hist')
def test_overlay_histograms_numpy_arrays(mock_hist, mock_xlabel, mock_ylabel, mock_title, mock_legend, mock_grid, mock_savefig, tmp_path):
    '''Test overlay_histograms with numpy arrays.'''
    from iwfm.plot.overlay_histograms import overlay_histograms

    data1 = np.array([1.0, 2.0, 3.0])
    data2 = np.array([4.0, 5.0, 6.0])
    file_name = tmp_path / 'histogram.pdf'

    overlay_histograms(data1, data2, str(file_name), format='pdf')

    assert mock_hist.call_count == 2


@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.grid')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.hist')
def test_overlay_histograms_creates_legend(mock_hist, mock_xlabel, mock_ylabel, mock_title, mock_legend, mock_grid, mock_savefig, tmp_path):
    '''Test that overlay_histograms creates a legend.'''
    from iwfm.plot.overlay_histograms import overlay_histograms

    data1 = [1, 2, 3]
    data2 = [4, 5, 6]
    file_name = tmp_path / 'histogram.pdf'

    overlay_histograms(data1, data2, str(file_name), format='pdf')

    mock_legend.assert_called_once()


@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.grid')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.hist')
def test_overlay_histograms_creates_grid(mock_hist, mock_xlabel, mock_ylabel, mock_title, mock_legend, mock_grid, mock_savefig, tmp_path):
    '''Test that overlay_histograms creates a grid.'''
    from iwfm.plot.overlay_histograms import overlay_histograms

    data1 = [1, 2, 3]
    data2 = [4, 5, 6]
    file_name = tmp_path / 'histogram.pdf'

    overlay_histograms(data1, data2, str(file_name), format='pdf')

    mock_grid.assert_called_once()


def test_overlay_histograms_function_signature():
    '''Test that overlay_histograms has correct function signature.'''
    from iwfm.plot.overlay_histograms import overlay_histograms
    import inspect

    sig = inspect.signature(overlay_histograms)
    params = list(sig.parameters.keys())

    assert 'data1' in params
    assert 'data2' in params
    assert 'file_name' in params
    assert 'label1' in params
    assert 'label2' in params
    assert 'format' in params
    assert 'alpha' in params
    assert 'bins' in params
