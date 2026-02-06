# test_finite_element.py
# unit tests for finite element utility functions in the iwfm package
# Copyright (C) 2025 University of California
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


class TestGetElemCentroids:
    """Test the get_elem_centroids function."""
    
    def test_get_elem_centroids_triangular_elements(self):
        """Test centroid calculation for triangular elements."""
        elem_ids = [1, 2]
        elem_nodes = [[1, 2, 3], [2, 3, 4]]
        # node_coords format: [node_id, x, y]
        node_coords = [
            [1, 0.0, 0.0],    # node 1: (0, 0)
            [2, 3.0, 0.0],    # node 2: (3, 0)
            [3, 1.5, 2.6],    # node 3: (1.5, 2.6)
            [4, 4.5, 2.6]     # node 4: (4.5, 2.6)
        ]
        
        result = iwfm.get_elem_centroids(elem_ids, elem_nodes, node_coords)
        
        # Check first element centroid: (0+3+1.5)/3, (0+0+2.6)/3 = (1.5, 0.867)
        assert len(result) == 2
        assert result[0][0] == 1  # element ID
        assert abs(result[0][1] - 1.5) < 1e-10  # x centroid
        assert abs(result[0][2] - (2.6/3)) < 1e-10  # y centroid
        
        # Check second element centroid: (3+1.5+4.5)/3, (0+2.6+2.6)/3 = (3.0, 1.733)
        assert result[1][0] == 2  # element ID
        assert abs(result[1][1] - 3.0) < 1e-10  # x centroid
        assert abs(result[1][2] - (5.2/3)) < 1e-10  # y centroid
    
    def test_get_elem_centroids_quadrilateral_elements(self):
        """Test centroid calculation for quadrilateral elements."""
        elem_ids = [1]
        elem_nodes = [[1, 2, 3, 4]]
        node_coords = [
            [1, 0.0, 0.0],    # node 1: (0, 0)
            [2, 4.0, 0.0],    # node 2: (4, 0)
            [3, 4.0, 4.0],    # node 3: (4, 4)
            [4, 0.0, 4.0]     # node 4: (0, 4)
        ]
        
        result = iwfm.get_elem_centroids(elem_ids, elem_nodes, node_coords)
        
        # Check square centroid: (0+4+4+0)/4, (0+0+4+4)/4 = (2.0, 2.0)
        assert len(result) == 1
        assert result[0][0] == 1  # element ID
        assert abs(result[0][1] - 2.0) < 1e-10  # x centroid
        assert abs(result[0][2] - 2.0) < 1e-10  # y centroid
    
    def test_get_elem_centroids_single_element(self):
        """Test centroid calculation for single element."""
        elem_ids = [100]
        elem_nodes = [[1, 2, 3]]
        node_coords = [
            [1, 1.0, 1.0],
            [2, 5.0, 1.0],
            [3, 3.0, 4.0]
        ]
        
        result = iwfm.get_elem_centroids(elem_ids, elem_nodes, node_coords)
        
        # Check centroid: (1+5+3)/3, (1+1+4)/3 = (3.0, 2.0)
        assert len(result) == 1
        assert result[0][0] == 100
        assert abs(result[0][1] - 3.0) < 1e-10
        assert abs(result[0][2] - 2.0) < 1e-10


class TestElemPolyCoords:
    """Test the elem_poly_coords function."""
    
    def test_elem_poly_coords_triangular(self):
        """Test polygon coordinate extraction for triangular elements."""
        elem_nodes = [[1, 2, 3]]
        node_coord_dict = {
            1: [0.0, 0.0],
            2: [3.0, 0.0],
            3: [1.5, 2.6]
        }
        
        result = iwfm.elem_poly_coords(elem_nodes, node_coord_dict)
        
        # Should have one polygon with 4 points (closed)
        assert len(result) == 1
        polygon = result[0]
        assert len(polygon) == 4  # 3 nodes + closing point
        
        # Check coordinates
        assert polygon[0] == (0.0, 0.0)  # node 1
        assert polygon[1] == (3.0, 0.0)  # node 2
        assert polygon[2] == (1.5, 2.6)  # node 3
        assert polygon[3] == (0.0, 0.0)  # closing point (same as node 1)
    
    def test_elem_poly_coords_quadrilateral(self):
        """Test polygon coordinate extraction for quadrilateral elements."""
        elem_nodes = [[1, 2, 3, 4]]
        node_coord_dict = {
            1: [0.0, 0.0],
            2: [2.0, 0.0],
            3: [2.0, 2.0],
            4: [0.0, 2.0]
        }
        
        result = iwfm.elem_poly_coords(elem_nodes, node_coord_dict)
        
        # Should have one polygon with 5 points (closed)
        assert len(result) == 1
        polygon = result[0]
        assert len(polygon) == 5  # 4 nodes + closing point
        
        # Check coordinates
        assert polygon[0] == (0.0, 0.0)  # node 1
        assert polygon[1] == (2.0, 0.0)  # node 2
        assert polygon[2] == (2.0, 2.0)  # node 3
        assert polygon[3] == (0.0, 2.0)  # node 4
        assert polygon[4] == (0.0, 0.0)  # closing point
    
    def test_elem_poly_coords_multiple_elements(self):
        """Test polygon coordinate extraction for multiple elements."""
        elem_nodes = [[1, 2, 3], [2, 3, 4]]
        node_coord_dict = {
            1: [0.0, 0.0],
            2: [1.0, 0.0],
            3: [0.5, 1.0],
            4: [1.5, 1.0]
        }
        
        result = iwfm.elem_poly_coords(elem_nodes, node_coord_dict)
        
        # Should have two polygons
        assert len(result) == 2
        
        # Check first polygon
        polygon1 = result[0]
        assert len(polygon1) == 4
        assert polygon1[0] == (0.0, 0.0)
        assert polygon1[1] == (1.0, 0.0)
        assert polygon1[2] == (0.5, 1.0)
        assert polygon1[3] == (0.0, 0.0)  # closed
        
        # Check second polygon
        polygon2 = result[1]
        assert len(polygon2) == 4
        assert polygon2[0] == (1.0, 0.0)
        assert polygon2[1] == (0.5, 1.0)
        assert polygon2[2] == (1.5, 1.0)
        assert polygon2[3] == (1.0, 0.0)  # closed


class TestNearest:
    """Test the nearest function."""
    
    def test_nearest_basic(self):
        """Test finding nearest node to a point."""
        d_nodes = {
            1: [0.0, 0.0],
            2: [3.0, 4.0],
            3: [1.0, 1.0],
            4: [10.0, 10.0]
        }
        
        # Point closest to node 3
        result = iwfm.nearest(d_nodes, 1.1, 0.9)
        assert result == 3
        
        # Point closest to node 1
        result = iwfm.nearest(d_nodes, 0.1, 0.1)
        assert result == 1
        
        # Point closest to node 2
        result = iwfm.nearest(d_nodes, 3.2, 3.8)
        assert result == 2
    
    def test_nearest_exact_match(self):
        """Test finding nearest node when point is exactly at a node."""
        d_nodes = {
            1: [0.0, 0.0],
            2: [5.0, 5.0],
            3: [2.0, 2.0]
        }
        
        # Point exactly at node 3
        result = iwfm.nearest(d_nodes, 2.0, 2.0)
        assert result == 3
    
    def test_nearest_single_node(self):
        """Test with single node."""
        d_nodes = {
            42: [1.5, 2.5]
        }
        
        result = iwfm.nearest(d_nodes, 10.0, 10.0)
        assert result == 42
    
    def test_nearest_negative_coordinates(self):
        """Test with negative coordinates."""
        d_nodes = {
            1: [-1.0, -1.0],
            2: [1.0, 1.0],
            3: [-2.0, 2.0]
        }
        
        # Point closest to node 1
        result = iwfm.nearest(d_nodes, -0.8, -0.8)
        assert result == 1
        
        # Point closest to node 3
        result = iwfm.nearest(d_nodes, -1.5, 1.8)
        assert result == 3


# Note: in_element function now properly imports Point from shapely.geometry
class TestInElement:
    """Test the in_element function."""
    
    def test_in_element_placeholder(self):
        """Test in_element function for point-in-polygon detection."""
        # Test data: simple triangle element
        e_nodes = [[1, 2, 3]]  # One triangular element with nodes 1, 2, 3
        e_nos = [101]          # Element number 101
        d_nodexy = {
            1: [0.0, 0.0],     # node 1 at origin
            2: [2.0, 0.0],     # node 2 at (2, 0)  
            3: [1.0, 2.0]      # node 3 at (1, 2)
        }
        
        # Test point inside the triangle
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 1.0, 0.5)
        assert result == 101, f"Point (1.0, 0.5) should be in element 101, got {result}"
        
        # Test point outside the triangle
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 5.0, 5.0)
        assert result == 0, f"Point (5.0, 5.0) should not be in any element, got {result}"
        
        # Test point on the edge - shapely.contains() returns False for boundary points
        # This is expected behavior in computational geometry
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 1.0, 0.0)
        assert result == 0, f"Point (1.0, 0.0) on edge returns 0 with contains(), got {result}"
        
        # Test another clearly inside point
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 1.0, 0.8)
        assert result == 101, f"Point (1.0, 0.8) should be in element 101, got {result}"
        
    def test_in_element_multiple_elements(self):
        """Test in_element with multiple elements."""
        # Two triangular elements
        e_nodes = [
            [1, 2, 3],  # First triangle
            [2, 3, 4]   # Second triangle sharing edge with first
        ]
        e_nos = [101, 102]
        d_nodexy = {
            1: [0.0, 0.0],     # node 1
            2: [2.0, 0.0],     # node 2
            3: [1.0, 2.0],     # node 3
            4: [3.0, 2.0]      # node 4
        }
        
        # Point in first element
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 0.5, 0.5)
        assert result == 101, f"Point should be in element 101, got {result}"
        
        # Point in second element (clearly inside, away from edges)
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 2.2, 1.5)
        assert result == 102, f"Point should be in element 102, got {result}"
        
        # Point outside both elements
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, -1.0, -1.0)
        assert result == 0, f"Point should not be in any element, got {result}"
        
    def test_in_element_quadrilateral(self):
        """Test in_element with quadrilateral element."""
        # Square element
        e_nodes = [[1, 2, 3, 4]]
        e_nos = [201]
        d_nodexy = {
            1: [0.0, 0.0],     # bottom-left
            2: [2.0, 0.0],     # bottom-right
            3: [2.0, 2.0],     # top-right
            4: [0.0, 2.0]      # top-left
        }
        
        # Point inside square
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 1.0, 1.0)
        assert result == 201, f"Point (1.0, 1.0) should be in element 201, got {result}"
        
        # Point outside square
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 3.0, 3.0)
        assert result == 0, f"Point (3.0, 3.0) should not be in any element, got {result}"
        
        # Point on corner - shapely.contains() returns False for boundary points
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 0.0, 0.0)
        assert result == 0, f"Point (0.0, 0.0) on corner returns 0 with contains(), got {result}"
        
        # Point clearly inside
        result = iwfm.in_element(e_nodes, e_nos, d_nodexy, 0.5, 0.5)
        assert result == 201, f"Point (0.5, 0.5) should be in element 201, got {result}"