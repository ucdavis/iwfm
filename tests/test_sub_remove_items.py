# test_sub_remove_items.py
# unit tests for sub_remove_items function
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

import iwfm


class TestSubRemoveItemsBasic:
    """Basic tests for sub_remove_items function."""

    def test_remove_single_item(self):
        """Test removing a single item not in the submodel."""
        file_lines = [
            "C Header comment",
            "1    100.0    200.0",
            "2    150.0    250.0",
            "3    200.0    300.0",
            "C End of section",
        ]
        items = [1, 3]  # Keep items 1 and 3, remove item 2

        result = iwfm.sub_remove_items(file_lines, 1, items)

        # Item 2 should be removed
        assert "2    150.0    250.0" not in file_lines
        assert len(file_lines) == 4  # Original 5 - 1 removed

    def test_keep_all_items(self):
        """Test when all items are in the submodel (no removal)."""
        file_lines = [
            "C Header",
            "1    100.0    200.0",
            "2    150.0    250.0",
            "C End",
        ]
        items = [1, 2]  # Keep both items

        original_len = len(file_lines)
        iwfm.sub_remove_items(file_lines, 1, items)

        assert len(file_lines) == original_len

    def test_remove_all_items(self):
        """Test removing all items (none in submodel)."""
        file_lines = [
            "C Header",
            "1    100.0    200.0",
            "2    150.0    250.0",
            "C End",
        ]
        items = [99, 100]  # Keep none of the existing items

        iwfm.sub_remove_items(file_lines, 1, items)

        # Both data lines should be removed
        assert len(file_lines) == 2  # Only comments remain

    def test_returns_int(self):
        """Test that function returns an integer."""
        file_lines = [
            "C Header",
            "1    100.0    200.0",
            "C End",
        ]
        items = [1]

        result = iwfm.sub_remove_items(file_lines, 1, items)

        assert isinstance(result, int)

    def test_modifies_list_in_place(self):
        """Test that function modifies the list in place."""
        file_lines = [
            "C Header",
            "1    100.0    200.0",
            "2    150.0    250.0",
            "C End",
        ]
        items = [1]
        original_id = id(file_lines)

        iwfm.sub_remove_items(file_lines, 1, items)

        assert id(file_lines) == original_id  # Same list object


class TestSubRemoveItemsMultiple:
    """Tests for removing multiple items."""

    def test_remove_multiple_non_consecutive(self):
        """Test removing multiple non-consecutive items."""
        file_lines = [
            "C Header",
            "1    100.0    200.0",
            "2    150.0    250.0",
            "3    200.0    300.0",
            "4    250.0    350.0",
            "5    300.0    400.0",
            "C End",
        ]
        items = [1, 3, 5]  # Keep 1, 3, 5; remove 2, 4

        iwfm.sub_remove_items(file_lines, 1, items)

        # Check items 2 and 4 were removed
        remaining_ids = []
        for line in file_lines:
            if line[0] not in 'Cc*#':
                remaining_ids.append(int(line.split()[0]))
        assert 2 not in remaining_ids
        assert 4 not in remaining_ids
        assert 1 in remaining_ids
        assert 3 in remaining_ids
        assert 5 in remaining_ids

    def test_remove_consecutive_items(self):
        """Test removing consecutive items."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "3    200.0",
            "4    250.0",
            "C End",
        ]
        items = [1, 4]  # Keep only first and last

        iwfm.sub_remove_items(file_lines, 1, items)

        # Check only items 1 and 4 remain
        data_lines = [l for l in file_lines if l[0] not in 'Cc*#']
        assert len(data_lines) == 2

    def test_remove_first_items(self):
        """Test removing items from the beginning."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "3    200.0",
            "C End",
        ]
        items = [3]  # Keep only item 3

        iwfm.sub_remove_items(file_lines, 1, items)

        data_lines = [l for l in file_lines if l[0] not in 'Cc*#']
        assert len(data_lines) == 1
        assert "3" in data_lines[0]

    def test_remove_last_items(self):
        """Test removing items from the end."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "3    200.0",
            "C End",
        ]
        items = [1]  # Keep only item 1

        iwfm.sub_remove_items(file_lines, 1, items)

        data_lines = [l for l in file_lines if l[0] not in 'Cc*#']
        assert len(data_lines) == 1
        assert "1" in data_lines[0]


class TestSubRemoveItemsComments:
    """Tests for comment handling."""

    def test_stops_at_c_comment(self):
        """Test that processing stops at C comment."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "C Section end",
            "3    200.0",  # This should not be processed
        ]
        items = [1]

        iwfm.sub_remove_items(file_lines, 1, items)

        # Item 2 should be removed, but item 3 untouched
        assert "3    200.0" in file_lines

    def test_stops_at_lowercase_c_comment(self):
        """Test that processing stops at lowercase c comment."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "c Section end",
            "3    200.0",
        ]
        items = [1]

        iwfm.sub_remove_items(file_lines, 1, items)

        assert "3    200.0" in file_lines

    def test_stops_at_asterisk_comment(self):
        """Test that processing stops at * comment."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "* Section end",
            "3    200.0",
        ]
        items = [1]

        iwfm.sub_remove_items(file_lines, 1, items)

        assert "3    200.0" in file_lines

    def test_stops_at_hash_comment(self):
        """Test that processing stops at # comment."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "# Section end",
            "3    200.0",
        ]
        items = [1]

        iwfm.sub_remove_items(file_lines, 1, items)

        assert "3    200.0" in file_lines


class TestSubRemoveItemsSkip:
    """Tests for skip parameter."""

    def test_skip_one_line(self):
        """Test skipping one non-comment line before processing."""
        file_lines = [
            "C Header",
            "  5                        / NELEM",  # Skip this line
            "1    100.0",
            "2    150.0",
            "C End",
        ]
        items = [1]

        iwfm.sub_remove_items(file_lines, 1, items, skip=1)

        # The NELEM line should still be there
        assert "5" in file_lines[1]
        # Item 2 should be removed
        assert not any("2    150.0" in line for line in file_lines)

    def test_skip_zero(self):
        """Test with skip=0 (default)."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "C End",
        ]
        items = [1]

        iwfm.sub_remove_items(file_lines, 1, items, skip=0)

        # Item 2 should be removed
        assert not any("2    150.0" in line for line in file_lines)


class TestSubRemoveItemsZeroValue:
    """Tests for zero value handling."""

    def test_zero_first_value_skips_processing(self):
        """Test that zero value in first position skips processing."""
        file_lines = [
            "C Header",
            "0                          / Count is zero",
            "C End",
        ]
        items = [1, 2, 3]

        result = iwfm.sub_remove_items(file_lines, 1, items)

        # Should just increment line_index and return
        assert len(file_lines) == 3  # No changes

    def test_negative_first_value_skips_processing(self):
        """Test that negative value in first position skips processing."""
        file_lines = [
            "C Header",
            "-1                         / Negative count",
            "C End",
        ]
        items = [1, 2, 3]

        result = iwfm.sub_remove_items(file_lines, 1, items)

        # Should just increment line_index
        assert len(file_lines) == 3


class TestSubRemoveItemsIWFMFormat:
    """Tests simulating real IWFM file formats."""

    def test_node_coordinates_section(self):
        """Test with node coordinates format."""
        file_lines = [
            "C Node Coordinates",
            "C ID        X           Y",
            "    1     100.0       200.0",
            "    2     150.0       250.0",
            "    3     200.0       300.0",
            "    4     250.0       350.0",
            "    5     300.0       400.0",
            "C End of nodes",
        ]
        # Submodel only contains nodes 1, 3, 5
        items = [1, 3, 5]

        iwfm.sub_remove_items(file_lines, 2, items)

        # Nodes 2 and 4 should be removed
        data_lines = [l for l in file_lines if l.strip() and l[0] not in 'Cc*#']
        assert len(data_lines) == 3

    def test_element_section(self):
        """Test with element definition format."""
        file_lines = [
            "C Element Definitions",
            "C IE   N1   N2   N3   N4   SUBREGION",
            "  1    1    2    5    4    1",
            "  2    2    3    6    5    1",
            "  3    4    5    8    7    2",
            "C End of elements",
        ]
        # Submodel only contains elements 1, 3
        items = [1, 3]

        iwfm.sub_remove_items(file_lines, 2, items)

        # Element 2 should be removed
        data_lines = [l for l in file_lines if l.strip() and l[0] not in 'Cc*#']
        assert len(data_lines) == 2

    def test_stream_node_section(self):
        """Test with stream node format."""
        file_lines = [
            "C Stream Nodes",
            "C ISRND   STRM_ELEM   LAYER",
            "    1         10        1",
            "    2         11        1",
            "    3         12        1",
            "    4         13        1",
            "C End of stream nodes",
        ]
        # Submodel only contains stream nodes 2, 4
        items = [2, 4]

        iwfm.sub_remove_items(file_lines, 2, items)

        # Stream nodes 1 and 3 should be removed
        data_lines = [l for l in file_lines if l.strip() and l[0] not in 'Cc*#']
        assert len(data_lines) == 2


class TestSubRemoveItemsReturnValue:
    """Tests for return value (line_index)."""

    def test_returns_correct_index_after_removal(self):
        """Test that returned index is correct after removal."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "C End",
            "C Next section",
        ]
        items = [1]

        result = iwfm.sub_remove_items(file_lines, 1, items)

        # Should return index pointing to "C End" line
        assert file_lines[result][0] in 'Cc*#'

    def test_returns_correct_index_no_removal(self):
        """Test that returned index is correct with no removal."""
        file_lines = [
            "C Header",
            "1    100.0",
            "2    150.0",
            "C End",
        ]
        items = [1, 2]

        result = iwfm.sub_remove_items(file_lines, 1, items)

        # Should return index pointing to "C End" line (index 3)
        assert result == 3


class TestSubRemoveItemsEdgeCases:
    """Edge case tests."""

    def test_single_data_line_kept(self):
        """Test with single data line that is kept."""
        file_lines = [
            "C Header",
            "1    100.0",
            "C End",
        ]
        items = [1]

        iwfm.sub_remove_items(file_lines, 1, items)

        assert "1    100.0" in file_lines

    def test_single_data_line_removed(self):
        """Test with single data line that is removed."""
        file_lines = [
            "C Header",
            "1    100.0",
            "C End",
        ]
        items = [99]  # Item 1 not in list

        iwfm.sub_remove_items(file_lines, 1, items)

        assert "1    100.0" not in file_lines

    def test_large_item_ids(self):
        """Test with large item IDs."""
        file_lines = [
            "C Header",
            "1000    100.0",
            "2000    150.0",
            "3000    200.0",
            "C End",
        ]
        items = [1000, 3000]

        iwfm.sub_remove_items(file_lines, 1, items)

        data_lines = [l for l in file_lines if l.strip() and l[0] not in 'Cc*#']
        assert len(data_lines) == 2

    def test_items_with_extra_columns(self):
        """Test items with many columns of data."""
        file_lines = [
            "C Header",
            "1    100.0    200.0    300.0    400.0    500.0",
            "2    150.0    250.0    350.0    450.0    550.0",
            "C End",
        ]
        items = [1]

        iwfm.sub_remove_items(file_lines, 1, items)

        # Item 2 should be removed
        assert not any("2    150.0" in line for line in file_lines)
        # Item 1 should remain with all its columns
        assert any("1    100.0    200.0    300.0    400.0    500.0" in line for line in file_lines)

    def test_whitespace_variations(self):
        """Test with different whitespace in lines."""
        file_lines = [
            "C Header",
            "  1     100.0",  # Leading spaces
            "   2      150.0",  # More leading spaces
            "C End",
        ]
        items = [1]

        iwfm.sub_remove_items(file_lines, 1, items)

        # Item 2 should be removed regardless of whitespace
        data_lines = [l for l in file_lines if l.strip() and l[0] not in 'Cc*#']
        assert len(data_lines) == 1
