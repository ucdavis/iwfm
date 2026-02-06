# test_plot_iwfm_map_params.py
# Unit tests for plot/iwfm_map_params.py
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

import os
import pytest
import numpy as np
from unittest.mock import patch
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path


# ---------------------------------------------------------------------------
# Load the module under test directly from file to avoid circular imports
# ---------------------------------------------------------------------------
def _load_module():
    base = Path(__file__).resolve().parents[1] / "iwfm" / "plot" / "iwfm_map_params.py"
    spec = spec_from_file_location("iwfm_map_params", str(base))
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

map_params_mod = _load_module()
get_params = map_params_mod.get_params
iwfm_map_params = map_params_mod.iwfm_map_params
INPUT_DICT = map_params_mod.INPUT_DICT
CATEGORY_TO_FILETYPE = map_params_mod.CATEGORY_TO_FILETYPE
CATEGORY_DISPATCH = map_params_mod.CATEGORY_DISPATCH
RZ_SUBFILE_MAP = map_params_mod.RZ_SUBFILE_MAP


# ===========================================================================
# Tests for INPUT_DICT
# ===========================================================================
class TestInputDict:
    """Tests for the module-level INPUT_DICT."""

    def test_input_dict_not_empty(self):
        assert len(INPUT_DICT) > 0

    def test_all_entries_have_category_and_description(self):
        for key, val in INPUT_DICT.items():
            assert isinstance(val, list), f"INPUT_DICT['{key}'] is not a list"
            assert len(val) == 2, f"INPUT_DICT['{key}'] should have 2 elements"
            assert isinstance(val[0], str), f"INPUT_DICT['{key}'][0] should be str"
            assert isinstance(val[1], str), f"INPUT_DICT['{key}'][1] should be str"

    def test_all_categories_in_dispatch(self):
        """Every category in INPUT_DICT should appear in CATEGORY_DISPATCH."""
        for key, val in INPUT_DICT.items():
            category = val[0]
            assert category in CATEGORY_DISPATCH, \
                f"Category '{category}' for param '{key}' not in CATEGORY_DISPATCH"

    def test_all_categories_in_filetype_map(self):
        """Every category in INPUT_DICT should appear in CATEGORY_TO_FILETYPE."""
        for key, val in INPUT_DICT.items():
            category = val[0]
            assert category in CATEGORY_TO_FILETYPE, \
                f"Category '{category}' for param '{key}' not in CATEGORY_TO_FILETYPE"

    def test_all_param_types_in_dispatch_index(self):
        """Every param keyword should be in the index dict for its category."""
        for key, val in INPUT_DICT.items():
            category = val[0]
            _, param_index, _ = CATEGORY_DISPATCH[category]
            assert key in param_index, \
                f"Param '{key}' not in dispatch index for category '{category}'"


# ===========================================================================
# Tests for CATEGORY_TO_FILETYPE
# ===========================================================================
class TestCategoryToFiletype:
    """Tests for the CATEGORY_TO_FILETYPE mapping."""

    def test_groundwater_maps_to_gw_file(self):
        assert CATEGORY_TO_FILETYPE['Groundwater'] == 'gw_file'

    def test_rootzone_subtypes_map_to_root_file(self):
        for cat in ['Rootzone', 'Non-ponded', 'Ponded', 'Urban', 'Native']:
            assert CATEGORY_TO_FILETYPE[cat] == 'root_file'

    def test_et_maps_to_et_file(self):
        assert CATEGORY_TO_FILETYPE['ET'] == 'et_file'

    def test_precip_maps_to_precip_file(self):
        assert CATEGORY_TO_FILETYPE['Precip'] == 'precip_file'


# ===========================================================================
# Tests for RZ_SUBFILE_MAP
# ===========================================================================
class TestRzSubfileMap:
    """Tests for the RZ_SUBFILE_MAP."""

    def test_has_expected_keys(self):
        expected = {'Non-ponded', 'Ponded', 'Urban', 'Native'}
        assert set(RZ_SUBFILE_MAP.keys()) == expected

    def test_rootzone_not_in_subfile_map(self):
        """Rootzone itself should NOT be in the subfile map."""
        assert 'Rootzone' not in RZ_SUBFILE_MAP


# ===========================================================================
# Tests for get_params()
# ===========================================================================
class TestGetParams:
    """Tests for the get_params() function."""

    def test_groundwater_returns_nodes_format(self):
        """Groundwater parameters should return 'nodes' format."""
        mock_data = [np.array([1.0, 2.0, 3.0]) for _ in range(6)]
        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data):
            data, data_format = get_params('fake.dat', 'kh',
                                           ['Groundwater', 'Kh'])
            assert data_format == 'nodes'
            np.testing.assert_array_equal(data, np.array([1.0, 2.0, 3.0]))

    def test_rootzone_returns_elements_format(self):
        """Rootzone parameters should return 'elements' format."""
        mock_data = [np.array([10.0, 20.0]) for _ in range(13)]
        with patch('iwfm.iwfm_read_rz_params', return_value=mock_data):
            data, data_format = get_params('fake.dat', 'wp',
                                           ['Rootzone', 'Wilting point'])
            assert data_format == 'elements'

    def test_unknown_category_raises_valueerror(self):
        """Unknown category should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown category"):
            get_params('fake.dat', 'bad', ['BadCategory', 'desc'])

    def test_multilayer_selects_first_layer_by_default(self):
        """Multi-layer numpy array should select layer 0 by default."""
        layer_data = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        mock_data = [layer_data for _ in range(6)]
        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data):
            data, _ = get_params('fake.dat', 'kh',
                                 ['Groundwater', 'Kh'])
            np.testing.assert_array_equal(data, np.array([1.0, 3.0, 5.0]))

    def test_multilayer_selects_specified_layer(self):
        """Should select the layer specified by the layer parameter."""
        layer_data = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        mock_data = [layer_data for _ in range(6)]
        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data):
            data, _ = get_params('fake.dat', 'kh',
                                 ['Groundwater', 'Kh'], layer=1)
            np.testing.assert_array_equal(data, np.array([2.0, 4.0, 6.0]))

    def test_multilayer_invalid_layer_raises_valueerror(self):
        """Requesting layer beyond data range should raise ValueError."""
        layer_data = np.array([[1.0, 2.0], [3.0, 4.0]])
        mock_data = [layer_data for _ in range(6)]
        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data):
            with pytest.raises(ValueError, match="Requested layer 10"):
                get_params('fake.dat', 'kh',
                           ['Groundwater', 'Kh'], layer=9)

    def test_list_of_lists_multilayer_handling(self):
        """Multi-value list-of-lists should select the correct layer."""
        mock_data = [[[10, 20], [30, 40]] for _ in range(6)]
        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data):
            data, _ = get_params('fake.dat', 'kh',
                                 ['Groundwater', 'Kh'], layer=1)
            assert data == [20, 40]

    def test_1d_data_returned_unchanged(self):
        """1D data should pass through without modification."""
        mock_data = [np.array([100.0, 200.0, 300.0]) for _ in range(6)]
        with patch('iwfm.iwfm_read_gw_params', return_value=mock_data):
            data, _ = get_params('fake.dat', 'kh',
                                 ['Groundwater', 'Kh'])
            np.testing.assert_array_equal(data, np.array([100.0, 200.0, 300.0]))

    def test_each_category_dispatches_correctly(self):
        """Verify each category calls the correct reader function."""
        test_cases = {
            'Groundwater': ('iwfm_read_gw_params', 'kh', 6),
            'Rootzone':    ('iwfm_read_rz_params', 'wp', 13),
            'Non-ponded':  ('iwfm_read_rz_npc', 'cnnp', 9),
            'Ponded':      ('iwfm_read_rz_pc', 'cnpc', 9),
            'Urban':       ('iwfm_read_rz_urban', 'perv', 10),
            'Native':      ('iwfm_read_rz_nr', 'cnnv', 7),
            'Unsaturated': ('iwfm_read_uz_params', 'nuz', 6),
            'ET':          ('iwfm_read_et_vals', 'et', 1),
            'Precip':      ('iwfm_read_precip_vals', 'pr', 1),
        }
        for category, (reader_name, param_key, n_returns) in test_cases.items():
            mock_data = [np.array([1.0, 2.0]) for _ in range(n_returns)]
            with patch(f'iwfm.{reader_name}', return_value=mock_data) as mock_reader:
                data, _ = get_params('fake.dat', param_key,
                                     [category, 'description'])
                mock_reader.assert_called_once_with('fake.dat')


# ===========================================================================
# Tests for iwfm_map_params()
# ===========================================================================
class TestIwfmMapParams:
    """Tests for the iwfm_map_params() plotting function."""

    @pytest.fixture
    def sample_dataset(self):
        """Create a simple dataset for testing."""
        return [[0.0, 0.0, 1.0],
                [1.0, 0.0, 2.0],
                [1.0, 1.0, 3.0],
                [0.0, 1.0, 4.0],
                [0.5, 0.5, 2.5]]

    @pytest.fixture
    def sample_boundary(self):
        """Create a simple square boundary polygon."""
        from shapely import geometry
        return geometry.Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])

    @pytest.fixture
    def list_boundary(self):
        """Create boundary as list of tuples."""
        return [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]

    def test_creates_png_file(self, sample_dataset, sample_boundary, tmp_path):
        """Should create a PNG image file."""
        result = iwfm_map_params(sample_dataset, sample_boundary,
                                 'test_output', output_dir=str(tmp_path))
        assert os.path.exists(result)
        assert result.endswith('.png')

    def test_output_in_specified_directory(self, sample_dataset,
                                           sample_boundary, tmp_path):
        """Output file should be in the specified directory."""
        result = iwfm_map_params(sample_dataset, sample_boundary,
                                 'test_output', output_dir=str(tmp_path))
        assert str(tmp_path) in result

    def test_returns_image_path(self, sample_dataset, sample_boundary, tmp_path):
        """Should return the path to the created image."""
        result = iwfm_map_params(sample_dataset, sample_boundary,
                                 'test_output', output_dir=str(tmp_path))
        assert isinstance(result, str)
        assert 'test_output.png' in result

    def test_custom_title(self, sample_dataset, sample_boundary, tmp_path):
        """Should accept custom title without error."""
        result = iwfm_map_params(sample_dataset, sample_boundary,
                                 'test_title', title='Custom Title',
                                 output_dir=str(tmp_path))
        assert os.path.exists(result)

    def test_filled_contour(self, sample_dataset, sample_boundary, tmp_path):
        """Should create filled contour plot without error."""
        result = iwfm_map_params(sample_dataset, sample_boundary,
                                 'test_filled', contour='filled',
                                 output_dir=str(tmp_path))
        assert os.path.exists(result)

    def test_line_contour(self, sample_dataset, sample_boundary, tmp_path):
        """Should create line contour plot without error."""
        result = iwfm_map_params(sample_dataset, sample_boundary,
                                 'test_line', contour='line',
                                 output_dir=str(tmp_path))
        assert os.path.exists(result)

    def test_list_boundary(self, sample_dataset, list_boundary, tmp_path):
        """Should accept boundary as list of tuples."""
        result = iwfm_map_params(sample_dataset, list_boundary,
                                 'test_list_bnd', output_dir=str(tmp_path))
        assert os.path.exists(result)

    def test_verbose_mode(self, sample_dataset, sample_boundary, tmp_path,
                          capsys):
        """Verbose mode should print status messages."""
        iwfm_map_params(sample_dataset, sample_boundary,
                        'test_verbose', output_dir=str(tmp_path), verbose=True)
        captured = capsys.readouterr()
        assert "Image saved to" in captured.out

    def test_creates_output_dir_if_needed(self, sample_dataset,
                                           sample_boundary, tmp_path):
        """Should create output directory if it doesn't exist."""
        new_dir = str(tmp_path / 'subdir')
        result = iwfm_map_params(sample_dataset, sample_boundary,
                                 'test_mkdir', output_dir=new_dir)
        assert os.path.exists(new_dir)
        assert os.path.exists(result)

    def test_colorbar_label_with_units(self, sample_dataset,
                                       sample_boundary, tmp_path):
        """Should accept label and units without error."""
        result = iwfm_map_params(sample_dataset, sample_boundary,
                                 'test_units', label='Kh', units='ft/day',
                                 output_dir=str(tmp_path))
        assert os.path.exists(result)
