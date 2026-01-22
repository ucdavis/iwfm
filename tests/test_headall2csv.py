# test_headall2csv.py
# unit tests for headall2csv function
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
import polars as pl
from pathlib import Path


def _load_headall2csv():
    """Load the headall2csv function dynamically."""
    from importlib.util import spec_from_file_location, module_from_spec
    base = Path(__file__).resolve().parents[1] / "iwfm" / "headall2csv.py"
    spec = spec_from_file_location("headall2csv", str(base))
    assert spec is not None, "Failed to load module specification"
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return getattr(mod, "headall2csv")


headall2csv = _load_headall2csv()


class TestHeadall2csv:
    """Tests for the headall2csv function."""

    def test_basic_output(self, tmp_path):
        """Test basic CSV output for single layer."""
        # Create test data: 2 time steps, 1 layer, 3 nodes
        data = [
            [[100.0, 110.0, 120.0]],  # time step 1, layer 1
            [[105.0, 115.0, 125.0]],  # time step 2, layer 1
        ]
        layers = 1
        dates = ['01/01/2022', '02/01/2022']
        nodes = [1, 2, 3]
        output_file = str(tmp_path / "test_heads")

        headall2csv(data, layers, dates, nodes, output_file, verbose=False)

        # Check output file exists
        output_path = tmp_path / "test_heads_1.csv"
        assert output_path.exists()

        # Read and verify
        result = pl.read_csv(str(output_path))
        assert 'Node' in result.columns
        assert '01/01/2022' in result.columns
        assert '02/01/2022' in result.columns
        assert len(result) == 3  # 3 nodes

    def test_multiple_layers(self, tmp_path):
        """Test CSV output for multiple layers."""
        # Create test data: 2 time steps, 3 layers, 2 nodes
        data = [
            [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0]],  # time step 1
            [[15.0, 25.0], [35.0, 45.0], [55.0, 65.0]],  # time step 2
        ]
        layers = 3
        dates = ['01/01/2022', '02/01/2022']
        nodes = [1, 2]
        output_file = str(tmp_path / "multi_layer")

        headall2csv(data, layers, dates, nodes, output_file, verbose=False)

        # Check all layer files exist
        for i in range(1, 4):
            output_path = tmp_path / f"multi_layer_{i}.csv"
            assert output_path.exists(), f"Layer {i} file missing"

    def test_verbose_output(self, tmp_path, capsys):
        """Test that verbose mode produces output."""
        data = [[[100.0]]]
        layers = 1
        dates = ['01/01/2022']
        nodes = [1]
        output_file = str(tmp_path / "verbose_test")

        headall2csv(data, layers, dates, nodes, output_file, verbose=True)

        captured = capsys.readouterr()
        assert "Wrote layer 1" in captured.out

    def test_verbose_false_no_output(self, tmp_path, capsys):
        """Test that verbose=False produces no output."""
        data = [[[100.0]]]
        layers = 1
        dates = ['01/01/2022']
        nodes = [1]
        output_file = str(tmp_path / "quiet_test")

        headall2csv(data, layers, dates, nodes, output_file, verbose=False)

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_data_values_correct(self, tmp_path):
        """Test that data values are correctly written to CSV."""
        data = [
            [[100.5, 200.5]],  # time step 1
            [[150.5, 250.5]],  # time step 2
        ]
        layers = 1
        dates = ['2022-01', '2022-02']
        nodes = [1, 2]
        output_file = str(tmp_path / "values_test")

        headall2csv(data, layers, dates, nodes, output_file, verbose=False)

        result = pl.read_csv(str(tmp_path / "values_test_1.csv"))

        # Verify node column
        assert result['Node'].to_list() == [1, 2]

        # Verify data columns
        assert result['2022-01'].to_list() == [100.5, 200.5]
        assert result['2022-02'].to_list() == [150.5, 250.5]


class TestHeadall2csvEdgeCases:
    """Edge case tests for headall2csv."""

    def test_single_node_single_layer_single_date(self, tmp_path):
        """Test minimal input: single node, layer, and date."""
        data = [[[42.0]]]
        layers = 1
        dates = ['2022-01-01']
        nodes = [99]
        output_file = str(tmp_path / "minimal")

        headall2csv(data, layers, dates, nodes, output_file, verbose=False)

        result = pl.read_csv(str(tmp_path / "minimal_1.csv"))
        assert len(result) == 1
        assert result['Node'][0] == 99
        assert result['2022-01-01'][0] == 42.0

    def test_many_dates(self, tmp_path):
        """Test with many date columns."""
        num_dates = 50
        data = [[[float(i)]] for i in range(num_dates)]
        layers = 1
        dates = [f'2022-{i:02d}' for i in range(1, num_dates + 1)]
        nodes = [1]
        output_file = str(tmp_path / "many_dates")

        headall2csv(data, layers, dates, nodes, output_file, verbose=False)

        result = pl.read_csv(str(tmp_path / "many_dates_1.csv"))
        # Should have Node column plus all date columns
        assert len(result.columns) == num_dates + 1

    def test_file_naming_convention(self, tmp_path):
        """Test that output files follow naming convention."""
        data = [[[1.0], [2.0], [3.0]]]
        layers = 3
        dates = ['2022']
        nodes = [1]
        output_file = str(tmp_path / "naming_test")

        headall2csv(data, layers, dates, nodes, output_file, verbose=False)

        # Verify file names: base_1.csv, base_2.csv, base_3.csv
        assert (tmp_path / "naming_test_1.csv").exists()
        assert (tmp_path / "naming_test_2.csv").exists()
        assert (tmp_path / "naming_test_3.csv").exists()
