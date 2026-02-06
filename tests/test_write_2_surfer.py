# test_write_2_surfer.py
# Unit tests for write_2_surfer.py - Write node data to Surfer file
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


class TestWrite2Surfer:
    """Tests for write_2_surfer function"""

    def test_basic_functionality(self, tmp_path):
        """Test basic functionality with simple data."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        # x_y_locs: [NodeID, X, Y]
        x_y_locs = [
            [1, 100.0, 200.0],
            [2, 150.0, 250.0],
            [3, 200.0, 300.0],
        ]
        # data: layers x nodes (will be transposed)
        data = [
            [10.0, 20.0, 30.0],  # Layer 1 values for nodes 1, 2, 3
            [11.0, 21.0, 31.0],  # Layer 2 values for nodes 1, 2, 3
        ]
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        assert os.path.exists(outfile)

    def test_header_format(self, tmp_path):
        """Test that header contains correct column names."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        x_y_locs = [[1, 100.0, 200.0]]
        data = [[10.0], [20.0], [30.0]]  # 3 layers
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        with open(outfile, 'r') as f:
            header = f.readline().strip()

        assert "'NodeID'" in header
        assert "'X'" in header
        assert "'Y'" in header
        assert "'Layer 1'" in header
        assert "'Layer 2'" in header
        assert "'Layer 3'" in header

    def test_data_rows(self, tmp_path):
        """Test that data rows contain NodeID, X, Y and layer values."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        x_y_locs = [
            [1, 100.5, 200.5],
            [2, 150.5, 250.5],
        ]
        # 2 layers, 2 nodes
        data = [
            [10.0, 20.0],  # Layer 1
            [11.0, 21.0],  # Layer 2
        ]
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        # Check first data row (node 1)
        assert '1,100.5,200.5' in lines[1]
        assert '10.0' in lines[1]
        assert '11.0' in lines[1]

        # Check second data row (node 2)
        assert '2,150.5,250.5' in lines[2]
        assert '20.0' in lines[2]
        assert '21.0' in lines[2]

    def test_single_layer(self, tmp_path):
        """Test with single layer data."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        x_y_locs = [[1, 100.0, 200.0], [2, 150.0, 250.0]]
        data = [[10.0, 20.0]]  # 1 layer
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        with open(outfile, 'r') as f:
            header = f.readline().strip()

        assert "'Layer 1'" in header
        assert "'Layer 2'" not in header

    def test_many_layers(self, tmp_path):
        """Test with many layers."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        x_y_locs = [[1, 100.0, 200.0]]
        num_layers = 10
        data = [[float(i)] for i in range(num_layers)]
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        with open(outfile, 'r') as f:
            header = f.readline().strip()

        for i in range(1, num_layers + 1):
            assert f"'Layer {i}'" in header

    def test_many_nodes(self, tmp_path):
        """Test with many nodes."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        num_nodes = 100
        x_y_locs = [[i, float(i * 10), float(i * 20)] for i in range(1, num_nodes + 1)]
        data = [[float(i) for i in range(num_nodes)]]  # 1 layer
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        # Header + 100 data rows
        assert len(lines) == 101

    def test_large_coordinates(self, tmp_path):
        """Test with large coordinate values (typical UTM coordinates)."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        x_y_locs = [
            [1, 622426.423, 4296803.182],
            [2, 642045.125, 4291704.836],
        ]
        data = [[100.5, 200.5]]
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        assert '622426.423' in lines[1]
        assert '4296803.182' in lines[1]

    def test_negative_values(self, tmp_path):
        """Test with negative data values."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        x_y_locs = [[1, 100.0, 200.0]]
        data = [[-50.5], [-100.25]]  # Negative values (e.g., depth to water)
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        with open(outfile, 'r') as f:
            content = f.read()

        assert '-50.5' in content
        assert '-100.25' in content

    def test_transpose_behavior(self, tmp_path):
        """Test that data is correctly transposed (layers become columns)."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        # 3 nodes, 2 layers
        x_y_locs = [
            [1, 100.0, 200.0],
            [2, 150.0, 250.0],
            [3, 200.0, 300.0],
        ]
        # Input: layers x nodes
        data = [
            [1.1, 2.1, 3.1],  # Layer 1: node1, node2, node3
            [1.2, 2.2, 3.2],  # Layer 2: node1, node2, node3
        ]
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        with open(outfile, 'r') as f:
            lines = f.readlines()

        # After transpose, each row should be: NodeID, X, Y, Layer1_val, Layer2_val
        # Node 1: 1, 100.0, 200.0, 1.1, 1.2
        assert '1.1' in lines[1] and '1.2' in lines[1]
        # Node 2: 2, 150.0, 250.0, 2.1, 2.2
        assert '2.1' in lines[2] and '2.2' in lines[2]
        # Node 3: 3, 200.0, 300.0, 3.1, 3.2
        assert '3.1' in lines[3] and '3.2' in lines[3]

    def test_file_is_comma_separated(self, tmp_path):
        """Test that output file uses comma separation."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        x_y_locs = [[1, 100.0, 200.0]]
        data = [[10.0]]
        date = '01/01/2020'

        write_2_surfer(outfile, x_y_locs, data, date)

        with open(outfile, 'r') as f:
            content = f.read()

        # Count commas in data row
        data_line = content.split('\n')[1]
        assert data_line.count(',') >= 3  # NodeID, X, Y, Layer1

    def test_return_value(self, tmp_path):
        """Test that function returns None."""
        from iwfm.write_2_surfer import write_2_surfer

        outfile = str(tmp_path / 'test_output.csv')
        
        x_y_locs = [[1, 100.0, 200.0]]
        data = [[10.0]]
        date = '01/01/2020'

        result = write_2_surfer(outfile, x_y_locs, data, date)

        assert result is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
