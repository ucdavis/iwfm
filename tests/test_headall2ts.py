# test_headall2ts.py
# Tests for headall2ts function
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

"""
Tests for iwfm.headall2ts function.

The headall2ts function reads an IWFM HeadAll.out file and writes out a
time series with one CSV file for each layer.

Example files used for testing:
- HeadAll file: iwfm/tests/C2VSimCG-2021/Results/C2VSimCG_GW_HeadAll.out

C2VSimCG model characteristics (truncated test data):
- 1,393 nodes
- 4 layers
- Date range: 09/30/1973 to 09/30/1974 (13 timesteps)

Output format:
- One CSV file per layer (e.g., basename_1.csv, basename_2.csv, etc.)
- Columns: Node, then one column per date
- Rows: One row per node
"""

import pytest
import os
import sys
import inspect
import tempfile
import glob

# Add the iwfm directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from iwfm.headall2ts import headall2ts

# Path to example files
EXAMPLE_HEADALL_FILE = os.path.join(
    os.path.dirname(__file__),
    'C2VSimCG-2021', 'Results', 'C2VSimCG_GW_HeadAll.out'
)

# Check if example files exist
EXAMPLE_FILES_EXIST = os.path.exists(EXAMPLE_HEADALL_FILE)

# Check if polars is available (required by headall2csv)
try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False

# Combined check for all dependencies
ALL_DEPS_AVAILABLE = EXAMPLE_FILES_EXIST and POLARS_AVAILABLE


class TestHeadall2TsFunctionExists:
    """Test that headall2ts function exists and has correct signature."""

    def test_function_exists(self):
        """Test that headall2ts function is importable."""
        assert headall2ts is not None

    def test_function_is_callable(self):
        """Test that headall2ts is callable."""
        assert callable(headall2ts)

    def test_function_has_docstring(self):
        """Test that headall2ts has a docstring."""
        assert headall2ts.__doc__ is not None
        assert len(headall2ts.__doc__) > 0

    def test_function_signature(self):
        """Test that headall2ts has the expected parameters."""
        sig = inspect.signature(headall2ts)
        params = list(sig.parameters.keys())

        assert 'input_file' in params
        assert 'output_file' in params
        assert 'verbose' in params


class TestHeadall2TsParameters:
    """Test headall2ts parameter handling."""

    def test_verbose_default_is_false(self):
        """Test that verbose parameter defaults to False."""
        sig = inspect.signature(headall2ts)
        verbose_param = sig.parameters['verbose']
        assert verbose_param.default is False


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="polars or example files not available")
class TestHeadall2TsOutputFiles:
    """Test that headall2ts creates output files."""

    def test_creates_csv_files(self):
        """Test that headall2ts creates CSV files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # Should create one file per layer
            csv_files = glob.glob(os.path.join(temp_dir, '*.csv'))
            assert len(csv_files) == layers

    def test_creates_correct_number_of_files(self):
        """Test that headall2ts creates correct number of CSV files (4 for C2VSimCG)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # C2VSimCG has 4 layers
            assert layers == 4
            csv_files = glob.glob(os.path.join(temp_dir, '*.csv'))
            assert len(csv_files) == 4

    def test_file_naming_convention(self):
        """Test that output files follow naming convention (basename_N.csv)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # Check each layer file exists
            for layer in range(1, layers + 1):
                expected_file = f'{output_base}_{layer}.csv'
                assert os.path.exists(expected_file), f"Missing file: {expected_file}"


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="polars or example files not available")
class TestHeadall2TsOutputContent:
    """Test the content of output CSV files."""

    def test_csv_has_node_column(self):
        """Test that CSV files have a Node column."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # Read first layer file
            csv_file = f'{output_base}_1.csv'
            df = pl.read_csv(csv_file)

            assert 'Node' in df.columns

    def test_csv_has_date_columns(self):
        """Test that CSV files have date columns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # Read first layer file
            csv_file = f'{output_base}_1.csv'
            df = pl.read_csv(csv_file)

            # Should have Node column plus date columns
            assert len(df.columns) > 1

            # Check for expected date format (MM/DD/YYYY)
            date_cols = [c for c in df.columns if c != 'Node']
            assert len(date_cols) > 0
            # First date should be 09/30/1973
            assert '09/30/1973' in date_cols

    def test_csv_has_correct_number_of_rows(self):
        """Test that CSV files have correct number of rows (1393 nodes)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # Read first layer file
            csv_file = f'{output_base}_1.csv'
            df = pl.read_csv(csv_file)

            # C2VSimCG has 1393 nodes
            assert len(df) == 1393

    def test_csv_has_correct_number_of_columns(self):
        """Test that CSV files have correct number of columns (1 + 13 dates)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # Read first layer file
            csv_file = f'{output_base}_1.csv'
            df = pl.read_csv(csv_file)

            # 1 Node column + 13 date columns (truncated test data)
            assert len(df.columns) == 14

    def test_node_ids_are_sequential(self):
        """Test that Node IDs are present and sequential (1 to 1393)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            csv_file = f'{output_base}_1.csv'
            df = pl.read_csv(csv_file)

            nodes = df['Node'].to_list()
            assert min(nodes) == 1
            assert max(nodes) == 1393


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="polars or example files not available")
class TestHeadall2TsReturnValue:
    """Test the return value of headall2ts."""

    def test_returns_int(self):
        """Test that headall2ts returns an integer."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            result = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            assert isinstance(result, int)

    def test_returns_layer_count(self):
        """Test that headall2ts returns the number of layers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # C2VSimCG has 4 layers
            assert layers == 4


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="polars or example files not available")
class TestHeadall2TsVerbose:
    """Test verbose output of headall2ts."""

    def test_verbose_false_no_output(self, capsys):
        """Test that verbose=False produces no output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base, verbose=False)

            captured = capsys.readouterr()
            assert captured.out == ''

    def test_verbose_true_produces_output(self, capsys):
        """Test that verbose=True produces output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base, verbose=True)

            captured = capsys.readouterr()
            assert len(captured.out) > 0

    def test_verbose_output_mentions_layers(self, capsys):
        """Test that verbose output mentions layer numbers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base, verbose=True)

            captured = capsys.readouterr()
            # Should mention each layer
            for layer in range(1, layers + 1):
                assert f'layer {layer}' in captured.out


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="polars or example files not available")
class TestHeadall2TsDataIntegrity:
    """Test data integrity of output CSV files."""

    def test_all_layers_same_node_count(self):
        """Test that all layer files have the same number of nodes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            row_counts = []
            for layer in range(1, layers + 1):
                csv_file = f'{output_base}_{layer}.csv'
                df = pl.read_csv(csv_file)
                row_counts.append(len(df))

            # All layers should have same node count
            assert len(set(row_counts)) == 1

    def test_all_layers_same_date_columns(self):
        """Test that all layer files have the same date columns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            column_sets = []
            for layer in range(1, layers + 1):
                csv_file = f'{output_base}_{layer}.csv'
                df = pl.read_csv(csv_file)
                column_sets.append(set(df.columns))

            # All layers should have same columns
            first_cols = column_sets[0]
            for cols in column_sets[1:]:
                assert cols == first_cols

    def test_head_values_are_numeric(self):
        """Test that head values are numeric."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            csv_file = f'{output_base}_1.csv'
            df = pl.read_csv(csv_file)

            # Get first date column (not Node)
            date_cols = [c for c in df.columns if c != 'Node']
            first_date_col = date_cols[0]

            # Values should be numeric (floats)
            col_dtype = df[first_date_col].dtype
            assert col_dtype in [pl.Float64, pl.Float32, pl.Int64, pl.Int32]


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="polars or example files not available")
class TestHeadall2TsOutputPath:
    """Test output path handling."""

    def test_output_to_different_directory(self):
        """Test that output files are created in specified directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a subdirectory
            sub_dir = os.path.join(temp_dir, 'subdir')
            os.makedirs(sub_dir)
            output_base = os.path.join(sub_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # Files should be in subdirectory
            for layer in range(1, layers + 1):
                expected_file = f'{output_base}_{layer}.csv'
                assert os.path.exists(expected_file)

    def test_output_base_with_special_characters(self):
        """Test output base with spaces in path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create directory with space
            sub_dir = os.path.join(temp_dir, 'sub dir')
            os.makedirs(sub_dir)
            output_base = os.path.join(sub_dir, 'heads ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            # Files should be created
            for layer in range(1, layers + 1):
                expected_file = f'{output_base}_{layer}.csv'
                assert os.path.exists(expected_file)


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="polars or example files not available")
class TestHeadall2TsC2VSimCGSpecific:
    """Test C2VSimCG-specific expectations."""

    def test_c2vsimcg_layer_count(self):
        """Test that C2VSimCG has 4 layers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            layers = headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            assert layers == 4

    def test_c2vsimcg_node_count(self):
        """Test that C2VSimCG has 1393 nodes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            csv_file = f'{output_base}_1.csv'
            df = pl.read_csv(csv_file)

            assert len(df) == 1393

    def test_c2vsimcg_date_range(self):
        """Test that C2VSimCG date range is correct (truncated test data)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            csv_file = f'{output_base}_1.csv'
            df = pl.read_csv(csv_file)

            date_cols = [c for c in df.columns if c != 'Node']

            # First date should be 09/30/1973
            assert date_cols[0] == '09/30/1973'

            # Last date should be 09/30/1974 (truncated test data)
            assert date_cols[-1] == '09/30/1974'

    def test_c2vsimcg_timestep_count(self):
        """Test that C2VSimCG has 13 timesteps (truncated test data)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads_ts')

            headall2ts(EXAMPLE_HEADALL_FILE, output_base)

            csv_file = f'{output_base}_1.csv'
            df = pl.read_csv(csv_file)

            date_cols = [c for c in df.columns if c != 'Node']

            assert len(date_cols) == 13
