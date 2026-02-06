# test_hdf5_get_zbudget_data_h5.py
# Tests for hdf5/get_zbudget_data_h5.py - h5py-based zone budget data reader
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
TEST_DATA_DIR = os.path.dirname(__file__)
TEST_ZBUDGET_FILE = os.path.join(TEST_DATA_DIR, 'C2VSimCG-2021', 'Results', 'C2VSimCG_GW_ZBudget.hdf')
TEST_ZONE_FILE = os.path.join(TEST_DATA_DIR, 'C2VSimCG-2021', 'ZBudget', 'C2VSimCG_ZBudget_SRs.dat')


class TestGetZbudgetDataH5Imports:
    """Tests for get_zbudget_data_h5 imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import get_zbudget_data
        assert callable(get_zbudget_data)

    @pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.get_zbudget_data_h5 import get_zbudget_data
        assert callable(get_zbudget_data)

    @pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.hdf5.get_zbudget_data_h5 import get_zbudget_data

        assert get_zbudget_data.__doc__ is not None
        assert 'zone' in get_zbudget_data.__doc__.lower()


class TestGetZbudgetDataH5Signature:
    """Tests for get_zbudget_data_h5 function signature."""

    @pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
    def test_function_signature(self):
        """Test that get_zbudget_data has correct function signature."""
        from iwfm.hdf5.get_zbudget_data_h5 import get_zbudget_data
        import inspect

        sig = inspect.signature(get_zbudget_data)
        params = list(sig.parameters.keys())

        assert 'zbud_file' in params
        assert 'zone_file' in params
        assert 'area_conversion_factor' in params
        assert 'volume_conversion_factor' in params
        assert 'area_units' in params
        assert 'volume_units' in params
        assert 'verbose' in params

    @pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
    def test_default_conversion_factors(self):
        """Test that default conversion factors are correct."""
        from iwfm.hdf5.get_zbudget_data_h5 import get_zbudget_data
        import inspect

        sig = inspect.signature(get_zbudget_data)

        assert sig.parameters['area_conversion_factor'].default == 0.0000229568411
        assert sig.parameters['volume_conversion_factor'].default == 0.0000229568411


@pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
@pytest.mark.skipif(
    not (os.path.exists(TEST_ZBUDGET_FILE) and os.path.exists(TEST_ZONE_FILE)),
    reason="Test data not available"
)
class TestGetZbudgetDataH5WithRealData:
    """Tests for get_zbudget_data_h5 with real HDF5 data."""

    def test_reads_zbudget_file(self):
        """Test that function reads zbudget file successfully."""
        from iwfm.hdf5.get_zbudget_data_h5 import get_zbudget_data

        result = get_zbudget_data(TEST_ZBUDGET_FILE, TEST_ZONE_FILE)

        zone_names, column_headers, zone_values, titles, zone_list, zone_extent_ids = result

        assert len(zone_names) > 0
        assert len(column_headers) > 0
        assert len(zone_values) > 0
        assert len(titles) > 0
        assert len(zone_list) > 0

    def test_returns_correct_structure(self):
        """Test that return values have correct structure."""
        from iwfm.hdf5.get_zbudget_data_h5 import get_zbudget_data

        zone_names, column_headers, zone_values, titles, zone_list, zone_extent_ids = get_zbudget_data(
            TEST_ZBUDGET_FILE, TEST_ZONE_FILE
        )

        # zone_names should be a list of strings
        assert isinstance(zone_names, list)
        assert all(isinstance(name, str) for name in zone_names)

        # zone_list should be list of integers
        assert isinstance(zone_list, list)
        assert all(isinstance(z, int) for z in zone_list)

        # zone_values should be list of DataFrames
        assert isinstance(zone_values, list)
        assert all(hasattr(df, 'columns') for df in zone_values)

        # zone_extent_ids should be int (1 or 0)
        assert zone_extent_ids in [0, 1]

    def test_has_expected_zones(self):
        """Test that expected zones are present."""
        from iwfm.hdf5.get_zbudget_data_h5 import get_zbudget_data

        zone_names, _, _, _, zone_list, _ = get_zbudget_data(TEST_ZBUDGET_FILE, TEST_ZONE_FILE)

        # C2VSimCG has 21 subregions
        assert len(zone_list) == 21
        assert any('Subregion' in name for name in zone_names)

    def test_dataframe_has_time_column(self):
        """Test that DataFrames have Time column."""
        from iwfm.hdf5.get_zbudget_data_h5 import get_zbudget_data

        _, _, zone_values, _, _, _ = get_zbudget_data(TEST_ZBUDGET_FILE, TEST_ZONE_FILE)

        for df in zone_values:
            assert 'Time' in df.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
