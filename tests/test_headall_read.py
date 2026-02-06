# test_headall_read.py
# Unit tests for the headall_read function in the iwfm package
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
from iwfm.headall_read import headall_read

# Path to the example C2VSimCG headall file
EXAMPLE_HEADALL_FILE = os.path.join(
    os.path.dirname(__file__),
    'C2VSimCG-2021',
    'Results',
    'C2VSimCG_GW_HeadAll.out'
)

# Check if the example file exists for tests that require it
EXAMPLE_FILE_EXISTS = os.path.exists(EXAMPLE_HEADALL_FILE)


class TestHeadallReadFunctionExists:
    """Test that the headall_read function exists and is callable."""

    def test_headall_read_exists(self):
        """Test that headall_read function exists and is callable."""
        assert headall_read is not None
        assert callable(headall_read)


@pytest.mark.skipif(not EXAMPLE_FILE_EXISTS, reason="C2VSimCG example file not found")
class TestHeadallReadReturnTypes:
    """Test the return types of headall_read."""

    def test_returns_tuple_of_four(self):
        """Test that headall_read returns four values."""
        result = headall_read(EXAMPLE_HEADALL_FILE)
        assert len(result) == 4

    def test_data_is_list(self):
        """Test that data is a list."""
        data, _, _, _ = headall_read(EXAMPLE_HEADALL_FILE)
        assert isinstance(data, list)

    def test_layers_is_integer(self):
        """Test that layers is an integer."""
        _, layers, _, _ = headall_read(EXAMPLE_HEADALL_FILE)
        assert isinstance(layers, int)

    def test_dates_is_list(self):
        """Test that dates is a list."""
        _, _, dates, _ = headall_read(EXAMPLE_HEADALL_FILE)
        assert isinstance(dates, list)

    def test_nodes_is_list(self):
        """Test that nodes is a list."""
        _, _, _, nodes = headall_read(EXAMPLE_HEADALL_FILE)
        assert isinstance(nodes, list)


@pytest.mark.skipif(not EXAMPLE_FILE_EXISTS, reason="C2VSimCG example file not found")
class TestHeadallReadLayerCount:
    """Test the layers count returned by headall_read."""

    def test_layers_positive(self):
        """Test that layers count is positive."""
        _, layers, _, _ = headall_read(EXAMPLE_HEADALL_FILE)
        assert layers > 0

    def test_layers_reasonable(self):
        """Test that layers count is reasonable for IWFM models.

        Most IWFM models have 1-10 layers.
        """
        _, layers, _, _ = headall_read(EXAMPLE_HEADALL_FILE)
        assert 1 <= layers <= 20


@pytest.mark.skipif(not EXAMPLE_FILE_EXISTS, reason="C2VSimCG example file not found")
class TestHeadallReadDates:
    """Test the dates list returned by headall_read."""

    def test_dates_not_empty(self):
        """Test that dates list is not empty."""
        _, _, dates, _ = headall_read(EXAMPLE_HEADALL_FILE)
        assert len(dates) > 0

    def test_dates_are_strings(self):
        """Test that dates are strings."""
        _, _, dates, _ = headall_read(EXAMPLE_HEADALL_FILE)
        for date in dates:
            assert isinstance(date, str)

    def test_dates_format(self):
        """Test that dates are in expected format (MM/DD/YYYY)."""
        _, _, dates, _ = headall_read(EXAMPLE_HEADALL_FILE)

        # Check first date format
        first_date = dates[0]
        parts = first_date.split('/')
        assert len(parts) == 3

        # Month, day, year
        month, day, year = parts
        assert len(month) == 2
        assert len(day) == 2
        assert len(year) == 4

    def test_first_date_value(self):
        """Test the first date value for C2VSimCG."""
        _, _, dates, _ = headall_read(EXAMPLE_HEADALL_FILE)

        # C2VSimCG typically starts at water year 1974 (10/1/1973 or 09/30/1973)
        first_date = dates[0]
        assert '1973' in first_date or '1974' in first_date


@pytest.mark.skipif(not EXAMPLE_FILE_EXISTS, reason="C2VSimCG example file not found")
class TestHeadallReadNodes:
    """Test the nodes list returned by headall_read."""

    def test_nodes_not_empty(self):
        """Test that nodes list is not empty."""
        _, _, _, nodes = headall_read(EXAMPLE_HEADALL_FILE)
        assert len(nodes) > 0

    def test_nodes_are_strings(self):
        """Test that nodes are strings (as read from file)."""
        _, _, _, nodes = headall_read(EXAMPLE_HEADALL_FILE)
        for node in nodes:
            assert isinstance(node, str)

    def test_nodes_convertible_to_int(self):
        """Test that node strings can be converted to integers."""
        _, _, _, nodes = headall_read(EXAMPLE_HEADALL_FILE)
        for node in nodes:
            assert int(node)  # Should not raise exception

    def test_first_node_is_one(self):
        """Test that first node is 1."""
        _, _, _, nodes = headall_read(EXAMPLE_HEADALL_FILE)
        assert int(nodes[0]) == 1


@pytest.mark.skipif(not EXAMPLE_FILE_EXISTS, reason="C2VSimCG example file not found")
class TestHeadallReadData:
    """Test the data list returned by headall_read."""

    def test_data_not_empty(self):
        """Test that data list is not empty."""
        data, _, _, _ = headall_read(EXAMPLE_HEADALL_FILE)
        assert len(data) > 0

    def test_data_length_matches_dates(self):
        """Test that data has same length as dates (one entry per timestep)."""
        data, _, dates, _ = headall_read(EXAMPLE_HEADALL_FILE)
        assert len(data) == len(dates)

    def test_data_is_nested_list(self):
        """Test that data is a nested list (timesteps x layers x nodes)."""
        data, layers, _, nodes = headall_read(EXAMPLE_HEADALL_FILE)

        # Each timestep should have 'layers' sublists
        first_timestep = data[0]
        assert isinstance(first_timestep, list)
        assert len(first_timestep) == layers

    def test_data_layer_length_matches_nodes(self):
        """Test that each layer has same number of values as nodes."""
        data, _, _, nodes = headall_read(EXAMPLE_HEADALL_FILE)

        # Check first timestep, first layer
        first_layer_data = data[0][0]
        assert len(first_layer_data) == len(nodes)

    def test_data_values_are_floats(self):
        """Test that data values are floats."""
        data, _, _, _ = headall_read(EXAMPLE_HEADALL_FILE)

        # Check first timestep, first layer, first few values
        for value in data[0][0][:10]:
            assert isinstance(value, float)


@pytest.mark.skipif(not EXAMPLE_FILE_EXISTS, reason="C2VSimCG example file not found")
class TestHeadallReadDataValues:
    """Test the actual data values returned by headall_read."""

    def test_head_values_reasonable(self):
        """Test that head values are in reasonable range.

        Groundwater heads in California typically range from below sea level
        to a few thousand feet.
        """
        data, _, _, _ = headall_read(EXAMPLE_HEADALL_FILE)

        # Check first timestep, first layer
        for value in data[0][0]:
            # Heads typically between -500 and 5000 feet
            assert -1000 < value < 10000

    def test_no_obviously_invalid_values(self):
        """Test that there are no obviously invalid head values."""
        data, _, _, _ = headall_read(EXAMPLE_HEADALL_FILE)

        # Check first timestep
        for layer_data in data[0]:
            for value in layer_data:
                # No infinite or NaN values
                assert value != float('inf')
                assert value != float('-inf')
                assert value == value  # NaN check (NaN != NaN)


@pytest.mark.skipif(not EXAMPLE_FILE_EXISTS, reason="C2VSimCG example file not found")
class TestHeadallReadC2VSimCGSpecific:
    """Test headall_read with C2VSimCG-specific expectations."""

    def test_c2vsimcg_has_expected_node_count(self):
        """Test that C2VSimCG has expected number of nodes.

        C2VSimCG (Coarse Grid) has 1,393 nodes.
        """
        _, _, _, nodes = headall_read(EXAMPLE_HEADALL_FILE)

        # C2VSimCG should have 1,393 nodes
        assert len(nodes) == 1393

    def test_c2vsimcg_has_expected_layer_count(self):
        """Test that C2VSimCG has expected number of layers.

        C2VSimCG has 4 layers.
        """
        _, layers, _, _ = headall_read(EXAMPLE_HEADALL_FILE)

        assert layers == 4

    def test_c2vsimcg_timesteps(self):
        """Test that C2VSimCG has reasonable number of timesteps.

        The example file should have multiple timesteps.
        """
        _, _, dates, _ = headall_read(EXAMPLE_HEADALL_FILE)

        # Should have at least a few timesteps
        assert len(dates) >= 1


@pytest.mark.skipif(not EXAMPLE_FILE_EXISTS, reason="C2VSimCG example file not found")
class TestHeadallReadSkipParameter:
    """Test the skip parameter of headall_read."""

    def test_default_skip_works(self):
        """Test that default skip=5 works correctly."""
        data, layers, dates, nodes = headall_read(EXAMPLE_HEADALL_FILE)

        # Should return valid data
        assert len(data) > 0
        assert len(nodes) > 0

    def test_skip_parameter_explicit(self):
        """Test that explicit skip=5 works same as default."""
        result_default = headall_read(EXAMPLE_HEADALL_FILE)
        result_explicit = headall_read(EXAMPLE_HEADALL_FILE, skip=5)

        assert result_default[1] == result_explicit[1]  # layers
        assert result_default[2] == result_explicit[2]  # dates
        assert result_default[3] == result_explicit[3]  # nodes


@pytest.mark.skipif(not EXAMPLE_FILE_EXISTS, reason="C2VSimCG example file not found")
class TestHeadallReadConsistency:
    """Test consistency of headall_read results."""

    def test_multiple_calls_return_same_results(self):
        """Test that multiple calls return the same results."""
        result1 = headall_read(EXAMPLE_HEADALL_FILE)
        result2 = headall_read(EXAMPLE_HEADALL_FILE)

        # Layers should match
        assert result1[1] == result2[1]

        # Dates should match
        assert result1[2] == result2[2]

        # Nodes should match
        assert result1[3] == result2[3]

        # Data should match
        assert len(result1[0]) == len(result2[0])

    def test_data_structure_consistent_across_timesteps(self):
        """Test that data structure is consistent across all timesteps."""
        data, layers, _, nodes = headall_read(EXAMPLE_HEADALL_FILE)

        for timestep_data in data:
            # Each timestep should have correct number of layers
            assert len(timestep_data) == layers

            # Each layer should have correct number of nodes
            for layer_data in timestep_data:
                assert len(layer_data) == len(nodes)


class TestHeadallReadWithSyntheticData:
    """Test headall_read with synthetic test files.

    Note: The headall_read function determines the number of layers by checking
    if the line following the first data line starts with a space. For single-layer
    files, there must be at least two timesteps so the function can determine
    that the second line starts with a date (not a space), indicating single layer.
    """

    def test_single_layer_multiple_timesteps(self):
        """Test reading a simple single-layer file with multiple timesteps.

        Single-layer detection requires at least 2 timesteps.
        """
        content = """*                                        ***************************************
*                                        *    GROUNDWATER HEAD AT ALL NODES    *
*                                        *             (UNIT=FEET)             *
*                                        ***************************************
*
*        TIME                   1           2           3
09/30/1973_24:00         100.0       200.0       300.0
10/31/1973_24:00         101.0       201.0       301.0
"""
        fd, temp_file = tempfile.mkstemp(suffix='.out', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            data, layers, dates, nodes = headall_read(temp_file)

            assert layers == 1
            assert len(dates) == 2
            assert dates[0] == '09/30/1973'
            assert len(nodes) == 3
            assert nodes == ['1', '2', '3']
            assert data[0][0] == [100.0, 200.0, 300.0]
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_two_layers_multiple_timesteps(self):
        """Test reading a two-layer file with multiple timesteps."""
        content = """*                                        ***************************************
*                                        *    GROUNDWATER HEAD AT ALL NODES    *
*                                        *             (UNIT=FEET)             *
*                                        ***************************************
*
*        TIME                   1           2           3
09/30/1973_24:00         100.0       200.0       300.0
                         110.0       210.0       310.0
10/31/1973_24:00         101.0       201.0       301.0
                         111.0       211.0       311.0
"""
        fd, temp_file = tempfile.mkstemp(suffix='.out', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            data, layers, dates, nodes = headall_read(temp_file)

            assert layers == 2
            assert len(dates) == 2
            assert len(nodes) == 3
            assert data[0][0] == [100.0, 200.0, 300.0]  # Timestep 1, Layer 1
            assert data[0][1] == [110.0, 210.0, 310.0]  # Timestep 1, Layer 2
            assert data[1][0] == [101.0, 201.0, 301.0]  # Timestep 2, Layer 1
            assert data[1][1] == [111.0, 211.0, 311.0]  # Timestep 2, Layer 2
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_multiple_timesteps(self):
        """Test reading file with multiple timesteps."""
        content = """*                                        ***************************************
*                                        *    GROUNDWATER HEAD AT ALL NODES    *
*                                        *             (UNIT=FEET)             *
*                                        ***************************************
*
*        TIME                   1           2           3
09/30/1973_24:00         100.0       200.0       300.0
10/31/1973_24:00         101.0       201.0       301.0
11/30/1973_24:00         102.0       202.0       302.0
"""
        fd, temp_file = tempfile.mkstemp(suffix='.out', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            data, layers, dates, nodes = headall_read(temp_file)

            assert layers == 1
            assert len(dates) == 3
            assert dates[0] == '09/30/1973'
            assert dates[1] == '10/31/1973'
            assert dates[2] == '11/30/1973'
            assert len(data) == 3
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_negative_head_values(self):
        """Test reading file with negative head values (below sea level)."""
        content = """*                                        ***************************************
*                                        *    GROUNDWATER HEAD AT ALL NODES    *
*                                        *             (UNIT=FEET)             *
*                                        ***************************************
*
*        TIME                   1           2           3
09/30/1973_24:00         -50.0       100.0       -25.5
10/31/1973_24:00         -51.0       101.0       -26.5
"""
        fd, temp_file = tempfile.mkstemp(suffix='.out', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            data, layers, dates, nodes = headall_read(temp_file)

            assert data[0][0][0] == -50.0
            assert data[0][0][1] == 100.0
            assert data[0][0][2] == -25.5
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_four_layers(self):
        """Test reading file with four layers (like C2VSimCG)."""
        content = """*                                        ***************************************
*                                        *    GROUNDWATER HEAD AT ALL NODES    *
*                                        *             (UNIT=FEET)             *
*                                        ***************************************
*
*        TIME                   1           2           3
09/30/1973_24:00         100.0       200.0       300.0
                         110.0       210.0       310.0
                         120.0       220.0       320.0
                         130.0       230.0       330.0
10/31/1973_24:00         101.0       201.0       301.0
                         111.0       211.0       311.0
                         121.0       221.0       321.0
                         131.0       231.0       331.0
"""
        fd, temp_file = tempfile.mkstemp(suffix='.out', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)

            data, layers, dates, nodes = headall_read(temp_file)

            assert layers == 4
            assert len(dates) == 2
            assert len(nodes) == 3

            # Check all layers for first timestep
            assert data[0][0] == [100.0, 200.0, 300.0]  # Layer 1
            assert data[0][1] == [110.0, 210.0, 310.0]  # Layer 2
            assert data[0][2] == [120.0, 220.0, 320.0]  # Layer 3
            assert data[0][3] == [130.0, 230.0, 330.0]  # Layer 4
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestHeadallReadErrorHandling:
    """Test error handling in headall_read."""

    def test_nonexistent_file_raises_error(self):
        """Test that nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            headall_read('nonexistent_headall_file.out')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
