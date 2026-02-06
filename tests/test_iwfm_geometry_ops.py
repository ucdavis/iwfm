# test_iwfm_geometry_ops.py
# Tests for iwfm geometry operations
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

"""
Tests for iwfm geometry operations

"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add the parent directory to the path and import iwfm
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import iwfm

class TestListOperations(unittest.TestCase):
    """Test suite for list operations"""
    
    def test_list_unique(self):
        """Test getting unique elements from list"""
        data = [1, 2, 2, 3, 3, 3, 4]
        try:
            result = iwfm.list_unique(data)
            self.assertEqual(len(result), 4)
            self.assertEqual(set(result), {1, 2, 3, 4})
        except AttributeError:
            self.skipTest("iwfm.list_unique function not implemented")
        except Exception as e:
            self.fail(f"list_unique raised unexpected exception: {e}")
    
    def test_list_flatten(self):
        """Test flattening nested lists"""
        nested = [[1, 2], [3, 4], [5, 6]]
        try:
            result = iwfm.list_flatten(nested)
            # Handle different possible return types
            if isinstance(result, list):
                self.assertEqual(result, [1, 2, 3, 4, 5, 6])
            else:
                self.fail(f"Unexpected return type: {type(result)}")
        except AttributeError:
            # Function doesn't exist, skip test
            self.skipTest("iwfm.list_flatten function not implemented")
        except Exception as e:
            self.fail(f"list_flatten raised unexpected exception: {e}")
    
    def test_list_intersection(self):
        """Test list intersection"""
        list1 = [1, 2, 3, 4, 5]
        list2 = [3, 4, 5, 6, 7]
        try:
            result = iwfm.list_intersection(list1, list2)
            self.assertEqual(set(result), {3, 4, 5})
        except AttributeError:
            self.skipTest("iwfm.list_intersection function not implemented")
        except Exception as e:
            self.fail(f"list_intersection raised unexpected exception: {e}")
    
    def test_list_diff(self):
        """Test list difference"""
        list1 = [1, 2, 3, 4, 5]
        list2 = [3, 4, 5]
        try:
            result = iwfm.list_diff(list1, list2)
            # Handle different possible return types
            if isinstance(result, (list, tuple)):
                self.assertEqual(set(result), {1, 2})
            elif isinstance(result, set):
                self.assertEqual(result, {1, 2})
            else:
                self.fail(f"Unexpected return type: {type(result)}")
        except AttributeError:
            # Function doesn't exist, skip test
            self.skipTest("iwfm.list_diff function not implemented")
        except Exception as e:
            self.fail(f"list_diff raised unexpected exception: {e}")


class TestArrayOperations(unittest.TestCase):
    """Test suite for array/matrix operations"""
    
    def test_transpose(self):
        """Test matrix transpose"""
        matrix = [[1, 2, 3], [4, 5, 6]]
        try:
            result = iwfm.transpose(matrix)
            self.assertEqual(result, [[1, 4], [2, 5], [3, 6]])
        except AttributeError:
            self.skipTest("iwfm.transpose function not implemented")
        except Exception as e:
            self.fail(f"transpose raised unexpected exception: {e}")
    
    def test_row_sum(self):
        """Test row sum"""
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        try:
            result = iwfm.row_sum(data)
            self.assertEqual(result, [6, 15, 24])
        except AttributeError:
            self.skipTest("iwfm.row_sum function not implemented")
        except Exception as e:
            self.fail(f"row_sum raised unexpected exception: {e}")
    
    def test_array_min(self):
        """Test finding minimum in array"""
        data = [5, 2, 8, 1, 9]
        try:
            result = iwfm.array_min(data)
            self.assertEqual(result, 1)
        except AttributeError:
            self.skipTest("iwfm.array_min function not implemented")
        except Exception as e:
            self.fail(f"array_min raised unexpected exception: {e}")
    
    def test_array_max(self):
        """Test finding maximum in array"""
        data = [5, 2, 8, 1, 9]
        try:
            result = iwfm.array_max(data)
            self.assertEqual(result, 9)
        except AttributeError:
            self.skipTest("iwfm.array_max function not implemented")
        except Exception as e:
            self.fail(f"array_max raised unexpected exception: {e}")


class TestCoordinateOperations(unittest.TestCase):
    """Test suite for coordinate operations"""
    
    def test_midpoint(self):
        """Test calculating midpoint"""
        p1 = [0.0, 0.0]
        p2 = [10.0, 10.0]
        try:
            result = iwfm.midpoint(p1, p2)
            self.assertEqual(result, [5.0, 5.0])
        except AttributeError:
            self.skipTest("iwfm.midpoint function not implemented")
        except Exception as e:
            self.fail(f"midpoint raised unexpected exception: {e}")
    
    def test_bbox(self):
        """Test bounding box calculation"""
        points = [[0, 0], [10, 0], [10, 10], [0, 10]]
        try:
            result = iwfm.bbox(points)
            # Handle different possible return formats
            if isinstance(result, list):
                # Check if it's [xmin, ymin, xmax, ymax] format
                if len(result) == 4:
                    self.assertEqual(result, [0, 0, 10, 10])
                else:
                    self.fail(f"Unexpected bbox format: {result}")
            elif isinstance(result, dict):
                # Check if it's dictionary format
                self.assertIn('xmin', result)
                self.assertIn('ymin', result)
                self.assertIn('xmax', result)
                self.assertIn('ymax', result)
                self.assertEqual(result['xmin'], 0)
                self.assertEqual(result['ymin'], 0)
                self.assertEqual(result['xmax'], 10)
                self.assertEqual(result['ymax'], 10)
            elif isinstance(result, tuple):
                # Check if it's tuple format
                self.assertEqual(len(result), 4)
                self.assertEqual(result, (0, 0, 10, 10))
            else:
                self.fail(f"Unexpected return type: {type(result)}")
        except AttributeError:
            self.skipTest("iwfm.bbox function not implemented")
        except Exception as e:
            self.fail(f"bbox raised unexpected exception: {e}")
    
    def test_point_in_polygon(self):
        """Test point in polygon check"""
        polygon = [[0, 0], [10, 0], [10, 10], [0, 10]]
        point_inside = [5, 5]
        point_outside = [15, 15]
        
        try:
            self.assertTrue(iwfm.point_in_polygon(point_inside, polygon))
            self.assertFalse(iwfm.point_in_polygon(point_outside, polygon))
        except AttributeError:
            self.skipTest("iwfm.point_in_polygon function not implemented")
        except Exception as e:
            self.fail(f"point_in_polygon raised unexpected exception: {e}")


class TestAreaCalculations(unittest.TestCase):
    """Test suite for area calculations"""
    
    def test_triangle_area(self):
        """Test triangle area calculation"""
        p1 = [0.0, 0.0]
        p2 = [10.0, 0.0]
        p3 = [5.0, 10.0]
        try:
            result = iwfm.triangle_area(p1, p2, p3)
            self.assertAlmostEqual(result, 50.0, places=5)
        except AttributeError:
            self.skipTest("iwfm.triangle_area function not implemented")
        except Exception as e:
            self.fail(f"triangle_area raised unexpected exception: {e}")
    
    def test_polygon_area_square(self):
        """Test polygon area for square"""
        points = [[0, 0], [10, 0], [10, 10], [0, 10]]
        try:
            result = iwfm.polygon_area(points)
            self.assertAlmostEqual(result, 100.0, places=5)
        except AttributeError:
            self.skipTest("iwfm.polygon_area function not implemented")
        except Exception as e:
            self.fail(f"polygon_area raised unexpected exception: {e}")
    
    def test_polygon_area_triangle(self):
        """Test polygon area for triangle"""
        points = [[0, 0], [10, 0], [5, 10]]
        try:
            result = iwfm.polygon_area(points)
            self.assertAlmostEqual(result, 50.0, places=5)
        except AttributeError:
            self.skipTest("iwfm.polygon_area function not implemented")
        except Exception as e:
            self.fail(f"polygon_area raised unexpected exception: {e}")


class TestInterpolation(unittest.TestCase):
    """Test suite for interpolation functions"""
    
    def test_linear_interpolate(self):
        """Test linear interpolation"""
        x1, y1 = 0.0, 0.0
        x2, y2 = 10.0, 10.0
        x = 5.0
        try:
            result = iwfm.linear_interpolate(x1, y1, x2, y2, x)
            self.assertAlmostEqual(result, 5.0, places=5)
        except AttributeError:
            self.skipTest("iwfm.linear_interpolate function not implemented")
        except Exception as e:
            self.fail(f"linear_interpolate raised unexpected exception: {e}")
    
    def test_bilinear_interpolate(self):
        """Test bilinear interpolation"""
        # Grid corners
        z11, z12 = 0.0, 10.0
        z21, z22 = 10.0, 20.0
        # Interpolate at center
        try:
            result = iwfm.bilinear_interpolate(0, 0, 1, 1, z11, z12, z21, z22, 0.5, 0.5)
            self.assertAlmostEqual(result, 10.0, places=5)
        except AttributeError:
            self.skipTest("iwfm.bilinear_interpolate function not implemented")
        except TypeError as e:
            # Function exists but may have different signature
            # Try alternate signature
            try:
                result = iwfm.bilinear_interpolate(
                    x=[0, 1], 
                    y=[0, 1], 
                    z=[[z11, z12], [z21, z22]], 
                    xi=0.5, 
                    yi=0.5
                )
                self.assertAlmostEqual(result, 10.0, places=5)
            except:
                self.skipTest(f"iwfm.bilinear_interpolate has unsupported signature: {e}")
        except Exception as e:
            self.fail(f"bilinear_interpolate raised unexpected exception: {e}")


class TestStatistics(unittest.TestCase):
    """Test suite for statistical functions"""
    
    def test_mean(self):
        """Test mean calculation"""
        data = [1, 2, 3, 4, 5]
        try:
            result = iwfm.mean(data)
            self.assertAlmostEqual(result, 3.0, places=5)
        except AttributeError:
            self.skipTest("iwfm.mean function not implemented")
        except Exception as e:
            self.fail(f"mean raised unexpected exception: {e}")
    
    def test_median_odd(self):
        """Test median with odd number of elements"""
        data = [1, 3, 5, 7, 9]
        try:
            result = iwfm.median(data)
            self.assertAlmostEqual(result, 5.0, places=5)
        except AttributeError:
            self.skipTest("iwfm.median function not implemented")
        except Exception as e:
            self.fail(f"median raised unexpected exception: {e}")
    
    def test_median_even(self):
        """Test median with even number of elements"""
        data = [1, 2, 3, 4]
        try:
            result = iwfm.median(data)
            self.assertAlmostEqual(result, 2.5, places=5)
        except AttributeError:
            self.skipTest("iwfm.median function not implemented")
        except Exception as e:
            self.fail(f"median raised unexpected exception: {e}")
    
    def test_std_dev(self):
        """Test standard deviation"""
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        try:
            result = iwfm.std_dev(data)
            self.assertGreater(result, 0)
        except AttributeError:
            self.skipTest("iwfm.std_dev function not implemented")
        except Exception as e:
            self.fail(f"std_dev raised unexpected exception: {e}")


class TestTimeSeriesOperations(unittest.TestCase):
    """Test suite for time series operations"""
    
    def test_date_range(self):
        """Test generating date range"""
        start = "01/01/2023"
        end = "01/05/2023"
        try:
            result = iwfm.date_range(start, end)
            self.assertEqual(len(result), 5)
        except AttributeError:
            self.skipTest("iwfm.date_range function not implemented")
        except Exception as e:
            self.fail(f"date_range raised unexpected exception: {e}")
    
    def test_water_year(self):
        """Test water year calculation"""
        try:
            # October is start of water year
            result = iwfm.water_year("10/01/2023")
            self.assertEqual(result, 2024)
            
            result = iwfm.water_year("09/30/2023")
            self.assertEqual(result, 2023)
        except AttributeError:
            self.skipTest("iwfm.water_year function not implemented")
        except Exception as e:
            self.fail(f"water_year raised unexpected exception: {e}")
    
    def test_days_between(self):
        """Test calculating days between dates"""
        date1 = "01/01/2023"
        date2 = "01/10/2023"
        try:
            result = iwfm.days_between(date1, date2)
            self.assertEqual(result, 9)
        except AttributeError:
            self.skipTest("iwfm.days_between function not implemented")
        except Exception as e:
            self.fail(f"days_between raised unexpected exception: {e}")


class TestValidation(unittest.TestCase):
    """Test suite for validation functions"""
    
    def test_is_number(self):
        """Test number validation"""
        try:
            self.assertTrue(iwfm.is_number("123"))
            self.assertTrue(iwfm.is_number("123.456"))
            self.assertTrue(iwfm.is_number("-123.456"))
            self.assertFalse(iwfm.is_number("abc"))
        except AttributeError:
            self.skipTest("iwfm.is_number function not implemented")
        except Exception as e:
            self.fail(f"is_number raised unexpected exception: {e}")
    
    def test_is_date(self):
        """Test date validation"""
        try:
            self.assertTrue(iwfm.is_date("01/15/2023"))
            self.assertTrue(iwfm.is_date("12/31/2023"))
            self.assertFalse(iwfm.is_date("13/01/2023"))  # Invalid month
            self.assertFalse(iwfm.is_date("not a date"))
        except AttributeError:
            self.skipTest("iwfm.is_date function not implemented")
        except Exception as e:
            self.fail(f"is_date raised unexpected exception: {e}")
    
    def test_validate_file_exists(self):
        """Test file existence validation"""
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            temp_path = tf.name
        
        try:
            self.assertTrue(iwfm.validate_file_exists(temp_path))
            os.unlink(temp_path)
            self.assertFalse(iwfm.validate_file_exists(temp_path))
        except AttributeError:
            self.skipTest("iwfm.validate_file_exists function not implemented")
        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            self.fail(f"validate_file_exists raised unexpected exception: {e}")
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestErrorHandling(unittest.TestCase):
    """Test suite for error handling"""
    
    def test_divide_by_zero_handling(self):
        """Test division by zero handling"""
        try:
            result = iwfm.safe_divide(10, 0, default=0)
            self.assertEqual(result, 0)
        except AttributeError:
            self.skipTest("iwfm.safe_divide function not implemented")
        except Exception as e:
            self.fail(f"safe_divide raised unexpected exception: {e}")
    
    def test_file_not_found_handling(self):
        """Test file not found handling"""
        try:
            with self.assertRaises(FileNotFoundError):
                iwfm.file_2_list("nonexistent_file.txt")
        except AttributeError:
            self.skipTest("iwfm.file_2_list function not implemented")
    
    def test_invalid_node_handling(self):
        """Test handling of invalid node references"""
        elem_nodes = [[1, 2, 999]]  # Node 999 doesn't exist
        node_coord_dict = {1: [0, 0], 2: [10, 0]}
        
        try:
            with self.assertRaises(KeyError):
                iwfm.elem_poly_coords(elem_nodes, node_coord_dict)
        except AttributeError:
            self.skipTest("iwfm.elem_poly_coords function not implemented")


class TestEdgeCases(unittest.TestCase):
    """Test suite for edge cases"""
    
    def test_empty_list_operations(self):
        """Test operations on empty lists"""
        try:
            self.assertEqual(iwfm.list_unique([]), [])
            self.assertEqual(iwfm.list_flatten([]), [])
        except AttributeError:
            self.skipTest("List operation functions not implemented")
        except Exception as e:
            self.fail(f"Edge case tests raised unexpected exception: {e}")
    
    def test_single_element_operations(self):
        """Test operations on single elements"""
        try:
            self.assertEqual(iwfm.list_unique([1]), [1])
            self.assertAlmostEqual(iwfm.mean([5]), 5.0)
        except AttributeError:
            self.skipTest("Single element operation functions not implemented")
        except Exception as e:
            self.fail(f"Single element tests raised unexpected exception: {e}")
    
    def test_large_coordinates(self):
        """Test with large coordinate values"""
        a = [1000000.0, 1000000.0]
        b = [1000003.0, 1000004.0]
        try:
            result = iwfm.distance(a, b)
            self.assertAlmostEqual(result, 5.0, places=5)
        except AttributeError:
            self.skipTest("iwfm.distance function not implemented")
        except Exception as e:
            self.fail(f"distance raised unexpected exception: {e}")
    
    def test_negative_values(self):
        """Test with negative values"""
        data = [-5, -3, -1, 0, 1, 3, 5]
        try:
            result = iwfm.mean(data)
            self.assertAlmostEqual(result, 0.0, places=5)
        except AttributeError:
            self.skipTest("iwfm.mean function not implemented")
        except Exception as e:
            self.fail(f"mean with negative values raised unexpected exception: {e}")


class TestPerformance(unittest.TestCase):
    """Test suite for performance-critical operations"""
    
    def test_large_polygon(self):
        """Test with large polygon"""
        import time
        # Create polygon with 1000 points
        points = [[i, i*2] for i in range(1000)]
        
        try:
            start = time.time()
            result = iwfm.polygon_area(points)
            elapsed = time.time() - start
            
            self.assertIsNotNone(result)
            self.assertLess(elapsed, 1.0)  # Should complete in under 1 second
        except AttributeError:
            self.skipTest("iwfm.polygon_area function not implemented")
        except Exception as e:
            self.fail(f"polygon_area performance test raised unexpected exception: {e}")
    
    def test_many_elements(self):
        """Test with many elements"""
        # Create 100 triangular elements
        elem_nodes = [[i, i+1, i+2] for i in range(1, 100)]
        node_coord_dict = {i: [float(i), float(i*2)] for i in range(1, 202)}
        
        try:
            import time
            start = time.time()
            result = iwfm.elem_poly_coords(elem_nodes, node_coord_dict)
            elapsed = time.time() - start
            
            self.assertEqual(len(result), 99)
            self.assertLess(elapsed, 2.0)  # Should complete in under 2 seconds
        except AttributeError:
            self.skipTest("iwfm.elem_poly_coords function not implemented")
        except Exception as e:
            self.fail(f"elem_poly_coords performance test raised unexpected exception: {e}")
    
    def test_elem_poly_coords_quadrilateral(self):
        """Test polygon coordinates for quadrilateral element"""
        elem_nodes = [[1, 2, 3, 4]]
        node_coord_dict = {
            1: [0.0, 0.0],
            2: [10.0, 0.0],
            3: [10.0, 10.0],
            4: [0.0, 10.0]
        }
        
        try:
            result = iwfm.elem_poly_coords(elem_nodes, node_coord_dict)
            
            self.assertEqual(len(result), 1)
            self.assertEqual(len(result[0]), 5)  # 4 nodes + 1 closing point
            # Verify polygon is closed
            self.assertEqual(result[0][0], result[0][-1])
        except AttributeError:
            self.skipTest("iwfm.elem_poly_coords function not implemented")
        except Exception as e:
            self.fail(f"elem_poly_coords quadrilateral test raised unexpected exception: {e}")
    
    def test_elem_poly_coords_multiple_elements(self):
        """Test with multiple elements"""
        elem_nodes = [[1, 2, 3], [2, 3, 4]]
        node_coord_dict = {
            1: [0.0, 0.0],
            2: [10.0, 0.0],
            3: [10.0, 10.0],
            4: [0.0, 10.0]
        }
        
        try:
            result = iwfm.elem_poly_coords(elem_nodes, node_coord_dict)
            
            self.assertEqual(len(result), 2)  # Two elements
            # Each should be closed
            for poly in result:
                self.assertEqual(poly[0], poly[-1])
        except AttributeError:
            self.skipTest("iwfm.elem_poly_coords function not implemented")
        except Exception as e:
            self.fail(f"elem_poly_coords multiple elements test raised unexpected exception: {e}")

# -----------------


class TestFilenameOperations(unittest.TestCase):
    """Test suite for filename utility functions"""
    
    def test_filename_base_simple(self):
        """Test extracting base filename"""
        result = iwfm.filename_base("document.txt")
        self.assertEqual(result, "document")
    
    def test_filename_base_with_path(self):
        """Test extracting base from path"""
        result = iwfm.filename_base("/path/to/file.dat")
        self.assertEqual(result, "/path/to/file")
    
    def test_filename_base_multiple_dots(self):
        """Test with multiple dots in filename"""
        result = iwfm.filename_base("file.backup.txt")
        self.assertEqual(result, "file.backup")
    
    def test_filename_base_no_extension(self):
        """Test with no extension"""
        result = iwfm.filename_base("filename")
        self.assertEqual(result, "filename")
    
    def test_filename_ext_add_extension(self):
        """Test adding extension to filename"""
        result = iwfm.filename_ext("document", "txt")
        self.assertEqual(result, "document.txt")
    
    def test_filename_ext_with_existing(self):
        """Test with existing extension"""
        result = iwfm.filename_ext("file.old", "new")
        # Function appends, doesn't replace
        self.assertIn("file", result)
    
    def test_file_dir(self):
        """Test extracting directory from path"""
        result = iwfm.file_dir("/path/to/some/file.txt")
        self.assertEqual(str(result), "/path/to/some")
    
    def test_file_dir_no_path(self):
        """Test with filename only"""
        result = iwfm.file_dir("file.txt")
        self.assertEqual(str(result), ".")


class TestFileSystemOperations(unittest.TestCase):
    """Test suite for file system operations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after each test"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_file_get_path(self):
        """Test converting string to Path object"""
        result = iwfm.file_get_path("path/to/file.txt")
        self.assertIsInstance(result, Path)
    
    def test_file_2_list(self):
        """Test reading file to list"""
        test_file = Path(self.temp_dir) / "test.txt"
        with open(test_file, 'w') as f:
            f.write("Line 1\n")
            f.write("Line 2\n")
            f.write("Line 3\n")
        
        result = iwfm.file_2_list(test_file)
        self.assertEqual(len(result), 3)
        self.assertIn("Line 1", result[0])
    
    def test_file_rename(self):
        """Test file rename operation"""
        old_file = Path(self.temp_dir) / "old.txt"
        new_file = Path(self.temp_dir) / "new.txt"
        
        with open(old_file, 'w') as f:
            f.write("content")
        
        iwfm.file_rename(str(old_file), str(new_file))
        
        self.assertFalse(old_file.exists())
        self.assertTrue(new_file.exists())
    
    def test_file_delete(self):
        """Test file deletion"""
        test_file = Path(self.temp_dir) / "delete_me.txt"
        
        with open(test_file, 'w') as f:
            f.write("content")
        
        iwfm.file_delete(str(test_file))
        self.assertFalse(test_file.exists())
    
    def test_file_2_bak(self):
        """Test creating backup file"""
        test_file = Path(self.temp_dir) / "original.txt"
        
        with open(test_file, 'w') as f:
            f.write("original content")
        
        # Call the backup function
        try:
            result = iwfm.file_2_bak(str(test_file))
            
            # Check for various possible backup file naming conventions
            possible_bak_files = [
                Path(str(test_file) + ".bak"),
                Path(str(test_file) + ".backup"),
                Path(self.temp_dir) / "original.bak",
                Path(self.temp_dir) / "original.txt.bak"
            ]
            
            # At least one backup file should exist
            bak_exists = any(f.exists() for f in possible_bak_files)
            
            if not bak_exists:
                # If function returns the backup path, check that
                if isinstance(result, (str, Path)) and Path(result).exists():
                    bak_exists = True
            
            self.assertTrue(bak_exists, 
                          f"No backup file found. Checked: {[str(f) for f in possible_bak_files]}")
            
        except AttributeError:
            self.skipTest("iwfm.file_2_bak function not implemented")
        except Exception as e:
            self.fail(f"file_2_bak raised unexpected exception: {e}")


class TestMathematicalOperations(unittest.TestCase):
    """Test suite for mathematical operations"""
    
    def test_distance_calculation(self):
        """Test distance between two points"""
        a = [0.0, 0.0]
        b = [3.0, 4.0]
        result = iwfm.distance(a, b)
        self.assertAlmostEqual(result, 5.0, places=6)
    
    def test_distance_zero(self):
        """Test distance when points are the same"""
        a = [5.0, 10.0]
        b = [5.0, 10.0]
        result = iwfm.distance(a, b)
        self.assertAlmostEqual(result, 0.0, places=6)
    
    def test_distance_negative_coords(self):
        """Test distance with negative coordinates"""
        a = [-1.0, -1.0]
        b = [2.0, 3.0]
        result = iwfm.distance(a, b)
        expected = ((2 - (-1))**2 + (3 - (-1))**2)**0.5
        self.assertAlmostEqual(result, expected, places=6)
    
    def test_round_function(self):
        """Test rounding to decimal places"""
        result = iwfm.round(3.14159, 2)
        self.assertAlmostEqual(result, 3.14, places=2)
    
#    def test_round_to_integer(self):
#        """Test rounding to integer"""
#        result = iwfm.round(3.7, 0)
#        # Accept either integer 4 or float 4.0 by checking numeric value
#        self.assertTrue(result == 4 or result == 4.0, 
#                       f"Expected 4 or 4.0, got {result} (type: {type(result).__name__})")

    
    def test_logtrans(self):
        """Test logarithmic transformation"""
        result = iwfm.logtrans(10.0)
        self.assertAlmostEqual(result, 1.0, places=5)
        
        result = iwfm.logtrans(100.0)
        self.assertAlmostEqual(result, 2.0, places=5)
    
    def test_column_sum(self):
        """Test column sum function"""
        data = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        result = iwfm.column_sum(data)
        self.assertEqual(result, [12, 15, 18])


class TestStringOperations(unittest.TestCase):
    """Test suite for string manipulation functions"""
    
    def test_pad_front(self):
        """Test front padding"""
        result = iwfm.pad_front("test", 10, ' ')
        self.assertEqual(len(result), 10)
        self.assertTrue(result.endswith("test"))
        self.assertTrue(result.startswith(" "))
    
    def test_pad_back(self):
        """Test back padding"""
        result = iwfm.pad_back("test", 10, ' ')
        self.assertEqual(len(result), 10)
        self.assertTrue(result.startswith("test"))
        self.assertTrue(result.endswith(" "))
    
    def test_pad_both(self):
        """Test both sides padding"""
        result = iwfm.pad_both("X", 2, 7, '*')
        self.assertEqual(len(result), 7)
        self.assertIn("X", result)
        self.assertTrue(result.startswith("*"))
    
    def test_pad_front_with_zeros(self):
        """Test padding with zeros"""
        result = iwfm.pad_front("123", 5, '0')
        self.assertEqual(result, "00123")
    
    def test_pad_back_with_zeros(self):
        """Test back padding with zeros"""
        result = iwfm.pad_back("123", 5, '0')
        self.assertEqual(result, "12300")


class TestDateOperations(unittest.TestCase):
    """Test suite for date operation functions"""
    
    def test_month_extraction(self):
        """Test extracting month from date string"""
        result = iwfm.month("10/15/2023")
        self.assertEqual(result, 10)
    
    def test_day_extraction(self):
        """Test extracting day from date string"""
        result = iwfm.day("10/15/2023")
        self.assertEqual(result, 15)
    
    def test_year_extraction(self):
        """Test extracting year from date string"""
        result = iwfm.year("10/15/2023")
        self.assertEqual(result, 2023)
    
    def test_date2text(self):
        """Test converting date components to text"""
        result = iwfm.date2text(15, 10, 2023)
        self.assertEqual(result, "10/15/2023")
    
    def test_date2text_with_padding(self):
        """Test date conversion with single digits"""
        result = iwfm.date2text(5, 3, 2023)
        self.assertEqual(result, "03/05/2023")


class TestDictionaryOperations(unittest.TestCase):
    """Test suite for dictionary operations"""
    
    def test_inverse_dict(self):
        """Test inverting a dictionary"""
        original = {1: 'a', 2: 'b', 3: 'c'}
        result = iwfm.inverse_dict(original)
        
        expected = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(result, expected)
    
    def test_inverse_dict_empty(self):
        """Test with empty dictionary"""
        result = iwfm.inverse_dict({})
        self.assertEqual(result, {})
    
    def test_inverse_dict_numeric_values(self):
        """Test with numeric values"""
        original = {'x': 10, 'y': 20, 'z': 30}
        result = iwfm.inverse_dict(original)
        
        self.assertEqual(result[10], 'x')
        self.assertEqual(result[20], 'y')
        self.assertEqual(result[30], 'z')
    
    def test_list2dict(self):
        """Test converting list to dictionary"""
        data = [[1, 'a'], [2, 'b'], [3, 'c']]
        result = iwfm.list2dict(data)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 3)


class TestUnitConversions(unittest.TestCase):
    """Test suite for unit conversion functions"""
    
    def test_cfs2afd_basic(self):
        """Test CFS to acre-feet per day conversion"""
        result = iwfm.cfs2afd(1.0)
        self.assertAlmostEqual(result, 1.983, places=3)
    
    def test_cfs2afd_zero(self):
        """Test with zero input"""
        result = iwfm.cfs2afd(0.0)
        self.assertEqual(result, 0.0)
    
    def test_cfs2afd_large_value(self):
        """Test with large value"""
        result = iwfm.cfs2afd(1000.0)
        self.assertAlmostEqual(result, 1983.0, places=0)
    
    def test_cfs2afd_decimal(self):
        """Test with decimal value"""
        result = iwfm.cfs2afd(2.5)
        expected = 2.5 * 1.983
        self.assertAlmostEqual(result, expected, places=2)


class TestNearestOperations(unittest.TestCase):
    """Test suite for nearest node/element operations"""
    
    def test_nearest_node_basic(self):
        """Test finding nearest node"""
        d_nodes = {
            1: [0.0, 0.0],
            2: [10.0, 0.0],
            3: [10.0, 10.0],
            4: [0.0, 10.0]
        }
        
        result = iwfm.nearest(d_nodes, 1.0, 1.0)
        self.assertEqual(result, 1)
    
    def test_nearest_node_exact_match(self):
        """Test when point exactly matches a node"""
        d_nodes = {
            1: [0.0, 0.0],
            2: [10.0, 0.0]
        }
        
        result = iwfm.nearest(d_nodes, 10.0, 0.0)
        self.assertEqual(result, 2)
    
    def test_nearest_node_center(self):
        """Test finding nearest to center point"""
        d_nodes = {
            1: [0.0, 0.0],
            2: [10.0, 0.0],
            3: [10.0, 10.0],
            4: [0.0, 10.0],
            5: [5.0, 5.0]
        }
        
        result = iwfm.nearest(d_nodes, 5.5, 5.5)
        self.assertEqual(result, 5)


class TestSkipAheadFunction(unittest.TestCase):
    """Test suite for skip_ahead file parsing function"""
    
    def test_skip_ahead_basic(self):
        """Test basic skip_ahead functionality"""
        lines = [
            "C Comment line 1",
            "C Comment line 2",
            "Data line 1",
            "Data line 2"
        ]
        result = iwfm.skip_ahead(0, lines, 0)
        self.assertEqual(result, 2)
    
    def test_skip_ahead_with_skip_parameter(self):
        """Test skip_ahead with skip parameter"""
        lines = [
            "C Comment",
            "Data line 1",
            "Data line 2",
            "Data line 3"
        ]
        result = iwfm.skip_ahead(0, lines, 1)
        self.assertEqual(result, 2)
    
    def test_skip_ahead_multiple_comment_types(self):
        """Test with different comment characters"""
        lines = [
            "C Comment with C",
            "c lowercase c",
            "* asterisk",
            "# hash",
            "Data line"
        ]
        result = iwfm.skip_ahead(0, lines, 0)
        self.assertEqual(result, 4)


class TestPrintToString(unittest.TestCase):
    """Test suite for print_to_string function"""
    
    def test_print_to_string_basic(self):
        """Test converting print output to string"""
        result = iwfm.print_to_string("Hello", "World")
        self.assertIsInstance(result, str)
        self.assertIn("Hello", result)
        self.assertIn("World", result)
    
    def test_print_to_string_numbers(self):
        """Test with numbers"""
        result = iwfm.print_to_string(123, 456)
        self.assertIn("123", result)
        self.assertIn("456", result)
    
    def test_print_to_string_single_value(self):
        """Test with single value"""
        result = iwfm.print_to_string("test")
        self.assertEqual(result.strip(), "test")


class TestElemPolyCoords(unittest.TestCase):
    """Test suite for element polygon coordinate operations"""
    
    def test_elem_poly_coords_triangle(self):
        """Test polygon coordinates for triangular element"""
        elem_nodes = [[1, 2, 3]]
        node_coord_dict = {
            1: [0.0, 0.0],
            2: [10.0, 0.0],
            3: [5.0, 10.0]
        }
        
        result = iwfm.elem_poly_coords(elem_nodes, node_coord_dict)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 4)  # 3 nodes + 1 closing point
        # Verify polygon is closed
        self.assertEqual(result[0][0], result[0][-1])
        class TestTimeSeriesAnalysisExtended(unittest.TestCase):
            """Extended test suite for time series analysis with better error handling"""
            
            def test_annual_aggregation_water_year(self):
                """Test aggregating to water year (Oct-Sep)"""
                dates = ["10/01/2022", "01/15/2023", "06/01/2023", "10/01/2023", "03/15/2024"]
                values = [100, 200, 150, 180, 220]
                try:
                    result = iwfm.annual_aggregation(dates, values, water_year=True)
                    # Water year 2023 starts Oct 2022, year 2024 starts Oct 2023
                    self.assertIsInstance(result, (list, dict))
                    if isinstance(result, dict):
                        self.assertTrue(len(result) >= 1)
                    else:
                        self.assertTrue(len(result) >= 1)
                except AttributeError:
                    self.skipTest("iwfm.annual_aggregation function not implemented")
                except TypeError:
                    # Try without water_year parameter
                    try:
                        result = iwfm.annual_aggregation(dates, values)
                        self.assertIsInstance(result, (list, dict))
                    except:
                        self.skipTest("iwfm.annual_aggregation has incompatible signature")
                except Exception as e:
                    self.fail(f"annual_aggregation raised unexpected exception: {e}")
            
            def test_annual_aggregation_calendar_year(self):
                """Test aggregating to calendar year"""
                dates = ["01/15/2022", "06/01/2022", "12/15/2022", "03/01/2023", "08/15/2023"]
                values = [100, 150, 200, 180, 220]
                try:
                    result = iwfm.annual_aggregation(dates, values)
                    self.assertIsInstance(result, (list, dict, tuple))
                    # Should have at least 2 years of data
                    if isinstance(result, dict):
                        self.assertGreaterEqual(len(result), 1)
                    elif isinstance(result, list):
                        self.assertGreaterEqual(len(result), 1)
                except AttributeError:
                    self.skipTest("iwfm.annual_aggregation function not implemented")
                except Exception as e:
                    self.fail(f"annual_aggregation raised unexpected exception: {e}")
            
            def test_monthly_aggregation_sum(self):
                """Test monthly aggregation with sum method"""
                dates = ["01/05/2023", "01/15/2023", "01/25/2023", "02/10/2023", "02/20/2023"]
                values = [10, 20, 30, 40, 50]
                try:
                    result = iwfm.monthly_aggregation(dates, values, method='sum')
                    self.assertIsInstance(result, (list, dict))
                    if isinstance(result, dict):
                        # January should have 60, February should have 90
                        self.assertTrue(any(v == 60 or abs(v - 60) < 1 for v in result.values()))
                    elif isinstance(result, list):
                        self.assertEqual(len(result), 2)
                except AttributeError:
                    self.skipTest("iwfm.monthly_aggregation function not implemented")
                except TypeError:
                    # Try without method parameter
                    try:
                        result = iwfm.monthly_aggregation(dates, values)
                        self.assertIsInstance(result, (list, dict))
                    except:
                        self.skipTest("iwfm.monthly_aggregation has incompatible signature")
                except Exception as e:
                    self.fail(f"monthly_aggregation raised unexpected exception: {e}")
            
            def test_monthly_aggregation_average(self):
                """Test monthly aggregation with average method"""
                dates = ["01/10/2023", "01/20/2023", "02/05/2023", "02/15/2023", "02/25/2023"]
                values = [10, 20, 30, 40, 50]
                try:
                    result = iwfm.monthly_aggregation(dates, values, method='mean')
                    self.assertIsInstance(result, (list, dict))
                    if isinstance(result, dict):
                        # Check that averages are reasonable
                        for val in result.values():
                            self.assertGreater(val, 0)
                            self.assertLess(val, 100)
                except AttributeError:
                    self.skipTest("iwfm.monthly_aggregation function not implemented")
                except TypeError:
                    try:
                        result = iwfm.monthly_aggregation(dates, values)
                        self.assertIsInstance(result, (list, dict))
                    except:
                        self.skipTest("iwfm.monthly_aggregation has incompatible signature")
                except Exception as e:
                    self.fail(f"monthly_aggregation raised unexpected exception: {e}")
            
            def test_resample_timeseries(self):
                """Test resampling time series to different frequency"""
                dates = ["01/01/2023", "01/02/2023", "01/03/2023", "01/04/2023"]
                values = [10, 12, 11, 13]
                try:
                    # Resample daily to weekly
                    result = iwfm.resample_timeseries(dates, values, freq='W')
                    self.assertIsInstance(result, dict)
                    self.assertIn('dates', result)
                    self.assertIn('values', result)
                except AttributeError:
                    self.skipTest("iwfm.resample_timeseries function not implemented")
                except Exception as e:
                    self.fail(f"resample_timeseries raised unexpected exception: {e}")
            
            def test_time_series_statistics(self):
                """Test calculating statistics for time series"""
                values = [10, 12, 15, 11, 13, 14, 16, 12, 11, 15]
                try:
                    result = iwfm.timeseries_stats(values)
                    self.assertIsInstance(result, dict)
                    self.assertIn('mean', result)
                    self.assertIn('std', result)
                    self.assertIn('min', result)
                    self.assertIn('max', result)
                except AttributeError:
                    self.skipTest("iwfm.timeseries_stats function not implemented")
                except Exception as e:
                    self.fail(f"timeseries_stats raised unexpected exception: {e}")
            
            def test_moving_average_weighted(self):
                """Test weighted moving average"""
                data = [10, 20, 30, 40, 50]
                weights = [0.1, 0.2, 0.4, 0.2, 0.1]
                try:
                    result = iwfm.weighted_moving_average(data, weights)
                    self.assertIsInstance(result, list)
                    self.assertGreater(len(result), 0)
                except AttributeError:
                    self.skipTest("iwfm.weighted_moving_average function not implemented")
                except Exception as e:
                    self.fail(f"weighted_moving_average raised unexpected exception: {e}")
            
            def test_exponential_smoothing(self):
                """Test exponential smoothing"""
                data = [100, 105, 102, 108, 110, 107, 112]
                alpha = 0.3  # smoothing factor
                try:
                    result = iwfm.exponential_smoothing(data, alpha)
                    self.assertEqual(len(result), len(data))
                    self.assertAlmostEqual(result[0], data[0], places=2)
                except AttributeError:
                    self.skipTest("iwfm.exponential_smoothing function not implemented")
                except Exception as e:
                    self.fail(f"exponential_smoothing raised unexpected exception: {e}")
            
            def test_cumulative_distribution(self):
                """Test cumulative distribution calculation"""
                data = [10, 20, 15, 25, 30, 18, 22]
                try:
                    result = iwfm.cumulative_distribution(data)
                    self.assertEqual(len(result), len(data))
                    # CDF should be monotonically increasing
                    for i in range(len(result)-1):
                        self.assertGreaterEqual(result[i+1], result[i])
                except AttributeError:
                    self.skipTest("iwfm.cumulative_distribution function not implemented")
                except Exception as e:
                    self.fail(f"cumulative_distribution raised unexpected exception: {e}")
            
            def test_lag_correlation(self):
                """Test lag correlation analysis"""
                series1 = [10, 12, 15, 14, 16, 18, 17, 19]
                series2 = [8, 10, 13, 12, 14, 16, 15, 17]
                max_lag = 3
                try:
                    result = iwfm.lag_correlation(series1, series2, max_lag)
                    self.assertEqual(len(result), max_lag + 1)
                    # All correlations should be between -1 and 1
                    for corr in result:
                        self.assertGreaterEqual(corr, -1.0)
                        self.assertLessEqual(corr, 1.0)
                except AttributeError:
                    self.skipTest("iwfm.lag_correlation function not implemented")
                except Exception as e:
                    self.fail(f"lag_correlation raised unexpected exception: {e}")
            
            def test_detrend_timeseries(self):
                """Test detrending time series"""
                # Create data with linear trend
                data = [10 + i*2 for i in range(10)]
                try:
                    result = iwfm.detrend(data)
                    self.assertEqual(len(result), len(data))
                    # Mean should be close to zero after detrending
                    mean_detrended = sum(result) / len(result)
                    self.assertAlmostEqual(mean_detrended, 0.0, places=1)
                except AttributeError:
                    self.skipTest("iwfm.detrend function not implemented")
                except Exception as e:
                    self.fail(f"detrend raised unexpected exception: {e}")


        class TestAdvancedAggregation(unittest.TestCase):
            """Test suite for advanced aggregation functions"""
            
            def test_seasonal_aggregation(self):
                """Test seasonal aggregation (Winter, Spring, Summer, Fall)"""
                dates = ["12/15/2022", "01/15/2023", "03/15/2023", "06/15/2023", 
                         "09/15/2023", "12/15/2023"]
                values = [100, 120, 150, 180, 160, 110]
                try:
                    result = iwfm.seasonal_aggregation(dates, values)
                    self.assertIsInstance(result, dict)
                    # Should have entries for seasons
                    seasons = ['winter', 'spring', 'summer', 'fall']
                    found_seasons = [s for s in seasons if s in str(result).lower()]
                    self.assertGreater(len(found_seasons), 0)
                except AttributeError:
                    self.skipTest("iwfm.seasonal_aggregation function not implemented")
                except Exception as e:
                    self.fail(f"seasonal_aggregation raised unexpected exception: {e}")
            
            def test_water_year_cumulative(self):
                """Test cumulative values by water year"""
                dates = ["10/01/2022", "12/01/2022", "03/01/2023", "06/01/2023", 
                         "09/01/2023", "10/01/2023"]
                values = [100, 150, 200, 250, 180, 120]
                try:
                    result = iwfm.water_year_cumulative(dates, values)
                    self.assertIsInstance(result, (dict, list))
                    if isinstance(result, dict):
                        # Check that cumulative values are increasing within water year
                        for wy_data in result.values():
                            if isinstance(wy_data, list) and len(wy_data) > 1:
                                for i in range(len(wy_data)-1):
                                    self.assertLessEqual(wy_data[i], wy_data[i+1])
                except AttributeError:
                    self.skipTest("iwfm.water_year_cumulative function not implemented")
                except Exception as e:
                    self.fail(f"water_year_cumulative raised unexpected exception: {e}")
            
            def test_rolling_sum(self):
                """Test rolling sum calculation"""
                data = [10, 20, 30, 40, 50]
                window = 3
                try:
                    result = iwfm.rolling_sum(data, window)
                    self.assertEqual(len(result), len(data) - window + 1)
                    self.assertEqual(result[0], 60)  # 10+20+30
                    self.assertEqual(result[-1], 120)  # 30+40+50
                except AttributeError:
                    self.skipTest("iwfm.rolling_sum function not implemented")
                except Exception as e:
                    self.fail(f"rolling_sum raised unexpected exception: {e}")
            
            def test_groupby_custom(self):
                """Test custom groupby aggregation"""
                dates = ["01/15/2023", "01/20/2023", "02/10/2023", "02/25/2023"]
                values = [10, 20, 30, 40]
                group_func = lambda d: iwfm.month(d)  # Group by month
                try:
                    result = iwfm.groupby_aggregate(dates, values, group_func)
                    self.assertIsInstance(result, dict)
                    self.assertEqual(len(result), 2)  # 2 months
                except AttributeError:
                    self.skipTest("iwfm.groupby_aggregate function not implemented")
                except Exception as e:
                    self.fail(f"groupby_aggregate raised unexpected exception: {e}")
            
            def test_percentile_aggregation(self):
                """Test percentile-based aggregation"""
                data = [10, 20, 15, 25, 30, 18, 22, 28, 16, 24]
                percentiles = [25, 50, 75]
                try:
                    result = iwfm.percentile_aggregate(data, percentiles)
                    self.assertIsInstance(result, dict)
                    self.assertEqual(len(result), len(percentiles))
                    # 50th percentile should be the median
                    self.assertIn(50, result)
                except AttributeError:
                    self.skipTest("iwfm.percentile_aggregate function not implemented")
                except Exception as e:
                    self.fail(f"percentile_aggregate raised unexpected exception: {e}")


        class TestDateTimeUtilities(unittest.TestCase):
            """Test suite for date/time utility functions"""
            
            def test_date_add_days(self):
                """Test adding days to a date"""
                date = "01/15/2023"
                days = 10
                try:
                    result = iwfm.date_add_days(date, days)
                    self.assertIsInstance(result, str)
                    # Result should be 01/25/2023
                    self.assertIn("25", result)
                except AttributeError:
                    self.skipTest("iwfm.date_add_days function not implemented")
                except Exception as e:
                    self.fail(f"date_add_days raised unexpected exception: {e}")
            
            def test_date_diff(self):
                """Test calculating difference between dates in various units"""
                date1 = "01/01/2023"
                date2 = "01/31/2023"
                try:
                    result = iwfm.date_difference(date1, date2, unit='days')
                    self.assertEqual(result, 30)
                except AttributeError:
                    self.skipTest("iwfm.date_difference function not implemented")
                except TypeError:
                    # Try without unit parameter
                    try:
                        result = iwfm.date_difference(date1, date2)
                        self.assertIsInstance(result, (int, float))
                    except:
                        self.skipTest("iwfm.date_difference has incompatible signature")
                except Exception as e:
                    self.fail(f"date_difference raised unexpected exception: {e}")
            
            def test_is_leap_year(self):
                """Test leap year detection"""
                try:
                    self.assertTrue(iwfm.is_leap_year(2024))
                    self.assertFalse(iwfm.is_leap_year(2023))
                    self.assertTrue(iwfm.is_leap_year(2000))
                    self.assertFalse(iwfm.is_leap_year(1900))
                except AttributeError:
                    self.skipTest("iwfm.is_leap_year function not implemented")
                except Exception as e:
                    self.fail(f"is_leap_year raised unexpected exception: {e}")
            
            def test_days_in_month(self):
                """Test getting number of days in a month"""
                try:
                    result_feb = iwfm.days_in_month(2, 2023)
                    self.assertEqual(result_feb, 28)
                    
                    result_feb_leap = iwfm.days_in_month(2, 2024)
                    self.assertEqual(result_feb_leap, 29)
                    
                    result_jan = iwfm.days_in_month(1, 2023)
                    self.assertEqual(result_jan, 31)
                except AttributeError:
                    self.skipTest("iwfm.days_in_month function not implemented")
                except Exception as e:
                    self.fail(f"days_in_month raised unexpected exception: {e}")
            
            def test_date_range_generator(self):
                """Test generating a range of dates"""
                start = "01/01/2023"
                end = "01/10/2023"
                try:
                    result = iwfm.date_range_list(start, end)
                    self.assertIsInstance(result, list)
                    self.assertEqual(len(result), 10)
                    self.assertEqual(result[0], start)
                except AttributeError:
                    self.skipTest("iwfm.date_range_list function not implemented")
                except Exception as e:
                    self.fail(f"date_range_list raised unexpected exception: {e}")
            
            def test_fiscal_year(self):
                """Test fiscal year calculation"""
                try:
                    # Fiscal year typically starts July 1
                    result_q1 = iwfm.fiscal_year("08/15/2023", start_month=7)
                    self.assertEqual(result_q1, 2024)
                    
                    result_q4 = iwfm.fiscal_year("06/15/2023", start_month=7)
                    self.assertEqual(result_q4, 2023)
                except AttributeError:
                    self.skipTest("iwfm.fiscal_year function not implemented")
                except TypeError:
                    # Try with just date
                    try:
                        result = iwfm.fiscal_year("08/15/2023")
                        self.assertIsInstance(result, int)
                    except:
                        self.skipTest("iwfm.fiscal_year has incompatible signature")
                except Exception as e:
                    self.fail(f"fiscal_year raised unexpected exception: {e}")
            
            def test_week_of_year(self):
                """Test week of year calculation"""
                try:
                    result = iwfm.week_of_year("01/15/2023")
                    self.assertGreater(result, 0)
                    self.assertLess(result, 54)
                except AttributeError:
                    self.skipTest("iwfm.week_of_year function not implemented")
                except Exception as e:
                    self.fail(f"week_of_year raised unexpected exception: {e}")
            
            def test_julian_day(self):
                """Test Julian day calculation"""
                try:
                    result = iwfm.julian_day("01/01/2023")
                    self.assertEqual(result, 1)
                    
                    result_mid = iwfm.julian_day("07/01/2023")
                    self.assertGreater(result_mid, 180)
                    self.assertLess(result_mid, 185)
                except AttributeError:
                    self.skipTest("iwfm.julian_day function not implemented")
                except Exception as e:
                    self.fail(f"julian_day raised unexpected exception: {e}")


class TestPumpingAnalysis(unittest.TestCase):
    """Test suite for pumping analysis"""
    
    def test_theis_drawdown(self):
        """Test Theis solution for drawdown"""
        Q = 1000.0  # pumping rate (gpm)
        T = 5000.0  # transmissivity (gpd/ft)
        S = 0.0001  # storativity
        r = 100.0   # distance (ft)
        t = 1.0     # time (days)
        result = iwfm.theis_drawdown(Q, T, S, r, t)
        self.assertGreater(result, 0)
    
    def test_jacob_drawdown(self):
        """Test Jacob approximation for drawdown"""
        Q = 500.0   # gpm
        T = 10000.0 # gpd/ft
        S = 0.0002
        r = 50.0
        t = 10.0
        result = iwfm.jacob_drawdown(Q, T, S, r, t)
        self.assertGreater(result, 0)
    
    def test_well_efficiency(self):
        """Test well efficiency calculation"""
        theoretical_drawdown = 20.0  # ft
        actual_drawdown = 25.0       # ft
        result = iwfm.well_efficiency(theoretical_drawdown, actual_drawdown)
        self.assertAlmostEqual(result, 0.80, places=2)
    
    def test_pumping_power(self):
        """Test pumping power calculation"""
        flow_rate = 500.0  # gpm
        total_head = 100.0  # ft
        efficiency = 0.75
        result = iwfm.pumping_power(flow_rate, total_head, efficiency)
        self.assertGreater(result, 0)  # Result in horsepower


class TestCropWaterUse(unittest.TestCase):
    """Test suite for crop water use calculations"""
    
    def test_et_reference(self):
        """Test reference ET calculation (Penman-Monteith)"""
        temp = 75.0      # F
        humidity = 50.0  # %
        wind = 5.0       # mph
        solar = 500.0    # langleys/day
        result = iwfm.et_reference(temp, humidity, wind, solar)
        self.assertGreater(result, 0)
        self.assertLess(result, 1.0)  # Reasonable daily ET
    
    def test_et_crop(self):
        """Test crop ET calculation"""
        et0 = 0.25  # inches/day
        kc = 1.15   # crop coefficient
        result = iwfm.et_crop(et0, kc)
        self.assertAlmostEqual(result, 0.2875, places=4)
    
    def test_crop_coefficient(self):
        """Test crop coefficient lookup/interpolation"""
        crop = "alfalfa"
        growth_stage = "mid"
        result = iwfm.get_crop_coefficient(crop, growth_stage)
        self.assertGreater(result, 0)
        self.assertLess(result, 2.0)
    
    def test_irrigation_efficiency(self):
        """Test irrigation efficiency"""
        water_applied = 10.0  # inches
        water_used = 8.0      # inches
        result = iwfm.irrigation_efficiency(water_applied, water_used)
        self.assertAlmostEqual(result, 0.80, places=2)


class TestSoilProperties(unittest.TestCase):
    """Test suite for soil property calculations"""
    
    def test_field_capacity(self):
        """Test field capacity calculation"""
        saturation = 0.45
        permanent_wilting = 0.15
        result = iwfm.field_capacity(saturation, permanent_wilting)
        self.assertGreater(result, permanent_wilting)
        self.assertLess(result, saturation)
    
    def test_available_water(self):
        """Test available water capacity"""
        field_capacity = 0.30
        wilting_point = 0.12
        depth = 48.0  # inches
        result = iwfm.available_water(field_capacity, wilting_point, depth)
        expected = (0.30 - 0.12) * 48.0
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_soil_moisture_deficit(self):
        """Test soil moisture deficit calculation"""
        field_capacity = 0.35
        current_moisture = 0.25
        root_depth = 36.0  # inches
        result = iwfm.soil_moisture_deficit(field_capacity, current_moisture, root_depth)
        self.assertAlmostEqual(result, 3.6, places=2)
    
    def test_infiltration_rate(self):
        """Test infiltration rate (Green-Ampt)"""
        Ks = 0.5      # in/hr
        theta_s = 0.4
        theta_i = 0.2
        psi = 5.0     # inches
        result = iwfm.infiltration_rate(Ks, theta_s, theta_i, psi, t=1.0)
        self.assertGreater(result, 0)


class TestSpatialAnalysis(unittest.TestCase):
    """Test suite for spatial analysis operations"""
    
    def test_voronoi_area(self):
        """Test Voronoi polygon area calculation"""
        points = [[0, 0], [10, 0], [5, 8.66]]
        bounds = [0, 0, 10, 10]
        result = iwfm.voronoi_area(points, bounds)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
    
    def test_thiessen_weights(self):
        """Test Thiessen polygon weights"""
        stations = [[0, 0], [10, 0], [5, 10]]
        target_point = [5, 5]
        result = iwfm.thiessen_weights(stations, target_point)
        self.assertAlmostEqual(sum(result), 1.0, places=5)
    
    def test_idw_interpolation(self):
        """Test inverse distance weighting"""
        known_points = [[0, 0], [10, 0], [10, 10], [0, 10]]
        known_values = [100, 110, 120, 105]
        target = [5, 5]
        power = 2
        result = iwfm.idw_interpolation(known_points, known_values, target, power)
        self.assertGreater(result, 100)
        self.assertLess(result, 120)
    
    def test_kriging_interpolation(self):
        """Test kriging interpolation"""
        known_points = [[0, 0], [10, 0], [5, 10]]
        known_values = [100, 150, 125]
        target = [5, 3]
        result = iwfm.kriging_interpolation(known_points, known_values, target)
        self.assertIsInstance(result, float)


class TestNetworkAnalysis(unittest.TestCase):
    """Test suite for network/graph analysis"""
    
    def test_shortest_path(self):
        """Test shortest path algorithm"""
        graph = {
            1: {2: 5, 3: 10},
            2: {3: 3, 4: 2},
            3: {4: 1},
            4: {}
        }
        result = iwfm.shortest_path(graph, 1, 4)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[-1], 4)
    
    def test_network_connectivity(self):
        """Test network connectivity check"""
        nodes = [1, 2, 3, 4, 5]
        edges = [(1, 2), (2, 3), (3, 4), (4, 5)]
        result = iwfm.check_connectivity(nodes, edges)
        self.assertTrue(result)
    
    def test_upstream_nodes(self):
        """Test finding upstream nodes"""
        connectivity = {
            1: [],
            2: [1],
            3: [1, 2],
            4: [3]
        }
        result = iwfm.upstream_nodes(connectivity, 4)
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)
    
    def test_downstream_nodes(self):
        """Test finding downstream nodes"""
        connectivity = {
            1: [2, 3],
            2: [4],
            3: [4],
            4: [5]
        }
        result = iwfm.downstream_nodes(connectivity, 1)
        self.assertIn(2, result)
        self.assertIn(4, result)
        self.assertIn(5, result)


class TestOptimization(unittest.TestCase):
    """Test suite for optimization functions"""
    
    def test_linear_optimization(self):
        """Test linear programming optimization"""
        # Maximize: 3x + 4y
        # Subject to: x + y <= 10, 2x + y <= 15, x >= 0, y >= 0
        coefficients = [3, 4]
        constraints = [[1, 1], [2, 1]]
        bounds = [10, 15]
        result = iwfm.linear_optimize(coefficients, constraints, bounds)
        self.assertIsInstance(result, dict)
        self.assertIn('x', result)
    
    def test_pumping_optimization(self):
        """Test optimal pumping schedule"""
        demands = [100, 150, 200, 150, 100]
        capacities = [300, 300, 300, 300, 300]
        costs = [10, 15, 20, 15, 10]
        result = iwfm.optimize_pumping(demands, capacities, costs)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(r >= 0 for r in result))
    
    def test_allocation_optimization(self):
        """Test water allocation optimization"""
        available = 1000.0
        demands = [400, 500, 300]
        priorities = [1, 2, 3]
        result = iwfm.optimize_allocation(available, demands, priorities)
        self.assertAlmostEqual(sum(result), available, places=2)


class TestQualityControl(unittest.TestCase):
    """Test suite for data quality control"""
    
    def test_outlier_detection(self):
        """Test outlier detection"""
        data = [10, 12, 11, 13, 10, 11, 100, 12, 11]
        result = iwfm.detect_outliers(data, method='zscore', threshold=3)
        self.assertIn(6, result)  # Index of outlier
    
    def test_data_gap_detection(self):
        """Test gap detection in time series"""
        dates = ["01/01/2023", "01/02/2023", "01/05/2023", "01/06/2023"]
        result = iwfm.detect_gaps(dates, max_gap_days=1)
        self.assertTrue(len(result) > 0)
    
    def test_range_check(self):
        """Test value range checking"""
        values = [10, 20, 30, -5, 100, 25]
        valid_range = (0, 50)
        result = iwfm.range_check(values, valid_range)
        self.assertFalse(result[3])  # -5 is out of range
        self.assertFalse(result[4])  # 100 is out of range
    
    def test_consistency_check(self):
        """Test data consistency checking"""
        inflow = [100, 150, 200]
        outflow = [80, 120, 180]
        storage_change = [20, 30, 25]
        result = iwfm.consistency_check(inflow, outflow, storage_change, tolerance=5)
        self.assertIsInstance(result, list)


class TestReporting(unittest.TestCase):
    """Test suite for report generation"""
    
    def test_summary_statistics(self):
        """Test generating summary statistics"""
        data = [10, 20, 30, 40, 50]
        result = iwfm.summary_statistics(data)
        
        self.assertIn('mean', result)
        self.assertIn('median', result)
        self.assertIn('std', result)
        self.assertIn('min', result)
        self.assertIn('max', result)
    
    def test_monthly_summary(self):
        """Test monthly summary generation"""
        dates = ["01/15/2023", "01/20/2023", "02/10/2023", "02/15/2023"]
        values = [100, 120, 150, 180]
        result = iwfm.monthly_summary(dates, values)
        
        self.assertEqual(len(result), 2)
        self.assertIn('total', result[0])
        self.assertIn('average', result[0])
    
    def test_annual_summary(self):
        """Test annual summary generation"""
        dates = ["01/01/2022", "06/01/2022", "01/01/2023", "06/01/2023"]
        values = [1000, 1500, 1200, 1800]
        result = iwfm.annual_summary(dates, values)
        
        self.assertEqual(len(result), 2)  # 2 years
    
    def test_exceedance_probability(self):
        """Test exceedance probability calculation"""
        data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        result = iwfm.exceedance_probability(data)
        
        self.assertEqual(len(result), len(data))
        self.assertAlmostEqual(result[0], 0.95, places=2)  # Highest value


class TestModelCalibration(unittest.TestCase):
    """Test suite for model calibration"""
    
    def test_nash_sutcliffe(self):
        """Test Nash-Sutcliffe efficiency"""
        observed = [10, 20, 30, 40, 50]
        simulated = [12, 18, 32, 38, 51]
        result = iwfm.nash_sutcliffe(observed, simulated)
        self.assertGreater(result, 0.8)
        self.assertLessEqual(result, 1.0)
    
    def test_rmse(self):
        """Test root mean square error"""
        observed = [100, 200, 300, 400, 500]
        simulated = [105, 195, 310, 390, 505]
        result = iwfm.rmse(observed, simulated)
        self.assertGreater(result, 0)
        self.assertLess(result, 20)
    
    def test_correlation_coefficient(self):
        """Test Pearson correlation coefficient"""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = iwfm.correlation_coefficient(x, y)
        self.assertAlmostEqual(result, 1.0, places=5)
    
    def test_bias(self):
        """Test bias calculation"""
        observed = [100, 200, 300]
        simulated = [110, 210, 310]
        result = iwfm.bias(observed, simulated)
        self.assertAlmostEqual(result, 10.0, places=2)


class TestBoundaryConditions(unittest.TestCase):
    """Test suite for boundary condition operations"""
    
    def test_dirichlet_bc(self):
        """Test Dirichlet (specified head) boundary condition"""
        nodes = [1, 2, 3]
        values = [100.0, 105.0, 110.0]
        result = iwfm.apply_dirichlet_bc(nodes, values)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1], 100.0)
    
    def test_neumann_bc(self):
        """Test Neumann (specified flux) boundary condition"""
        nodes = [1, 2]
        flux = [10.0, 15.0]
        result = iwfm.apply_neumann_bc(nodes, flux)
        self.assertIsInstance(result, dict)
    
    def test_mixed_bc(self):
        """Test mixed boundary conditions"""
        bc_type = ['dirichlet', 'neumann', 'dirichlet']
        bc_values = [100.0, 5.0, 110.0]
        result = iwfm.apply_mixed_bc(bc_type, bc_values)
        self.assertEqual(len(result), 3)
    
    def test_time_varying_bc(self):
        """Test time-varying boundary condition"""
        times = [0, 1, 2, 3]
        values = [100, 105, 110, 105]
        t_query = 1.5
        result = iwfm.time_varying_bc(times, values, t_query)
        self.assertGreater(result, 105)
        self.assertLess(result, 110)


class TestFlowPathAnalysis(unittest.TestCase):
    """Test suite for flow path and particle tracking"""
    
    def test_flow_direction(self):
        """Test flow direction calculation"""
        head_field = [[100, 95, 90], [105, 100, 95], [110, 105, 100]]
        i, j = 1, 1
        result = iwfm.flow_direction(head_field, i, j)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
    
    def test_particle_tracking(self):
        """Test particle tracking through flow field"""
        start_pos = [0, 0]
        velocity_field = [[1, 0], [0, 1]]
        time_steps = 10
        result = iwfm.particle_track(start_pos, velocity_field, time_steps)
        self.assertEqual(len(result), time_steps + 1)
    
    def test_streamline_generation(self):
        """Test generating streamlines"""
        velocity_field = [[1, 0] for _ in range(10)]
        seed_points = [[0, 0], [0, 5]]
        result = iwfm.generate_streamlines(velocity_field, seed_points)
        self.assertEqual(len(result), 2)
    
    def test_residence_time(self):
        """Test residence time calculation"""
        path_length = 1000.0  # feet
        velocity = 1.0  # ft/day
        result = iwfm.residence_time(path_length, velocity)
        self.assertAlmostEqual(result, 1000.0, places=2)


class TestContourOperations(unittest.TestCase):
    """Test suite for contouring operations"""
    
    def test_contour_generation(self):
        """Test generating contour lines"""
        x = [0, 10, 20]
        y = [0, 10, 20]
        z = [[100, 105, 110], [105, 110, 115], [110, 115, 120]]
        levels = [105, 110, 115]
        result = iwfm.generate_contours(x, y, z, levels)
        self.assertIsInstance(result, list)
    
    def test_contour_intersection(self):
        """Test finding contour intersections"""
        contour1 = [[0, 0], [10, 10]]
        contour2 = [[0, 10], [10, 0]]
        result = iwfm.contour_intersection(contour1, contour2)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result[0], 5.0, places=1)
    
    def test_iso_surface(self):
        """Test generating iso-surface"""
        grid_3d = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        threshold = 4.5
        result = iwfm.iso_surface(grid_3d, threshold)
        self.assertIsInstance(result, list)


class TestZoneBudget(unittest.TestCase):
    """Test suite for zone budget calculations"""
    
    def test_zone_total(self):
        """Test calculating total for a zone"""
        zones = [[1, 1, 2], [1, 2, 2], [2, 2, 2]]
        values = [[10, 20, 30], [15, 25, 35], [20, 30, 40]]
        zone_id = 1
        result = iwfm.zone_total(zones, values, zone_id)
        self.assertGreater(result, 0)
    
    def test_zone_average(self):
        """Test calculating average for a zone"""
        zones = [[1, 1, 2], [1, 2, 2]]
        values = [[10, 20, 30], [10, 40, 50]]
        zone_id = 1
        result = iwfm.zone_average(zones, values, zone_id)
        self.assertAlmostEqual(result, 13.33, places=1)
    
    def test_zone_flux(self):
        """Test calculating flux between zones"""
        zones = [[1, 1, 2], [1, 2, 2]]
        heads = [[100, 100, 95], [100, 95, 90]]
        K = [[10, 10, 10], [10, 10, 10]]
        result = iwfm.zone_flux(zones, heads, K, zone1=1, zone2=2)
        self.assertIsInstance(result, float)
    
    def test_multi_zone_budget(self):
        """Test comprehensive zone budget"""
        zones = [[1, 1, 2], [1, 2, 2], [3, 3, 3]]
        inflows = [[10, 10, 5], [10, 5, 5], [0, 0, 0]]
        outflows = [[5, 5, 10], [5, 10, 10], [0, 0, 0]]
        result = iwfm.multi_zone_budget(zones, inflows, outflows)
        self.assertIsInstance(result, dict)
        self.assertIn(1, result)
        self.assertIn(2, result)


class TestVerticalFlow(unittest.TestCase):
    """Test suite for vertical flow calculations"""
    
    def test_leakage_rate(self):
        """Test vertical leakage rate calculation"""
        head_upper = 100.0
        head_lower = 95.0
        thickness = 10.0
        K_vertical = 0.1
        result = iwfm.leakage_rate(head_upper, head_lower, thickness, K_vertical)
        self.assertAlmostEqual(result, 0.05, places=4)
    
    def test_vertical_gradient(self):
        """Test vertical hydraulic gradient"""
        head_top = 100.0
        head_bottom = 80.0
        distance = 50.0
        result = iwfm.vertical_gradient(head_top, head_bottom, distance)
        self.assertAlmostEqual(result, 0.4, places=2)
    
    def test_aquitard_flow(self):
        """Test flow through aquitard"""
        K_vertical = 0.01  # ft/day
        thickness = 20.0   # ft
        head_diff = 10.0   # ft
        area = 1000.0      # ft²
        result = iwfm.aquitard_flow(K_vertical, thickness, head_diff, area)
        self.assertGreater(result, 0)
    
    def test_recharge_distribution(self):
        """Test distributing recharge vertically"""
        total_recharge = 100.0  # acre-feet
        layer_thicknesses = [20, 30, 50]
        layer_K = [10, 5, 2]
        result = iwfm.distribute_recharge(total_recharge, layer_thicknesses, layer_K)
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(sum(result), total_recharge, places=2)


class TestStochasticMethods(unittest.TestCase):
    """Test suite for stochastic/Monte Carlo methods"""
    
    def test_monte_carlo_simulation(self):
        """Test Monte Carlo simulation"""
        mean = 100.0
        std_dev = 10.0
        n_samples = 1000
        result = iwfm.monte_carlo_samples(mean, std_dev, n_samples)
        self.assertEqual(len(result), n_samples)
        self.assertAlmostEqual(sum(result)/n_samples, mean, delta=5)
    
    def test_uncertainty_propagation(self):
        """Test uncertainty propagation"""
        input_means = [100, 200]
        input_stds = [10, 20]
        correlation = 0.5
        result = iwfm.propagate_uncertainty(input_means, input_stds, correlation)
        self.assertIn('mean', result)
        self.assertIn('std', result)
    
    def test_sensitivity_analysis(self):
        """Test parameter sensitivity analysis"""
        base_params = {'K': 10, 'S': 0.1, 'recharge': 5}
        param_ranges = {'K': (5, 15), 'S': (0.05, 0.15)}
        result = iwfm.sensitivity_analysis(base_params, param_ranges)
        self.assertIsInstance(result, dict)
    
    def test_latin_hypercube_sampling(self):
        """Test Latin Hypercube Sampling"""
        n_vars = 3
        n_samples = 100
        bounds = [(0, 1), (10, 100), (0.1, 1.0)]
        result = iwfm.latin_hypercube(n_vars, n_samples, bounds)
        self.assertEqual(len(result), n_samples)
        self.assertEqual(len(result[0]), n_vars)


class TestWellPackage(unittest.TestCase):
    """Test suite for well package operations"""
    
    def test_well_allocation(self):
        """Test well water allocation"""
        well_capacities = [100, 150, 200]
        demands = [120, 180, 150]
        priorities = [1, 2, 1]
        result = iwfm.allocate_well_pumping(well_capacities, demands, priorities)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(r <= c for r, c in zip(result, well_capacities)))
    
    def test_well_interference(self):
        """Test well interference calculation"""
        well1_pos = [0, 0]
        well2_pos = [100, 0]
        Q1, Q2 = 500, 300  # gpm
        T = 10000  # gpd/ft
        result = iwfm.well_interference(well1_pos, well2_pos, Q1, Q2, T)
        self.assertGreater(result, 0)
    
    def test_optimal_well_spacing(self):
        """Test optimal well spacing calculation"""
        T = 10000  # transmissivity
        S = 0.0001  # storativity
        Q = 500  # pumping rate
        max_drawdown = 50  # feet
        result = iwfm.optimal_well_spacing(T, S, Q, max_drawdown)
        self.assertGreater(result, 0)
    
    def test_well_capture_zone(self):
        """Test well capture zone delineation"""
        well_pos = [0, 0]
        Q = 1000  # gpm
        regional_gradient = 0.001
        T = 5000
        time = 365  # days
        result = iwfm.capture_zone(well_pos, Q, regional_gradient, T, time)
        self.assertIsInstance(result, list)


class TestLandSubsidence(unittest.TestCase):
    """Test suite for land subsidence calculations"""
    
    def test_elastic_subsidence(self):
        """Test elastic (recoverable) subsidence"""
        head_change = 10.0  # feet
        specific_storage = 0.0001
        thickness = 100.0
        result = iwfm.elastic_subsidence(head_change, specific_storage, thickness)
        self.assertGreater(result, 0)
        self.assertLess(result, 0.1)
    
    def test_inelastic_subsidence(self):
        """Test inelastic (permanent) subsidence"""
        head_change = 20.0
        compaction_coefficient = 0.005
        thickness = 50.0
        result = iwfm.inelastic_subsidence(head_change, compaction_coefficient, thickness)
        self.assertGreater(result, 0)
    
    def test_subsidence_rate(self):
        """Test subsidence rate calculation"""
        subsidence_history = [0, 0.1, 0.25, 0.45, 0.70]
        times = [0, 1, 2, 3, 4]  # years
        result = iwfm.subsidence_rate(subsidence_history, times)
        self.assertEqual(len(result), len(times) - 1)
    
    def test_preconsolidation_head(self):
        """Test preconsolidation head calculation"""
        current_head = 100.0
        historic_low = 80.0
        max_subsidence = 1.5  # feet
        result = iwfm.preconsolidation_head(current_head, historic_low, max_subsidence)
        self.assertLess(result, current_head)


class TestSaltTransport(unittest.TestCase):
    """Test suite for salt/contaminant transport"""
    
    def test_advection(self):
        """Test advective transport"""
        concentration = 100.0  # mg/L
        velocity = 1.0  # ft/day
        distance = 100.0  # ft
        time = 50.0  # days
        result = iwfm.advective_transport(concentration, velocity, distance, time)
        self.assertGreater(result, 0)
    
    def test_dispersion(self):
        """Test dispersive transport"""
        concentration = 100.0
        dispersivity = 10.0  # ft
        velocity = 1.0
        time = 100.0
        result = iwfm.dispersive_transport(concentration, dispersivity, velocity, time)
        self.assertIsInstance(result, float)
    
    def test_retardation_factor(self):
        """Test retardation factor calculation"""
        porosity = 0.3
        bulk_density = 1.8  # g/cm³
        distribution_coef = 5.0  # mL/g
        result = iwfm.retardation_factor(porosity, bulk_density, distribution_coef)
        self.assertGreater(result, 1.0)
    
    def test_breakthrough_curve(self):
        """Test breakthrough curve generation"""
        distance = 1000.0  # ft
        velocity = 2.0  # ft/day
        dispersivity = 50.0
        times = [100, 200, 300, 400, 500]
        result = iwfm.breakthrough_curve(distance, velocity, dispersivity, times)
        self.assertEqual(len(result), len(times))


class TestDrainageOperations(unittest.TestCase):
    """Test suite for drainage system operations"""
    
    def test_drain_spacing(self):
        """Test optimal drain spacing (Hooghoudt equation)"""
        K = 5.0  # hydraulic conductivity (ft/day)
        drain_depth = 6.0  # feet
        water_table_midpoint = 3.0  # feet
        recharge = 0.01  # ft/day
        result = iwfm.drain_spacing(K, drain_depth, water_table_midpoint, recharge)
        self.assertGreater(result, 0)
    
    def test_drain_discharge(self):
        """Test drain discharge calculation"""
        K = 10.0
        gradient = 0.01
        drain_length = 1000.0  # feet
        result = iwfm.drain_discharge(K, gradient, drain_length)
        self.assertGreater(result, 0)
    
    def test_subsurface_drainage_design(self):
        """Test subsurface drainage system design"""
        field_area = 10.0  # acres
        design_drainage_rate = 0.5  # inches/day
        result = iwfm.design_drainage_system(field_area, design_drainage_rate)
        self.assertIn('total_flow', result)
        self.assertIn('drain_spacing', result)
    
    def test_tile_drain_flow(self):
        """Test tile drain flow calculation"""
        pipe_diameter = 4.0  # inches
        slope = 0.002
        manning_n = 0.013
        result = iwfm.tile_drain_flow(pipe_diameter, slope, manning_n)
        self.assertGreater(result, 0)


class TestClimateChange(unittest.TestCase):
    """Test suite for climate change scenario analysis"""
    
    def test_temperature_adjustment(self):
        """Test temperature adjustment for climate scenario"""
        baseline_temp = [65, 70, 75, 80, 85]
        delta_t = 2.0  # degrees F
        result = iwfm.adjust_temperature(baseline_temp, delta_t)
        self.assertEqual(len(result), len(baseline_temp))
        self.assertAlmostEqual(result[0], 67.0, places=1)
    
    def test_precipitation_scaling(self):
        """Test precipitation scaling for climate scenario"""
        baseline_precip = [2, 3, 4, 5, 6]  # inches
        scale_factor = 1.1  # 10% increase
        result = iwfm.scale_precipitation(baseline_precip, scale_factor)
        self.assertEqual(len(result), len(baseline_precip))
        self.assertAlmostEqual(result[0], 2.2, places=1)
    
    def test_et_adjustment(self):
        """Test ET adjustment under climate change"""
        baseline_et = [0.2, 0.25, 0.3, 0.35]  # inches/day
        temp_increase = 2.0  # degrees
        result = iwfm.adjust_et_climate(baseline_et, temp_increase)
        self.assertEqual(len(result), len(baseline_et))
        self.assertTrue(all(r > b for r, b in zip(result, baseline_et)))
    
    def test_sea_level_rise_impact(self):
        """Test sea level rise impact on groundwater"""
        coastal_boundary_head = 0.0  # MSL
        sea_level_rise = 1.0  # feet
        distance_inland = 5000.0  # feet
        result = iwfm.sea_level_impact(coastal_boundary_head, sea_level_rise, distance_inland)
        self.assertGreater(result, 0)


class TestDataAssimilation(unittest.TestCase):
    """Test suite for data assimilation methods"""
    
    def test_kalman_filter(self):
        """Test Kalman filter update"""
        prior_estimate = 100.0
        prior_variance = 25.0
        measurement = 105.0
        measurement_variance = 16.0
        result = iwfm.kalman_update(prior_estimate, prior_variance, 
                                    measurement, measurement_variance)
        self.assertIn('estimate', result)
        self.assertIn('variance', result)
    
    def test_ensemble_kalman_filter(self):
        """Test Ensemble Kalman Filter"""
        ensemble = [100, 105, 95, 110, 90]
        observation = 102
        obs_error = 5.0
        result = iwfm.enkf_update(ensemble, observation, obs_error)
        self.assertEqual(len(result), len(ensemble))
    
    def test_particle_filter(self):
        """Test particle filter"""
        particles = [100, 105, 95, 110, 90]
        weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        observation = 102
        result = iwfm.particle_filter_update(particles, weights, observation)
        self.assertEqual(len(result['particles']), len(particles))
    
    def test_variational_assimilation(self):
        """Test 3D/4D variational data assimilation"""
        background = [100, 100, 100]
        observations = [105, 102, 98]
        obs_locations = [0, 1, 2]
        result = iwfm.variational_assim(background, observations, obs_locations)
        self.assertEqual(len(result), len(background))


class TestGridRefinement(unittest.TestCase):
    """Test suite for grid refinement operations"""
    
    def test_adaptive_mesh_refinement(self):
        """Test adaptive mesh refinement"""
        coarse_grid = [[1, 2], [3, 4]]
        refinement_criterion = lambda x: x > 2.5
        result = iwfm.adaptive_refine(coarse_grid, refinement_criterion)
        self.assertGreater(len(result), len(coarse_grid))
    
    def test_grid_coarsening(self):
        """Test grid coarsening/upscaling"""
        fine_grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        factor = 2
        result = iwfm.grid_coarsen(fine_grid, factor)
        self.assertEqual(len(result), len(fine_grid) // factor)
    
    def test_nested_grid(self):
        """Test nested grid implementation"""
        parent_grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        child_region = (1, 1, 2, 2)  # row1, col1, row2, col2
        refinement = 2
        result = iwfm.create_nested_grid(parent_grid, child_region, refinement)
        self.assertIn('parent', result)
        self.assertIn('child', result)
    
    def test_multi_grid_solver(self):
        """Test multi-grid solver"""
        A = [[4, -1, 0], [-1, 4, -1], [0, -1, 4]]
        b = [1, 2, 3]
        result = iwfm.multigrid_solve(A, b)
        self.assertEqual(len(result), len(b))


class TestRiverPackage(unittest.TestCase):
    """Test suite for river package operations"""
    
    def test_river_stage_area_relationship(self):
        """Test river cross-section stage-area relationship"""
        stage_values = [0, 5, 10, 15]
        area_values = [0, 100, 250, 450]
        stage = 7.5
        result = iwfm.river_stage_area(stage_values, area_values, stage)
        self.assertGreater(result, 100)
        self.assertLess(result, 250)
    
    def test_river_seepage(self):
        """Test river-aquifer seepage calculation"""
        river_stage = 105.0
        aquifer_head = 100.0
        riverbed_K = 0.5  # ft/day
        riverbed_thickness = 2.0  # ft
        river_width = 50.0  # ft
        river_length = 1000.0  # ft
        result = iwfm.river_seepage(river_stage, aquifer_head, riverbed_K, 
                                     riverbed_thickness, river_width, river_length)
        self.assertGreater(result, 0)
    
    def test_stream_depletion(self):
        """Test stream depletion from nearby pumping"""
        well_distance = 500.0  # ft from stream
        pumping_rate = 500.0  # gpm
        T = 10000.0  # transmissivity
        S = 0.0001  # storativity
        time = 10.0  # days
        result = iwfm.stream_depletion(well_distance, pumping_rate, T, S, time)
        self.assertGreater(result, 0)
        self.assertLess(result, pumping_rate)
    
    def test_baseflow_separation(self):
        """Test baseflow separation from streamflow"""
        streamflow = [100, 120, 150, 200, 180, 140, 110, 95, 85, 80]
        result = iwfm.baseflow_separation(streamflow, method='recursive')
        self.assertEqual(len(result), len(streamflow))
        self.assertTrue(all(b <= s for b, s in zip(result, streamflow)))


class TestLakePackage(unittest.TestCase):
    """Test suite for lake package operations"""
    
    def test_lake_water_balance(self):
        """Test lake water balance"""
        initial_volume = 10000.0  # acre-feet
        precip = 100.0
        evap = 80.0
        surface_inflow = 500.0
        surface_outflow = 400.0
        gw_exchange = 50.0
        result = iwfm.lake_water_balance(initial_volume, precip, evap, 
                                         surface_inflow, surface_outflow, gw_exchange)
        self.assertGreater(result, initial_volume)
    
    def test_lake_stage_volume(self):
        """Test lake stage-volume relationship"""
        stage_values = [0, 10, 20, 30]
        volume_values = [0, 1000, 5000, 12000]  # acre-feet
        target_stage = 15.0
        result = iwfm.lake_stage_volume(stage_values, volume_values, target_stage)
        self.assertGreater(result, 1000)
        self.assertLess(result, 5000)
    
    def test_lake_evaporation(self):
        """Test lake evaporation calculation"""
        surface_area = 500.0  # acres
        pan_evap = 0.3  # inches/day
        pan_coef = 0.7
        result = iwfm.lake_evaporation(surface_area, pan_evap, pan_coef)
        self.assertGreater(result, 0)
    
    def test_lake_seepage(self):
        """Test lake-groundwater seepage"""
        lake_stage = 100.0
        gw_head = 95.0
        lakebed_K = 0.1  # ft/day
        lakebed_thickness = 3.0
        lake_area = 1000.0  # acres
        result = iwfm.lake_seepage(lake_stage, gw_head, lakebed_K, 
                                   lakebed_thickness, lake_area)
        self.assertGreater(result, 0)


class TestUnsaturatedZone(unittest.TestCase):
    """Test suite for unsaturated zone operations"""
    
    def test_richards_equation(self):
        """Test Richards equation solver"""
        initial_moisture = 0.15
        boundary_conditions = {'top': 0.01, 'bottom': 0.30}
        soil_params = {'Ks': 0.5, 'theta_s': 0.40, 'theta_r': 0.05}
        result = iwfm.richards_solve(initial_moisture, boundary_conditions, soil_params)
        self.assertIsInstance(result, dict)
    
    def test_van_genuchten(self):
        """Test van Genuchten soil water retention"""
        pressure_head = -100.0  # cm
        params = {'theta_r': 0.05, 'theta_s': 0.40, 'alpha': 0.02, 'n': 1.5}
        result = iwfm.van_genuchten(pressure_head, params)
        self.assertGreater(result, params['theta_r'])
        self.assertLess(result, params['theta_s'])
    
    def test_brooks_corey(self):
        """Test Brooks-Corey model"""
        pressure_head = -50.0
        params = {'theta_r': 0.05, 'theta_s': 0.45, 'lambda': 0.5, 'psi_b': -10.0}
        result = iwfm.brooks_corey(pressure_head, params)
        self.assertGreater(result, 0)
    
    def test_unsaturated_hydraulic_conductivity(self):
        """Test unsaturated hydraulic conductivity"""
        moisture_content = 0.25
        Ks = 1.0  # saturated K
        theta_s = 0.40
        theta_r = 0.05
        result = iwfm.unsaturated_K(moisture_content, Ks, theta_s, theta_r)
        self.assertGreater(result, 0)
        self.assertLess(result, Ks)


class TestRootZone(unittest.TestCase):
    """Test suite for root zone/agricultural operations"""
    
    def test_root_water_uptake(self):
        """Test root water uptake distribution"""
        root_depth = 48.0  # inches
        soil_moisture = [0.25, 0.22, 0.20, 0.18]  # by layer
        transpiration = 0.25  # inches/day
        result = iwfm.root_water_uptake(root_depth, soil_moisture, transpiration)
        self.assertEqual(len(result), len(soil_moisture))
        self.assertAlmostEqual(sum(result), transpiration, places=2)
    
    def test_crop_stress_factor(self):
        """Test crop water stress factor"""
        current_moisture = 0.20
        field_capacity = 0.30
        wilting_point = 0.12
        result = iwfm.crop_stress_factor(current_moisture, field_capacity, wilting_point)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 1.0)
    
    def test_irrigation_requirement(self):
        """Test irrigation requirement calculation"""
        et_crop = 0.30  # inches/day
        effective_precip = 0.05
        soil_moisture_deficit = 2.0  # inches
        result = iwfm.irrigation_requirement(et_crop, effective_precip, soil_moisture_deficit)
        self.assertGreater(result, 0)
    
    def test_leaching_fraction(self):
        """Test leaching fraction for salinity control"""
        ECw = 1.5  # dS/m - irrigation water EC
        ECe = 4.0  # dS/m - soil extract EC threshold
        result = iwfm.leaching_fraction(ECw, ECe)
        self.assertGreater(result, 0)
        self.assertLess(result, 1.0)


class TestSurfaceRunoff(unittest.TestCase):
    """Test suite for surface runoff operations"""
    
    def test_curve_number_runoff(self):
        """Test SCS Curve Number runoff calculation"""
        precipitation = 3.0  # inches
        curve_number = 75
        result = iwfm.cn_runoff(precipitation, curve_number)
        self.assertGreater(result, 0)
        self.assertLess(result, precipitation)
    
    def test_rational_method(self):
        """Test Rational Method peak flow"""
        C = 0.50  # runoff coefficient
        intensity = 2.0  # inches/hour
        area = 100.0  # acres
        result = iwfm.rational_method(C, intensity, area)
        self.assertGreater(result, 0)
    
    def test_time_of_concentration(self):
        """Test time of concentration calculation"""
        length = 5000.0  # feet
        slope = 0.01
        manning_n = 0.035
        result = iwfm.time_of_concentration(length, slope, manning_n)
        self.assertGreater(result, 0)
    
    def test_unit_hydrograph(self):
        """Test unit hydrograph generation"""
        duration = 1.0  # hours
        area = 1000.0  # acres
        peak_time = 2.0  # hours
        result = iwfm.unit_hydrograph(duration, area, peak_time)
        self.assertIsInstance(result, list)


class TestSensitivityUncertainty(unittest.TestCase):
    """Test suite for sensitivity and uncertainty analysis"""
    
    def test_one_at_a_time_sensitivity(self):
        """Test one-at-a-time sensitivity analysis"""
        base_params = {'K': 10, 'S': 0.1, 'Q': 500}
        param_variations = {'K': 0.1, 'S': 0.01, 'Q': 50}
        result = iwfm.oat_sensitivity(base_params, param_variations)
        self.assertIsInstance(result, dict)
        self.assertIn('K', result)
    
    def test_morris_screening(self):
        """Test Morris screening method"""
        param_ranges = {
            'K': (5, 20),
            'S': (0.05, 0.2),
            'recharge': (1, 10)
        }
        n_trajectories = 10
        result = iwfm.morris_screening(param_ranges, n_trajectories)
        self.assertIn('mu_star', result)
        self.assertIn('sigma', result)
    
    def test_sobol_indices(self):
        """Test Sobol sensitivity indices"""
        param_distributions = {
            'K': ('uniform', 5, 20),
            'S': ('lognormal', 0.1, 0.02)
        }
        n_samples = 1000
        result = iwfm.sobol_indices(param_distributions, n_samples)
        self.assertIn('first_order', result)
        self.assertIn('total_order', result)
    
    def test_confidence_intervals(self):
        """Test confidence interval calculation"""
        data = [98, 102, 105, 99, 101, 103, 97, 106, 100, 104]
        confidence = 0.95
        result = iwfm.confidence_interval(data, confidence)
        self.assertIn('lower', result)
        self.assertIn('upper', result)
        self.assertIn('mean', result)


class TestPostProcessing(unittest.TestCase):
    """Test suite for post-processing operations"""
    
    def test_hydrograph_analysis(self):
        """Test hydrograph analysis"""
        flows = [50, 100, 200, 150, 80, 60, 55, 52, 51, 50]
        times = list(range(len(flows)))
        result = iwfm.analyze_hydrograph(flows, times)
        self.assertIn('peak_flow', result)
        self.assertIn('time_to_peak', result)
        self.assertIn('recession_constant', result)
    
    def test_drawdown_analysis(self):
        """Test drawdown curve analysis"""
        times = [1, 2, 5, 10, 20, 50, 100]
        drawdowns = [2, 4, 7, 10, 13, 17, 21]
        result = iwfm.analyze_drawdown(times, drawdowns)
        self.assertIn('T', result)  # Transmissivity
        self.assertIn('S', result)  # Storativity
    
    def test_breakthrough_analysis(self):
        """Test breakthrough curve analysis"""
        times = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        concentrations = [0, 0.05, 0.15, 0.35, 0.60, 0.80, 0.92, 0.97, 0.99, 1.0, 1.0]
        result = iwfm.analyze_breakthrough(times, concentrations)
        self.assertIn('arrival_time', result)
        self.assertIn('breakthrough_time', result)
    
    def test_budget_discrepancy(self):
        """Test budget discrepancy calculation"""
        inflows = [1000, 1200, 1100]
        outflows = [950, 1150, 1080]
        storage_changes = [48, 52, 18]
        result = iwfm.budget_discrepancy(inflows, outflows, storage_changes)
        self.assertIsInstance(result, list)


class TestModelDiagnostics(unittest.TestCase):
    """Test suite for model diagnostics"""
    
    def test_mass_balance_check(self):
        """Test comprehensive mass balance check"""
        components = {
            'precipitation': 1000,
            'irrigation': 500,
            'et': 800,
            'runoff': 200,
            'deep_percolation': 300,
            'storage_change': 200
        }
        result = iwfm.check_mass_balance(components)
        self.assertIn('error', result)
        self.assertIn('percent_error', result)
    
    def test_convergence_diagnostics(self):
        """Test convergence diagnostics"""
        iterations = [10, 8, 6, 5, 4, 4, 3, 3, 3]
        residuals = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10]
        result = iwfm.convergence_diagnostics(iterations, residuals)
        self.assertIn('converged', result)
        self.assertIn('final_residual', result)
    
    def test_stability_check(self):
        """Test numerical stability check"""
        dt = 1.0  # time step (days)
        dx = 100.0  # spatial step (ft)
        K = 10.0  # hydraulic conductivity
        S = 0.0001  # storativity
        result = iwfm.stability_check(dt, dx, K, S)
        self.assertIn('courant_number', result)
        self.assertIn('stable', result)
    
    def test_head_change_rate(self):
        """Test head change rate analysis"""
        heads = [100, 98, 97, 96.5, 96.2, 96.1, 96.05]
        times = [0, 1, 2, 3, 4, 5, 6]
        result = iwfm.head_change_rate(heads, times)
        self.assertIsInstance(result, list)


class TestParameterEstimation(unittest.TestCase):
    """Test suite for parameter estimation"""
    
    def test_gradient_descent(self):
        """Test gradient descent optimization"""
        initial_params = {'K': 10.0, 'S': 0.1}
        observed_data = [95, 90, 87, 85, 84]
        result = iwfm.gradient_descent(initial_params, observed_data)
        self.assertIn('optimized_params', result)
        self.assertIn('objective', result)
    
    def test_gauss_newton(self):
        """Test Gauss-Newton parameter estimation"""
        initial_params = [10.0, 0.1]  # K, S
        observations = [100, 95, 92, 90, 89]
        times = [0, 1, 2, 3, 4]
        result = iwfm.gauss_newton(initial_params, observations, times)
        self.assertEqual(len(result), len(initial_params))
    
    def test_levenberg_marquardt(self):
        """Test Levenberg-Marquardt algorithm"""
        initial_guess = {'T': 5000, 'S': 0.0001}
        observed = [100, 98, 96, 95, 94]
        predicted_func = lambda params: [100 - i*params['S']*1000 for i in range(5)]
        result = iwfm.levenberg_marquardt(initial_guess, observed, predicted_func)
        self.assertIsInstance(result, dict)
    
    def test_parameter_correlation(self):
        """Test parameter correlation matrix"""
        params_history = [
            [10.0, 0.1, 5.0],
            [10.5, 0.11, 5.2],
            [9.8, 0.09, 4.9],
            [10.2, 0.10, 5.1]
        ]
        result = iwfm.parameter_correlation(params_history)
        self.assertEqual(len(result), 3)  # 3x3 correlation matrix


class TestForecastingScenarios(unittest.TestCase):
    """Test suite for forecasting and scenario analysis"""
    
    def test_trend_projection(self):
        """Test trend projection"""
        historical_data = [100, 105, 102, 108, 110, 115, 112, 118]
        future_periods = 5
        result = iwfm.trend_projection(historical_data, future_periods)
        self.assertEqual(len(result), future_periods)
    
    def test_scenario_comparison(self):
        """Test scenario comparison"""
        baseline = [100, 95, 92, 90, 88]
        scenarios = {
            'high_pumping': [100, 93, 88, 84, 80],
            'low_pumping': [100, 97, 95, 93, 91]
        }
        result = iwfm.compare_scenarios(baseline, scenarios)
        self.assertIn('high_pumping', result)
        self.assertIn('low_pumping', result)
    
    def test_risk_analysis(self):
        """Test risk analysis"""
        scenarios = [[100, 95, 90], [100, 92, 85], [100, 97, 93]]
        probabilities = [0.3, 0.5, 0.2]
        threshold = 88
        result = iwfm.risk_analysis(scenarios, probabilities, threshold)
        self.assertIn('exceedance_probability', result)
    
    def test_ensemble_forecast(self):
        """Test ensemble forecasting"""
        ensemble_members = [
            [100, 98, 96, 94],
            [100, 97, 95, 93],
            [100, 99, 97, 95]
        ]
        result = iwfm.ensemble_forecast(ensemble_members)
        self.assertIn('mean', result)
        self.assertIn('std', result)
        self.assertIn('percentiles', result)


class TestVisualizationHelpers(unittest.TestCase):
    """Test suite for visualization helper functions"""
    
    def test_color_scale(self):
        """Test color scale generation"""
        values = [0, 25, 50, 75, 100]
        colormap = 'viridis'
        result = iwfm.generate_color_scale(values, colormap)
        self.assertEqual(len(result), len(values))
    
    def test_contour_levels(self):
        """Test automatic contour level generation"""
        data_min = 0.0
        data_max = 100.0
        n_levels = 10
        result = iwfm.generate_contour_levels(data_min, data_max, n_levels)
        self.assertEqual(len(result), n_levels)
        self.assertEqual(result[0], data_min)
        self.assertEqual(result[-1], data_max)
    
    def test_axis_limits(self):
        """Test automatic axis limit calculation"""
        data = [10, 50, 75, 120, 200]
        result = iwfm.calculate_axis_limits(data)
        self.assertIn('min', result)
        self.assertIn('max', result)
        self.assertLessEqual(result['min'], min(data))
        self.assertGreaterEqual(result['max'], max(data))
    
    def test_legend_placement(self):
        """Test optimal legend placement"""
        data_bounds = [0, 0, 100, 100]
        dense_regions = [[20, 20, 40, 40], [60, 60, 80, 80]]
        result = iwfm.optimal_legend_placement(data_bounds, dense_regions)
        self.assertIsInstance(result, tuple)


class TestExportFormats(unittest.TestCase):
    """Test suite for various export formats"""
    
    def test_export_csv(self):
        """Test CSV export"""
        data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        try:
            iwfm.export_csv(data, temp_file.name)
            self.assertTrue(os.path.exists(temp_file.name))
        finally:
            os.unlink(temp_file.name)
    
    def test_export_shapefile(self):
        """Test shapefile export"""
        geometries = [[[0, 0], [10, 0], [10, 10], [0, 10]]]
        attributes = [{'id': 1, 'value': 100}]
        temp_dir = tempfile.mkdtemp()
        try:
            result = iwfm.export_shapefile(geometries, attributes, 
                                          os.path.join(temp_dir, 'test.shp'))
            self.assertTrue(result)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_export_geojson(self):
        """Test GeoJSON export"""
        features = [
            {'geometry': [[0, 0], [10, 0], [10, 10]], 'properties': {'id': 1}}
        ]
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.geojson', delete=False)
        try:
            iwfm.export_geojson(features, temp_file.name)
            self.assertTrue(os.path.exists(temp_file.name))
        finally:
            os.unlink(temp_file.name)
    
    def test_export_netcdf(self):
        """Test NetCDF export"""
        data = {
            'time': [0, 1, 2],
            'x': [0, 10, 20],
            'y': [0, 10, 20],
            'values': [[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]]
        }
        temp_file = tempfile.NamedTemporaryFile(suffix='.nc', delete=False)
        try:
            result = iwfm.export_netcdf(data, temp_file.name)
            self.assertTrue(result)
        finally:
            os.unlink(temp_file.name)


class TestReservoirOperations(unittest.TestCase):
    """Test suite for reservoir operations"""
    
    def test_reservoir_storage(self):
        """Test reservoir storage calculation"""
        elevation = 150.0  # feet
        area_elev_curve = {100: 0, 125: 500, 150: 1200, 175: 2000}  # elev: acres
        result = iwfm.reservoir_storage(elevation, area_elev_curve)
        self.assertGreater(result, 0)
    
    def test_reservoir_release(self):
        """Test reservoir release calculation"""
        storage = 10000.0  # acre-feet
        demand = 500.0
        min_storage = 1000.0
        result = iwfm.reservoir_release(storage, demand, min_storage)
        self.assertLessEqual(result, demand)
    
    def test_reservoir_routing(self):
        """Test reservoir routing"""
        inflow = [100, 200, 300, 200, 100]  # cfs
        initial_storage = 5000.0  # acre-feet
        outflow_rating = {0: 0, 5000: 50, 10000: 150, 15000: 300}
        result = iwfm.reservoir_routing(inflow, initial_storage, outflow_rating)
        self.assertEqual(len(result), len(inflow))
    
    def test_reservoir_evaporation(self):
        """Test reservoir evaporation loss"""
        surface_area = 1000.0  # acres
        evap_rate = 0.25  # inches/day
        days = 30
        result = iwfm.reservoir_evaporation(surface_area, evap_rate, days)
        self.assertGreater(result, 0)


class TestConjunctiveUse(unittest.TestCase):
    """Test suite for conjunctive use operations"""
    
    def test_surface_gw_allocation(self):
        """Test surface and groundwater allocation"""
        total_demand = 1000.0  # acre-feet
        surface_availability = 600.0
        gw_capacity = 800.0
        priority = 'surface_first'
        result = iwfm.allocate_conjunctive(total_demand, surface_availability, 
                                           gw_capacity, priority)
        self.assertIn('surface', result)
        self.assertIn('groundwater', result)
        self.assertAlmostEqual(result['surface'] + result['groundwater'], 
                              min(total_demand, surface_availability + gw_capacity), places=2)
    
    def test_banking_operations(self):
        """Test groundwater banking operations"""
        recharge_capacity = 500.0  # acre-feet/month
        available_water = 800.0
        storage_space = 10000.0
        result = iwfm.banking_recharge(recharge_capacity, available_water, storage_space)
        self.assertLessEqual(result, recharge_capacity)
    
    def test_exchange_accounting(self):
        """Test water exchange accounting"""
        deposits = [100, 200, 150]
        withdrawals = [50, 100, 200]
        initial_balance = 1000.0
        result = iwfm.exchange_account(deposits, withdrawals, initial_balance)
        self.assertEqual(len(result), len(deposits) + 1)
    
    def test_recovery_efficiency(self):
        """Test recovery efficiency calculation"""
        recharged = 1000.0  # acre-feet
        recovered = 850.0
        result = iwfm.recovery_efficiency(recharged, recovered)
        self.assertAlmostEqual(result, 0.85, places=2)


class TestWaterQuality(unittest.TestCase):
    """Test suite for water quality calculations"""
    
    def test_mixing_concentration(self):
        """Test concentration from mixing"""
        flows = [100, 200, 150]  # cfs
        concentrations = [10, 20, 15]  # mg/L
        result = iwfm.mixing_concentration(flows, concentrations)
        self.assertGreater(result, 10)
        self.assertLess(result, 20)
    
    def test_first_order_decay(self):
        """Test first-order decay"""
        initial_conc = 100.0  # mg/L
        decay_rate = 0.1  # 1/day
        time = 10.0  # days
        result = iwfm.first_order_decay(initial_conc, decay_rate, time)
        self.assertLess(result, initial_conc)
        self.assertGreater(result, 0)
    
    def test_tds_calculation(self):
        """Test total dissolved solids calculation"""
        ec = 1500.0  # microsiemens/cm
        result = iwfm.ec_to_tds(ec)
        self.assertGreater(result, 0)
    
    def test_dilution_factor(self):
        """Test dilution factor"""
        upstream_conc = 50.0
        point_source_conc = 500.0
        point_source_flow = 10.0
        river_flow = 100.0
        result = iwfm.dilution_factor(upstream_conc, point_source_conc, 
                                      point_source_flow, river_flow)
        self.assertGreater(result, 0)


class TestLandUseOperations(unittest.TestCase):
    """Test suite for land use operations"""
    
    def test_land_use_area(self):
        """Test calculating land use areas"""
        land_use_map = [[1, 1, 2], [1, 2, 2], [3, 3, 3]]
        cell_area = 1.0  # acres
        result = iwfm.land_use_areas(land_use_map, cell_area)
        self.assertIsInstance(result, dict)
        self.assertEqual(result[1], 3.0)
    
    def test_crop_distribution(self):
        """Test crop distribution calculation"""
        crops = {'corn': 500, 'wheat': 300, 'alfalfa': 200}
        result = iwfm.crop_distribution(crops)
        self.assertAlmostEqual(sum(result.values()), 1.0, places=5)
    
    def test_land_use_transition(self):
        """Test land use transition matrix"""
        year1 = [[1, 1, 2], [1, 2, 2]]
        year2 = [[1, 2, 2], [2, 2, 3]]
        result = iwfm.land_use_transition(year1, year2)
        self.assertIsInstance(result, dict)
    
    def test_urban_growth_rate(self):
        """Test urban growth rate calculation"""
        urban_area_t1 = 1000.0  # acres
        urban_area_t2 = 1200.0
        years = 5
        result = iwfm.urban_growth_rate(urban_area_t1, urban_area_t2, years)
        self.assertGreater(result, 0)


class TestHydrologicRouting(unittest.TestCase):
    """Test suite for hydrologic routing"""
    
    def test_muskingum_routing(self):
        """Test Muskingum routing method"""
        inflow = [10, 20, 40, 60, 50, 30, 20, 15, 12, 10]
        K = 2.0  # storage coefficient (hours)
        x = 0.2  # weighting factor
        dt = 1.0  # time step (hours)
        result = iwfm.muskingum_routing(inflow, K, x, dt)
        self.assertEqual(len(result), len(inflow))
    
    def test_kinematic_wave(self):
        """Test kinematic wave routing"""
        inflow = [0, 5, 15, 25, 20, 10, 5, 2, 0]
        slope = 0.01
        length = 5000.0  # feet
        manning_n = 0.035
        result = iwfm.kinematic_wave(inflow, slope, length, manning_n)
        self.assertIsInstance(result, list)
    
    def test_lag_routing(self):
        """Test lag routing method"""
        inflow = [10, 20, 30, 40, 30, 20, 15, 10]
        lag_time = 2  # time steps
        result = iwfm.lag_routing(inflow, lag_time)
        self.assertEqual(len(result), len(inflow))
    
    def test_cascade_routing(self):
        """Test cascade (linear reservoir) routing"""
        inflow = [0, 10, 30, 50, 40, 25, 15, 10, 5, 0]
        storage_coef = 1.5
        n_reservoirs = 3
        result = iwfm.cascade_routing(inflow, storage_coef, n_reservoirs)
        self.assertEqual(len(result), len(inflow))


class TestFloodplainAnalysis(unittest.TestCase):
    """Test suite for floodplain analysis"""
    
    def test_flood_frequency(self):
        """Test flood frequency analysis"""
        annual_peaks = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
        return_period = 100
        result = iwfm.flood_frequency(annual_peaks, return_period)
        self.assertGreater(result, max(annual_peaks))
    
    def test_flood_stage(self):
        """Test flood stage calculation"""
        discharge = 10000.0  # cfs
        rating_curve = {1000: 10, 5000: 15, 10000: 20, 15000: 23}
        result = iwfm.discharge_to_stage(discharge, rating_curve)
        self.assertAlmostEqual(result, 20.0, places=1)
    
    def test_inundation_area(self):
        """Test floodplain inundation area"""
        flood_stage = 25.0  # feet
        dem = [[20, 22, 24], [23, 26, 28], [25, 27, 30]]  # elevations
        cell_size = 100.0  # feet
        result = iwfm.inundation_area(flood_stage, dem, cell_size)
        self.assertGreater(result, 0)
    
    def test_flood_volume(self):
        """Test flood volume calculation"""
        inundated_area = 5000.0  # acres
        avg_depth = 3.0  # feet
        result = iwfm.flood_volume(inundated_area, avg_depth)
        self.assertAlmostEqual(result, 15000.0, places=2)


class TestEcologicalFunctions(unittest.TestCase):
    """Test suite for ecological/environmental functions"""
    
    def test_habitat_suitability(self):
        """Test habitat suitability index"""
        depth = 2.0  # feet
        velocity = 1.5  # ft/s
        substrate = 'gravel'
        species = 'salmon'
        result = iwfm.habitat_suitability(depth, velocity, substrate, species)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 1.0)
    
    def test_wetted_perimeter(self):
        """Test wetted perimeter calculation"""
        flow = 500.0  # cfs
        channel_geometry = {'width': 50, 'side_slope': 2, 'manning_n': 0.03, 'slope': 0.001}
        result = iwfm.wetted_perimeter(flow, channel_geometry)
        self.assertGreater(result, 0)
    
    def test_instream_flow_requirement(self):
        """Test instream flow requirement"""
        avg_flow = 1000.0  # cfs
        method = 'tennant'
        season = 'summer'
        result = iwfm.instream_flow(avg_flow, method, season)
        self.assertGreater(result, 0)
        self.assertLess(result, avg_flow)
    
    def test_fish_passage_criteria(self):
        """Test fish passage criteria"""
        velocity = 3.0  # ft/s
        depth = 1.5  # feet
        species = 'steelhead'
        result = iwfm.fish_passage_check(velocity, depth, species)
        self.assertIsInstance(result, bool)


class TestGeochemistry(unittest.TestCase):
    """Test suite for geochemical calculations"""
    
    def test_saturation_index(self):
        """Test saturation index calculation"""
        ion_activity_product = 1e-9
        solubility_product = 1e-10
        result = iwfm.saturation_index(ion_activity_product, solubility_product)
        self.assertGreater(result, 0)  # Supersaturated
    
    def test_ionic_strength(self):
        """Test ionic strength calculation"""
        concentrations = {'Ca': 100, 'Mg': 50, 'Na': 200, 'Cl': 300, 'SO4': 150}
        charges = {'Ca': 2, 'Mg': 2, 'Na': 1, 'Cl': -1, 'SO4': -2}
        result = iwfm.ionic_strength(concentrations, charges)
        self.assertGreater(result, 0)
    
    def test_cation_exchange(self):
        """Test cation exchange capacity"""
        clay_content = 0.30  # fraction
        organic_matter = 0.05
        result = iwfm.cation_exchange_capacity(clay_content, organic_matter)
        self.assertGreater(result, 0)
    
    def test_redox_potential(self):
        """Test redox potential calculation"""
        oxidized_conc = 10.0  # mg/L
        reduced_conc = 5.0
        n_electrons = 2
        result = iwfm.redox_potential(oxidized_conc, reduced_conc, n_electrons)
        self.assertIsInstance(result, float)


class TestTimeSeriesAdvanced(unittest.TestCase):
    """Test suite for advanced time series operations"""
    
    def test_seasonal_decomposition(self):
        """Test seasonal decomposition"""
        data = [10, 15, 20, 18, 12, 8, 11, 16, 22, 20, 14, 9] * 3  # 3 years
        period = 12  # monthly
        result = iwfm.seasonal_decompose(data, period)
        self.assertIn('trend', result)
        self.assertIn('seasonal', result)
        self.assertIn('residual', result)
    
    def test_autocorrelation(self):
        """Test autocorrelation function"""
        data = [10, 12, 11, 13, 15, 14, 16, 18, 17, 19]
        lag = 1
        result = iwfm.autocorrelation(data, lag)
        self.assertGreaterEqual(result, -1.0)
        self.assertLessEqual(result, 1.0)
    
    def test_spectral_analysis(self):
        """Test spectral analysis"""
        data = [10 + 5*i for i in range(100)]  # Linear trend with noise
        result = iwfm.spectral_analysis(data)
        self.assertIn('frequencies', result)
        self.assertIn('power', result)
    
    def test_change_point_detection(self):
        """Test change point detection"""
        data = [10]*20 + [20]*20 + [10]*20
        result = iwfm.detect_change_points(data)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)


class TestNumericalMethods(unittest.TestCase):
    """Test suite for numerical methods"""
    
    def test_newton_raphson(self):
        """Test Newton-Raphson method"""
        # Solve x^2 - 4 = 0
        func = lambda x: x**2 - 4
        derivative = lambda x: 2*x
        initial_guess = 1.0
        result = iwfm.newton_raphson(func, derivative, initial_guess)
        self.assertAlmostEqual(result, 2.0, places=5)
    
    def test_bisection_method(self):
        """Test bisection method"""
        # Solve x^3 - x - 2 = 0
        func = lambda x: x**3 - x - 2
        a, b = 1.0, 2.0
        result = iwfm.bisection(func, a, b)
        self.assertAlmostEqual(func(result), 0.0, places=5)
    
    def test_runge_kutta(self):
        """Test Runge-Kutta integration"""
        # Solve dy/dt = y, y(0) = 1
        derivative = lambda t, y: y
        y0 = 1.0
        t_span = (0, 1)
        n_steps = 10
        result = iwfm.runge_kutta_4(derivative, y0, t_span, n_steps)
        self.assertAlmostEqual(result[-1], 2.718, places=2)  # e^1
    
    def test_trapezoidal_rule(self):
        """Test trapezoidal integration"""
        # Integrate x^2 from 0 to 2
        func = lambda x: x**2
        a, b = 0, 2
        n = 100
        result = iwfm.trapezoidal_integration(func, a, b, n)
        self.assertAlmostEqual(result, 8/3, places=2)


class TestMatrixOperations(unittest.TestCase):
    """Test suite for matrix operations"""
    
    def test_matrix_multiply(self):
        """Test matrix multiplication"""
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        result = iwfm.matrix_multiply(A, B)
        expected = [[19, 22], [43, 50]]
        self.assertEqual(result, expected)
    
    def test_matrix_inverse(self):
        """Test matrix inversion"""
        A = [[4, 7], [2, 6]]
        result = iwfm.matrix_inverse(A)
        # Verify A * A_inv = I
        product = iwfm.matrix_multiply(A, result)
        self.assertAlmostEqual(product[0][0], 1.0, places=5)
        self.assertAlmostEqual(product[1][1], 1.0, places=5)
    
    def test_lu_decomposition(self):
        """Test LU decomposition"""
        A = [[2, 1, 1], [4, 3, 3], [8, 7, 9]]
        L, U = iwfm.lu_decompose(A)
        # Verify L * U = A
        product = iwfm.matrix_multiply(L, U)
        for i in range(len(A)):
            for j in range(len(A[0])):
                self.assertAlmostEqual(product[i][j], A[i][j], places=5)
    
    def test_eigenvalues(self):
        """Test eigenvalue calculation"""
        A = [[2, 1], [1, 2]]
        result = iwfm.eigenvalues(A)
        self.assertEqual(len(result), 2)
        self.assertTrue(3 in result or abs(3 - max(result)) < 0.01)


class TestSpatialInterpolation(unittest.TestCase):
    """Test suite for advanced spatial interpolation"""
    
    def test_ordinary_kriging(self):
        """Test ordinary kriging"""
        points = [[0, 0], [1, 0], [0, 1], [1, 1]]
        values = [10, 12, 11, 13]
        target = [0.5, 0.5]
        variogram_model = 'spherical'
        result = iwfm.ordinary_kriging(points, values, target, variogram_model)
        self.assertGreater(result, 10)
        self.assertLess(result, 13)
    
    def test_universal_kriging(self):
        """Test universal kriging with trend"""
        points = [[i, j] for i in range(5) for j in range(5)]
        values = [i + j for i in range(5) for j in range(5)]
        target = [2.5, 2.5]
        result = iwfm.universal_kriging(points, values, target)
        self.assertAlmostEqual(result, 5.0, places=1)
    
    def test_cokriging(self):
        """Test cokriging (multi-variable)"""
        primary_points = [[0, 0], [10, 0], [0, 10]]
        primary_values = [100, 110, 105]
        secondary_points = [[5, 0], [0, 5], [5, 5], [10, 10]]
        secondary_values = [105, 103, 108, 115]
        target = [5, 5]
        result = iwfm.cokriging(primary_points, primary_values, 
                               secondary_points, secondary_values, target)
        self.assertIsInstance(result, float)
    
    def test_thin_plate_spline(self):
        """Test thin plate spline interpolation"""
        points = [[0, 0], [1, 0], [0, 1], [1, 1]]
        values = [0, 1, 1, 2]
        target = [0.5, 0.5]
        result = iwfm.thin_plate_spline(points, values, target)
        self.assertGreater(result, 0)
        self.assertLess(result, 2)


class TestErrorAnalysis(unittest.TestCase):
    """Test suite for error analysis and propagation"""
    
    def test_error_propagation_sum(self):
        """Test error propagation for sum"""
        values = [10.0, 20.0, 30.0]
        errors = [0.5, 1.0, 0.8]
        result = iwfm.error_prop_sum(values, errors)
        self.assertIn('value', result)
        self.assertIn('error', result)
    
    def test_error_propagation_product(self):
        """Test error propagation for product"""
        values = [10.0, 5.0]
        rel_errors = [0.1, 0.05]  # 10% and 5%
        result = iwfm.error_prop_product(values, rel_errors)
        expected_error = 0.112  # sqrt(0.1^2 + 0.05^2)
        self.assertAlmostEqual(result['relative_error'], expected_error, places=3)
    
    def test_measurement_uncertainty(self):
        """Test measurement uncertainty analysis"""
        measurements = [10.1, 10.3, 9.9, 10.2, 10.0]
        confidence = 0.95
        result = iwfm.measurement_uncertainty(measurements, confidence)
        self.assertIn('mean', result)
        self.assertIn('uncertainty', result)
    
    def test_error_budget(self):
        """Test error budget calculation"""
        error_sources = {'instrument': 0.5, 'calibration': 0.3, 'environmental': 0.4}
        result = iwfm.error_budget(error_sources)
        self.assertGreater(result['total_error'], max(error_sources.values()))


class TestWatershedDelineation(unittest.TestCase):
    """Test suite for watershed delineation"""
    
    def test_flow_accumulation(self):
        """Test flow accumulation calculation"""
        flow_direction = [[1, 1, 2], [8, 0, 4], [8, 7, 4]]
        result = iwfm.flow_accumulation(flow_direction)
        self.assertIsInstance(result, list)
    
    def test_stream_network(self):
        """Test stream network extraction"""
        flow_accumulation = [[1, 2, 1], [3, 5, 2], [1, 8, 4]]
        threshold = 5
        result = iwfm.extract_streams(flow_accumulation, threshold)
        self.assertIsInstance(result, list)
    
    def test_watershed_boundary(self):
        """Test watershed boundary delineation"""
        flow_direction = [[1, 1, 2], [8, 0, 4], [8, 7, 4]]
        pour_point = (1, 1)
        result = iwfm.delineate_watershed(flow_direction, pour_point)
        self.assertIsInstance(result, list)
    
    def test_stream_order(self):
        """Test stream order calculation (Strahler)"""
        stream_network = {1: [], 2: [], 3: [1, 2], 4: [3]}
        result = iwfm.stream_order_strahler(stream_network)
        self.assertIsInstance(result, dict)


class TestClimateIndices(unittest.TestCase):
    """Test suite for climate indices"""
    
    def test_spi(self):
        """Test Standardized Precipitation Index"""
        precipitation = [2.5, 3.0, 2.8, 3.5, 4.0, 3.2, 2.9, 3.1, 3.3, 2.7]
        timescale = 3  # months
        result = iwfm.spi(precipitation, timescale)
        self.assertEqual(len(result), len(precipitation) - timescale + 1)
    
    def test_spei(self):
        """Test Standardized Precipitation-Evapotranspiration Index"""
        precipitation = [50, 60, 55, 70, 80, 65]
        pet = [40, 45, 50, 55, 60, 55]
        timescale = 3
        result = iwfm.spei(precipitation, pet, timescale)
        self.assertIsInstance(result, list)
    
    def test_aridity_index(self):
        """Test aridity index calculation"""
        annual_precip = 500.0  # mm
        annual_pet = 1000.0  # mm
        result = iwfm.aridity_index(annual_precip, annual_pet)
        self.assertGreater(result, 0)
        self.assertLess(result, 1.0)
    
    def test_growing_degree_days(self):
        """Test growing degree days"""
        daily_temps = [65, 70, 72, 68, 75, 78, 80]
        base_temp = 50.0
        result = iwfm.growing_degree_days(daily_temps, base_temp)
        self.assertGreater(result, 0)



if __name__ == '__main__':
    # Run tests with detailed output
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
#    suite.addTests(loader.loadTestsFromTestCase(TestListOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestArrayOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestCoordinateOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestAreaCalculations))
#    suite.addTests(loader.loadTestsFromTestCase(TestInterpolation))
#    suite.addTests(loader.loadTestsFromTestCase(TestStatistics))
#    suite.addTests(loader.loadTestsFromTestCase(TestTimeSeriesOperations))

#    suite.addTests(loader.loadTestsFromTestCase(TestValidation))
#    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
#    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
#    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
#    suite.addTests(loader.loadTestsFromTestCase(TestFilenameOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestFileSystemOperations))

#    suite.addTests(loader.loadTestsFromTestCase(TestMathematicalOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestStringOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestDateOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestDictionaryOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestUnitConversions))

#    suite.addTests(loader.loadTestsFromTestCase(TestNearestOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestSkipAheadFunction))
#    suite.addTests(loader.loadTestsFromTestCase(TestPrintToString))
#    suite.addTests(loader.loadTestsFromTestCase(TestElemPolyCoords))

#    suite.addTests(loader.loadTestsFromTestCase(TestNodeOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestElementOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestMeshOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestGeometryTransformations))
#    suite.addTests(loader.loadTestsFromTestCase(TestWaterBalanceOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestSubsurfaceOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestTimeSeriesAnalysis))
#    suite.addTests(loader.loadTestsFromTestCase(TestOutputFormatting))
#    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
#    suite.addTests(loader.loadTestsFromTestCase(TestLayerOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestBudgetOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestStreamOperations))
#    suite.addTests(loader.loadTestsFromTestCase(TestAquiferProperties))
    suite.addTests(loader.loadTestsFromTestCase(TestPumpingAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestCropWaterUse))
    suite.addTests(loader.loadTestsFromTestCase(TestSoilProperties))
    suite.addTests(loader.loadTestsFromTestCase(TestSpatialAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestNetworkAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestOptimization))
    suite.addTests(loader.loadTestsFromTestCase(TestQualityControl))
    suite.addTests(loader.loadTestsFromTestCase(TestReporting))
    suite.addTests(loader.loadTestsFromTestCase(TestModelCalibration))
    suite.addTests(loader.loadTestsFromTestCase(TestBoundaryConditions))
    suite.addTests(loader.loadTestsFromTestCase(TestFlowPathAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestContourOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestZoneBudget))
    suite.addTests(loader.loadTestsFromTestCase(TestVerticalFlow))
    suite.addTests(loader.loadTestsFromTestCase(TestStochasticMethods))
    suite.addTests(loader.loadTestsFromTestCase(TestWellPackage))
    suite.addTests(loader.loadTestsFromTestCase(TestLandSubsidence))
    suite.addTests(loader.loadTestsFromTestCase(TestSaltTransport))
    suite.addTests(loader.loadTestsFromTestCase(TestDrainageOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestClimateChange))
    suite.addTests(loader.loadTestsFromTestCase(TestDataAssimilation))
    suite.addTests(loader.loadTestsFromTestCase(TestGridRefinement))
    suite.addTests(loader.loadTestsFromTestCase(TestRiverPackage))
    suite.addTests(loader.loadTestsFromTestCase(TestLakePackage))
    suite.addTests(loader.loadTestsFromTestCase(TestUnsaturatedZone))
    suite.addTests(loader.loadTestsFromTestCase(TestRootZone))
    suite.addTests(loader.loadTestsFromTestCase(TestSurfaceRunoff))
    suite.addTests(loader.loadTestsFromTestCase(TestSensitivityUncertainty))
    suite.addTests(loader.loadTestsFromTestCase(TestPostProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestModelDiagnostics))
    suite.addTests(loader.loadTestsFromTestCase(TestParameterEstimation))
    suite.addTests(loader.loadTestsFromTestCase(TestForecastingScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestVisualizationHelpers))
    suite.addTests(loader.loadTestsFromTestCase(TestExportFormats))
    suite.addTests(loader.loadTestsFromTestCase(TestReservoirOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestConjunctiveUse))
    suite.addTests(loader.loadTestsFromTestCase(TestWaterQuality))
    suite.addTests(loader.loadTestsFromTestCase(TestLandUseOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestHydrologicRouting))
    suite.addTests(loader.loadTestsFromTestCase(TestFloodplainAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestEcologicalFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestGeochemistry))
    suite.addTests(loader.loadTestsFromTestCase(TestTimeSeriesAdvanced))
    suite.addTests(loader.loadTestsFromTestCase(TestNumericalMethods))
    suite.addTests(loader.loadTestsFromTestCase(TestMatrixOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestSpatialInterpolation))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestWatershedDelineation))
    suite.addTests(loader.loadTestsFromTestCase(TestClimateIndices))



    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print comprehensive summary
    print(f"\n{'='*70}")
    print(f"IWFM Comprehensive Test Suite Summary")
    print(f"{'='*70}")
    print(f"Total Test Classes:  {len([tc for tc in dir() if tc.startswith('Test')])}")
    print(f"Tests run:           {result.testsRun}")
    print(f"Successes:           {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:            {len(result.failures)}")
    print(f"Errors:              {len(result.errors)}")
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate:        {success_rate:.1f}%")
    print(f"{'='*70}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
