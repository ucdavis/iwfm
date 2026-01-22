# test_iwfm_map_params.py
# unit tests for iwfm_map_params functions
# Copyright (C) 2025-2026 University of California
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
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock


def _load_module():
    """Load the iwfm_map_params module dynamically."""
    from importlib.util import spec_from_file_location, module_from_spec
    base = Path(__file__).resolve().parents[1] / "iwfm" / "plot" / "iwfm_map_params.py"
    spec = spec_from_file_location("iwfm_map_params", str(base))
    assert spec is not None, "Failed to load module specification"
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


_module = _load_module()
get_params = _module.get_params
iwfm_map_params = _module.iwfm_map_params


class TestGetParams:
    """Tests for the get_params function."""

    def test_groundwater_params(self):
        """Test reading groundwater parameters."""
        # Setup mock data - 6 parameter types
        mock_data = [
            np.array([1.0, 2.0, 3.0]),  # kh
            np.array([0.1, 0.2, 0.3]),  # ss
            np.array([0.01, 0.02, 0.03]),  # sy
            np.array([0.5, 0.6, 0.7]),  # kq
            np.array([0.05, 0.06, 0.07]),  # kv
            np.array([10.0, 20.0, 30.0]),  # gwic
        ]

        param_values = ['Groundwater', 'sim_file', 'description']

        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data) as mock_read:
            data, format_type = get_params('gw_data.dat', 'kh', param_values, verbose=False)

            mock_read.assert_called_once_with('gw_data.dat')
            assert format_type == 'nodes'
            np.testing.assert_array_equal(data, np.array([1.0, 2.0, 3.0]))

    def test_groundwater_different_param(self):
        """Test reading different groundwater parameter types."""
        mock_data = [
            np.array([1.0, 2.0]),  # kh
            np.array([0.1, 0.2]),  # ss
            np.array([0.01, 0.02]),  # sy
            np.array([0.5, 0.6]),  # kq
            np.array([0.05, 0.06]),  # kv
            np.array([10.0, 20.0]),  # gwic
        ]

        param_values = ['Groundwater', 'sim_file', 'description']

        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data):
            data, format_type = get_params('gw_data.dat', 'sy', param_values, verbose=False)

            assert format_type == 'nodes'
            np.testing.assert_array_equal(data, np.array([0.01, 0.02]))

    def test_rootzone_params(self):
        """Test reading rootzone parameters."""
        mock_data = [np.array([i]) for i in range(13)]  # 13 param types

        param_values = ['Rootzone', 'sim_file', 'description']

        with patch('iwfm.iwfm_read_rz_params', return_value=mock_data) as mock_read:
            data, format_type = get_params('rz_data.dat', 'wp', param_values, verbose=False)

            mock_read.assert_called_once_with('rz_data.dat')
            assert format_type == 'elements'

    def test_nonponded_params(self):
        """Test reading non-ponded parameters."""
        mock_data = [np.array([i]) for i in range(9)]  # 9 param types

        param_values = ['Non-ponded', 'sim_file', 'description']

        # Patch iwfm module at the sys.modules level since it's imported inside the function
        with patch('iwfm.iwfm_read_rz_npc', return_value=mock_data) as mock_read:
            data, format_type = get_params('npc_data.dat', 'cnnp', param_values, verbose=False)

            mock_read.assert_called_once_with('npc_data.dat')
            assert format_type == 'elements'

    def test_ponded_params(self):
        """Test reading ponded parameters."""
        mock_data = [np.array([i]) for i in range(9)]  # 9 param types

        param_values = ['Ponded', 'sim_file', 'description']

        # Patch iwfm module at the sys.modules level since it's imported inside the function
        with patch('iwfm.iwfm_read_rz_pc', return_value=mock_data) as mock_read:
            data, format_type = get_params('pc_data.dat', 'cnpc', param_values, verbose=False)

            mock_read.assert_called_once_with('pc_data.dat')
            assert format_type == 'elements'

    def test_verbose_output(self, capsys):
        """Test verbose mode produces output."""
        mock_data = [np.array([1.0]) for _ in range(6)]

        param_values = ['Groundwater', 'sim_file', 'description']

        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data):
            get_params('gw_data.dat', 'kh', param_values, verbose=True)

        captured = capsys.readouterr()
        assert "Reading parameter values" in captured.out

    def test_2d_data_flattening(self):
        """Test that 2D data is flattened to first layer."""
        # Create 2D data: 3 nodes x 2 layers
        mock_data = [
            np.array([[1.0, 1.1], [2.0, 2.1], [3.0, 3.1]]),  # kh with 2 layers
            np.array([[0.1, 0.2]]),  # ss
            np.array([[0.01]]),  # sy
            np.array([[0.5]]),  # kq
            np.array([[0.05]]),  # kv
            np.array([[10.0]]),  # gwic
        ]

        param_values = ['Groundwater', 'sim_file', 'description']

        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data):
            data, format_type = get_params('gw_data.dat', 'kh', param_values, verbose=False)

            # Should return first layer only
            np.testing.assert_array_equal(data, np.array([1.0, 2.0, 3.0]))


class TestIwfmMapParams:
    """Tests for the iwfm_map_params function."""

    def test_basic_plot_creation(self, tmp_path):
        """Test basic contour map creation."""
        # Create test dataset with at least 4 non-collinear points for scipy griddata
        # scipy's Delaunay triangulation needs at least 4 points not on the same line
        dataset = [
            [0, 0, 10], [4, 0, 20], [4, 4, 30], [0, 4, 40],  # corners
            [2, 2, 25],  # center point
        ]

        # Create boundary polygon (simple square)
        bounding_poly = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]

        image_basename = str(tmp_path / "test_map")

        with patch('iwfm.plot.get_XYvalues', return_value=(
                np.array([0, 4, 4, 0, 2]),
                np.array([0, 0, 4, 4, 2]),
                np.array([10, 20, 30, 40, 25])
             )), \
             patch('iwfm.plot.contour_levels', return_value=np.linspace(10, 40, 5)), \
             patch('matplotlib.pyplot.savefig') as mock_savefig, \
             patch('matplotlib.pyplot.close') as mock_close, \
             patch('matplotlib.pyplot.subplots') as mock_subplots, \
             patch('matplotlib.pyplot.contour'), \
             patch('matplotlib.pyplot.colorbar'):
            fig_mock = MagicMock()
            ax_mock = MagicMock()
            mock_subplots.return_value = (fig_mock, ax_mock)

            iwfm_map_params(dataset, bounding_poly, image_basename, verbose=False)

            # Verify savefig was called
            mock_savefig.assert_called_once()
            mock_close.assert_called_with('all')

    def test_filled_contour(self, tmp_path):
        """Test filled contour option."""
        # Need at least 4 non-collinear points for scipy griddata
        dataset = [
            [0, 0, 10], [4, 0, 20], [4, 4, 30], [0, 4, 40], [2, 2, 25]
        ]
        bounding_poly = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
        image_basename = str(tmp_path / "filled_map")

        with patch('iwfm.plot.get_XYvalues', return_value=(
                np.array([0, 4, 4, 0, 2]),
                np.array([0, 0, 4, 4, 2]),
                np.array([10, 20, 30, 40, 25])
             )), \
             patch('iwfm.plot.contour_levels', return_value=np.linspace(10, 40, 5)), \
             patch('matplotlib.pyplot.savefig'), \
             patch('matplotlib.pyplot.close'), \
             patch('matplotlib.pyplot.subplots') as mock_subplots, \
             patch('matplotlib.pyplot.contourf') as mock_contourf, \
             patch('matplotlib.pyplot.colorbar'):
            fig_mock = MagicMock()
            ax_mock = MagicMock()
            mock_subplots.return_value = (fig_mock, ax_mock)

            iwfm_map_params(dataset, bounding_poly, image_basename, contour='filled', verbose=False)

            # Should use contourf for filled contours
            mock_contourf.assert_called_once()

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose mode."""
        # Need at least 4 non-collinear points for scipy griddata
        dataset = [
            [0, 0, 10], [4, 0, 20], [4, 4, 30], [0, 4, 40], [2, 2, 25]
        ]
        bounding_poly = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
        image_basename = str(tmp_path / "verbose_map")

        with patch('iwfm.plot.get_XYvalues', return_value=(
                np.array([0, 4, 4, 0, 2]),
                np.array([0, 0, 4, 4, 2]),
                np.array([10, 20, 30, 40, 25])
             )), \
             patch('iwfm.plot.contour_levels', return_value=np.linspace(10, 40, 5)), \
             patch('matplotlib.pyplot.savefig'), \
             patch('matplotlib.pyplot.close'), \
             patch('matplotlib.pyplot.subplots') as mock_subplots, \
             patch('matplotlib.pyplot.contour'), \
             patch('matplotlib.pyplot.colorbar'):
            fig_mock = MagicMock()
            ax_mock = MagicMock()
            mock_subplots.return_value = (fig_mock, ax_mock)

            iwfm_map_params(dataset, bounding_poly, image_basename, verbose=True)

        captured = capsys.readouterr()
        assert "Image saved" in captured.out

    def test_shapely_polygon_support(self, tmp_path):
        """Test support for shapely Polygon objects."""
        try:
            from shapely.geometry import Polygon
            bounding_poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])
        except ImportError:
            pytest.skip("shapely not installed")

        # Need at least 4 non-collinear points for scipy griddata
        dataset = [
            [0, 0, 10], [4, 0, 20], [4, 4, 30], [0, 4, 40], [2, 2, 25]
        ]
        image_basename = str(tmp_path / "shapely_map")

        with patch('iwfm.plot.get_XYvalues', return_value=(
                np.array([0, 4, 4, 0, 2]),
                np.array([0, 0, 4, 4, 2]),
                np.array([10, 20, 30, 40, 25])
             )), \
             patch('iwfm.plot.contour_levels', return_value=np.linspace(10, 40, 5)), \
             patch('matplotlib.pyplot.savefig') as mock_savefig, \
             patch('matplotlib.pyplot.close'), \
             patch('matplotlib.pyplot.subplots') as mock_subplots, \
             patch('matplotlib.pyplot.contour'), \
             patch('matplotlib.pyplot.colorbar'):
            fig_mock = MagicMock()
            ax_mock = MagicMock()
            mock_subplots.return_value = (fig_mock, ax_mock)

            # Should not raise error with shapely Polygon
            iwfm_map_params(dataset, bounding_poly, image_basename, verbose=False)

            mock_savefig.assert_called_once()


class TestIwfmMapParamsEdgeCases:
    """Edge case tests for iwfm_map_params."""

    def test_custom_colormap(self, tmp_path):
        """Test custom colormap parameter."""
        # Need at least 4 non-collinear points for scipy griddata
        dataset = [
            [0, 0, 10], [4, 0, 20], [4, 4, 30], [0, 4, 40], [2, 2, 25]
        ]
        bounding_poly = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
        image_basename = str(tmp_path / "cmap_map")

        with patch('iwfm.plot.get_XYvalues', return_value=(
                np.array([0, 4, 4, 0, 2]),
                np.array([0, 0, 4, 4, 2]),
                np.array([10, 20, 30, 40, 25])
             )), \
             patch('iwfm.plot.contour_levels', return_value=np.linspace(10, 40, 5)), \
             patch('matplotlib.pyplot.savefig'), \
             patch('matplotlib.pyplot.close'), \
             patch('matplotlib.pyplot.subplots') as mock_subplots, \
             patch('matplotlib.pyplot.contour') as mock_contour, \
             patch('matplotlib.pyplot.colorbar'):
            fig_mock = MagicMock()
            ax_mock = MagicMock()
            mock_subplots.return_value = (fig_mock, ax_mock)

            iwfm_map_params(dataset, bounding_poly, image_basename, cmap='viridis', verbose=False)

            # Verify contour was called with viridis cmap
            call_args = mock_contour.call_args
            assert call_args.kwargs.get('cmap') == 'viridis'

    def test_custom_levels(self, tmp_path):
        """Test custom number of contour levels."""
        # Need at least 4 non-collinear points for scipy griddata
        dataset = [
            [0, 0, 10], [4, 0, 20], [4, 4, 30], [0, 4, 40], [2, 2, 25]
        ]
        bounding_poly = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
        image_basename = str(tmp_path / "levels_map")

        with patch('iwfm.plot.get_XYvalues', return_value=(
                np.array([0, 4, 4, 0, 2]),
                np.array([0, 0, 4, 4, 2]),
                np.array([10, 20, 30, 40, 25])
             )), \
             patch('iwfm.plot.contour_levels', return_value=np.linspace(10, 40, 10)) as mock_levels, \
             patch('matplotlib.pyplot.savefig'), \
             patch('matplotlib.pyplot.close'), \
             patch('matplotlib.pyplot.subplots') as mock_subplots, \
             patch('matplotlib.pyplot.contour'), \
             patch('matplotlib.pyplot.colorbar'):
            fig_mock = MagicMock()
            ax_mock = MagicMock()
            mock_subplots.return_value = (fig_mock, ax_mock)

            iwfm_map_params(dataset, bounding_poly, image_basename, no_levels=10, verbose=False)

            # contour_levels should be called with no_levels=10
            mock_levels.assert_called_once()
            call_kwargs = mock_levels.call_args.kwargs
            assert call_kwargs.get('no_levels') == 10
