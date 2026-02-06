# test_lu2tables.py
# unit tests for lu2tables function
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
import csv
import os
import shutil
import tempfile

import pytest

import iwfm


class TestLu2tables:
    """Tests for the lu2tables function."""

    def create_minimal_lu_file(self, filepath, num_elements=3, num_timesteps=2, num_crops=2):
        """Helper to create a minimal land use file for testing."""
        lines = []
        # Comment lines
        lines.append("C This is a comment line")
        lines.append("C Another comment")
        # Header lines (skip=4 by default in IWFM)
        lines.append(" 43560.0                                    / FACTLNNRV")
        lines.append(" 1                                          / NSPLNVRV")
        lines.append(" 0                                          / NFQLNVRV")
        lines.append("                                            / DSSFL")
        lines.append("C Data header comment")
        lines.append("C   ITLN               IE       ALANDNV     ALANDRV")

        # Data lines - each timestep starts with date, followed by element data
        dates = ["09/30/1974_24:00", "10/31/1974_24:00"]
        for ts in range(num_timesteps):
            for elem in range(1, num_elements + 1):
                if elem == 1:
                    # First element line has date
                    values = "\t".join([f"{100.0 + ts*10 + elem + crop*0.1:.3f}" for crop in range(num_crops)])
                    lines.append(f"{dates[ts]}\t{elem}\t{values}")
                else:
                    # Subsequent elements have no date (just tabs for alignment)
                    values = "\t".join([f"{100.0 + ts*10 + elem + crop*0.1:.3f}" for crop in range(num_crops)])
                    lines.append(f"\t\t\t{elem}\t{values}")

        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))

        return num_elements, num_timesteps, num_crops

    def test_basic_dat_output(self, tmp_path):
        """Test basic conversion to .dat output files."""
        input_file = tmp_path / "test_landuse.dat"
        num_elems, num_ts, num_crops = self.create_minimal_lu_file(str(input_file))

        # Run the function
        iwfm.lu2tables(str(input_file), 'dat')

        # Check output files were created (one per crop)
        for crop in range(1, num_crops + 1):
            output_file = tmp_path / f"test_landuse_{crop}.dat"
            assert output_file.exists(), f"Expected output file {output_file} not found"

        # Verify content of first crop file
        output_file = tmp_path / "test_landuse_1.dat"
        with open(output_file, 'r') as f:
            content = f.read()

        # Should have header with WYr and years
        assert 'WYr' in content
        assert '1974' in content

    def test_basic_csv_output(self, tmp_path):
        """Test basic conversion to .csv output files."""
        input_file = tmp_path / "test_landuse.dat"
        num_elems, num_ts, num_crops = self.create_minimal_lu_file(str(input_file))

        # Run the function with csv output
        iwfm.lu2tables(str(input_file), 'csv')

        # Check output files were created (one per crop)
        for crop in range(1, num_crops + 1):
            output_file = tmp_path / f"test_landuse_{crop}.csv"
            assert output_file.exists(), f"Expected output file {output_file} not found"

        # Verify CSV content structure
        output_file = tmp_path / "test_landuse_1.csv"
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # First row should be header with WYr and years
        assert rows[0][0] == 'WYr'
        assert '1974' in rows[0][1]

        # Should have one row per element plus header
        assert len(rows) == num_elems + 1

    def test_csv_content_values(self, tmp_path):
        """Test that CSV output contains correct values."""
        input_file = tmp_path / "test_values.dat"
        num_elems, num_ts, num_crops = self.create_minimal_lu_file(
            str(input_file), num_elements=2, num_timesteps=2, num_crops=2
        )

        iwfm.lu2tables(str(input_file), 'csv')

        # Read the first crop file
        output_file = tmp_path / "test_values_1.csv"
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Verify element numbers in first column (after header)
        assert rows[1][0] == '1'  # First element
        assert rows[2][0] == '2'  # Second element

    def test_multiple_crops(self, tmp_path):
        """Test file with multiple crops creates multiple output files."""
        input_file = tmp_path / "test_crops.dat"
        num_elems, num_ts, num_crops = self.create_minimal_lu_file(
            str(input_file), num_elements=3, num_timesteps=2, num_crops=4
        )

        iwfm.lu2tables(str(input_file), 'dat')

        # Should create 4 output files
        for crop in range(1, 5):
            output_file = tmp_path / f"test_crops_{crop}.dat"
            assert output_file.exists(), f"Missing output file for crop {crop}"

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output shows processing information."""
        input_file = tmp_path / "test_verbose.dat"
        self.create_minimal_lu_file(str(input_file))

        iwfm.lu2tables(str(input_file), 'dat', verbose=True)

        captured = capsys.readouterr()
        assert 'test_verbose' in captured.out
        assert 'land use' in captured.out.lower()

    def test_no_verbose_output(self, tmp_path, capsys):
        """Test that verbose=False produces no output."""
        input_file = tmp_path / "test_quiet.dat"
        self.create_minimal_lu_file(str(input_file))

        iwfm.lu2tables(str(input_file), 'dat', verbose=False)

        captured = capsys.readouterr()
        assert captured.out == ''

    def test_dat_file_format(self, tmp_path):
        """Test .dat output file format has proper spacing."""
        input_file = tmp_path / "test_format.dat"
        self.create_minimal_lu_file(str(input_file), num_elements=2, num_timesteps=1)

        iwfm.lu2tables(str(input_file), 'dat')

        output_file = tmp_path / "test_format_1.dat"
        with open(output_file, 'r') as f:
            lines = f.readlines()

        # First line should be header
        assert 'WYr' in lines[0]
        # Data lines should have fixed-width formatting
        assert len(lines) >= 3  # header + 2 elements

    def test_empty_file_error(self, tmp_path):
        """Test that empty file causes error."""
        input_file = tmp_path / "test_empty.dat"
        input_file.write_text("C Comment only\nC Another comment\n")

        with pytest.raises(SystemExit):
            iwfm.lu2tables(str(input_file), 'dat')

    def test_no_data_lines_error(self, tmp_path):
        """Test that file with no data lines causes error."""
        input_file = tmp_path / "test_nodata.dat"
        content = """\
C Comment
C Comment
 h1
 h2
 h3
 h4
"""
        input_file.write_text(content)

        with pytest.raises(SystemExit):
            iwfm.lu2tables(str(input_file), 'dat')

    def test_default_output_type_is_dat(self, tmp_path):
        """Test that unknown output type defaults to .dat."""
        input_file = tmp_path / "test_default.dat"
        self.create_minimal_lu_file(str(input_file))

        # Use unknown type - should default to dat
        iwfm.lu2tables(str(input_file), 'unknown_type')

        output_file = tmp_path / "test_default_1.dat"
        assert output_file.exists()

    def test_with_real_test_file(self):
        """Test with actual C2VSimCG test data file if available."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Simulation',
            'RootZone',
            'C2VSimCG_NativeVeg_Area.dat'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        # Create a temporary output directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Copy input file to temp dir so output goes there
            temp_input = os.path.join(tmp_dir, 'C2VSimCG_NativeVeg_Area.dat')
            shutil.copy(test_file, temp_input)

            # Run conversion to CSV
            iwfm.lu2tables(temp_input, 'csv', verbose=False)

            # Check output files exist (should be 2 crops: native veg and riparian)
            output_file_1 = os.path.join(tmp_dir, 'C2VSimCG_NativeVeg_Area_1.csv')
            output_file_2 = os.path.join(tmp_dir, 'C2VSimCG_NativeVeg_Area_2.csv')
            assert os.path.exists(output_file_1)
            assert os.path.exists(output_file_2)

            # Verify CSV content structure
            with open(output_file_1, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)

            # Should have header row plus element rows
            assert len(rows) > 1
            # Header should have WYr
            assert rows[0][0] == 'WYr'
            # Should have element numbers in first column
            assert rows[1][0] == '1'

    def test_single_timestep(self, tmp_path):
        """Test file with single timestep."""
        input_file = tmp_path / "test_single_ts.dat"
        self.create_minimal_lu_file(str(input_file), num_timesteps=1)

        iwfm.lu2tables(str(input_file), 'csv')

        output_file = tmp_path / "test_single_ts_1.csv"
        assert output_file.exists()

        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Header should have WYr and one year
        assert len(rows[0]) == 2  # WYr column + 1 timestep

    def test_single_element(self, tmp_path):
        """Test file with single element."""
        input_file = tmp_path / "test_single_elem.dat"
        self.create_minimal_lu_file(str(input_file), num_elements=1)

        iwfm.lu2tables(str(input_file), 'csv')

        output_file = tmp_path / "test_single_elem_1.csv"
        assert output_file.exists()

        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Should have header + 1 element row
        assert len(rows) == 2

    def test_single_crop(self, tmp_path):
        """Test file with single crop."""
        input_file = tmp_path / "test_single_crop.dat"
        self.create_minimal_lu_file(str(input_file), num_crops=1)

        iwfm.lu2tables(str(input_file), 'csv')

        # Should only create one output file
        output_file_1 = tmp_path / "test_single_crop_1.csv"
        output_file_2 = tmp_path / "test_single_crop_2.csv"
        assert output_file_1.exists()
        assert not output_file_2.exists()

    def test_output_file_base_name(self, tmp_path):
        """Test that output files use input file base name."""
        input_file = tmp_path / "my_landuse_data.dat"
        self.create_minimal_lu_file(str(input_file))

        iwfm.lu2tables(str(input_file), 'dat')

        # Output should use same base name
        output_file = tmp_path / "my_landuse_data_1.dat"
        assert output_file.exists()

    def test_dat_output_element_numbers(self, tmp_path):
        """Test that .dat output includes correct element numbers."""
        input_file = tmp_path / "test_elem_nums.dat"
        self.create_minimal_lu_file(str(input_file), num_elements=5)

        iwfm.lu2tables(str(input_file), 'dat')

        output_file = tmp_path / "test_elem_nums_1.dat"
        with open(output_file, 'r') as f:
            lines = f.readlines()

        # Check element numbers are present (lines 2-6 after header)
        for i, elem in enumerate(range(1, 6), start=1):
            assert str(elem) in lines[i]

    def test_csv_years_in_header(self, tmp_path):
        """Test that CSV header contains years from all timesteps."""
        input_file = tmp_path / "test_years.dat"
        lines = []
        lines.append("C Comment")
        lines.append(" 43560.0                                    / FACTLNNRV")
        lines.append(" 1                                          / NSPLNVRV")
        lines.append(" 0                                          / NFQLNVRV")
        lines.append("                                            / DSSFL")
        lines.append("C Data")
        lines.append("C Data")
        # Two timesteps with different years
        lines.append("09/30/1974_24:00\t1\t100.0\t200.0")
        lines.append("\t\t\t2\t101.0\t201.0")
        lines.append("09/30/1975_24:00\t1\t110.0\t210.0")
        lines.append("\t\t\t2\t111.0\t211.0")

        input_file.write_text('\n'.join(lines))

        iwfm.lu2tables(str(input_file), 'csv')

        output_file = tmp_path / "test_years_1.csv"
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)

        # Header should contain both years
        assert '1974' in header[1]
        assert '1975' in header[2]
