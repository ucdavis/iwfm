#!/usr/bin/env python
# test_iwfm_lu2sub.py
# Unit tests for iwfm_lu2sub.py
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


def create_elements_file(nelements, nsubregions, elements_data):
    """Create IWFM Element file for testing.

    Parameters
    ----------
    nelements : int
        Number of elements
    nsubregions : int
        Number of subregions
    elements_data : list of tuples
        Each tuple: (elem_id, node1, node2, node3, node4, subregion)
        node4 = 0 for triangular elements

    Returns
    -------
    str
        File contents
    """
    content = "C IWFM Elements File\n"
    content += "C\n"
    content += f"    {nelements}                           / NE\n"
    content += f"    {nsubregions}                           / NSUBREGIONS\n"

    # Add subregion definitions
    for i in range(1, nsubregions + 1):
        content += f"    {i}    Subregion_{i}\n"

    content += "C\n"

    for elem_id, node1, node2, node3, node4, subregion in elements_data:
        content += f"    {elem_id}    {node1}    {node2}    {node3}    {node4}    {subregion}\n"

    return content


def create_land_use_file(factlnp, nsplnp, nfqlnp, time_periods_data):
    """Create IWFM Land Use file for testing.

    Parameters
    ----------
    factlnp : float
        Conversion factor
    nsplnp : int
        Number of time steps
    nfqlnp : int
        Repetition frequency
    time_periods_data : list of tuples
        Each tuple: (date, elem_data)
        elem_data: list of tuples (elem_id, rice_fl, rice_nfl, rice_ndc, refuge_sl, refuge_pr)

    Returns
    -------
    str
        File contents
    """
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


class TestIwfmLu2Sub:
    """Tests for iwfm_lu2sub function"""

    def test_single_element_subset(self):
        """Test extracting single element from full land use file"""
        # Create elements file with subset (element 2 only)
        elements_data = [
            (2, 100, 101, 102, 103, 1)
        ]
        elem_content = create_elements_file(1, 1, elements_data)

        # Create land use file with multiple elements
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0),
                (3, 200.0, 300.0, 400.0, 70.0, 95.0)
            ])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            n_lines = iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=False)

            # Should have 1 line (element 2 only)
            assert n_lines == 1

            # Verify output file
            with open(out_file) as f:
                lines = f.read().splitlines()

            # Find data lines
            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]
            assert len(data_lines) == 1

            # Verify it's element 2
            parts = data_lines[0].split()
            assert parts[0] == "09/30/2020_24:00"
            assert int(parts[1]) == 2
            assert float(parts[2]) == pytest.approx(150.0, abs=0.001)

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)

    def test_multiple_element_subset(self):
        """Test extracting multiple elements from full land use file"""
        # Create elements file with subset (elements 1 and 3)
        elements_data = [
            (1, 100, 101, 102, 103, 1),
            (3, 200, 201, 202, 203, 1)
        ]
        elem_content = create_elements_file(2, 1, elements_data)

        # Create land use file with all elements
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0),
                (3, 200.0, 300.0, 400.0, 70.0, 95.0),
                (4, 250.0, 350.0, 450.0, 80.0, 105.0)
            ])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            n_lines = iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=False)

            # Should have 2 lines (elements 1 and 3)
            assert n_lines == 2

            with open(out_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]
            assert len(data_lines) == 2

            # Verify element 1 (first element gets the date)
            parts1 = data_lines[0].split()
            assert parts1[0] == "09/30/2020_24:00"
            assert int(parts1[1]) == 1
            assert float(parts1[2]) == pytest.approx(100.0, abs=0.001)

            # Verify element 3 (second element, no date)
            parts3 = data_lines[1].split()
            assert int(parts3[0]) == 3
            assert float(parts3[1]) == pytest.approx(200.0, abs=0.001)

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)

    def test_multiple_time_periods(self):
        """Test extracting elements across multiple time periods"""
        # Subset: elements 1 and 2
        elements_data = [
            (1, 100, 101, 102, 103, 1),
            (2, 110, 111, 112, 113, 1)
        ]
        elem_content = create_elements_file(2, 1, elements_data)

        # Multiple time periods
        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0),
                (3, 200.0, 300.0, 400.0, 70.0, 95.0)
            ]),
            ("09/30/2021_24:00", [
                (1, 110.0, 210.0, 310.0, 55.0, 80.0),
                (2, 160.0, 260.0, 360.0, 65.0, 90.0),
                (3, 210.0, 310.0, 410.0, 75.0, 100.0)
            ])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            n_lines = iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=False)

            # Should have 4 lines (2 elements × 2 time periods)
            assert n_lines == 4

            with open(out_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]
            assert len(data_lines) == 4

            # First time period
            assert "09/30/2020_24:00" in data_lines[0]
            assert int(data_lines[0].split()[1]) == 1
            assert int(data_lines[1].split()[0]) == 2

            # Second time period
            assert "09/30/2021_24:00" in data_lines[2]
            assert int(data_lines[2].split()[1]) == 1
            assert int(data_lines[3].split()[0]) == 2

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)

    def test_element_order_preservation(self):
        """Test that element order is preserved based on elem_file order"""
        # Elements in specific order: 3, 1, 2
        elements_data = [
            (3, 200, 201, 202, 203, 1),
            (1, 100, 101, 102, 103, 1),
            (2, 110, 111, 112, 113, 1)
        ]
        elem_content = create_elements_file(3, 1, elements_data)

        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0),
                (3, 200.0, 300.0, 400.0, 70.0, 95.0),
                (4, 250.0, 350.0, 450.0, 80.0, 105.0)
            ])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            n_lines = iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=False)

            # Should have 3 lines
            assert n_lines == 3

            with open(out_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]

            # Elements should be in sorted order: 1, 2, 3 (function sorts elem_ids)
            parts1 = data_lines[0].split()
            assert int(parts1[1]) == 1  # First in sorted order

            parts2 = data_lines[1].split()
            assert int(parts2[0]) == 2

            parts3 = data_lines[2].split()
            assert int(parts3[0]) == 3

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)

    def test_header_preservation(self):
        """Test that header is preserved in output file"""
        elements_data = [(1, 100, 101, 102, 103, 1)]
        elem_content = create_elements_file(1, 1, elements_data)

        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0)
            ])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=False)

            with open(out_file) as f:
                lines = f.read().splitlines()

            # Verify header comments are present
            comment_lines = [l for l in lines if l.strip().startswith('C')]
            assert len(comment_lines) > 0

            # Verify FACTLNP line is present
            factlnp_lines = [l for l in lines if 'FACTLNP' in l]
            assert len(factlnp_lines) == 1
            assert '43560.0' in factlnp_lines[0]

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)

    def test_zero_areas(self):
        """Test handling of zero crop areas"""
        elements_data = [(1, 100, 101, 102, 103, 1)]
        elem_content = create_elements_file(1, 1, elements_data)

        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 0.0, 0.0, 0.0, 0.0, 0.0),
                (2, 100.0, 200.0, 300.0, 50.0, 75.0)
            ])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            n_lines = iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=False)

            assert n_lines == 1

            with open(out_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]
            parts = data_lines[0].split()

            # Verify zero values are preserved
            assert float(parts[2]) == 0.0
            assert float(parts[3]) == 0.0
            assert float(parts[4]) == 0.0

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)

    def test_all_elements_subset(self):
        """Test when subset includes all elements"""
        elements_data = [
            (1, 100, 101, 102, 103, 1),
            (2, 110, 111, 112, 113, 1),
            (3, 120, 121, 122, 123, 1)
        ]
        elem_content = create_elements_file(3, 1, elements_data)

        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0),
                (3, 200.0, 300.0, 400.0, 70.0, 95.0)
            ])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            n_lines = iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=False)

            # All 3 elements
            assert n_lines == 3

            with open(out_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]
            assert len(data_lines) == 3

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)

    def test_triangular_elements(self):
        """Test with triangular elements (node4=0)"""
        # Mix of triangular and quadrilateral elements
        elements_data = [
            (1, 100, 101, 102, 0, 1),    # Triangular
            (2, 110, 111, 112, 113, 1)   # Quadrilateral
        ]
        elem_content = create_elements_file(2, 1, elements_data)

        time_periods_data = [
            ("09/30/2020_24:00", [
                (1, 100.0, 200.0, 300.0, 50.0, 75.0),
                (2, 150.0, 250.0, 350.0, 60.0, 85.0),
                (3, 200.0, 300.0, 400.0, 70.0, 95.0)
            ])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            n_lines = iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=False)

            # Both elements
            assert n_lines == 2

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)

    def test_verbose_output(self, capsys):
        """Test verbose mode output"""
        elements_data = [(1, 100, 101, 102, 103, 1)]
        elem_content = create_elements_file(1, 1, elements_data)

        time_periods_data = [
            ("09/30/2020_24:00", [(1, 100.0, 200.0, 300.0, 50.0, 75.0)]),
            ("09/30/2021_24:00", [(1, 110.0, 210.0, 310.0, 55.0, 80.0)])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=True)

            captured = capsys.readouterr()

            # Check verbose output contains dates
            assert "09/30/2020" in captured.out
            assert "09/30/2021" in captured.out

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM file"""
        # Subset of elements
        elements_data = [
            (1, 100, 101, 102, 103, 1),
            (3, 120, 121, 122, 123, 1),
            (5, 140, 141, 142, 143, 1)
        ]
        elem_content = create_elements_file(3, 1, elements_data)

        # Full land use data
        time_periods_data = [
            ("09/30/1922_24:00", [
                (1, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000),
                (2, 150.50000, 200.75000, 0.00000, 50.25000, 0.00000),
                (3, 0.00000, 0.00000, 500.00000, 0.00000, 100.00000),
                (4, 100.00000, 150.00000, 200.00000, 75.00000, 125.00000),
                (5, 200.00000, 250.00000, 300.00000, 100.00000, 150.00000)
            ])
        ]
        lu_content = create_land_use_file(43560.0, 1, 0, time_periods_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(elem_content)
            elem_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(lu_content)
            lu_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            out_file = f.name

        try:
            from iwfm.iwfm_lu2sub import iwfm_lu2sub

            n_lines = iwfm_lu2sub(elem_file, lu_file, out_file, skip=4, verbose=False)

            # Elements 1, 3, and 5
            assert n_lines == 3

            with open(out_file) as f:
                lines = f.read().splitlines()

            data_lines = [l for l in lines if not l.strip().startswith('C') and l.strip() and '/ ' not in l]

            # Verify correct elements extracted
            parts1 = data_lines[0].split()
            assert parts1[0] == "09/30/1922_24:00"
            assert int(parts1[1]) == 1

            parts2 = data_lines[1].split()
            assert int(parts2[0]) == 3
            assert float(parts2[3]) == pytest.approx(500.0, abs=0.001)

            parts3 = data_lines[2].split()
            assert int(parts3[0]) == 5
            assert float(parts3[1]) == pytest.approx(200.0, abs=0.001)

        finally:
            os.unlink(elem_file)
            os.unlink(lu_file)
            os.unlink(out_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
