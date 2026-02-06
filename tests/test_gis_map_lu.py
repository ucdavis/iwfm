#!/usr/bin/env python
# test_gis_map_lu.py
# Unit tests for gis/map_lu.py
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


def create_land_use_test_file(area_factor, nsplnp, nfqlnp, time_steps_data):
    """Create properly structured IWFM land use file for testing.

    Parameters
    ----------
    area_factor : float
        Conversion factor for land use area (FACTLNP)
    nsplnp : int
        Number of time steps to update land use data
    nfqlnp : int
        Repetition frequency of land use data
    time_steps_data : list of tuples
        Each tuple: (date_string, element_data_list)
        date_string: e.g., "09/30/1922_24:00"
        element_data_list: list of tuples (elem_id, rice_fl, rice_nfl, rice_ndc, refuge_sl, refuge_pr)

    Returns
    -------
    str
        File content with proper IWFM land use format
    """
    content = "C***********************************************************************\n"
    content += "C                          PONDED CROP AREA FILE\n"
    content += "C                          Root Zone Component\n"
    content += "C***********************************************************************\n"
    content += "C                           Land Use Data Specifications\n"
    content += "C\n"
    content += "C   FACTLNP;   Conversion factor for land use area\n"
    content += "C   NSPLNP ;   Number of time steps to update the land use data\n"
    content += "C   NFQLNP ;   Repetition frequency of the land use data\n"
    content += "C   DSSFL   ;   The name of the DSS file for data input\n"
    content += "C----------------------------------------------------------------------------------------\n"
    content += f"          {area_factor:.1f}                                    / FACTLNP\n"
    content += f"          {nsplnp}                                          / NSPLNP\n"
    content += f"          {nfqlnp}                                          / NFQLNP\n"
    content += "                                                     / DSSFL\n"
    content += "C----------------------------------------------------------------------------------------\n"
    content += "C                             Land Use Data\n"
    content += "C-----------------------------------------------------------------------------------------------------------------------------------\n"
    content += "C   ITLN          IE        ALANDRI_FLALANDRI_NFLALANDRI_NDC ALANDRF_SLALANDRF_PR\n"
    content += "C-----------------------------------------------------------------------------------------------------------------------------------\n"

    # Add time step data
    for date_str, element_data in time_steps_data:
        # First line of time step has date and first element data
        if element_data:
            elem_id, rice_fl, rice_nfl, rice_ndc, refuge_sl, refuge_pr = element_data[0]
            content += f"{date_str}\t{elem_id}\t{rice_fl:.5f}\t{rice_nfl:.5f}\t{rice_ndc:.5f}\t{refuge_sl:.5f}\t{refuge_pr:.5f}\n"

            # Subsequent lines for this time step (no date)
            for elem_id, rice_fl, rice_nfl, rice_ndc, refuge_sl, refuge_pr in element_data[1:]:
                content += f"\t{elem_id}\t{rice_fl:.5f}\t{rice_nfl:.5f}\t{rice_ndc:.5f}\t{refuge_sl:.5f}\t{refuge_pr:.5f}\n"

    return content


class TestMapLuFileReading:
    """Tests for file reading logic in map_lu function"""

    def test_read_area_factor(self):
        """Test reading area conversion factor (FACTLNP)"""
        time_steps = [
            ("09/30/1922_24:00", [(1, 0.0, 0.0, 0.0, 0.0, 0.0)])
        ]
        content = create_land_use_test_file(
            area_factor=43560.0,
            nsplnp=1,
            nfqlnp=0,
            time_steps_data=time_steps
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            # Read file and extract area_factor using same logic as map_lu
            import iwfm
            with open(temp_file) as f:
                file_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, file_lines, 0)
            area_factor = float(file_lines[line_index].split()[0])

            assert area_factor == 43560.0

        finally:
            os.unlink(temp_file)

    def test_skip_to_data_section(self):
        """Test skipping to data section (skip 4 lines after area_factor)"""
        time_steps = [
            ("09/30/1922_24:00", [(1, 100.5, 200.3, 300.2, 50.1, 75.4)])
        ]
        content = create_land_use_test_file(
            area_factor=43560.0,
            nsplnp=1,
            nfqlnp=0,
            time_steps_data=time_steps
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                file_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, file_lines, 0)
            area_factor = float(file_lines[line_index].split()[0])

            # Skip 4 lines (NSPLNP, NFQLNP, DSSFL, comments) to reach data
            line_index = iwfm.skip_ahead(line_index, file_lines, 4)

            # Should be at first data line with date
            assert '09/30/1922_24:00' in file_lines[line_index]

        finally:
            os.unlink(temp_file)

    def test_count_lines_per_timestep_single_element(self):
        """Test counting lines per time step with single element"""
        time_steps = [
            ("09/30/1922_24:00", [(1, 100.0, 200.0, 300.0, 50.0, 75.0)]),
            ("09/30/1923_24:00", [(1, 110.0, 210.0, 310.0, 55.0, 80.0)])
        ]
        content = create_land_use_test_file(
            area_factor=43560.0,
            nsplnp=2,
            nfqlnp=0,
            time_steps_data=time_steps
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                file_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, file_lines, 0)
            area_factor = float(file_lines[line_index].split()[0])
            line_index = iwfm.skip_ahead(line_index, file_lines, 4)

            # Count lines to next date
            lu_lines = 1
            while file_lines[line_index + lu_lines].find('_24:00') == -1:
                lu_lines += 1

            # Should be 1 (just the date line with first element)
            assert lu_lines == 1

        finally:
            os.unlink(temp_file)

    def test_count_lines_per_timestep_multiple_elements(self):
        """Test counting lines per time step with multiple elements"""
        time_steps = [
            ("09/30/1922_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0),
                (3, 200.0, 300.0, 400.0, 70.0, 95.0)
            ]),
            ("09/30/1923_24:00", [
                (1, 110.0, 210.0, 310.0, 55.0, 80.0),
                (2, 160.0, 260.0, 360.0, 65.0, 90.0),
                (3, 210.0, 310.0, 410.0, 75.0, 100.0)
            ])
        ]
        content = create_land_use_test_file(
            area_factor=43560.0,
            nsplnp=2,
            nfqlnp=0,
            time_steps_data=time_steps
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                file_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, file_lines, 0)
            area_factor = float(file_lines[line_index].split()[0])
            line_index = iwfm.skip_ahead(line_index, file_lines, 4)

            # Count lines to next date
            lu_lines = 1
            while file_lines[line_index + lu_lines].find('_24:00') == -1:
                lu_lines += 1

            # Should be 3 (1 date line + 2 element lines)
            assert lu_lines == 3

        finally:
            os.unlink(temp_file)

    def test_calculate_timesteps(self):
        """Test calculating number of time steps"""
        time_steps = [
            ("09/30/1922_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0)
            ]),
            ("09/30/1923_24:00", [
                (1, 110.0, 210.0, 310.0, 55.0, 80.0),
                (2, 160.0, 260.0, 360.0, 65.0, 90.0)
            ]),
            ("09/30/1924_24:00", [
                (1, 120.0, 220.0, 320.0, 60.0, 85.0),
                (2, 170.0, 270.0, 370.0, 70.0, 95.0)
            ])
        ]
        content = create_land_use_test_file(
            area_factor=43560.0,
            nsplnp=3,
            nfqlnp=0,
            time_steps_data=time_steps
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                file_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, file_lines, 0)
            area_factor = float(file_lines[line_index].split()[0])
            line_index = iwfm.skip_ahead(line_index, file_lines, 4)

            # Count lines to next date
            lu_lines = 1
            while file_lines[line_index + lu_lines].find('_24:00') == -1:
                lu_lines += 1

            # Calculate time steps
            data_lines = len(file_lines) - line_index
            time_steps_count = int(data_lines / lu_lines)

            assert time_steps_count == 3

        finally:
            os.unlink(temp_file)

    def test_parse_date_string(self):
        """Test parsing and formatting date string"""
        import re

        time_steps = [
            ("09/30/1922_24:00", [(1, 100.0, 200.0, 300.0, 50.0, 75.0)])
        ]
        content = create_land_use_test_file(
            area_factor=43560.0,
            nsplnp=1,
            nfqlnp=0,
            time_steps_data=time_steps
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                file_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, file_lines, 0)
            line_index = iwfm.skip_ahead(line_index, file_lines, 4)

            # Parse date from first data line
            work_str = file_lines[line_index]
            work_str = re.sub("/", "-", work_str)
            work_str = re.sub("_24:00", "", work_str)
            work_str = re.sub("\t", " ", work_str)
            work_str = work_str.split()
            field_name = work_str.pop(0)

            assert field_name == "09-30-1922"

        finally:
            os.unlink(temp_file)

    def test_parse_area_values_single_crop(self):
        """Test parsing area values from data line"""
        time_steps = [
            ("09/30/1922_24:00", [(1, 100.5, 200.3, 300.2, 50.1, 75.4)])
        ]
        content = create_land_use_test_file(
            area_factor=43560.0,
            nsplnp=1,
            nfqlnp=0,
            time_steps_data=time_steps
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            with open(temp_file) as f:
                file_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, file_lines, 0)
            line_index = iwfm.skip_ahead(line_index, file_lines, 4)

            # Parse first data line
            work_str = file_lines[line_index].split()
            # Remove date (first element)
            work_str.pop(0)

            # Calculate total area (sum of all crop types, excluding element ID)
            if len(work_str) > 2:
                area = 0
                for k in range(1, len(work_str)):
                    area += float(work_str[k])
            else:
                area = float(work_str[1])

            # Total should be 100.5 + 200.3 + 300.2 + 50.1 + 75.4 = 726.5
            assert abs(area - 726.5) < 0.01

        finally:
            os.unlink(temp_file)

    def test_area_factor_variants(self):
        """Test different area factor values"""
        for factor in [1.0, 43560.0, 4046.9]:  # acre, sq ft, sq meter (rounded to .1f)
            time_steps = [
                ("09/30/1922_24:00", [(1, 100.0, 200.0, 300.0, 50.0, 75.0)])
            ]
            content = create_land_use_test_file(
                area_factor=factor,
                nsplnp=1,
                nfqlnp=0,
                time_steps_data=time_steps
            )

            with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
                f.write(content)
                temp_file = f.name

            try:
                import iwfm
                with open(temp_file) as f:
                    file_lines = f.read().splitlines()

                line_index = iwfm.skip_ahead(0, file_lines, 0)
                area_factor = float(file_lines[line_index].split()[0])

                # Note: create_land_use_test_file formats with .1f, so precision is limited
                assert abs(area_factor - factor) < 0.01

            finally:
                os.unlink(temp_file)

    def test_multiple_timesteps_data_extraction(self):
        """Test extracting data from multiple time steps"""
        time_steps = [
            ("09/30/1922_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0)
            ]),
            ("09/30/1923_24:00", [
                (1, 110.0, 210.0, 310.0, 55.0, 80.0),
                (2, 160.0, 260.0, 360.0, 65.0, 90.0)
            ])
        ]
        content = create_land_use_test_file(
            area_factor=43560.0,
            nsplnp=2,
            nfqlnp=0,
            time_steps_data=time_steps
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            import iwfm
            import re

            with open(temp_file) as f:
                file_lines = f.read().splitlines()

            line_index = iwfm.skip_ahead(0, file_lines, 0)
            area_factor = float(file_lines[line_index].split()[0])
            line_index = iwfm.skip_ahead(line_index, file_lines, 4)

            # Count lines per timestep
            lu_lines = 1
            while file_lines[line_index + lu_lines].find('_24:00') == -1:
                lu_lines += 1

            # Extract dates from both time steps
            dates = []
            for i in range(2):
                work_str = file_lines[line_index + i * lu_lines]
                work_str = re.sub("/", "-", work_str)
                work_str = re.sub("_24:00", "", work_str)
                work_str = re.sub("\t", " ", work_str)
                work_str = work_str.split()
                field_name = work_str.pop(0)
                dates.append(field_name)

            assert dates[0] == "09-30-1922"
            assert dates[1] == "09-30-1923"

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
