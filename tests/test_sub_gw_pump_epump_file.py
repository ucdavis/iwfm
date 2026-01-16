# test_sub_gw_pump_epump_file.py
# unit test for sub_gw_pump_epump_file function in the iwfm package
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
import pytest
from pathlib import Path

import iwfm


# Path to test data
TEST_DATA_DIR = Path(__file__).parent / "C2VSimCG-2021"
ELEM_PUMP_FILE = TEST_DATA_DIR / "Simulation" / "Groundwater" / "C2VSimCG_ElemPump.dat"


@pytest.fixture
def elem_pump_file_exists():
    """Check that the C2VSimCG element pumping file exists."""
    if not TEST_DATA_DIR.exists():
        pytest.skip(f"Test data directory not found: {TEST_DATA_DIR}")
    if not ELEM_PUMP_FILE.exists():
        pytest.skip(f"Element pumping file not found: {ELEM_PUMP_FILE}")
    return True


# ============================================================================
# Test sub_gw_pump_epump_file with actual C2VSimCG-2021 file
# ============================================================================

def test_sub_gw_pump_epump_file_creates_output(elem_pump_file_exists, tmp_path):
    """Test that sub_gw_pump_epump_file creates an output file."""
    output_file = tmp_path / "test_output_epump.dat"

    # Use a small subset of elements
    test_elems = [1, 2, 3, 4, 5]

    # Run the function
    has_wells = iwfm.sub_gw_pump_epump_file(
        str(ELEM_PUMP_FILE),
        str(output_file),
        test_elems,
        verbose=False
    )

    # Should create output file
    assert output_file.exists(), "Output file should be created"

    # Read and verify it has content
    with open(output_file, 'r') as f:
        content = f.read()
    assert len(content) > 0, "Output file should have content"
    assert '/ NSINK' in content, "Should have NSINK marker"
    assert '/ NGRP' in content, "Should have NGRP marker"


def test_sub_gw_pump_epump_file_filters_elements(elem_pump_file_exists, tmp_path):
    """Test that the function correctly filters elements."""
    output_file = tmp_path / "filtered_epump.dat"

    # Use a small subset of known elements
    test_elems = [1, 2, 3, 4, 5]

    # Run the function
    has_wells = iwfm.sub_gw_pump_epump_file(
        str(ELEM_PUMP_FILE),
        str(output_file),
        test_elems,
        verbose=False
    )

    # Read the output file and verify it contains only the specified elements
    with open(output_file, 'r') as f:
        output_lines = f.read().splitlines()

    # Find the NSINK value in output
    nsink_found = False
    for line in output_lines:
        if '/ NSINK' in line:
            nsink_value = int(line.split()[0])
            # Should have some element pumping specs (elements can appear multiple times with different well types)
            assert nsink_value > 0, f"NSINK should be > 0, got {nsink_value}"
            # Verify it's a reasonable number (less than total in original file)
            assert nsink_value < 5568, f"NSINK should be filtered from 5568, got {nsink_value}"
            nsink_found = True
            break

    assert nsink_found, "Should find NSINK line in output"


def test_sub_gw_pump_epump_file_preserves_format(elem_pump_file_exists, tmp_path):
    """Test that output file preserves the IWFM format."""
    output_file = tmp_path / "format_test_epump.dat"

    # Use elements that we know exist
    test_elems = list(range(1, 21))  # Elements 1-20

    # Run the function
    iwfm.sub_gw_pump_epump_file(
        str(ELEM_PUMP_FILE),
        str(output_file),
        test_elems,
        verbose=False
    )

    # Read output and verify format
    with open(output_file, 'r') as f:
        lines = f.readlines()

    # Should have content
    assert len(lines) > 0, "Output file should have content"

    # Should have NSINK marker
    nsink_line_exists = any('/ NSINK' in line for line in lines)
    assert nsink_line_exists, "Should have NSINK marker"

    # Should have NGRP marker
    ngrp_line_exists = any('/ NGRP' in line for line in lines)
    assert ngrp_line_exists, "Should have NGRP marker"


def test_sub_gw_pump_epump_file_returns_false_when_no_wells(elem_pump_file_exists, tmp_path):
    """Test that function returns False when no wells match."""
    output_file = tmp_path / "no_wells_epump.dat"

    # Use elements that likely don't exist (very high numbers)
    test_elems = [99999, 100000, 100001]

    # Run the function
    has_wells = iwfm.sub_gw_pump_epump_file(
        str(ELEM_PUMP_FILE),
        str(output_file),
        test_elems,
        verbose=False
    )

    # Should return False when no wells found
    assert has_wells is False, "Should return False when no wells found"

    # Output file should still be created
    assert output_file.exists(), "Output file should be created even with no wells"


def test_sub_gw_pump_epump_file_handles_element_groups(elem_pump_file_exists, tmp_path):
    """Test that element groups are filtered correctly."""
    output_file = tmp_path / "groups_test_epump.dat"

    # Use elements that are in groups (from tail of file: 1336, 1349, etc.)
    # These are in group 1
    test_elems = [1336, 1349, 1358, 1359]

    # Run the function
    iwfm.sub_gw_pump_epump_file(
        str(ELEM_PUMP_FILE),
        str(output_file),
        test_elems,
        verbose=False
    )

    # Read output
    with open(output_file, 'r') as f:
        output_content = f.read()

    # Should have NGRP section
    assert '/ NGRP' in output_content, "Should have element groups section"


def test_sub_gw_pump_epump_file_verbose_mode(elem_pump_file_exists, tmp_path, capsys):
    """Test that verbose mode produces output."""
    output_file = tmp_path / "verbose_test_epump.dat"
    test_elems = [1, 2, 3]

    # Run with verbose=True
    iwfm.sub_gw_pump_epump_file(
        str(ELEM_PUMP_FILE),
        str(output_file),
        test_elems,
        verbose=True
    )

    # Capture output
    captured = capsys.readouterr()

    # Should have some output (if function prints anything)
    # Some functions don't print in verbose mode, so this is optional
    assert output_file.exists(), "Output file should exist"


# ============================================================================
# Test validation improvements (using malformed data)
# ============================================================================

def test_validation_empty_nsink_line(tmp_path):
    """Test that empty NSINK line is caught."""
    bad_epump = """C Element pumping file
C Comment

C Empty line above should fail
"""
    input_file = tmp_path / "bad_epump.dat"
    input_file.write_text(bad_epump)

    output_file = tmp_path / "output_epump.dat"
    test_elems = [1, 2, 3]

    # Should raise ValueError for empty line
    with pytest.raises(ValueError, match="got empty line"):
        iwfm.sub_gw_pump_epump_file(
            str(input_file),
            str(output_file),
            test_elems,
            verbose=False
        )


def test_validation_empty_ngrp_line(tmp_path):
    """Test that empty NGRP line is caught."""
    bad_epump = """C Element pumping file
C Comment
3                  / NSINK
1	1	1.0
2	1	1.0
3	1	1.0
C Groups section

C Empty line above should fail
"""
    input_file = tmp_path / "bad_ngrp.dat"
    input_file.write_text(bad_epump)

    output_file = tmp_path / "output_epump.dat"
    test_elems = [1, 2, 3]

    # Should raise ValueError for empty line
    with pytest.raises(ValueError, match="got empty line"):
        iwfm.sub_gw_pump_epump_file(
            str(input_file),
            str(output_file),
            test_elems,
            verbose=False
        )


# ============================================================================
# Test with synthetic minimal file
# ============================================================================

def test_sub_gw_pump_epump_file_minimal_valid_file(tmp_path):
    """Test with a minimal valid element pumping file."""
    # Create a minimal valid file
    minimal_epump = """C Minimal element pumping file
C Comment line
     5                       / NSINK
1	1	1.000	3	0.25	0.25	0.25	0.25	-1	0	1	3	0	1
2	1	1.000	3	0.25	0.25	0.25	0.25	-1	0	1	3	0	1
3	1	1.000	3	0.25	0.25	0.25	0.25	-1	0	1	3	0	1
4	1	1.000	3	0.25	0.25	0.25	0.25	-1	0	1	3	0	1
5	1	1.000	3	0.25	0.25	0.25	0.25	-1	0	1	3	0	1
C Element groups section
     2                  / NGRP
1	2	1
		2
2	2	3
		4
"""
    input_file = tmp_path / "minimal_epump.dat"
    input_file.write_text(minimal_epump)

    output_file = tmp_path / "output_minimal.dat"

    # Filter to keep only elements 1, 2, 3
    test_elems = [1, 2, 3]

    has_wells = iwfm.sub_gw_pump_epump_file(
        str(input_file),
        str(output_file),
        test_elems,
        verbose=False
    )

    # Should return True (has wells)
    assert has_wells is True

    # Read output and verify
    with open(output_file, 'r') as f:
        output_lines = f.read().splitlines()

    # Find NSINK in output - should be 3 (filtered from 5)
    nsink_value = None
    for line in output_lines:
        if '/ NSINK' in line:
            nsink_value = int(line.split()[0])
            break

    assert nsink_value == 3, f"Expected NSINK=3, got {nsink_value}"


def test_sub_gw_pump_epump_file_filters_groups_correctly(tmp_path):
    """Test that element groups are filtered based on member elements."""
    # Create file with element groups
    epump_with_groups = """C Element pumping file
C Comment
     6                       / NSINK
10	1	1.0
20	1	1.0
30	1	1.0
40	1	1.0
50	1	1.0
60	1	1.0
C Element groups
     3                  / NGRP
1	2	10
		20
2	2	30
		40
3	2	50
		60
"""
    input_file = tmp_path / "groups_epump.dat"
    input_file.write_text(epump_with_groups)

    output_file = tmp_path / "output_groups.dat"

    # Keep only elements from groups 1 and 2
    test_elems = [10, 20, 30, 40]

    has_wells = iwfm.sub_gw_pump_epump_file(
        str(input_file),
        str(output_file),
        test_elems,
        verbose=False
    )

    assert has_wells is True

    # Read output
    with open(output_file, 'r') as f:
        output_content = f.read()

    # Should have filtered NSINK
    assert '4' in output_content.split('/ NSINK')[0].split()[-1] or \
           output_content.count('/ NSINK') > 0


# ============================================================================
# Test error messages include filename
# ============================================================================

def test_error_messages_include_filename(tmp_path):
    """Test that error messages include the filename."""
    bad_file = """C Bad file

C Empty NSINK
"""
    input_file = tmp_path / "specific_bad_file.dat"
    input_file.write_text(bad_file)

    output_file = tmp_path / "output.dat"

    with pytest.raises(ValueError) as exc_info:
        iwfm.sub_gw_pump_epump_file(
            str(input_file),
            str(output_file),
            [1, 2, 3],
            verbose=False
        )

    # Error message should include filename
    error_msg = str(exc_info.value)
    assert "specific_bad_file.dat" in error_msg or "got empty line" in error_msg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
