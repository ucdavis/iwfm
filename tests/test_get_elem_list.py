# test_get_elem_list.py
# Unit tests for the get_elem_list function in the iwfm package
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
import os
import tempfile

# Import directly from module since it may not be exported in __init__.py
from iwfm.get_elem_list import get_elem_list


class TestGetElemListFunctionExists:
    """Test that the get_elem_list function exists and is callable."""

    def test_get_elem_list_exists(self):
        """Test that get_elem_list function exists and is callable."""
        assert get_elem_list is not None
        assert callable(get_elem_list)


class TestGetElemListBasicFunctionality:
    """Test basic functionality of get_elem_list."""

    def test_simple_comma_delimited_file(self):
        """Test reading a simple comma-delimited element pairs file."""
        # Format: old_elem, new_elem, subregion
        content = "100,1,1\n200,2,1\n300,3,2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, new_srs, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            # elem_dict maps old -> [new, subregion]
            assert 100 in elem_dict
            assert elem_dict[100] == [1, 1]
            assert elem_dict[200] == [2, 1]
            assert elem_dict[300] == [3, 2]

            # rev_elem_dict maps new -> [old, subregion]
            assert 1 in rev_elem_dict
            assert rev_elem_dict[1] == [100, 1]
            assert rev_elem_dict[2] == [200, 1]
            assert rev_elem_dict[3] == [300, 2]

            # new_srs contains unique subregions
            assert new_srs == [1, 2]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_tab_delimited_file(self):
        """Test reading a tab-delimited file."""
        content = "100\t1\t1\n200\t2\t2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, new_srs, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            assert elem_dict[100] == [1, 1]
            assert elem_dict[200] == [2, 2]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_space_delimited_file(self):
        """Test reading a space-delimited file."""
        content = "100 1 1\n200 2 2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, new_srs, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            assert elem_dict[100] == [1, 1]
            assert elem_dict[200] == [2, 2]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_semicolon_delimited_file(self):
        """Test reading a semicolon-delimited file."""
        content = "100;1;1\n200;2;2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, new_srs, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            assert elem_dict[100] == [1, 1]
            assert elem_dict[200] == [2, 2]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_asterisk_delimited_file(self):
        """Test reading an asterisk-delimited file."""
        content = "100*1*1\n200*2*2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, new_srs, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            assert elem_dict[100] == [1, 1]
            assert elem_dict[200] == [2, 2]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestGetElemListReturnTypes:
    """Test the return types of get_elem_list."""

    def test_returns_tuple_of_four(self):
        """Test that get_elem_list returns four values."""
        content = "100,1,1\n200,2,2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            result = get_elem_list(temp_file)

            assert len(result) == 4
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_elem_list_is_list(self):
        """Test that elem_list is a list."""
        content = "100,1,1\n200,2,2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, _, _, _ = get_elem_list(temp_file)

            assert isinstance(elem_list, list)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_new_srs_is_list(self):
        """Test that new_srs is a list."""
        content = "100,1,1\n200,2,2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, new_srs, _, _ = get_elem_list(temp_file)

            assert isinstance(new_srs, list)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_elem_dict_is_dict(self):
        """Test that elem_dict is a dictionary."""
        content = "100,1,1\n200,2,2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, _, elem_dict, _ = get_elem_list(temp_file)

            assert isinstance(elem_dict, dict)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_rev_elem_dict_is_dict(self):
        """Test that rev_elem_dict is a dictionary."""
        content = "100,1,1\n200,2,2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, _, _, rev_elem_dict = get_elem_list(temp_file)

            assert isinstance(rev_elem_dict, dict)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestGetElemListElemDict:
    """Test the elem_dict (old -> new) dictionary."""

    def test_elem_dict_keys_are_old_elements(self):
        """Test that elem_dict keys are the old element numbers."""
        content = "100,1,1\n200,2,2\n300,3,3\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, _, elem_dict, _ = get_elem_list(temp_file)

            assert set(elem_dict.keys()) == {100, 200, 300}
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_elem_dict_values_contain_new_elem_and_subregion(self):
        """Test that elem_dict values are [new_elem, subregion]."""
        content = "100,1,5\n200,2,6\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, _, elem_dict, _ = get_elem_list(temp_file)

            # Values should be [new_elem, subregion]
            assert elem_dict[100] == [1, 5]
            assert elem_dict[200] == [2, 6]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestGetElemListRevElemDict:
    """Test the rev_elem_dict (new -> old) dictionary."""

    def test_rev_elem_dict_keys_are_new_elements(self):
        """Test that rev_elem_dict keys are the new element numbers."""
        content = "100,1,1\n200,2,2\n300,3,3\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, _, _, rev_elem_dict = get_elem_list(temp_file)

            assert set(rev_elem_dict.keys()) == {1, 2, 3}
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_rev_elem_dict_values_contain_old_elem_and_subregion(self):
        """Test that rev_elem_dict values are [old_elem, subregion]."""
        content = "100,1,5\n200,2,6\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, _, _, rev_elem_dict = get_elem_list(temp_file)

            # Values should be [old_elem, subregion]
            assert rev_elem_dict[1] == [100, 5]
            assert rev_elem_dict[2] == [200, 6]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_dictionaries_are_inverses(self):
        """Test that elem_dict and rev_elem_dict are proper inverses."""
        content = "100,1,1\n200,2,2\n300,3,3\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, _, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            # For each old->new mapping, verify new->old mapping exists
            for old_elem, values in elem_dict.items():
                new_elem = values[0]
                subregion = values[1]
                assert new_elem in rev_elem_dict
                assert rev_elem_dict[new_elem][0] == old_elem
                assert rev_elem_dict[new_elem][1] == subregion
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestGetElemListNewSrs:
    """Test the new_srs (subregions) list."""

    def test_new_srs_contains_unique_subregions(self):
        """Test that new_srs contains unique subregion values."""
        content = "100,1,1\n200,2,1\n300,3,2\n400,4,2\n500,5,3\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, new_srs, _, _ = get_elem_list(temp_file)

            assert new_srs == [1, 2, 3]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_new_srs_is_sorted(self):
        """Test that new_srs is sorted in ascending order."""
        content = "100,1,3\n200,2,1\n300,3,2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, new_srs, _, _ = get_elem_list(temp_file)

            assert new_srs == sorted(new_srs)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_new_srs_excludes_zero(self):
        """Test that subregion 0 is excluded from new_srs."""
        content = "100,1,0\n200,2,1\n300,3,2\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, new_srs, _, _ = get_elem_list(temp_file)

            assert 0 not in new_srs
            assert new_srs == [1, 2]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_all_zeros_subregion(self):
        """Test file where all elements have subregion 0."""
        content = "100,1,0\n200,2,0\n300,3,0\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, new_srs, _, _ = get_elem_list(temp_file)

            # After removing 0, list should be empty
            assert new_srs == []
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestGetElemListElemList:
    """Test the elem_list return value."""

    def test_elem_list_has_swapped_columns(self):
        """Test that elem_list has columns 0 and 1 swapped."""
        content = "100,1,5\n200,2,6\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, _, _, _ = get_elem_list(temp_file)

            # After swapping: [new_elem, old_elem, subregion]
            assert elem_list[0] == [1, 100, 5]
            assert elem_list[1] == [2, 200, 6]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_elem_list_length_matches_file_lines(self):
        """Test that elem_list has same number of rows as file lines."""
        content = "100,1,1\n200,2,2\n300,3,3\n400,4,4\n500,5,5\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, _, _, _ = get_elem_list(temp_file)

            assert len(elem_list) == 5
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestGetElemListEdgeCases:
    """Test edge cases for get_elem_list."""

    def test_single_element(self):
        """Test file with only one element."""
        content = "100,1,1\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, new_srs, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            assert len(elem_list) == 1
            assert len(elem_dict) == 1
            assert len(rev_elem_dict) == 1
            assert new_srs == [1]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_large_element_numbers(self):
        """Test with large element numbers."""
        content = "10000,1,1\n20000,2,2\n30000,3,3\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, _, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            assert 10000 in elem_dict
            assert 20000 in elem_dict
            assert 30000 in elem_dict
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_non_consecutive_new_elements(self):
        """Test with non-consecutive new element numbers."""
        content = "100,10,1\n200,20,2\n300,30,3\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, _, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            assert elem_dict[100] == [10, 1]
            assert rev_elem_dict[10] == [100, 1]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_many_subregions(self):
        """Test with many different subregions."""
        content = ""
        for i in range(10):
            content += f"{100+i},{i+1},{i+1}\n"

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, new_srs, _, _ = get_elem_list(temp_file)

            assert len(new_srs) == 10
            assert new_srs == list(range(1, 11))
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestGetElemListRealWorldScenarios:
    """Test get_elem_list with realistic IWFM scenarios."""

    def test_submodel_element_mapping(self):
        """Test typical submodel element mapping file."""
        # Parent model elements 1000-1009 map to submodel elements 1-10
        # with subregions 1-3
        content = """1000,1,1
1001,2,1
1002,3,1
1003,4,2
1004,5,2
1005,6,2
1006,7,3
1007,8,3
1008,9,3
1009,10,3
"""
        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, new_srs, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            # Check counts
            assert len(elem_list) == 10
            assert len(elem_dict) == 10
            assert len(rev_elem_dict) == 10
            assert new_srs == [1, 2, 3]

            # Check specific mappings
            assert elem_dict[1000] == [1, 1]
            assert elem_dict[1005] == [6, 2]
            assert rev_elem_dict[10] == [1009, 3]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_c2vsimcg_style_elements(self):
        """Test with C2VSimCG-style element numbering."""
        # C2VSimCG has elements numbered 1-32537
        # A submodel might extract a smaller region
        content = """1234,1,5
1235,2,5
1236,3,5
2345,4,6
2346,5,6
3456,6,7
"""
        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            elem_list, new_srs, elem_dict, rev_elem_dict = get_elem_list(temp_file)

            # Verify subregions
            assert new_srs == [5, 6, 7]

            # Verify we can look up both directions
            assert elem_dict[1234][0] == 1  # old -> new
            assert rev_elem_dict[1][0] == 1234  # new -> old
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_boundary_elements_with_subregion_zero(self):
        """Test elements on boundary (subregion 0) are handled correctly."""
        # Boundary elements might have subregion 0
        content = """100,1,0
101,2,1
102,3,1
103,4,0
104,5,2
"""
        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            _, new_srs, elem_dict, _ = get_elem_list(temp_file)

            # Subregion 0 should be excluded from new_srs
            assert 0 not in new_srs
            assert new_srs == [1, 2]

            # But elements with subregion 0 should still be in dictionaries
            assert 100 in elem_dict
            assert 103 in elem_dict
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestGetElemListErrorHandling:
    """Test error handling in get_elem_list."""

    def test_nonexistent_file(self):
        """Test that nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            get_elem_list('nonexistent_file.txt')

    def test_empty_file_raises_error(self):
        """Test that empty file raises IndexError.

        Note: The current implementation doesn't handle empty files gracefully.
        It raises IndexError when trying to access new_srs[0].
        """
        content = ""

        fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            with pytest.raises(IndexError):
                get_elem_list(temp_file)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
