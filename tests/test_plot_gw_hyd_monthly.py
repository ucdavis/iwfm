#!/usr/bin/env python
# test_plot_gw_hyd_monthly.py
# Unit tests for plot/gw_hyd_monthly.py
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


class TestGwHydMonthlyFileReading:
    """Tests for file reading logic in gw_hyd_monthly function"""

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

    def test_month_extraction(self):
        """Test extracting month from date string [:2]"""
        data_lines = [
            ("09/30/1973_24:00", [478.8368]),
            ("10/01/1973_24:00", [457.6409])
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

            # Extract month from first data line
            month1 = gwhyd_lines[line_index][:2]
            line_index += 1
            # Extract month from second data line
            month2 = gwhyd_lines[line_index][:2]

            assert month1 == "09"
            assert month2 == "10"

        finally:
            os.unlink(temp_file)

    def test_daily_to_monthly_single_month(self):
        """Test file with daily data for single month (30 days in September)"""
        data_lines = [
            ("09/01/1973_24:00", [478.8]),
            ("09/05/1973_24:00", [477.5]),
            ("09/10/1973_24:00", [476.2]),
            ("09/15/1973_24:00", [475.0]),
            ("09/20/1973_24:00", [474.5]),
            ("09/25/1973_24:00", [473.8]),
            ("09/30/1973_24:00", [473.0]),
            ("10/01/1973_24:00", [472.5]),
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

            # Find month changes
            month_changes = []
            test_str = gwhyd_lines[line_index][:2]
            line_index += 1

            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][:2] != test_str:
                    month_changes.append(line_index)
                    test_str = gwhyd_lines[line_index][:2]
                line_index += 1

            # Should have 1 month change (from September to October)
            assert len(month_changes) == 1

        finally:
            os.unlink(temp_file)

    def test_multiple_months_data(self):
        """Test file with data across multiple months"""
        data_lines = [
            ("09/15/1973_24:00", [478.0]),
            ("09/30/1973_24:00", [477.0]),
            ("10/15/1973_24:00", [476.0]),
            ("10/31/1973_24:00", [475.0]),
            ("11/15/1973_24:00", [474.0]),
            ("11/30/1973_24:00", [473.0]),
            ("12/15/1973_24:00", [472.0]),
            ("12/31/1973_24:00", [471.0]),
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

            # Find month changes
            month_changes = []
            test_str = gwhyd_lines[line_index][:2]
            line_index += 1

            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][:2] != test_str:
                    month_changes.append(line_index)
                    test_str = gwhyd_lines[line_index][:2]
                line_index += 1

            # Should have 3 month changes (Sep→Oct, Oct→Nov, Nov→Dec)
            assert len(month_changes) == 3

        finally:
            os.unlink(temp_file)

    def test_output_line_collection(self):
        """Test collecting output lines (header + monthly data)"""
        data_lines = [
            ("09/15/1973_24:00", [478.0]),
            ("09/30/1973_24:00", [477.0]),
            ("10/31/1973_24:00", [475.0]),
            ("11/30/1973_24:00", [473.0]),
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
            test_str = gwhyd_lines[line_index][:2]
            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][:2] != test_str:
                    out_lines.append(gwhyd_lines[line_index-1])
                    test_str = gwhyd_lines[line_index][:2]
                line_index += 1

            # Add last line
            out_lines.append(gwhyd_lines[len(gwhyd_lines)-1])

            # Should have: header (9 lines) + first line + 2 month-ends + last line = 13 lines
            # Header: 4 + 4 + 1 = 9 lines
            # Data: first (09/15) + month-end (09/30) + month-end (10/31) + last (11/30) = 4 lines
            # Total: 9 + 4 = 13 lines
            assert len(out_lines) == 13

        finally:
            os.unlink(temp_file)

    def test_start_length_calculation(self):
        """Test calculating start length for statistics"""
        data_lines = [
            ("09/15/1973_24:00", [478.0]),
            ("09/20/1973_24:00", [477.5]),
            ("09/30/1973_24:00", [477.0]),
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
            ("09/15/1973_24:00", [478.0, 371.0, 367.0]),
            ("09/30/1973_24:00", [477.0, 370.0, 366.0]),
            ("10/31/1973_24:00", [475.0, 368.0, 364.0]),
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

    def test_month_boundary_detection(self):
        """Test detecting month boundaries correctly

        The function extracts the last line of each month by detecting when the
        month portion [:2] of the date changes.
        """
        data_lines = [
            ("09/10/1973_24:00", [478.5]),
            ("09/20/1973_24:00", [478.0]),
            ("09/30/1973_24:00", [477.5]),  # Last day of September
            ("10/05/1973_24:00", [477.0]),  # First entries of October
            ("10/15/1973_24:00", [476.5]),
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

            # Find the line before month change
            test_str = gwhyd_lines[line_index][:2]
            line_index += 1
            month_end_line = None

            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][:2] != test_str:
                    month_end_line = gwhyd_lines[line_index-1]
                    break
                line_index += 1

            # Should capture 09/30/1973 as month-end
            assert "09/30/1973" in month_end_line

        finally:
            os.unlink(temp_file)

    def test_complete_water_year_monthly(self):
        """Test file with complete water year of monthly data (Oct-Sep)

        Water Year 1974: 10/1/1973 - 9/30/1974 (12 months)

        The monthly function should extract:
        - First line (10/31/1973)
        - Last line of each month (12 months)
        """
        data_lines = [
            ("10/31/1973_24:00", [478.0]),  # Oct end
            ("11/30/1973_24:00", [477.0]),  # Nov end
            ("12/31/1973_24:00", [476.0]),  # Dec end
            ("01/31/1974_24:00", [475.0]),  # Jan end
            ("02/28/1974_24:00", [474.0]),  # Feb end
            ("03/31/1974_24:00", [473.0]),  # Mar end
            ("04/30/1974_24:00", [472.0]),  # Apr end
            ("05/31/1974_24:00", [471.0]),  # May end
            ("06/30/1974_24:00", [470.0]),  # Jun end
            ("07/31/1974_24:00", [469.0]),  # Jul end
            ("08/31/1974_24:00", [468.0]),  # Aug end
            ("09/30/1974_24:00", [467.0]),  # Sep end (WY 1974 end)
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

            # Collect monthly lines (same logic as gw_hyd_monthly function)
            out_lines = []
            for line in gwhyd_lines[:line_index]:
                out_lines.append(line)
            out_lines.append(gwhyd_lines[line_index])  # First data line
            line_index += 1

            test_str = gwhyd_lines[line_index][:2]
            while line_index < len(gwhyd_lines):
                if gwhyd_lines[line_index][:2] != test_str:
                    out_lines.append(gwhyd_lines[line_index-1])  # Last line of previous month
                    test_str = gwhyd_lines[line_index][:2]
                line_index += 1

            out_lines.append(gwhyd_lines[len(gwhyd_lines)-1])  # Last line

            # Should extract: header (9) + first (10/31) + 11 month-ends + last (09/30)
            # But first line IS 10/31, so we have: 9 + 1 + 11 + 0 = 21 lines
            # Actually: 9 + first + (Nov-Aug month ends = 10) + last Sep = 9 + 12 = 21
            # Wait, we have 12 months. First is Oct, then Nov-Sep are the remaining 11.
            # So: 9 header + 12 month-end lines = 21 lines
            assert len(out_lines) == 21

            # Verify all 12 months are present
            data_lines_only = [line for line in out_lines if '/' in line and '_24:00' in line]
            assert len(data_lines_only) == 12
            assert "10/31/1973" in data_lines_only[0]
            assert "09/30/1974" in data_lines_only[11]

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
