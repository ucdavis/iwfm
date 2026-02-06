# test_refined_lu_factors.py
# unit tests for refined_lu_factors function
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

from pathlib import Path
from unittest.mock import patch


def _load_refined_lu_factors():
    """Load the refined_lu_factors function dynamically."""
    from importlib.util import spec_from_file_location, module_from_spec
    base = Path(__file__).resolve().parents[1] / "iwfm" / "refined_lu_factors.py"
    spec = spec_from_file_location("refined_lu_factors", str(base))
    assert spec is not None, "Failed to load module specification"
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return getattr(mod, "refined_lu_factors")


refined_lu_factors = _load_refined_lu_factors()


class TestRefinedLuFactors:
    """Tests for the refined_lu_factors function."""

    @patch('iwfm.file_test')
    def test_basic_calculation(self, mock_file_test, tmp_path):
        """Test basic land use factor calculation."""
        # Create original areas file
        orig_areas_file = tmp_path / "orig_areas.csv"
        orig_areas_file.write_text("elem,area\n1,1000.0\n2,2000.0\n3,1500.0\n")

        # Create refined areas file
        refined_areas_file = tmp_path / "refined_areas.csv"
        refined_areas_file.write_text("elem,area\n101,250.0\n102,500.0\n103,300.0\n")

        # Create elem2elem mapping file (refined -> original)
        elem2elem_file = tmp_path / "elem2elem.csv"
        elem2elem_file.write_text("refined,original\n101,1\n102,2\n103,3\n")

        result = refined_lu_factors(
            str(orig_areas_file),
            str(refined_areas_file),
            str(elem2elem_file)
        )

        assert len(result) == 3
        # Check first element: refined 101, orig 1, factor = 250/1000 = 0.25
        assert result[0][0] == 101
        assert result[0][1] == 1
        assert abs(result[0][2] - 0.25) < 0.001

        # Check second element: refined 102, orig 2, factor = 500/2000 = 0.25
        assert result[1][0] == 102
        assert result[1][1] == 2
        assert abs(result[1][2] - 0.25) < 0.001

        # Check third element: refined 103, orig 3, factor = 300/1500 = 0.2
        assert result[2][0] == 103
        assert result[2][1] == 3
        assert abs(result[2][2] - 0.2) < 0.001

    @patch('iwfm.file_test')
    def test_multiple_refined_to_one_original(self, mock_file_test, tmp_path):
        """Test when multiple refined elements map to one original element."""
        orig_areas_file = tmp_path / "orig_multi.csv"
        orig_areas_file.write_text("elem,area\n1,1000.0\n")

        refined_areas_file = tmp_path / "refined_multi.csv"
        refined_areas_file.write_text("elem,area\n101,200.0\n102,300.0\n103,500.0\n")

        elem2elem_file = tmp_path / "elem2elem_multi.csv"
        elem2elem_file.write_text("refined,original\n101,1\n102,1\n103,1\n")

        result = refined_lu_factors(
            str(orig_areas_file),
            str(refined_areas_file),
            str(elem2elem_file)
        )

        assert len(result) == 3
        # All map to original elem 1 with area 1000
        assert result[0][2] == 0.2  # 200/1000
        assert result[1][2] == 0.3  # 300/1000
        assert result[2][2] == 0.5  # 500/1000

    @patch('iwfm.file_test')
    def test_factor_sum_to_one(self, mock_file_test, tmp_path):
        """Test that factors for refined elements summing to original equal 1."""
        orig_areas_file = tmp_path / "orig_sum.csv"
        orig_areas_file.write_text("elem,area\n1,1000.0\n")

        # Refined areas sum to original area
        refined_areas_file = tmp_path / "refined_sum.csv"
        refined_areas_file.write_text("elem,area\n101,400.0\n102,600.0\n")

        elem2elem_file = tmp_path / "elem2elem_sum.csv"
        elem2elem_file.write_text("refined,original\n101,1\n102,1\n")

        result = refined_lu_factors(
            str(orig_areas_file),
            str(refined_areas_file),
            str(elem2elem_file)
        )

        # Factors should sum to 1.0
        total = sum(r[2] for r in result)
        assert abs(total - 1.0) < 0.001

    @patch('iwfm.file_test')
    def test_return_format(self, mock_file_test, tmp_path):
        """Test the format of returned data."""
        orig_areas_file = tmp_path / "orig_fmt.csv"
        orig_areas_file.write_text("elem,area\n1,100.0\n")

        refined_areas_file = tmp_path / "refined_fmt.csv"
        refined_areas_file.write_text("elem,area\n10,50.0\n")

        elem2elem_file = tmp_path / "elem2elem_fmt.csv"
        elem2elem_file.write_text("refined,original\n10,1\n")

        result = refined_lu_factors(
            str(orig_areas_file),
            str(refined_areas_file),
            str(elem2elem_file)
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert len(result[0]) == 3
        assert isinstance(result[0][0], int)  # refined elem
        assert isinstance(result[0][1], int)  # original elem
        assert isinstance(result[0][2], float)  # factor


class TestRefinedLuFactorsEdgeCases:
    """Edge case tests for refined_lu_factors."""

    @patch('iwfm.file_test')
    def test_single_element(self, mock_file_test, tmp_path):
        """Test with single element mapping."""
        orig_areas_file = tmp_path / "orig_single.csv"
        orig_areas_file.write_text("elem,area\n1,500.0\n")

        refined_areas_file = tmp_path / "refined_single.csv"
        refined_areas_file.write_text("elem,area\n1,500.0\n")

        elem2elem_file = tmp_path / "elem2elem_single.csv"
        elem2elem_file.write_text("refined,original\n1,1\n")

        result = refined_lu_factors(
            str(orig_areas_file),
            str(refined_areas_file),
            str(elem2elem_file)
        )

        assert len(result) == 1
        assert result[0][2] == 1.0  # Same area = factor of 1

    @patch('iwfm.file_test')
    def test_large_factor(self, mock_file_test, tmp_path):
        """Test with refined area larger than original (factor > 1)."""
        orig_areas_file = tmp_path / "orig_large.csv"
        orig_areas_file.write_text("elem,area\n1,100.0\n")

        refined_areas_file = tmp_path / "refined_large.csv"
        refined_areas_file.write_text("elem,area\n1,200.0\n")

        elem2elem_file = tmp_path / "elem2elem_large.csv"
        elem2elem_file.write_text("refined,original\n1,1\n")

        result = refined_lu_factors(
            str(orig_areas_file),
            str(refined_areas_file),
            str(elem2elem_file)
        )

        assert result[0][2] == 2.0  # 200/100 = 2

    @patch('iwfm.file_test')
    def test_small_areas(self, mock_file_test, tmp_path):
        """Test with small decimal areas."""
        orig_areas_file = tmp_path / "orig_small.csv"
        orig_areas_file.write_text("elem,area\n1,0.001\n")

        refined_areas_file = tmp_path / "refined_small.csv"
        refined_areas_file.write_text("elem,area\n1,0.0005\n")

        elem2elem_file = tmp_path / "elem2elem_small.csv"
        elem2elem_file.write_text("refined,original\n1,1\n")

        result = refined_lu_factors(
            str(orig_areas_file),
            str(refined_areas_file),
            str(elem2elem_file)
        )

        assert abs(result[0][2] - 0.5) < 0.001

    @patch('iwfm.file_test')
    def test_file_test_called(self, mock_file_test, tmp_path):
        """Test that iwfm.file_test is called for all input files."""
        orig_areas_file = tmp_path / "orig_ft.csv"
        orig_areas_file.write_text("elem,area\n1,100.0\n")

        refined_areas_file = tmp_path / "refined_ft.csv"
        refined_areas_file.write_text("elem,area\n1,50.0\n")

        elem2elem_file = tmp_path / "elem2elem_ft.csv"
        elem2elem_file.write_text("refined,original\n1,1\n")

        refined_lu_factors(
            str(orig_areas_file),
            str(refined_areas_file),
            str(elem2elem_file)
        )

        # file_test should be called 3 times (once per file)
        assert mock_file_test.call_count == 3
