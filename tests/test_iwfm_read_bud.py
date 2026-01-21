#!/usr/bin/env python
# test_iwfm_read_bud.py
# Unit tests for iwfm_read_bud.py
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


def create_budget_file(factlou, unitlou, factarou, unitarou, factvolou, unitvolou,
                       cache, bdt, edt, nbudget, budget_data):
    """Create IWFM Budget input file for testing.

    Parameters
    ----------
    factlou : float
        Factor to convert length units
    unitlou : str
        Output unit of length
    factarou : float
        Factor to convert area units
    unitarou : str
        Output unit of area
    factvolou : float
        Factor to convert volume units
    unitvolou : str
        Output unit of volume
    cache : int
        Cache size for output
    bdt : str
        Beginning date/time (MM/DD/YYYY_HH:MM)
    edt : str
        Ending date/time (MM/DD/YYYY_HH:MM)
    nbudget : int
        Number of budget classes
    budget_data : list of tuples
        Each tuple: (hdffile, outfile, intprnt, nlprint, lprint)

    Returns
    -------
    str
        File contents
    """
    content = "C IWFM Budget Input File\n"
    content += "C\n"
    content += "C Output Unit Control\n"
    content += "C\n"

    # Conversion factors and units (skip_ahead(0, lines, 0) starts here)
    content += f"    {factlou}                           / FACTLTOU\n"
    content += f"    {unitlou}                          / UNITLTOU\n"
    content += f"    {factarou}                   / FACTAROU\n"
    content += f"    {unitarou}                            / UNITAROU\n"
    content += f"    {factvolou}                   / FACTVLOU\n"
    content += f"    {unitvolou}                        / UNITVLOU\n"

    # Cache size
    content += f"    {cache}                        / CACHE\n"

    # Begin and end dates
    content += f"    {bdt}            / BDT\n"
    content += f"    {edt}            / EDT\n"

    # Number of budgets
    content += f"    {nbudget}                           / NBUDGET\n"
    content += "C\n"

    # Budget data for each budget class
    for hdffile, outfile, intprnt, nlprint, lprint in budget_data:
        content += f"  {hdffile}             / HDFFILE\n"
        content += f"  {outfile}             / OUTFILE\n"
        # If intprnt is empty, format like real files (tabs then / INTPRNT)
        if intprnt == "":
            content += "\t\t\t\t\t/ INTPRNT\n"
        else:
            content += f"  {intprnt}                       / INTPRNT\n"
        content += f"   {nlprint}                        / NLPRNT\n"
        content += f"  {lprint}                        / LPRNT[1]\n"

    return content


class TestIwfmReadBud:
    """Tests for iwfm_read_bud function"""

    def test_single_budget(self):
        """Test reading budget file with single budget class"""
        budget_data = [
            ("GW_Budget.hdf", "GW_Budget.bud", "", "1", "-1")
        ]

        content = create_budget_file(
            factlou=1.0,
            unitlou="FEET",
            factarou=0.000022957,
            unitarou="AC",
            factvolou=0.000022957,
            unitvolou="AC.FT.",
            cache=500000,
            bdt="09/30/1900_24:00",
            edt="09/30/2100_24:00",
            nbudget=1,
            budget_data=budget_data
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_bud import iwfm_read_bud

            budget_list, factors = iwfm_read_bud(temp_file, verbose=False)

            # Verify factors
            assert factors[0] == 1  # nbudget
            assert factors[1] == 1.0  # factlou
            assert factors[2] == "FEET"  # unitlou
            assert factors[3] == pytest.approx(0.000022957, abs=1e-9)  # factarou
            assert factors[4] == "AC"  # unitarou
            assert factors[5] == pytest.approx(0.000022957, abs=1e-9)  # factvolou
            assert factors[6] == "AC.FT."  # unitvolou
            assert factors[7] == "09/30/1900_24:00"  # bdt
            assert factors[8] == "09/30/2100_24:00"  # edt

            # Verify budget list
            assert len(budget_list) == 1
            assert budget_list[0][0] == "GW_Budget.hdf"
            assert budget_list[0][1] == "GW_Budget.bud"
            assert budget_list[0][2] == "/"  # Empty interval reads as "/"
            assert budget_list[0][3] == "1"
            assert budget_list[0][4] == "-1"

        finally:
            os.unlink(temp_file)

    def test_multiple_budgets(self):
        """Test reading budget file with multiple budget classes"""
        budget_data = [
            ("GW_Budget.hdf", "GW_Budget.bud", "", "1", "-1"),
            ("LWU_Budget.hdf", "LWU_Budget.bud", "1MON", "1", "-1"),
            ("RZ_Budget.hdf", "RZ_Budget.bud", "", "2", "1")
        ]

        content = create_budget_file(
            factlou=1.0,
            unitlou="FEET",
            factarou=0.000022957,
            unitarou="AC",
            factvolou=0.000022957,
            unitvolou="AC.FT.",
            cache=500000,
            bdt="09/30/2000_24:00",
            edt="09/30/2020_24:00",
            nbudget=3,
            budget_data=budget_data
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_bud import iwfm_read_bud

            budget_list, factors = iwfm_read_bud(temp_file, verbose=False)

            # Verify nbudget
            assert factors[0] == 3

            # Verify budget list
            assert len(budget_list) == 3

            # First budget
            assert budget_list[0][0] == "GW_Budget.hdf"
            assert budget_list[0][1] == "GW_Budget.bud"

            # Second budget
            assert budget_list[1][0] == "LWU_Budget.hdf"
            assert budget_list[1][1] == "LWU_Budget.bud"
            assert budget_list[1][2] == "1MON"

            # Third budget
            assert budget_list[2][0] == "RZ_Budget.hdf"
            assert budget_list[2][1] == "RZ_Budget.bud"
            assert budget_list[2][3] == "2"
            assert budget_list[2][4] == "1"

        finally:
            os.unlink(temp_file)

    def test_metric_units(self):
        """Test reading budget file with metric units"""
        budget_data = [
            ("Budget.hdf", "Budget.bud", "", "1", "-1")
        ]

        content = create_budget_file(
            factlou=1.0,
            unitlou="METERS",
            factarou=1.0,
            unitarou="HA",
            factvolou=1.0,
            unitvolou="HA.M.",
            cache=100000,
            bdt="01/01/2000_00:00",
            edt="12/31/2020_24:00",
            nbudget=1,
            budget_data=budget_data
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_bud import iwfm_read_bud

            budget_list, factors = iwfm_read_bud(temp_file, verbose=False)

            # Verify metric units
            assert factors[1] == 1.0
            assert factors[2] == "METERS"
            assert factors[3] == 1.0
            assert factors[4] == "HA"
            assert factors[5] == 1.0
            assert factors[6] == "HA.M."

        finally:
            os.unlink(temp_file)

    def test_different_cache_sizes(self):
        """Test reading budget file with different cache sizes"""
        budget_data = [
            ("Budget.hdf", "Budget.bud", "", "1", "-1")
        ]

        for cache_size in [100000, 500000, 1000000]:
            content = create_budget_file(
                factlou=1.0,
                unitlou="FEET",
                factarou=0.000022957,
                unitarou="AC",
                factvolou=0.000022957,
                unitvolou="AC.FT.",
                cache=cache_size,
                bdt="09/30/1900_24:00",
                edt="09/30/2100_24:00",
                nbudget=1,
                budget_data=budget_data
            )

            with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
                f.write(content)
                temp_file = f.name

            try:
                from iwfm.iwfm_read_bud import iwfm_read_bud

                budget_list, factors = iwfm_read_bud(temp_file, verbose=False)

                # Cache is read but not returned in factors
                # Just verify the function executes successfully
                assert len(budget_list) == 1

            finally:
                os.unlink(temp_file)

    def test_different_date_formats(self):
        """Test reading budget file with different date formats"""
        budget_data = [
            ("Budget.hdf", "Budget.bud", "", "1", "-1")
        ]

        date_pairs = [
            ("01/01/1990_00:00", "12/31/2020_24:00"),
            ("10/01/2000_12:00", "09/30/2010_18:00"),
            ("06/15/1985_06:30", "06/15/2025_18:45")
        ]

        for bdt, edt in date_pairs:
            content = create_budget_file(
                factlou=1.0,
                unitlou="FEET",
                factarou=0.000022957,
                unitarou="AC",
                factvolou=0.000022957,
                unitvolou="AC.FT.",
                cache=500000,
                bdt=bdt,
                edt=edt,
                nbudget=1,
                budget_data=budget_data
            )

            with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
                f.write(content)
                temp_file = f.name

            try:
                from iwfm.iwfm_read_bud import iwfm_read_bud

                budget_list, factors = iwfm_read_bud(temp_file, verbose=False)

                assert factors[7] == bdt
                assert factors[8] == edt

            finally:
                os.unlink(temp_file)

    def test_interval_specifications(self):
        """Test reading budget files with different interval specifications"""
        budget_data = [
            ("Budget1.hdf", "Budget1.bud", "", "1", "-1"),
            ("Budget2.hdf", "Budget2.bud", "1DAY", "1", "-1"),
            ("Budget3.hdf", "Budget3.bud", "1MON", "1", "0"),
            ("Budget4.hdf", "Budget4.bud", "1YEAR", "3", "1")
        ]

        content = create_budget_file(
            factlou=1.0,
            unitlou="FEET",
            factarou=0.000022957,
            unitarou="AC",
            factvolou=0.000022957,
            unitvolou="AC.FT.",
            cache=500000,
            bdt="09/30/1900_24:00",
            edt="09/30/2100_24:00",
            nbudget=4,
            budget_data=budget_data
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_bud import iwfm_read_bud

            budget_list, factors = iwfm_read_bud(temp_file, verbose=False)

            # Verify intervals
            assert budget_list[0][2] == "/"  # Empty interval reads as "/"
            assert budget_list[1][2] == "1DAY"
            assert budget_list[2][2] == "1MON"
            assert budget_list[3][2] == "1YEAR"

            # Verify nlprint values
            assert budget_list[0][3] == "1"
            assert budget_list[1][3] == "1"
            assert budget_list[2][3] == "1"
            assert budget_list[3][3] == "3"

            # Verify lprint values
            assert budget_list[0][4] == "-1"
            assert budget_list[1][4] == "-1"
            assert budget_list[2][4] == "0"
            assert budget_list[3][4] == "1"

        finally:
            os.unlink(temp_file)

    def test_verbose_mode(self):
        """Test reading budget file in verbose mode"""
        budget_data = [
            ("Budget.hdf", "Budget.bud", "", "1", "-1")
        ]

        content = create_budget_file(
            factlou=1.0,
            unitlou="FEET",
            factarou=0.000022957,
            unitarou="AC",
            factvolou=0.000022957,
            unitvolou="AC.FT.",
            cache=500000,
            bdt="09/30/1900_24:00",
            edt="09/30/2100_24:00",
            nbudget=1,
            budget_data=budget_data
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_bud import iwfm_read_bud

            # Should run without error in verbose mode
            budget_list, factors = iwfm_read_bud(temp_file, verbose=True)

            assert len(budget_list) == 1
            assert factors[0] == 1

        finally:
            os.unlink(temp_file)

    def test_seven_budgets_real_format(self):
        """Test reading budget file with 7 budget classes like real C2VSimCG file"""
        budget_data = [
            ("../Results/C2VSimCG_GW_Budget.hdf", "../Results/C2VSimCG_GW_Budget.bud", "", "1", "-1"),
            ("../Results/C2VSimCG_LWU_Budget.hdf", "../Results/C2VSimCG_LWU_Budget.bud", "", "1", "-1"),
            ("../Results/C2VSimCG_RZ_Budget.hdf", "../Results/C2VSimCG_RZ_Budget.bud", "", "1", "-1"),
            ("../Results/C2VSimCG_Streams_Budget.hdf", "../Results/C2VSimCG_Streams_Budget.bud", "", "1", "-1"),
            ("../Results/C2VSimCG_SWatersheds_Budget.hdf", "../Results/C2VSimCG_SWatersheds_Budget.bud", "", "1", "-1"),
            ("../Results/C2VSimCG_Diversions.hdf", "../Results/C2VSimCG_Diversions.bud", "", "1", "-1"),
            ("../Results/C2VSimCG_Unsat_Budget.hdf", "../Results/C2VSimCG_Unsat_Budget.bud", "", "1", "-1")
        ]

        content = create_budget_file(
            factlou=1.0,
            unitlou="FEET",
            factarou=0.000022957,
            unitarou="AC",
            factvolou=0.000022957,
            unitvolou="AC.FT.",
            cache=500000,
            bdt="09/30/1900_24:00",
            edt="09/30/2100_24:00",
            nbudget=7,
            budget_data=budget_data
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_bud import iwfm_read_bud

            budget_list, factors = iwfm_read_bud(temp_file, verbose=False)

            # Verify all 7 budgets
            assert factors[0] == 7
            assert len(budget_list) == 7

            # Verify groundwater budget
            assert "GW_Budget" in budget_list[0][0]

            # Verify streams budget
            assert "Streams_Budget" in budget_list[3][0]

            # Verify unsaturated zone budget
            assert "Unsat_Budget" in budget_list[6][0]

        finally:
            os.unlink(temp_file)

    def test_conversion_factors(self):
        """Test reading budget file with various conversion factors"""
        budget_data = [
            ("Budget.hdf", "Budget.bud", "", "1", "-1")
        ]

        # Test different conversion factors
        test_factors = [
            (1.0, 0.000022957, 0.000022957),  # Standard (feet, acres, acre-feet)
            (0.3048, 0.0001, 0.0001),  # Feet to meters, sqft to ha
            (3.28084, 2.47105, 0.000810713)  # Meters to feet, ha to acres
        ]

        for factlou, factarou, factvolou in test_factors:
            content = create_budget_file(
                factlou=factlou,
                unitlou="UNIT1",
                factarou=factarou,
                unitarou="UNIT2",
                factvolou=factvolou,
                unitvolou="UNIT3",
                cache=500000,
                bdt="09/30/1900_24:00",
                edt="09/30/2100_24:00",
                nbudget=1,
                budget_data=budget_data
            )

            with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
                f.write(content)
                temp_file = f.name

            try:
                from iwfm.iwfm_read_bud import iwfm_read_bud

                budget_list, factors = iwfm_read_bud(temp_file, verbose=False)

                assert factors[1] == pytest.approx(factlou, abs=1e-6)
                assert factors[3] == pytest.approx(factarou, abs=1e-9)
                assert factors[5] == pytest.approx(factvolou, abs=1e-9)

            finally:
                os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Budget Input File\n"
        content += "C This is a comment\n"
        content += "c Another comment with lowercase c\n"
        content += "* Comment with asterisk\n"
        content += "# Comment with hash\n"
        content += "C\n"
        content += "    1.0                           / FACTLTOU\n"
        content += "C Comment between data\n"
        content += "    FEET                          / UNITLTOU\n"
        content += "    0.000022957                   / FACTAROU\n"
        content += "    AC                            / UNITAROU\n"
        content += "    0.000022957                   / FACTVLOU\n"
        content += "    AC.FT.                        / UNITVLOU\n"
        content += "    500000                        / CACHE\n"
        content += "    09/30/1900_24:00            / BDT\n"
        content += "    09/30/2100_24:00            / EDT\n"
        content += "C More comments\n"
        content += "    1                           / NBUDGET\n"
        content += "C Budget class 1\n"
        content += "  Budget.hdf             / HDFFILE\n"
        content += "  Budget.bud             / OUTFILE\n"
        content += "                       / INTPRNT\n"
        content += "   1                        / NLPRNT\n"
        content += "  -1                        / LPRNT[1]\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_bud import iwfm_read_bud

            budget_list, factors = iwfm_read_bud(temp_file, verbose=False)

            # Should read correctly despite comment lines
            assert factors[0] == 1
            assert len(budget_list) == 1
            assert budget_list[0][0] == "Budget.hdf"

        finally:
            os.unlink(temp_file)
