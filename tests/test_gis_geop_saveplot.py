# test_gis_geop_saveplot.py 
# Test gis/geop_saveplot function for saving geopandas plots
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


def test_geop_saveplot_imports():
    '''Test that geop_saveplot imports matplotlib.pyplot (verifies fix).'''
    # This verifies the fix: added 'import matplotlib.pyplot as plt'
    from iwfm.gis.geop_saveplot import plt

    assert plt is not None
    assert hasattr(plt, 'savefig')


@patch('iwfm.gis.geop_saveplot.plt')
def test_geop_saveplot_basic(mock_plt, tmp_path):
    '''Test basic functionality of geop_saveplot.'''
    from iwfm.gis.geop_saveplot import geop_saveplot

    # Create mock geopandas dataframe
    mock_gdf = Mock()
    mock_gdf.plot.return_value = Mock()

    outfile = tmp_path / 'plot.png'

    geop_saveplot(mock_gdf, str(outfile))

    mock_gdf.plot.assert_called_once()
    mock_plt.savefig.assert_called_once()


@patch('iwfm.gis.geop_saveplot.plt')
def test_geop_saveplot_with_args(mock_plt, tmp_path):
    '''Test geop_saveplot with plot arguments.'''
    from iwfm.gis.geop_saveplot import geop_saveplot

    mock_gdf = Mock()
    mock_gdf.plot.return_value = Mock()

    outfile = tmp_path / 'plot.png'

    geop_saveplot(mock_gdf, str(outfile), column='value', cmap='plasma')

    mock_gdf.plot.assert_called_once()


def test_geop_saveplot_function_signature():
    '''Test that geop_saveplot has correct function signature.'''
    from iwfm.gis.geop_saveplot import geop_saveplot
    import inspect

    sig = inspect.signature(geop_saveplot)
    params = list(sig.parameters.keys())

    assert 'gdf' in params
    assert 'outname' in params
