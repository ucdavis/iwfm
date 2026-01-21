#!/usr/bin/env python
# test_plot_gw_hyd_annual.py
# Unit tests for plot/gw_hyd_annual.py
# Copyright (C) 2020-2026 University of California
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


def create_gw_hydrograph_file(hydrograph_ids, data_lines):
    """Create properly structured IWFM groundwater hydrograph file for testing.

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
        File content with proper IWFM hydrograph format
    """
    num_hyd = len(hydrograph_ids)

    content = "*                                        ***************************************\n"
    content += "*                                        *       GROUNDWATER HYDROGRAPH        *\n"
    content += "*                                        *             (UNIT=FEET)             *\n"
    content += "*                                        ***************************************\n"

    # Header line with hydrograph IDs
    content += "*          HYDROGRAPH ID"
    for hyd_id in hydrograph_ids:
        content += f"  {hyd_id:10d}"
    content += "\n"

    # Layer line (all layer 1 for simplicity)
    content += "*                  LAYER"
    for _ in hydrograph_ids:
        content += f"  {1:10d}"
    content += "\n"

    # Node line (all node 0 for simplicity)
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
            content += f"  {value:10.4f}"
        content += "\n"

    return content


class TestGwHydAnnualFileReading:
    """Tests for file reading logic in gw_hyd_annual function"""

    def test_skip_to_data_section(self):
        """Test skipping header lines to reach data section"""
        data_lines = [
            ("09/30/1973_24:00", [478.8368, 371.7239])
        ]
        content = create_gw_hydrograph_file([1, 2], data_lines)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                gwhyd_lines = f.read().splitlines()

            # Skip to first data line
            line_index = iwfm.skip_ahead(0, gwhyd_lines, 0)

            # Should be at first data line
            assert '09/30/1973_24:00' in gwhyd_lines[line_index]

        finally:
            os.unlink(temp_file)

    def test_year_extraction(self):
        """Test extracting year from date string [6:10]"""
        data_lines = [
            ("09/30/1973_24:00", [478.8368]),
            ("10/31/1973_24:00", [457.6409])
        ]
        content = create_gw_hydrograph_file([1], data_lines)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                gwhyd_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, gwhyd_lines, 0)
            line_index += 1  # Skip first data line

            # Extract year from second data line
            year = gwhyd_lines[line_index][6:10]

            assert year == "1973"

        finally:
            os.unlink(temp_file)

    def test_single_water_year_data(self):
        """Test file with one complete water year (Oct 1 - Sep 30)

        Water Year 1974: Oct 1973 through Sep 1974
        The function detects year change from 1973 to 1974 and extracts the last
        line of each calendar year.
        """
        data_lines = [
            ("10/31/1973_24:00", [457.6409, 413.6935]),  # Start of WY 1974
            ("11/30/1973_24:00", [454.4333, 418.1065]),
            ("12/31/1973_24:00", [453.2251, 419.5090]),  # End of calendar year 1973
            ("01/31/1974_24:00", [453.0362, 420.4126]),  # Start of calendar year 1974
            ("02/28/1974_24:00", [451.8607, 419.7553]),
            ("03/31/1974_24:00", [452.0948, 420.2637]),
            ("04/30/1974_24:00", [451.4819, 419.8603]),
            ("05/31/1974_24:00", [450.8309, 419.3873]),
            ("06/30/1974_24:00", [450.4538, 419.1727]),
            ("07/31/1974_24:00", [450.2078, 419.0802]),
            ("08/31/1974_24:00", [450.0000, 419.0000]),
            ("09/30/1974_24:00", [449.5000, 418.5000])   # End of WY 1974
        ]
        content = create_gw_hydrograph_file([1, 2], data_lines)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                gwhyd_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, gwhyd_lines, 0)

            # Find year changes
            year_changes = []
            test_str = gwhyd_lines[line_index][6:10]
            line_index += 1

            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][6:10] != test_str:
                    year_changes.append(line_index)
                    test_str = gwhyd_lines[line_index][6:10]
                line_index += 1

            # Should have 1 year change (from 1973 to 1974)
            assert len(year_changes) == 1

        finally:
            os.unlink(temp_file)

    def test_multiple_years_data(self):
        """Test file with multiple years of data"""
        data_lines = [
            ("09/30/1973_24:00", [478.8368]),
            ("12/31/1973_24:00", [453.2251]),
            ("03/31/1974_24:00", [452.0948]),
            ("06/30/1974_24:00", [450.4538]),
            ("09/30/1974_24:00", [450.0000]),
            ("12/31/1974_24:00", [449.5000]),
            ("03/31/1975_24:00", [448.0000]),
            ("06/30/1975_24:00", [447.5000]),
        ]
        content = create_gw_hydrograph_file([1], data_lines)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                gwhyd_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, gwhyd_lines, 0)

            # Find year changes
            year_changes = []
            test_str = gwhyd_lines[line_index][6:10]
            line_index += 1

            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][6:10] != test_str:
                    year_changes.append(line_index)
                    test_str = gwhyd_lines[line_index][6:10]
                line_index += 1

            # Should have 2 year changes (1973→1974, 1974→1975)
            assert len(year_changes) == 2

        finally:
            os.unlink(temp_file)

    def test_output_line_collection(self):
        """Test collecting output lines (header + annual data)"""
        data_lines = [
            ("09/30/1973_24:00", [478.8368]),
            ("12/31/1973_24:00", [453.2251]),
            ("12/31/1974_24:00", [449.5000]),
        ]
        content = create_gw_hydrograph_file([1], data_lines)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                gwhyd_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, gwhyd_lines, 0)
            start_index = line_index

            # Copy header lines
            out_lines = []
            for line in gwhyd_lines[:line_index]:
                out_lines.append(line)
            out_lines.append(gwhyd_lines[line_index])
            line_index += 1

            # Process data lines
            test_str = gwhyd_lines[line_index][6:10]
            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][6:10] != test_str:
                    out_lines.append(gwhyd_lines[line_index-1])
                    test_str = gwhyd_lines[line_index][6:10]
                line_index += 1

            # Add last line
            out_lines.append(gwhyd_lines[len(gwhyd_lines)-1])

            # Should have: header (9 lines) + first line + 1 year-end + last line = 12 lines
            # Header: 4 + 4 + 1 = 9 lines
            # Data: first (09/30/1973) + year-end (12/31/1973) + last (12/31/1974) = 3 lines
            # Total: 9 + 3 = 12 lines
            assert len(out_lines) == 12

        finally:
            os.unlink(temp_file)

    def test_start_length_calculation(self):
        """Test calculating start length for statistics"""
        data_lines = [
            ("09/30/1973_24:00", [478.8368]),
            ("10/31/1973_24:00", [457.6409]),
            ("11/30/1973_24:00", [454.4333]),
        ]
        content = create_gw_hydrograph_file([1], data_lines)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                gwhyd_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, gwhyd_lines, 0)
            start_index = line_index
            start_len = len(gwhyd_lines) - start_index

            # Should be 3 data lines
            assert start_len == 3

        finally:
            os.unlink(temp_file)

    def test_multiple_hydrographs(self):
        """Test file with multiple hydrograph columns"""
        data_lines = [
            ("09/30/1973_24:00", [478.8368, 371.7239, 367.5474]),
            ("12/31/1973_24:00", [453.2251, 419.5090, 415.3000]),
            ("12/31/1974_24:00", [449.5000, 420.0000, 416.0000]),
        ]
        content = create_gw_hydrograph_file([1, 2, 3], data_lines)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            with open(temp_file) as f:
                gwhyd_lines = f.read().splitlines()

            # Verify header has 3 hydrographs
            assert '1' in gwhyd_lines[4] and '2' in gwhyd_lines[4] and '3' in gwhyd_lines[4]

            # Verify data lines have 3 values each
            import iwfm
            line_index = iwfm.skip_ahead(0, gwhyd_lines, 0)
            values = gwhyd_lines[line_index].split()[1:]  # Skip date
            assert len(values) == 3

        finally:
            os.unlink(temp_file)

    def test_year_boundary_detection(self):
        """Test detecting calendar year boundaries correctly

        Note: Water years run Oct 1 - Sep 30, but the function extracts the last
        line of each calendar year (December 31st) by detecting when the year
        portion [6:10] of the date changes.
        """
        data_lines = [
            ("10/31/1973_24:00", [457.6409]),
            ("11/30/1973_24:00", [454.4333]),
            ("12/31/1973_24:00", [453.2251]),  # Last day of calendar year 1973
            ("01/31/1974_24:00", [453.0362]),  # First month of calendar year 1974
            ("02/28/1974_24:00", [451.8607]),
        ]
        content = create_gw_hydrograph_file([1], data_lines)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                gwhyd_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, gwhyd_lines, 0)
            start_index = line_index

            # Find the line before year change
            test_str = gwhyd_lines[line_index][6:10]
            line_index += 1
            year_end_line = None

            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][6:10] != test_str:
                    year_end_line = gwhyd_lines[line_index-1]
                    break
                line_index += 1

            # Should capture 12/31/1973 as year-end (last line of calendar year 1973)
            assert "12/31/1973" in year_end_line

        finally:
            os.unlink(temp_file)

    def test_complete_water_years(self):
        """Test file with complete water years (Oct-Sep)

        Water Year 1974: 10/1/1973 - 9/30/1974 (12 months)
        Water Year 1975: 10/1/1974 - 9/30/1975 (12 months)

        The annual function should extract:
        - First line (10/31/1973)
        - Last line before year change (12/31/1973)
        - Last line before next year change (12/31/1974)
        - Last line (09/30/1975)
        """
        data_lines = [
            ("10/31/1973_24:00", [478.0]),  # WY 1974 start
            ("12/31/1973_24:00", [450.0]),  # Calendar year 1973 end
            ("06/30/1974_24:00", [445.0]),  # Mid WY 1974
            ("09/30/1974_24:00", [440.0]),  # WY 1974 end
            ("10/31/1974_24:00", [438.0]),  # WY 1975 start
            ("12/31/1974_24:00", [435.0]),  # Calendar year 1974 end
            ("06/30/1975_24:00", [430.0]),  # Mid WY 1975
            ("09/30/1975_24:00", [425.0]),  # WY 1975 end
        ]
        content = create_gw_hydrograph_file([1], data_lines)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                gwhyd_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, gwhyd_lines, 0)
            start_index = line_index

            # Collect annual lines (same logic as gw_hyd_annual function)
            out_lines = []
            for line in gwhyd_lines[:line_index]:
                out_lines.append(line)
            out_lines.append(gwhyd_lines[line_index])  # First data line
            line_index += 1

            test_str = gwhyd_lines[line_index][6:10]
            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][6:10] != test_str:
                    out_lines.append(gwhyd_lines[line_index-1])  # Last line of previous year
                    test_str = gwhyd_lines[line_index][6:10]
                line_index += 1

            out_lines.append(gwhyd_lines[len(gwhyd_lines)-1])  # Last line

            # Should extract: header (9) + first (10/31/1973) + year-end (12/31/1973)
            #                + year-end (12/31/1974) + last (09/30/1975)
            # Total: 9 + 4 = 13 lines
            assert len(out_lines) == 13

            # Verify the annual lines contain the right dates
            data_lines_only = [line for line in out_lines if '/' in line and '_24:00' in line]
            assert "10/31/1973" in data_lines_only[0]
            assert "12/31/1973" in data_lines_only[1]
            assert "12/31/1974" in data_lines_only[2]
            assert "09/30/1975" in data_lines_only[3]

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
