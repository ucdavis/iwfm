# test_gis_geop_plot.py 
# Test gis/geop_plot function for displaying geopandas plots
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


from unittest.mock import patch, Mock


def test_geop_plot_imports():
    '''Test that geop_plot imports matplotlib.pyplot (verifies fix).'''
    # This verifies the fix: added 'import matplotlib.pyplot as plt'
    from iwfm.gis.geop_plot import plt

    assert plt is not None
    assert hasattr(plt, 'show')


@patch('iwfm.gis.geop_plot.plt')
def test_geop_plot_basic(mock_plt):
    '''Test basic functionality of geop_plot.'''
    from iwfm.gis.geop_plot import geop_plot

    # Create mock geopandas dataframe
    mock_gdf = Mock()
    mock_gdf.plot.return_value = Mock()

    geop_plot(mock_gdf)

    mock_gdf.plot.assert_called_once()
    mock_plt.show.assert_called_once()


@patch('iwfm.gis.geop_plot.plt')
def test_geop_plot_with_args(mock_plt):
    '''Test geop_plot with arguments passed to plot.'''
    from iwfm.gis.geop_plot import geop_plot

    mock_gdf = Mock()
    mock_gdf.plot.return_value = Mock()

    geop_plot(mock_gdf, column='value', cmap='viridis')

    mock_gdf.plot.assert_called_once()


def test_geop_plot_function_signature():
    '''Test that geop_plot has correct function signature.'''
    from iwfm.gis.geop_plot import geop_plot
    import inspect

    sig = inspect.signature(geop_plot)
    params = list(sig.parameters.keys())

    assert 'gdf' in params
