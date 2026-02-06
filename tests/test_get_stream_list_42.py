#!/usr/bin/env python
# test_get_stream_list_42.py
# Unit tests for get_stream_list_42.py
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


def create_stream_spec_file_42(nreach, nrate, reaches_data, rating_factors=None, stream_aq_lines=None):
    """Create properly structured IWFM stream specification file (v4.2) for testing.

    Parameters
    ----------
    nreach : int
        Number of stream reaches
    nrate : int
        Number of points in rating table for each stream node
    reaches_data : list of tuples
        Each tuple: (reach_id, nnodes, outflow_dest, name, nodes_data)
        nodes_data: list of tuples (snode_id, gwnode_id)
    rating_factors : list of str, optional
        Rating table factor lines (FACTCN, TCUNITCN, FACTQ)
    stream_aq_lines : list of str, optional
        Stream-aquifer interaction section lines

    Returns
    -------
    list
        File lines (already split)
    """
    lines = []

    # Header with version
    lines.append("#4.2")
    lines.append("C *** DO NOT DELETE ABOVE LINE ***")
    lines.append("C Stream Specification File v4.2")

    # NREACH and NRATE section
    lines.append("C Number of reaches and rating table points")
    lines.append(f"    {nreach}    / NRH")
    lines.append(f"    {nrate}    / NRTB")

    # Reach section
    lines.append("C Stream reach definitions")
    for reach_id, nnodes, outflow, name, nodes_data in reaches_data:
        lines.append(f"    {reach_id}    {nnodes}    {outflow}    {name}")
        for snode_id, gwnode_id in nodes_data:
            lines.append(f"    {snode_id}    {gwnode_id}")

    # Rating table factors section
    lines.append("C Rating table factors")
    if rating_factors:
        lines.extend(rating_factors)
    else:
        lines.append("    1.0                   / FACTCN")
        lines.append("    1.0                   / TCUNITCN")
        lines.append("    1.0                   / FACTQ")

    lines.append("C Rating tables for each stream node")

    # Rating tables - one table per stream node
    # Count total stream nodes
    total_snodes = sum(len(nodes_data) for _, _, _, _, nodes_data in reaches_data)
    snode_list = []
    for _, _, _, _, nodes_data in reaches_data:
        for snode_id, _ in nodes_data:
            snode_list.append(snode_id)

    # Create rating table for each stream node
    for snode_id in snode_list:
        for i in range(nrate):
            # Rating table format: stage, flow
            stage = 0.0 + i * 1.0
            flow = 0.0 + i * 100.0
            lines.append(f"    {stage:.2f}    {flow:.2f}")

    # Stream-aquifer interaction section
    if stream_aq_lines:
        lines.extend(stream_aq_lines)
    else:
        lines.append("C Stream-aquifer interaction section")
        lines.append("    1.0    / FACTKH")

    return lines


class TestGetStreamList42FileReading:
    """Tests for file reading logic in get_stream_list_42 function"""

    def test_single_reach_single_node(self):
        """Test reading single reach with single node"""
        reaches = [
            (1, 1, 100, "Reach 1", [(10, 500)])
        ]
        nreach = 1
        nrate = 2
        stream_lines = create_stream_spec_file_42(nreach, nrate, reaches)

        from iwfm.get_stream_list_42 import get_stream_list_42

        # Start after NREACH and NRATE lines (line 6 is NRTB)
        line_index = 6

        snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq = get_stream_list_42(
            stream_lines, line_index, nreach, nrate
        )

        # Verify stream node IDs
        assert len(snode_ids) == 1
        assert 10 in snode_ids

        # Verify stream node dictionary
        assert snode_dict[10] == 500

        # Verify reach info
        assert len(reach_info) == 1
        assert reach_info[0][0] == 1  # reach_id
        assert reach_info[0][1] == 1  # nnodes
        assert reach_info[0][2] == 100  # outflow
        assert reach_info[0][4] == [10]  # snodes
        assert reach_info[0][5] == [500]  # gwnodes

    def test_single_reach_multiple_nodes(self):
        """Test reading single reach with multiple nodes"""
        reaches = [
            (1, 3, 100, "Reach 1", [(10, 500), (11, 501), (12, 502)])
        ]
        nreach = 1
        nrate = 2
        stream_lines = create_stream_spec_file_42(nreach, nrate, reaches)

        from iwfm.get_stream_list_42 import get_stream_list_42

        line_index = 6

        snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq = get_stream_list_42(
            stream_lines, line_index, nreach, nrate
        )

        # Verify stream node IDs
        assert len(snode_ids) == 3
        assert 10 in snode_ids
        assert 11 in snode_ids
        assert 12 in snode_ids

        # Verify stream node dictionary
        assert snode_dict[10] == 500
        assert snode_dict[11] == 501
        assert snode_dict[12] == 502

        # Verify reach info
        assert reach_info[0][4] == [10, 11, 12]
        assert reach_info[0][5] == [500, 501, 502]

    def test_multiple_reaches(self):
        """Test reading multiple reaches"""
        reaches = [
            (1, 2, 100, "Reach 1", [(10, 500), (11, 501)]),
            (2, 2, 200, "Reach 2", [(20, 600), (21, 601)])
        ]
        nreach = 2
        nrate = 2
        stream_lines = create_stream_spec_file_42(nreach, nrate, reaches)

        from iwfm.get_stream_list_42 import get_stream_list_42

        line_index = 6

        snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq = get_stream_list_42(
            stream_lines, line_index, nreach, nrate
        )

        # Verify total stream nodes
        assert len(snode_ids) == 4

        # Verify all nodes in dictionary
        assert snode_dict[10] == 500
        assert snode_dict[11] == 501
        assert snode_dict[20] == 600
        assert snode_dict[21] == 601

        # Verify reach count
        assert len(reach_info) == 2

    def test_rating_table_factors(self):
        """Test reading rating table factors"""
        reaches = [
            (1, 1, 100, "Reach 1", [(10, 500)])
        ]
        rating_factors = [
            "    2.5    / FACTCN",
            "    0.5    / TCUNITCN",
            "    1.5    / FACTQ"
        ]
        nreach = 1
        nrate = 2
        stream_lines = create_stream_spec_file_42(nreach, nrate, reaches, rating_factors=rating_factors)

        from iwfm.get_stream_list_42 import get_stream_list_42

        line_index = 6

        snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq = get_stream_list_42(
            stream_lines, line_index, nreach, nrate
        )

        # Verify rating header contains factors
        assert len(rating_header) > 0
        # Should contain the comment line plus 3 factor lines
        assert any("FACTCN" in line for line in rating_header)

    def test_rating_tables(self):
        """Test reading rating tables for stream nodes"""
        reaches = [
            (1, 2, 100, "Reach 1", [(10, 500), (11, 501)])
        ]
        nreach = 1
        nrate = 3
        stream_lines = create_stream_spec_file_42(nreach, nrate, reaches)

        from iwfm.get_stream_list_42 import get_stream_list_42

        line_index = 6

        snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq = get_stream_list_42(
            stream_lines, line_index, nreach, nrate
        )

        # Verify rating table dictionary has entries for all nodes
        assert len(rattab_dict) == 2
        assert 10 in rattab_dict
        assert 11 in rattab_dict

        # Verify each rating table has correct number of points
        assert len(rattab_dict[10]) == 3
        assert len(rattab_dict[11]) == 3

    def test_stream_aquifer_section(self):
        """Test reading stream-aquifer interaction section"""
        reaches = [
            (1, 1, 100, "Reach 1", [(10, 500)])
        ]
        stream_aq_lines = [
            "C Stream-aquifer interaction",
            "    2.0    / FACTKH",
            "    1DAY   / TUNITKH"
        ]
        nreach = 1
        nrate = 2
        stream_lines = create_stream_spec_file_42(nreach, nrate, reaches, stream_aq_lines=stream_aq_lines)

        from iwfm.get_stream_list_42 import get_stream_list_42

        line_index = 6

        snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq = get_stream_list_42(
            stream_lines, line_index, nreach, nrate
        )

        # Verify stream-aquifer section captured
        assert len(stream_aq) > 0
        assert any("FACTKH" in line for line in stream_aq)

    def test_reach_info_format(self):
        """Test reach info structure"""
        reaches = [
            (5, 2, 999, "Test Reach Name", [(100, 1000), (101, 1001)])
        ]
        nreach = 1
        nrate = 2
        stream_lines = create_stream_spec_file_42(nreach, nrate, reaches)

        from iwfm.get_stream_list_42 import get_stream_list_42

        line_index = 6

        snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq = get_stream_list_42(
            stream_lines, line_index, nreach, nrate
        )

        # Verify reach info structure: [reach_id, nnodes, outflow, name, snodes, gwnodes]
        assert len(reach_info) == 1
        assert len(reach_info[0]) == 6
        assert reach_info[0][0] == 5  # reach_id
        assert reach_info[0][1] == 2  # nnodes
        assert reach_info[0][2] == 999  # outflow
        assert "Test Reach Name" in reach_info[0][3]  # name
        assert isinstance(reach_info[0][4], list)  # snodes list
        assert isinstance(reach_info[0][5], list)  # gwnodes list


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
