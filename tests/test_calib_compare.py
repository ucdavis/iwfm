# test_calib_compare.py
# Unit tests for calib/compare.py - Compare two lists and find missing/common items
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


class TestCompare:
    """Tests for compare function"""

    def test_basic_functionality(self):
        """Test basic functionality with overlapping lists."""
        from iwfm.calib.compare import compare

        list1 = ['A', 'B', 'C', 'D']
        list2 = ['B', 'C', 'E', 'F']

        missing, in_both = compare(list1, list2)

        # Items in list1 but not in list2
        assert 'A' in missing
        assert 'D' in missing
        # Items in both lists
        assert 'B' in in_both
        assert 'C' in in_both

    def test_return_types(self):
        """Test that function returns two lists."""
        from iwfm.calib.compare import compare

        list1 = ['A', 'B']
        list2 = ['B', 'C']

        result = compare(list1, list2)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)

    def test_all_items_in_both(self):
        """Test when all list1 items are in list2."""
        from iwfm.calib.compare import compare

        list1 = ['A', 'B', 'C']
        list2 = ['A', 'B', 'C', 'D', 'E']

        missing, in_both = compare(list1, list2)

        assert missing == []
        assert sorted(in_both) == ['A', 'B', 'C']

    def test_no_items_in_common(self):
        """Test when no items are in common."""
        from iwfm.calib.compare import compare

        list1 = ['A', 'B', 'C']
        list2 = ['X', 'Y', 'Z']

        missing, in_both = compare(list1, list2)

        assert sorted(missing) == ['A', 'B', 'C']
        assert in_both == []

    def test_identical_lists(self):
        """Test with identical lists."""
        from iwfm.calib.compare import compare

        list1 = ['A', 'B', 'C']
        list2 = ['A', 'B', 'C']

        missing, in_both = compare(list1, list2)

        assert missing == []
        assert sorted(in_both) == ['A', 'B', 'C']

    def test_empty_list1(self):
        """Test with empty list1."""
        from iwfm.calib.compare import compare

        list1 = []
        list2 = ['A', 'B', 'C']

        missing, in_both = compare(list1, list2)

        assert missing == []
        assert in_both == []

    def test_empty_list2(self):
        """Test with empty list2."""
        from iwfm.calib.compare import compare

        list1 = ['A', 'B', 'C']
        list2 = []

        missing, in_both = compare(list1, list2)

        assert sorted(missing) == ['A', 'B', 'C']
        assert in_both == []

    def test_both_empty(self):
        """Test with both lists empty."""
        from iwfm.calib.compare import compare

        list1 = []
        list2 = []

        missing, in_both = compare(list1, list2)

        assert missing == []
        assert in_both == []

    def test_single_item_lists(self):
        """Test with single item lists."""
        from iwfm.calib.compare import compare

        # Same item
        missing, in_both = compare(['A'], ['A'])
        assert missing == []
        assert in_both == ['A']

        # Different items
        missing, in_both = compare(['A'], ['B'])
        assert missing == ['A']
        assert in_both == []

    def test_preserves_order(self):
        """Test that order of list1 items is preserved in results."""
        from iwfm.calib.compare import compare

        list1 = ['D', 'A', 'C', 'B']
        list2 = ['A', 'C']

        missing, in_both = compare(list1, list2)

        # Order should match list1 order
        assert missing == ['D', 'B']
        assert in_both == ['A', 'C']

    def test_well_names_typical_use_case(self):
        """Test with typical well name use case."""
        from iwfm.calib.compare import compare

        # Simulated well names (from model)
        sim_wells = ['WELL_001', 'WELL_002', 'WELL_003', 'WELL_004', 'WELL_005']
        # Observed well names (from measurements)
        obs_wells = ['WELL_002', 'WELL_004', 'WELL_006', 'WELL_007']

        missing, in_both = compare(sim_wells, obs_wells)

        # Wells in sim but not obs
        assert 'WELL_001' in missing
        assert 'WELL_003' in missing
        assert 'WELL_005' in missing
        # Wells in both
        assert 'WELL_002' in in_both
        assert 'WELL_004' in in_both

    def test_state_well_numbers(self):
        """Test with state well number format."""
        from iwfm.calib.compare import compare

        list1 = ['S_380313N1219426W001', 'S_381150N1215899W001', 'S_382000N1216000W001']
        list2 = ['S_380313N1219426W001', 'S_390000N1220000W001']

        missing, in_both = compare(list1, list2)

        assert 'S_381150N1215899W001' in missing
        assert 'S_382000N1216000W001' in missing
        assert 'S_380313N1219426W001' in in_both

    def test_case_sensitive(self):
        """Test that comparison is case-sensitive."""
        from iwfm.calib.compare import compare

        list1 = ['Well_A', 'WELL_A', 'well_a']
        list2 = ['WELL_A']

        missing, in_both = compare(list1, list2)

        assert 'Well_A' in missing
        assert 'well_a' in missing
        assert 'WELL_A' in in_both

    def test_numeric_strings(self):
        """Test with numeric strings."""
        from iwfm.calib.compare import compare

        list1 = ['1', '2', '3', '4', '5']
        list2 = ['2', '4', '6']

        missing, in_both = compare(list1, list2)

        assert missing == ['1', '3', '5']
        assert in_both == ['2', '4']

    def test_duplicates_in_list1(self):
        """Test behavior with duplicates in list1."""
        from iwfm.calib.compare import compare

        list1 = ['A', 'B', 'A', 'C', 'B']
        list2 = ['A', 'D']

        missing, in_both = compare(list1, list2)

        # Duplicates should appear multiple times in results
        assert missing.count('B') == 2
        assert missing.count('C') == 1
        assert in_both.count('A') == 2

    def test_special_characters(self):
        """Test with special characters in names."""
        from iwfm.calib.compare import compare

        list1 = ['Well-001', 'Well_002', 'Well.003', 'Well#004']
        list2 = ['Well-001', 'Well.003']

        missing, in_both = compare(list1, list2)

        assert 'Well_002' in missing
        assert 'Well#004' in missing
        assert 'Well-001' in in_both
        assert 'Well.003' in in_both

    def test_whitespace_in_names(self):
        """Test with whitespace in names."""
        from iwfm.calib.compare import compare

        list1 = ['Well 001', 'Well  002', ' Well003']
        list2 = ['Well 001', 'Well003']

        missing, in_both = compare(list1, list2)

        # Whitespace matters
        assert 'Well  002' in missing
        assert ' Well003' in missing  # Leading space
        assert 'Well 001' in in_both

    def test_large_lists(self):
        """Test with large lists."""
        from iwfm.calib.compare import compare

        list1 = [f'WELL_{i:04d}' for i in range(1000)]
        list2 = [f'WELL_{i:04d}' for i in range(500, 1500)]

        missing, in_both = compare(list1, list2)

        # Wells 0-499 should be missing
        assert len(missing) == 500
        # Wells 500-999 should be in both
        assert len(in_both) == 500

    def test_counts_add_up(self):
        """Test that missing + in_both equals list1 length."""
        from iwfm.calib.compare import compare

        list1 = ['A', 'B', 'C', 'D', 'E', 'F']
        list2 = ['B', 'D', 'F', 'G', 'H']

        missing, in_both = compare(list1, list2)

        assert len(missing) + len(in_both) == len(list1)


class TestCompareImport:
    """Test that compare can be imported from different paths."""

    def test_import_from_calib_module(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import compare
        assert callable(compare)

    def test_import_from_compare_file(self):
        """Test import directly from compare.py."""
        from iwfm.calib.compare import compare
        assert callable(compare)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
