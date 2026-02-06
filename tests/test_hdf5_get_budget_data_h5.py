# test_hdf5_get_budget_data_h5.py
# Tests for hdf5/get_budget_data_h5.py - h5py-based budget data reader
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
import os

# Check if h5py is available
try:
    import h5py  # noqa: F401
    del h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False

# Path to test data
TEST_DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    'C2VSimCG-2021', 'Results'
)
TEST_BUDGET_FILE = os.path.join(TEST_DATA_DIR, 'C2VSimCG_GW_Budget.hdf')


class TestGetBudgetDataH5Imports:
    """Tests for get_budget_data_h5 imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import get_budget_data
        assert callable(get_budget_data)

    @pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.get_budget_data_h5 import get_budget_data
        assert callable(get_budget_data)

    @pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.hdf5.get_budget_data_h5 import get_budget_data

        assert get_budget_data.__doc__ is not None
        assert 'budget' in get_budget_data.__doc__.lower()


class TestGetBudgetDataH5Signature:
    """Tests for get_budget_data_h5 function signature."""

    @pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
    def test_function_signature(self):
        """Test that get_budget_data has correct function signature."""
        from iwfm.hdf5.get_budget_data_h5 import get_budget_data
        import inspect

        sig = inspect.signature(get_budget_data)
        params = list(sig.parameters.keys())

        assert 'bud_file' in params
        assert 'area_conversion_factor' in params
        assert 'volume_conversion_factor' in params
        assert 'length_units' in params
        assert 'area_units' in params
        assert 'volume_units' in params
        assert 'verbose' in params

    @pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
    def test_default_conversion_factors(self):
        """Test that default conversion factors are correct."""
        from iwfm.hdf5.get_budget_data_h5 import get_budget_data
        import inspect

        sig = inspect.signature(get_budget_data)

        # 0.0000229568411 converts sq ft to acres
        assert sig.parameters['area_conversion_factor'].default == 0.0000229568411
        assert sig.parameters['volume_conversion_factor'].default == 0.0000229568411


@pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
@pytest.mark.skipif(not os.path.exists(TEST_BUDGET_FILE), reason="Test data not available")
class TestGetBudgetDataH5WithRealData:
    """Tests for get_budget_data_h5 with real HDF5 data."""

    def test_reads_budget_file(self):
        """Test that function reads budget file successfully."""
        from iwfm.hdf5.get_budget_data_h5 import get_budget_data

        loc_names, column_headers, loc_values, titles = get_budget_data(TEST_BUDGET_FILE)

        assert len(loc_names) > 0
        assert len(column_headers) > 0
        assert len(loc_values) > 0
        assert len(titles) > 0

    def test_returns_correct_structure(self):
        """Test that return values have correct structure."""
        from iwfm.hdf5.get_budget_data_h5 import get_budget_data

        loc_names, column_headers, loc_values, titles = get_budget_data(TEST_BUDGET_FILE)

        # loc_names should be a list of strings
        assert isinstance(loc_names, list)
        assert all(isinstance(name, str) for name in loc_names)

        # column_headers should be list of lists
        assert isinstance(column_headers, list)

        # loc_values should be list of DataFrames
        assert isinstance(loc_values, list)
        assert all(hasattr(df, 'columns') for df in loc_values)

        # titles should be list of tuples
        assert isinstance(titles, list)

    def test_has_expected_locations(self):
        """Test that expected locations are present."""
        from iwfm.hdf5.get_budget_data_h5 import get_budget_data

        loc_names, _, _, _ = get_budget_data(TEST_BUDGET_FILE)

        # C2VSimCG has subregions
        assert any('Subregion' in name for name in loc_names)

    def test_dataframe_has_time_column(self):
        """Test that DataFrames have Time column."""
        from iwfm.hdf5.get_budget_data_h5 import get_budget_data

        _, _, loc_values, _ = get_budget_data(TEST_BUDGET_FILE)

        for df in loc_values:
            assert 'Time' in df.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
