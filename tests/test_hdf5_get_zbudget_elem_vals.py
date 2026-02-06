# test_hdf5_get_zbudget_elem_vals.py
# Tests for hdf5/get_zbudget_elem_vals_pywfm.py - Get element values from ZBudget using pywfm
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
from unittest.mock import Mock
import pandas as pd
from datetime import datetime

# Check if pywfm is available
try:
    import pywfm  # noqa: F401
    del pywfm
    HAS_PYWFM = True
except ImportError:
    HAS_PYWFM = False


class TestGetZbudgetElemValsImports:
    """Tests for get_zbudget_elem_vals imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import get_zbudget_elem_vals
        assert callable(get_zbudget_elem_vals)

    @pytest.mark.skipif(not HAS_PYWFM, reason="pywfm not installed")
    def test_import_pywfm_directly(self):
        """Test direct module import of pywfm version."""
        from iwfm.hdf5.get_zbudget_elem_vals_pywfm import get_zbudget_elem_vals
        assert callable(get_zbudget_elem_vals)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.hdf5 import get_zbudget_elem_vals

        assert get_zbudget_elem_vals.__doc__ is not None
        assert 'zbudget' in get_zbudget_elem_vals.__doc__.lower()


@pytest.mark.skipif(not HAS_PYWFM, reason="pywfm not installed")
class TestGetZbudgetElemValsSignaturePywfm:
    """Tests for get_zbudget_elem_vals_pywfm function signature."""

    def test_function_signature(self):
        """Test that get_zbudget_elem_vals has correct function signature."""
        from iwfm.hdf5.get_zbudget_elem_vals_pywfm import get_zbudget_elem_vals
        import inspect

        sig = inspect.signature(get_zbudget_elem_vals)
        params = list(sig.parameters.keys())

        assert 'zbud' in params
        assert 'zones_file' in params
        assert 'col_ids' in params
        assert 'area_conversion_factor' in params
        assert 'area_units' in params
        assert 'volume_conversion_factor' in params
        assert 'volume_units' in params
        assert 'verbose' in params

    def test_default_conversion_factors(self):
        """Test that default conversion factors are correct."""
        from iwfm.hdf5.get_zbudget_elem_vals_pywfm import get_zbudget_elem_vals
        import inspect

        sig = inspect.signature(get_zbudget_elem_vals)

        assert sig.parameters['area_conversion_factor'].default == 0.0000229568411
        assert sig.parameters['volume_conversion_factor'].default == 0.0000229568411

    def test_default_units(self):
        """Test that default units are correct."""
        from iwfm.hdf5.get_zbudget_elem_vals_pywfm import get_zbudget_elem_vals
        import inspect

        sig = inspect.signature(get_zbudget_elem_vals)

        assert sig.parameters['area_units'].default == 'ACRES'
        assert sig.parameters['volume_units'].default == 'ACRE-FEET'
        assert sig.parameters['verbose'].default == False


@pytest.mark.skipif(not HAS_PYWFM, reason="pywfm not installed")
class TestGetZbudgetElemValsMockedPywfm:
    """Tests for get_zbudget_elem_vals_pywfm with mocked dependencies."""

    def test_returns_tuple_of_two(self, tmp_path):
        """Test that function returns a tuple of (dates, zone_data)."""
        from iwfm.hdf5.get_zbudget_elem_vals_pywfm import get_zbudget_elem_vals

        # Create mock zone file
        zone_file = tmp_path / "zones.dat"
        zone_file.write_text("zone data")

        # Setup mock zbud object
        mock_zbud = Mock()
        mock_zbud.get_zone_list.return_value = [1, 2]

        # Create mock dataframe for zone values
        mock_df = pd.DataFrame({
            'Time': [datetime(2000, 1, 1), datetime(2000, 2, 1)],
            'Col1': [100.0, 200.0],
            'Col2': [150.0, 250.0]
        })
        mock_zbud.get_values_for_a_zone.return_value = mock_df

        result = get_zbudget_elem_vals(
            mock_zbud,
            str(zone_file),
            col_ids=[1, 2]
        )

        assert isinstance(result, tuple)
        assert len(result) == 2  # dates, zone_data

    def test_generates_zone_list_from_file(self, tmp_path):
        """Test that function calls generate_zone_list_from_file."""
        from iwfm.hdf5.get_zbudget_elem_vals_pywfm import get_zbudget_elem_vals

        zone_file = tmp_path / "zones.dat"
        zone_file.write_text("zone data")

        mock_zbud = Mock()
        mock_zbud.get_zone_list.return_value = [1]  # Need at least one zone

        mock_df = pd.DataFrame({
            'Time': [datetime(2000, 1, 1)],
            'Col1': [100.0]
        })
        mock_zbud.get_values_for_a_zone.return_value = mock_df

        get_zbudget_elem_vals(mock_zbud, str(zone_file), col_ids=[1])

        mock_zbud.generate_zone_list_from_file.assert_called_once_with(
            zone_definition_file=str(zone_file)
        )

    def test_returns_zone_data_list(self, tmp_path):
        """Test that zone_data is a list with one entry per zone."""
        from iwfm.hdf5.get_zbudget_elem_vals_pywfm import get_zbudget_elem_vals

        zone_file = tmp_path / "zones.dat"
        zone_file.write_text("zone data")

        mock_zbud = Mock()
        mock_zbud.get_zone_list.return_value = [1, 2, 3]

        mock_df = pd.DataFrame({
            'Time': [datetime(2000, 1, 1)],
            'Col1': [100.0]
        })
        mock_zbud.get_values_for_a_zone.return_value = mock_df

        dates, zone_data = get_zbudget_elem_vals(
            mock_zbud,
            str(zone_file),
            col_ids=[1]
        )

        assert isinstance(zone_data, list)
        assert len(zone_data) == 3  # One entry per zone

    def test_zone_data_contains_zone_id(self, tmp_path):
        """Test that each zone_data entry starts with zone ID."""
        from iwfm.hdf5.get_zbudget_elem_vals_pywfm import get_zbudget_elem_vals

        zone_file = tmp_path / "zones.dat"
        zone_file.write_text("zone data")

        mock_zbud = Mock()
        mock_zbud.get_zone_list.return_value = [1]

        mock_df = pd.DataFrame({
            'Time': [datetime(2000, 1, 1)],
            'Col1': [100.0]
        })
        mock_zbud.get_values_for_a_zone.return_value = mock_df

        dates, zone_data = get_zbudget_elem_vals(
            mock_zbud,
            str(zone_file),
            col_ids=[1]
        )

        # First element of zone_data[0] should be zone ID (1-indexed)
        assert zone_data[0][0] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
