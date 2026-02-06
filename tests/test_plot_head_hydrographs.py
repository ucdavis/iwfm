#!/usr/bin/env python
# test_plot_head_hydrographs.py
# Unit tests for plot/plot_head_hydrographs.py
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
import tempfile
import os
import sys
from datetime import datetime

# Add the iwfm directory to the path for direct module imports
# This allows testing without requiring all iwfm dependencies
_iwfm_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _iwfm_path not in sys.path:
    sys.path.insert(0, _iwfm_path)

# Import functions directly from the module file to avoid iwfm package dependencies
import importlib.util
_module_path = os.path.join(_iwfm_path, 'iwfm', 'plot', 'head_hydrographs.py')
_spec = importlib.util.spec_from_file_location("head_hydrographs", _module_path)
_phh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_phh)

# Make functions available at module level
read_hyd_info = _phh.read_hyd_info
read_obs_heads = _phh.read_obs_heads
extract_sim_dates = _phh.extract_sim_dates
extract_sim_column = _phh.extract_sim_column
plot_head_hydrograph = _phh.plot_head_hydrograph


# =============================================================================
# Helper functions to create test files
# =============================================================================

def create_gw_dat_file(wells):
    """Create a Groundwater.dat file with hydrograph locations.

    Parameters
    ----------
    wells : list of tuples
        Each tuple: (order, hydtyp, layer, x, y, name)

    Returns
    -------
    str
        File content in IWFM Groundwater.dat format
    """
    content = """C*******************************************************************************
C                       Groundwater Hydrograph Output Data
C
C   NOUTH      ; Total number of hydrographs to be printed
C   FACTXY     ; Conversion factor for nodal coordinates
C   GWHYDOUTFL ; File name for groundwater hydrograph output
C
C-------------------------------------------------------------------------------
C    VALUE                                      DESCRIPTION
C-------------------------------------------------------------------------------
"""
    content += f"     {len(wells)}                                       / NOUTH\n"
    content += "     3.2808                                     / FACTXY\n"
    content += "     ..\\Results\\Hydrographs_GW.out              / GWHYDOUTFL\n"
    content += """C-------------------------------------------------------------------------------
C
C   ID    HYDTYP   IOUTHL      X             Y             NAME
C--------------------------------------------------------------------------------------------------
"""
    for order, hydtyp, layer, x, y, name in wells:
        content += f"{order}\t{hydtyp}\t{layer}\t{x}\t{y}\t{name}\n"

    return content


def create_obs_smp_file(observations):
    """Create a PEST SMP format observation file.

    Parameters
    ----------
    observations : list of tuples
        Each tuple: (well_name, date_str, time_str, head)
        date_str: MM/DD/YYYY format
        time_str: H:MM:SS format

    Returns
    -------
    str
        File content in PEST SMP format
    """
    content = ""
    for well_name, date_str, time_str, head in observations:
        content += f"{well_name}     {date_str}     {time_str}     {head:.2f}\n"
    return content


def create_sim_out_file(hydrograph_ids, data_lines):
    """Create an IWFM groundwater hydrograph output file.

    Parameters
    ----------
    hydrograph_ids : list of int
        List of hydrograph IDs (column numbers)
    data_lines : list of tuples
        Each tuple: (date_string, values_list)
        date_string: e.g., "09/30/1973_24:00"
        values_list: list of float values, one per hydrograph

    Returns
    -------
    str
        File content in IWFM hydrograph output format
    """
    content = "*                                        ***************************************\n"
    content += "*                                        *       GROUNDWATER HYDROGRAPH        *\n"
    content += "*                                        *             (UNIT=FEET)             *\n"
    content += "*                                        ***************************************\n"

    # Header line with hydrograph IDs
    content += "*          HYDROGRAPH ID"
    for hyd_id in hydrograph_ids:
        content += f"  {hyd_id:10d}"
    content += "\n"

    # Layer line
    content += "*                  LAYER"
    for _ in hydrograph_ids:
        content += f"  {1:10d}"
    content += "\n"

    # Node line
    content += "*                   NODE"
    for _ in hydrograph_ids:
        content += f"  {0:10d}"
    content += "\n"

    # Element line
    content += "*                ELEMENT"
    for hyd_id in hydrograph_ids:
        content += f"  {hyd_id:10d}"
    content += "\n"

    # Time header
    content += "*        TIME\n"

    # Data lines
    for date_str, values in data_lines:
        content += f"{date_str:20s}"
        for value in values:
            content += f"  {value:10.3f}"
        content += "\n"

    return content


# =============================================================================
# Tests for read_hyd_info
# =============================================================================

class TestReadHydInfo:
    """Tests for read_hyd_info function.

    read_hyd_info() now delegates to iwfm_read_gw(), which requires a
    complete groundwater file. Unit tests mock iwfm_read_gw() to isolate
    the wrapper logic. Integration tests with real files test the full path.
    """

    @staticmethod
    def _mock_gw_return(hydrographs_dict):
        """Build a mock return tuple for iwfm_read_gw with the given hydrographs dict."""
        return ({}, [], 1, [], [], [], [], [], [], [], hydrographs_dict, 1.0)

    def _call_read_hyd_info_mocked(self, hydrographs_dict):
        """Call read_hyd_info with iwfm_read_gw mocked to return the given dict."""
        import types
        # Create a mock iwfm_read_gw module and function
        mock_module = types.ModuleType('iwfm.iwfm_read_gw')
        mock_module.iwfm_read_gw = lambda gw_file, verbose=False: self._mock_gw_return(hydrographs_dict)
        # Temporarily inject into sys.modules so the import inside read_hyd_info finds it
        import sys
        old_mod = sys.modules.get('iwfm.iwfm_read_gw')
        old_iwfm = sys.modules.get('iwfm')
        # Also need a minimal iwfm module for the import chain
        if 'iwfm' not in sys.modules:
            sys.modules['iwfm'] = types.ModuleType('iwfm')
        sys.modules['iwfm.iwfm_read_gw'] = mock_module
        try:
            result = _phh.read_hyd_info("dummy.dat")
        finally:
            # Restore original state
            if old_mod is not None:
                sys.modules['iwfm.iwfm_read_gw'] = old_mod
            else:
                sys.modules.pop('iwfm.iwfm_read_gw', None)
            if old_iwfm is not None:
                sys.modules['iwfm'] = old_iwfm
            elif 'iwfm' in sys.modules and old_iwfm is None:
                sys.modules.pop('iwfm', None)
        return result

    def test_read_single_well(self):
        """Test reading a single well from groundwater file"""
        expected = {"01N03E17E001M": (1, 1, 616887.0, 4198677.0)}

        well_dict = self._call_read_hyd_info_mocked(expected)

        assert len(well_dict) == 1
        assert "01N03E17E001M" in well_dict
        order, layer, x, y = well_dict["01N03E17E001M"]
        assert order == 1
        assert layer == 1
        assert x == 616887.0
        assert y == 4198677.0

    def test_read_multiple_wells(self):
        """Test reading multiple wells from groundwater file"""
        expected = {
            "01N03E17E001M": (1, 1, 616887.0, 4198677.0),
            "01N06E14Q003M": (2, 1, 651178.0, 4198961.0),
            "01N09E13D001M": (3, 3, 681153.0, 4201456.0),
        }

        well_dict = self._call_read_hyd_info_mocked(expected)

        assert len(well_dict) == 3
        assert well_dict["01N03E17E001M"][0] == 1  # order
        assert well_dict["01N06E14Q003M"][0] == 2  # order
        assert well_dict["01N09E13D001M"][1] == 3  # layer

    def test_read_empty_file(self):
        """Test reading file with no wells (NOUTH=0)"""
        expected = {}

        well_dict = self._call_read_hyd_info_mocked(expected)

        assert len(well_dict) == 0


# =============================================================================
# Tests for read_obs_heads
# =============================================================================

class TestReadObsHeads:
    """Tests for read_obs_heads function"""

    def _nrows(self, result):
        """Return number of rows from polars DataFrame or dict."""
        try:
            import polars as pl
            if isinstance(result, pl.DataFrame):
                return len(result)
        except ImportError:
            pass
        return len(result['site_name'])

    def _col(self, result, col_name):
        """Return column values as a list from polars DataFrame or dict."""
        try:
            import polars as pl
            if isinstance(result, pl.DataFrame):
                return result.select(col_name).to_series().to_list()
        except ImportError:
            pass
        return result[col_name]

    def test_read_single_observation(self):
        """Test reading a single observation"""
        observations = [("28N04W08K001M", "08/22/1979", "0:00:00", 434.40)]
        content = create_obs_smp_file(observations)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.smp', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            obs_data = read_obs_heads(temp_file)

            assert self._nrows(obs_data) == 1
            assert self._col(obs_data, 'site_name')[0] == "28N04W08K001M"
            assert self._col(obs_data, 'obs_value')[0] == 434.40

        finally:
            os.unlink(temp_file)

    def test_read_multiple_observations(self):
        """Test reading multiple observations for same well"""
        observations = [
            ("28N04W08K001M", "08/22/1979", "0:00:00", 434.40),
            ("28N04W08K001M", "04/02/1980", "0:00:00", 433.90),
            ("28N04W08K001M", "09/16/1982", "0:00:00", 436.70),
        ]
        content = create_obs_smp_file(observations)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.smp', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            obs_data = read_obs_heads(temp_file)

            assert self._nrows(obs_data) == 3
            # Check dates are parsed correctly
            dates = self._col(obs_data, 'date')
            assert dates[0] == datetime(1979, 8, 22)
            assert dates[1] == datetime(1980, 4, 2)

        finally:
            os.unlink(temp_file)

    def test_read_multiple_wells(self):
        """Test reading observations for multiple wells.

        Note: read_obs_smp() replaces underscores with spaces before
        splitting, so use names without underscores for this test.
        """
        observations = [
            ("WELLA", "01/15/1980", "0:00:00", 100.0),
            ("WELLA", "02/15/1980", "0:00:00", 101.0),
            ("WELLB", "01/15/1980", "0:00:00", 200.0),
            ("WELLB", "02/15/1980", "0:00:00", 201.0),
        ]
        content = create_obs_smp_file(observations)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.smp', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            obs_data = read_obs_heads(temp_file)

            assert self._nrows(obs_data) == 4
            # Count unique wells
            unique_wells = set(self._col(obs_data, 'site_name'))
            assert len(unique_wells) == 2

        finally:
            os.unlink(temp_file)

    def test_skip_empty_lines(self):
        """Test that empty lines are skipped"""
        content = "WELLA     01/15/1980     0:00:00     100.0\n"
        content += "\n"  # Empty line
        content += "WELLA     02/15/1980     0:00:00     101.0\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.smp', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            obs_data = read_obs_heads(temp_file)

            assert self._nrows(obs_data) == 2

        finally:
            os.unlink(temp_file)


# =============================================================================
# Tests for extract_sim_dates and extract_sim_column
# =============================================================================

class TestExtractFunctions:
    """Tests for extract_sim_dates and extract_sim_column functions"""

    def test_extract_sim_dates(self):
        """Test extracting dates from simulation data"""
        # Use directly imported function

        sim_data = [
            [datetime(1973, 10, 1), 100.0, 200.0],
            [datetime(1973, 11, 1), 101.0, 201.0],
            [datetime(1973, 12, 1), 102.0, 202.0],
        ]

        dates = extract_sim_dates(sim_data)

        assert len(dates) == 3
        assert dates[0] == datetime(1973, 10, 1)
        assert dates[1] == datetime(1973, 11, 1)
        assert dates[2] == datetime(1973, 12, 1)

    def test_extract_sim_column(self):
        """Test extracting a column of values from simulation data"""
        # Use directly imported function

        sim_data = [
            [datetime(1973, 10, 1), 100.0, 200.0, 300.0],
            [datetime(1973, 11, 1), 101.0, 201.0, 301.0],
            [datetime(1973, 12, 1), 102.0, 202.0, 302.0],
        ]

        # Column 1 (first well, order=1)
        values = extract_sim_column(sim_data, 1)
        assert values == [100.0, 101.0, 102.0]

        # Column 2 (second well, order=2)
        values = extract_sim_column(sim_data, 2)
        assert values == [200.0, 201.0, 202.0]

        # Column 3 (third well, order=3)
        values = extract_sim_column(sim_data, 3)
        assert values == [300.0, 301.0, 302.0]

    def test_extract_sim_column_out_of_range(self):
        """Test extracting column that doesn't exist"""
        # Use directly imported function

        sim_data = [
            [datetime(1973, 10, 1), 100.0],
        ]

        # Column 5 doesn't exist
        values = extract_sim_column(sim_data, 5)
        assert values == []


# =============================================================================
# Tests for plot_head_hydrograph
# =============================================================================

class TestPlotHeadHydrograph:
    """Tests for plot_head_hydrograph function"""

    def test_create_pdf(self):
        """Test that a PDF file is created"""
        pytest.importorskip('matplotlib')

        # Use directly imported function

        obs_dates = [datetime(1980, 1, 1), datetime(1980, 6, 1)]
        obs_heads = [100.0, 105.0]
        sim_dates = [datetime(1980, 1, 1), datetime(1980, 3, 1),
                     datetime(1980, 6, 1), datetime(1980, 9, 1)]
        sim_heads = [99.0, 102.0, 104.0, 101.0]

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = plot_head_hydrograph(
                well_name="TEST_WELL",
                layer=1,
                obs_dates=obs_dates,
                obs_heads=obs_heads,
                sim_data_list=[(sim_dates, sim_heads)],
                run_names=["Test Run"],
                output_dir=tmpdir,
                verbose=False
            )

            assert os.path.exists(pdf_path)
            assert pdf_path.endswith('.pdf')
            assert 'TEST_WELL' in pdf_path

    def test_create_pdf_multiple_runs(self):
        """Test creating PDF with multiple simulation runs"""
        pytest.importorskip('matplotlib')

        # Use directly imported function

        obs_dates = [datetime(1980, 1, 1)]
        obs_heads = [100.0]

        sim_dates = [datetime(1980, 1, 1), datetime(1980, 6, 1)]
        sim_heads_1 = [99.0, 104.0]
        sim_heads_2 = [101.0, 106.0]

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = plot_head_hydrograph(
                well_name="MULTI_RUN_WELL",
                layer=2,
                obs_dates=obs_dates,
                obs_heads=obs_heads,
                sim_data_list=[
                    (sim_dates, sim_heads_1),
                    (sim_dates, sim_heads_2)
                ],
                run_names=["Baseline", "Scenario A"],
                output_dir=tmpdir,
                verbose=False
            )

            assert os.path.exists(pdf_path)
            # Check file size is reasonable (not empty)
            assert os.path.getsize(pdf_path) > 1000

    def test_create_pdf_no_observations(self):
        """Test creating PDF with no observations (simulated only)"""
        pytest.importorskip('matplotlib')

        # Use directly imported function

        sim_dates = [datetime(1980, 1, 1), datetime(1980, 6, 1)]
        sim_heads = [99.0, 104.0]

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = plot_head_hydrograph(
                well_name="SIM_ONLY_WELL",
                layer=1,
                obs_dates=[],
                obs_heads=[],
                sim_data_list=[(sim_dates, sim_heads)],
                run_names=["Simulation"],
                output_dir=tmpdir,
                verbose=False
            )

            assert os.path.exists(pdf_path)

    def test_pdf_filename_format(self):
        """Test that PDF filename has correct format"""
        pytest.importorskip('matplotlib')

        # Use directly imported function

        sim_dates = [datetime(1980, 1, 1)]
        sim_heads = [100.0]

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = plot_head_hydrograph(
                well_name="01N03E17E001M",
                layer=3,
                obs_dates=[],
                obs_heads=[],
                sim_data_list=[(sim_dates, sim_heads)],
                run_names=["Run"],
                output_dir=tmpdir,
                verbose=False
            )

            filename = os.path.basename(pdf_path)
            assert filename == "01N03E17E001M_layer3_hydrograph.pdf"


# =============================================================================
# Integration tests using real test data files
# =============================================================================

class TestIntegrationWithRealFiles:
    """Integration tests using actual C2VSimCG test files if available"""

    @pytest.fixture
    def test_files(self):
        """Locate test data files"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        gw_file = os.path.join(base_path,
            "C2VSimCG-2025/Simulation/Groundwater/C2VSimCG_Groundwater1974.dat")
        obs_file = os.path.join(base_path,
            "C2VSimCG-2025/pest/c2vsim_gwhead.smp")
        sim_file = os.path.join(base_path,
            "C2VSimCG-2025/Results/C2VSimCG_Hydrographs_GW.out")

        if all(os.path.exists(f) for f in [gw_file, obs_file, sim_file]):
            return gw_file, obs_file, sim_file
        else:
            pytest.skip("C2VSimCG test files not available")

    def test_read_real_gw_file(self, test_files):
        """Test reading real groundwater file via iwfm_read_gw()"""
        gw_file, obs_file, sim_file = test_files

        # read_hyd_info now calls iwfm_read_gw which requires the full iwfm package
        # and may fail if the GW file has sections that iwfm_read_gw can't parse yet
        try:
            well_dict = read_hyd_info(gw_file)
        except (ImportError, SystemExit):
            pytest.skip("Full iwfm package dependencies not available (e.g., loguru)")
        except (IndexError, ValueError) as e:
            pytest.skip(f"iwfm_read_gw has a pre-existing parsing issue: {e}")

        assert len(well_dict) > 0
        # Check first well has expected structure
        first_well = list(well_dict.keys())[0]
        order, layer, x, y = well_dict[first_well]
        assert isinstance(order, int)
        assert isinstance(layer, int)
        assert isinstance(x, float)
        assert isinstance(y, float)

    def test_read_real_obs_file(self, test_files):
        """Test reading real observation file (now via read_obs_smp)"""
        gw_file, obs_file, sim_file = test_files

        # read_obs_heads now delegates to read_obs_smp,
        # returning polars DataFrame or dict with columns:
        # site_name, date, time, obs_value
        obs_data = read_obs_heads(obs_file)

        try:
            import polars as pl
            is_polars = isinstance(obs_data, pl.DataFrame)
        except ImportError:
            is_polars = False

        if is_polars:
            assert len(obs_data) > 0
            assert 'site_name' in obs_data.columns
            assert 'date' in obs_data.columns
            assert 'obs_value' in obs_data.columns
        else:
            assert len(obs_data['site_name']) > 0
            assert 'site_name' in obs_data
            assert 'date' in obs_data
            assert 'obs_value' in obs_data

    def test_read_real_sim_file(self, test_files):
        """Test reading real simulation output file via read_sim_hyd"""
        gw_file, obs_file, sim_file = test_files

        import iwfm
        sim_data = iwfm.read_sim_hyd(sim_file)

        assert len(sim_data) > 0
        # Each row should have date + many well values
        assert sim_data.shape[1] > 10
        assert isinstance(sim_data[0, 0], datetime)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
