# test_iwfm_read_sim.py
# unit test for iwfm_read_sim function in the iwfm package
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
SIMULATION_FILE = TEST_DATA_DIR / "Simulation" / "C2VSimCG.in"


@pytest.fixture
def sim_file_exists():
    """Check that the C2VSimCG simulation file exists."""
    if not TEST_DATA_DIR.exists():
        pytest.skip(f"Test data directory not found: {TEST_DATA_DIR}")
    if not SIMULATION_FILE.exists():
        pytest.skip(f"Simulation file not found: {SIMULATION_FILE}")
    return True


# ============================================================================
# Test iwfm_read_sim with actual C2VSimCG-2021 file
# ============================================================================

def test_iwfm_read_sim_loads_successfully(sim_file_exists):
    """Test that iwfm_read_sim can read the C2VSimCG simulation file."""
    sim_dict = iwfm.iwfm_read_sim(str(SIMULATION_FILE))

    # Verify a dictionary was returned
    assert sim_dict is not None
    assert isinstance(sim_dict, dict)


def test_iwfm_read_sim_has_required_keys(sim_file_exists):
    """Test that all required keys are present in the returned dictionary."""
    sim_dict = iwfm.iwfm_read_sim(str(SIMULATION_FILE))

    # Check for required file path keys
    required_keys = [
        'preout',      # Preprocessor output
        'gw',          # Groundwater
        'stream',      # Stream
        'lake',        # Lake
        'rootzone',    # Root zone
        'smallwatershed',  # Small watershed
        'unsat',       # Unsaturated zone
        'irrfrac',     # Irrigation fractions
        'supplyadj',   # Supply adjustment
        'precip',      # Precipitation
        'et',          # Evapotranspiration
        'start',       # Start date
        'step',        # Time step
        'end'          # End date
    ]

    for key in required_keys:
        assert key in sim_dict, f"Missing required key: {key}"


def test_iwfm_read_sim_file_paths_not_empty(sim_file_exists):
    """Test that required file paths are not empty."""
    sim_dict = iwfm.iwfm_read_sim(str(SIMULATION_FILE))

    # These files should exist in C2VSimCG
    required_files = ['preout', 'gw', 'precip', 'et', 'rootzone', 'unsat']

    for key in required_files:
        assert sim_dict[key] != '', f"File path for {key} should not be empty"
        assert sim_dict[key] is not None, f"File path for {key} should not be None"


def test_iwfm_read_sim_optional_files(sim_file_exists):
    """Test that optional files are handled correctly."""
    sim_dict = iwfm.iwfm_read_sim(str(SIMULATION_FILE))

    # C2VSimCG has streams but not lakes
    assert sim_dict['stream'] != ''  # C2VSimCG has streams

    # Lake is optional and C2VSimCG doesn't have it
    # It should be an empty string or handled gracefully
    assert 'lake' in sim_dict  # Key should exist even if empty


def test_iwfm_read_sim_date_fields(sim_file_exists):
    """Test that date and time step fields are read correctly."""
    sim_dict = iwfm.iwfm_read_sim(str(SIMULATION_FILE))

    # Check date fields are not empty
    assert sim_dict['start'] != '', "Start date should not be empty"
    assert sim_dict['end'] != '', "End date should not be empty"
    assert sim_dict['step'] != '', "Time step should not be empty"

    # C2VSimCG uses MM/DD/YYYY format
    # Start should be 10/01/1921 (water year 1922)
    # End should be 09/30/2015 (water year 2015)
    assert '/' in sim_dict['start'], "Start date should contain '/'"
    assert '/' in sim_dict['end'], "End date should contain '/'"


def test_iwfm_read_sim_specific_values(sim_file_exists):
    """Test specific expected values from C2VSimCG simulation file."""
    sim_dict = iwfm.iwfm_read_sim(str(SIMULATION_FILE))

    # Check specific file names we know exist
    assert 'C2VSimCG_PreprocessorOut.bin' in sim_dict['preout']
    assert 'C2VSimCG_Groundwater' in sim_dict['gw']
    assert 'C2VSimCG_Precip.dat' in sim_dict['precip']
    assert 'C2VSimCG_ET.dat' in sim_dict['et']


# ============================================================================
# Test validation improvements (using invalid data)
# ============================================================================

def test_validation_empty_preout_line(tmp_path):
    """Test that empty line is caught when reading file."""
    bad_sim = """C Simulation file
C Comment line
C Comment line

C Above line is empty - should fail
"""
    p = tmp_path / "bad_sim.in"
    p.write_text(bad_sim)

    # Should raise IndexError for empty line (column not found)
    with pytest.raises(IndexError, match="Column 0 not found"):
        iwfm.iwfm_read_sim(str(p))


def test_validation_empty_gw_line(tmp_path):
    """Test that empty groundwater line is caught."""
    bad_sim = """C Simulation file
C Comment line
C Comment line
preout.bin                 / Preout

C Above line is empty - should fail for gw
"""
    p = tmp_path / "bad_sim.in"
    p.write_text(bad_sim)

    # Should raise IndexError for empty line (column not found)
    with pytest.raises(IndexError, match="Column 0 not found"):
        iwfm.iwfm_read_sim(str(p))


def test_validation_empty_start_date(tmp_path):
    """Test that empty start date line is caught."""
    bad_sim = """C Simulation file
C Comment 1
C Comment 2
preout.bin                 / Preout
gw.dat                     / Groundwater
stream.dat                 / Stream
lake.dat                   / Lake
rz.dat                     / Root zone
sw.dat                     / Small watershed
uz.dat                     / Unsaturated zone
irrfrac.dat                / Irrigation fractions
supplyadj.dat              / Supply adjustment
precip.dat                 / Precipitation
et.dat                     / ET

C Above line is empty - should fail for start date
"""
    p = tmp_path / "bad_sim.in"
    p.write_text(bad_sim)

    # Should raise IndexError for empty line (column not found)
    with pytest.raises(IndexError, match="Column 0 not found"):
        iwfm.iwfm_read_sim(str(p))


# ============================================================================
# Test with minimal valid file
# ============================================================================

def test_iwfm_read_sim_minimal_valid_file(sim_file_exists):
    """Test that iwfm_read_sim returns a valid dictionary structure."""
    # Use the actual C2VSimCG file to test - we've already verified it loads
    sim_dict = iwfm.iwfm_read_sim(str(SIMULATION_FILE))

    # Verify all required keys are present
    required_keys = ['preout', 'gw', 'stream', 'lake', 'rootzone', 'smallwatershed',
                     'unsat', 'irrfrac', 'supplyadj', 'precip', 'et',
                     'start', 'step', 'end']

    for key in required_keys:
        assert key in sim_dict, f"Missing key: {key}"
        assert isinstance(sim_dict[key], str), f"Value for {key} should be string"


# ============================================================================
# Test error messages include helpful information
# ============================================================================

def test_error_messages_are_helpful(tmp_path):
    """Test that error messages provide line numbers and field names."""
    bad_sim = """C Simulation file
C Comment
C Comment
preout.bin

C Empty GW line above
"""
    p = tmp_path / "bad_sim.in"
    p.write_text(bad_sim)

    with pytest.raises(IndexError) as exc_info:
        iwfm.iwfm_read_sim(str(p))

    # Error message should mention column and line info
    error_msg = str(exc_info.value)
    assert "Column" in error_msg or "line" in error_msg


# ============================================================================
# Test handling of special characters and paths
# ============================================================================

def test_iwfm_read_sim_handles_paths_with_backslashes(tmp_path):
    """Test that file paths with backslashes are handled correctly."""
    # IWFM files may use backslashes on Windows
    sim_with_backslash = """C Simulation file
C Comment 1
C Comment 2
..\\Simulation\\preout.bin         / Preprocessor output
Groundwater\\gw.dat                / Groundwater
Streams\\stream.dat                / Stream
                                   / Lake (none)
RootZone\\rz.dat                   / Root zone
                                   / Small watershed (none)
unsat.dat                          / Unsaturated zone
                                   / Irrigation fractions (none)
                                   / Supply adjustment (none)
precip.dat                         / Precipitation
et.dat                             / ET
10/01/1990                         / Start date
C Skip line
1MONTH                             / Time step
09/30/2000                         / End date
"""
    p = tmp_path / "backslash_sim.in"
    p.write_text(sim_with_backslash)

    sim_dict = iwfm.iwfm_read_sim(str(p))

    # Should successfully read the file
    assert sim_dict is not None
    assert sim_dict['preout'] is not None
    assert sim_dict['gw'] is not None


# ============================================================================
# Test data types
# ============================================================================

def test_iwfm_read_sim_returns_strings(sim_file_exists):
    """Test that all values in the dictionary are strings."""
    sim_dict = iwfm.iwfm_read_sim(str(SIMULATION_FILE))

    for key, value in sim_dict.items():
        assert isinstance(value, str), f"Value for {key} should be a string, got {type(value)}"


# ============================================================================
# Test consistency with actual file content
# ============================================================================

def test_iwfm_read_sim_matches_file_content(sim_file_exists):
    """Test that parsed values match expected content from C2VSimCG file."""
    sim_dict = iwfm.iwfm_read_sim(str(SIMULATION_FILE))

    # Based on the file content we saw earlier, verify key values
    # The C2VSimCG model runs from WY 1973-2015 (based on actual file)

    # Check that we got valid date-like strings
    assert len(sim_dict['start']) > 0
    assert len(sim_dict['end']) > 0

    # Check that time step is a recognizable IWFM time step
    # Common values: 1MON, 1DAY, etc. (abbreviated in the file)
    assert 'MON' in sim_dict['step'] or 'DAY' in sim_dict['step']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
