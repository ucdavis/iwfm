#!/usr/bin/env python
# test_iwfm_lu2refined.py
# Unit tests for iwfm_lu2refined.py
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


def create_land_use_file(factlnp, nsplnp, nfqlnp, time_periods_data):
    """Create properly structured IWFM Land Use file for testing.

    IWFM File Format Convention:
    - Comment lines start with 'C', 'c', '*', or '#' in column 1
    - Data lines MUST start with whitespace (space or tab)

    Parameters
    ----------
    factlnp : float
        Conversion factor for land use area
    nsplnp : int
        Number of time steps to update land use data
    nfqlnp : int
        Repetition frequency of land use data
    time_periods_data : list of tuples
        Each tuple: (date, elem_data)
        elem_data: list of tuples (elem_id, rice_fl, rice_nfl, rice_ndc, refuge_sl, refuge_pr)

    Returns
    -------
    str
        File contents
    """
    # Header comments
    content = "C IWFM Land Use Data File\n"
    content += "C\n"
    content += "C Ponded Crop Area File\n"
    content += "C\n"

    # Parameters (skip_ahead(0, lines, 4) skips these 4 non-comment lines)
    content += f"          {factlnp}                                    / FACTLNP\n"
    content += f"          {nsplnp}                                          / NSPLNP\n"
    content += f"          {nfqlnp}                                          / NFQLNP\n"
    content += "                                                     / DSSFL\n"

    content += "C\n"
    content += "C Land Use Data\n"
    content += "C\n"

    # Land use data for each time period
    for date, elem_data in time_periods_data:
        for i, (elem_id, rice_fl, rice_nfl, rice_ndc, refuge_sl, refuge_pr) in enumerate(elem_data):
            if i == 0:
                # First line contains date
                content += f"{date}\t{elem_id}\t{rice_fl:.5f}\t{rice_nfl:.5f}\t{rice_ndc:.5f}\t{refuge_sl:.5f}\t{refuge_pr:.5f}\n"
            else:
                # Subsequent lines start with tab
                content += f"\t{elem_id}\t{rice_fl:.5f}\t{rice_nfl:.5f}\t{rice_ndc:.5f}\t{refuge_sl:.5f}\t{refuge_pr:.5f}\n"

    return content


class TestIwfmLu2Refined:
    """Tests for iwfm_lu2refined function"""

    def test_single_time_period_single_element(self):
        """Test refining single time period with single element"""
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            # Create refinement factors: [refined_elem, orig_elem, area_mult]
            # Refine element 1 into two elements with different multipliers
            lu_factors = [
                [101, 1, 0.6],  # 60% of original element
                [102, 1, 0.4]   # 40% of original element
            ]

            iwfm_lu2refined(temp_file, lu_factors, verbose=False)

            # Check output file was created
            output_file = base_name + '_refined.dat'
            assert os.path.exists(output_file)

            # Read and verify output
            with open(output_file) as f:
                lines = f.read().splitlines()

            # Find data lines (after header) - exclude comments and parameter lines with '/ FACT'
            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and not '/ ' in l]

            # Should have 2 data lines (one for each refined element)
            assert len(data_lines) == 2

            # Verify first refined element (60% of original)
            parts1 = data_lines[0].split()
            assert parts1[0] == "09/30/2020_24:00"
            assert int(parts1[1]) == 101
            assert float(parts1[2]) == pytest.approx(60.0, abs=0.001)   # 100.0 * 0.6
            assert float(parts1[3]) == pytest.approx(120.0, abs=0.001)  # 200.0 * 0.6
            assert float(parts1[4]) == pytest.approx(180.0, abs=0.001)  # 300.0 * 0.6
            assert float(parts1[5]) == pytest.approx(30.0, abs=0.001)   # 50.0 * 0.6
            assert float(parts1[6]) == pytest.approx(45.0, abs=0.001)   # 75.0 * 0.6

            # Verify second refined element (40% of original)
            parts2 = data_lines[1].split()
            assert int(parts2[0]) == 102  # No date on second line
            assert float(parts2[1]) == pytest.approx(40.0, abs=0.001)   # 100.0 * 0.4
            assert float(parts2[2]) == pytest.approx(80.0, abs=0.001)   # 200.0 * 0.4
            assert float(parts2[3]) == pytest.approx(120.0, abs=0.001)  # 300.0 * 0.4

        finally:
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_single_time_period_multiple_elements(self):
        """Test refining single time period with multiple elements"""
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0),
                (3, 200.0, 300.0, 400.0, 70.0, 95.0)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            # Refine elements 1 and 3
            lu_factors = [
                [101, 1, 0.5],  # 50% of element 1
                [102, 1, 0.5],  # 50% of element 1
                [301, 3, 1.0]   # 100% of element 3
            ]

            iwfm_lu2refined(temp_file, lu_factors, verbose=False)

            output_file = base_name + '_refined.dat'
            assert os.path.exists(output_file)

            with open(output_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]
            assert len(data_lines) == 3

            # Verify refined elements
            parts1 = data_lines[0].split()
            assert parts1[0] == "09/30/2020_24:00"
            assert int(parts1[1]) == 101
            assert float(parts1[2]) == pytest.approx(50.0, abs=0.001)

            parts2 = data_lines[1].split()
            assert int(parts2[0]) == 102
            assert float(parts2[1]) == pytest.approx(50.0, abs=0.001)

            parts3 = data_lines[2].split()
            assert int(parts3[0]) == 301
            assert float(parts3[1]) == pytest.approx(200.0, abs=0.001)

        finally:
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_multiple_time_periods(self):
        """Test refining multiple time periods"""
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0)
            ]),
            ("09/30/2021_24:00", [
                (1, 110.0, 210.0, 310.0, 55.0, 80.0),
                (2, 160.0, 260.0, 360.0, 65.0, 90.0)
            ]),
            ("09/30/2022_24:00", [
                (1, 120.0, 220.0, 320.0, 60.0, 85.0),
                (2, 170.0, 270.0, 370.0, 70.0, 95.0)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            lu_factors = [
                [101, 1, 0.7],
                [201, 2, 0.5]
            ]

            iwfm_lu2refined(temp_file, lu_factors, verbose=False)

            output_file = base_name + '_refined.dat'
            assert os.path.exists(output_file)

            with open(output_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]

            # Should have 6 data lines (2 refined elements × 3 time periods)
            assert len(data_lines) == 6

            # Verify first time period
            assert "09/30/2020_24:00" in data_lines[0]
            assert int(data_lines[0].split()[1]) == 101
            assert float(data_lines[0].split()[2]) == pytest.approx(70.0, abs=0.001)  # 100.0 * 0.7

            # Verify second time period
            assert "09/30/2021_24:00" in data_lines[2]
            assert int(data_lines[2].split()[1]) == 101
            assert float(data_lines[2].split()[2]) == pytest.approx(77.0, abs=0.001)  # 110.0 * 0.7

            # Verify third time period
            assert "09/30/2022_24:00" in data_lines[4]
            assert int(data_lines[4].split()[1]) == 101
            assert float(data_lines[4].split()[2]) == pytest.approx(84.0, abs=0.001)  # 120.0 * 0.7

        finally:
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_zero_areas(self):
        """Test handling of zero crop areas"""
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 0.0, 0.0, 0.0, 0.0, 0.0),
                (2, 100.0, 0.0, 0.0, 0.0, 50.0)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            lu_factors = [
                [101, 1, 0.5],
                [201, 2, 0.6]
            ]

            iwfm_lu2refined(temp_file, lu_factors, verbose=False)

            output_file = base_name + '_refined.dat'
            with open(output_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]

            # Verify zero areas remain zero after multiplication
            parts1 = data_lines[0].split()
            assert float(parts1[2]) == 0.0
            assert float(parts1[3]) == 0.0

            # Verify non-zero areas are multiplied correctly
            parts2 = data_lines[1].split()
            assert float(parts2[1]) == pytest.approx(60.0, abs=0.001)   # 100.0 * 0.6
            assert float(parts2[5]) == pytest.approx(30.0, abs=0.001)   # 50.0 * 0.6

        finally:
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_fractional_multipliers(self):
        """Test various fractional area multipliers"""
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 1000.0, 2000.0, 3000.0, 500.0, 750.0)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            lu_factors = [
                [101, 1, 0.333],
                [102, 1, 0.667]
            ]

            iwfm_lu2refined(temp_file, lu_factors, verbose=False)

            output_file = base_name + '_refined.dat'
            with open(output_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]

            parts1 = data_lines[0].split()
            assert float(parts1[2]) == pytest.approx(333.0, abs=0.001)    # 1000.0 * 0.333
            assert float(parts1[3]) == pytest.approx(666.0, abs=0.001)    # 2000.0 * 0.333

            parts2 = data_lines[1].split()
            assert float(parts2[1]) == pytest.approx(667.0, abs=0.001)    # 1000.0 * 0.667
            assert float(parts2[2]) == pytest.approx(1334.0, abs=0.001)   # 2000.0 * 0.667

        finally:
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_output_file_naming(self):
        """Test that output file has correct naming convention"""
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.', prefix='test_lu_') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            lu_factors = [[101, 1, 1.0]]

            iwfm_lu2refined(temp_file, lu_factors, verbose=False)

            # Check output file name
            output_file = base_name + '_refined.dat'
            assert os.path.exists(output_file)
            assert output_file.endswith('_refined.dat')
            assert 'test_lu_' in output_file

        finally:
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_header_preservation(self):
        """Test that header lines are preserved in output"""
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            lu_factors = [[101, 1, 1.0]]

            iwfm_lu2refined(temp_file, lu_factors, verbose=False)

            output_file = base_name + '_refined.dat'

            with open(output_file) as f:
                lines = f.read().splitlines()

            # Verify header comments are present
            comment_lines = [l for l in lines if l.strip().startswith('C')]
            assert len(comment_lines) > 0

            # Verify FACTLNP line is present
            factlnp_lines = [l for l in lines if 'FACTLNP' in l]
            assert len(factlnp_lines) == 1
            assert '43560.0' in factlnp_lines[0]

        finally:
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_rounding_precision(self):
        """Test that values are rounded to 3 decimal places"""
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 123.456789, 234.567891, 345.678912, 456.789123, 567.891234)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            lu_factors = [[101, 1, 0.5]]

            iwfm_lu2refined(temp_file, lu_factors, verbose=False)

            output_file = base_name + '_refined.dat'

            with open(output_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]
            parts = data_lines[0].split()

            # Values should be rounded to 3 decimal places
            # 123.456789 * 0.5 = 61.7283945, rounded to 61.728
            assert parts[2] == "61.728"
            # 234.567891 * 0.5 = 117.2839455, rounded to 117.284
            assert parts[3] == "117.284"

        finally:
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_verbose_output(self, capsys):
        """Test verbose mode output"""
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0)
            ]),
            ("09/30/2021_24:00", [
                (1, 110.0, 210.0, 310.0, 55.0, 80.0)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            lu_factors = [[101, 1, 1.0]]

            iwfm_lu2refined(temp_file, lu_factors, verbose=True)

            captured = capsys.readouterr()

            # Check verbose output contains processing messages
            assert "Processing 09/30/2020_24:00" in captured.out
            assert "Processing 09/30/2021_24:00" in captured.out
            assert "Wrote 2 time periods" in captured.out

        finally:
            output_file = base_name + '_refined.dat'
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM file"""
        # Simulate real file with ponded crop data
        time_periods_data = [
            ("09/30/1922_24:00", [
                (1, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000),
                (2, 150.50000, 200.75000, 0.00000, 50.25000, 0.00000),
                (3, 0.00000, 0.00000, 500.00000, 0.00000, 100.00000)
            ])
        ]
        content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False, dir='.') as f:
            f.write(content)
            temp_file = f.name
            base_name = os.path.basename(temp_file).split('.')[0]

        try:
            from iwfm.iwfm_lu2refined import iwfm_lu2refined

            lu_factors = [
                [101, 1, 1.0],
                [201, 2, 0.6],
                [202, 2, 0.4],
                [301, 3, 1.0]
            ]

            iwfm_lu2refined(temp_file, lu_factors, verbose=False)

            output_file = base_name + '_refined.dat'
            with open(output_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]
            assert len(data_lines) == 4

            # Verify refined data
            parts1 = data_lines[0].split()
            assert parts1[0] == "09/30/1922_24:00"
            assert int(parts1[1]) == 101

            parts2 = data_lines[1].split()
            assert int(parts2[0]) == 201
            assert float(parts2[1]) == pytest.approx(90.3, abs=0.001)    # 150.5 * 0.6
            assert float(parts2[2]) == pytest.approx(120.45, abs=0.001)  # 200.75 * 0.6

            parts3 = data_lines[2].split()
            assert int(parts3[0]) == 202
            assert float(parts3[1]) == pytest.approx(60.2, abs=0.001)    # 150.5 * 0.4

        finally:
            os.unlink(temp_file)
            if os.path.exists(output_file):
                os.unlink(output_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
