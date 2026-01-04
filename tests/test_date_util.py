# test_date_util.py
# unit test for date_util functions in the iwfm package
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
import datetime

import iwfm


# ============================================================================
# Test validate_date_format
# ============================================================================

def test_validate_date_format_valid():
    """Test that valid MM/DD/YYYY dates are accepted."""
    # Valid dates
    month, day, year = iwfm.validate_date_format('01/15/2020', 'test_date')
    assert month == 1
    assert day == 15
    assert year == 2020

    month, day, year = iwfm.validate_date_format('12/31/1999', 'test_date')
    assert month == 12
    assert day == 31
    assert year == 1999


def test_validate_date_format_invalid_format():
    """Test that invalid date formats raise ValueError."""
    # Wrong format - not enough parts
    with pytest.raises(ValueError, match="must be in MM/DD/YYYY format"):
        iwfm.validate_date_format('01-15-2020', 'test_date')

    # Wrong format - too many parts
    with pytest.raises(ValueError, match="must be in MM/DD/YYYY format"):
        iwfm.validate_date_format('01/15/2020/extra', 'test_date')

    # Empty string
    with pytest.raises(ValueError, match="cannot be empty"):
        iwfm.validate_date_format('', 'test_date')


def test_validate_date_format_non_numeric():
    """Test that non-numeric values raise ValueError."""
    with pytest.raises(ValueError, match="contains non-numeric values"):
        iwfm.validate_date_format('01/ABC/2020', 'test_date')

    with pytest.raises(ValueError, match="contains non-numeric values"):
        iwfm.validate_date_format('XX/15/2020', 'test_date')


def test_validate_date_format_invalid_ranges():
    """Test that out-of-range values raise ValueError."""
    # Invalid month
    with pytest.raises(ValueError, match="invalid month"):
        iwfm.validate_date_format('13/15/2020', 'test_date')

    with pytest.raises(ValueError, match="invalid month"):
        iwfm.validate_date_format('00/15/2020', 'test_date')

    # Invalid day
    with pytest.raises(ValueError, match="invalid day"):
        iwfm.validate_date_format('01/32/2020', 'test_date')

    with pytest.raises(ValueError, match="invalid day"):
        iwfm.validate_date_format('01/00/2020', 'test_date')

    # Invalid year (too early or too late)
    with pytest.raises(ValueError, match="invalid year"):
        iwfm.validate_date_format('01/15/1700', 'test_date')

    with pytest.raises(ValueError, match="invalid year"):
        iwfm.validate_date_format('01/15/6000', 'test_date')


def test_validate_date_format_not_string():
    """Test that non-string input raises ValueError."""
    with pytest.raises(ValueError, match="must be a string"):
        iwfm.validate_date_format(20200115, 'test_date')

    with pytest.raises(ValueError, match="must be a string"):
        iwfm.validate_date_format(None, 'test_date')


# ============================================================================
# Test safe_parse_date
# ============================================================================

def test_safe_parse_date_valid():
    """Test that valid dates are parsed correctly."""
    dt = iwfm.safe_parse_date('01/15/2020', 'test_date')
    assert dt == datetime.datetime(2020, 1, 15)

    dt = iwfm.safe_parse_date('12/31/1999', 'test_date')
    assert dt == datetime.datetime(1999, 12, 31)


def test_safe_parse_date_invalid_logical_date():
    """Test that logically invalid dates raise ValueError."""
    # February 30th doesn't exist
    with pytest.raises(ValueError, match="Invalid test_date"):
        iwfm.safe_parse_date('02/30/2020', 'test_date')

    # April 31st doesn't exist
    with pytest.raises(ValueError, match="Invalid test_date"):
        iwfm.safe_parse_date('04/31/2020', 'test_date')


def test_safe_parse_date_invalid_format():
    """Test that invalid formats raise ValueError."""
    with pytest.raises(ValueError, match="must be in MM/DD/YYYY format"):
        iwfm.safe_parse_date('2020-01-15', 'test_date')

    with pytest.raises(ValueError):
        iwfm.safe_parse_date('not a date', 'test_date')


# ============================================================================
# Test validate_dss_date_format
# ============================================================================

def test_validate_dss_date_format_valid():
    """Test that valid DSS dates are accepted."""
    month, day, year, hour, minute = iwfm.validate_dss_date_format('10/31/1973_24:00', 'test_date')
    assert month == 10
    assert day == 31
    assert year == 1973
    assert hour == 24
    assert minute == 0

    month, day, year, hour, minute = iwfm.validate_dss_date_format('01/15/2020_12:30', 'test_date')
    assert month == 1
    assert day == 15
    assert year == 2020
    assert hour == 12
    assert minute == 30


def test_validate_dss_date_format_invalid_format():
    """Test that invalid DSS formats raise ValueError."""
    # Wrong length - too short
    with pytest.raises(ValueError, match="expected 16 characters"):
        iwfm.validate_dss_date_format('10/31/1973_24:0', 'test_date')

    # Wrong length - too long
    with pytest.raises(ValueError, match="expected 16 characters"):
        iwfm.validate_dss_date_format('10/31/1973_24:000', 'test_date')

    # Wrong separators - missing underscore
    with pytest.raises(ValueError, match="incorrect separators"):
        iwfm.validate_dss_date_format('10/31/1973 24:00', 'test_date')

    # Wrong separators - using colon instead of slash
    with pytest.raises(ValueError, match="incorrect separators"):
        iwfm.validate_dss_date_format('10:31:1973_24:00', 'test_date')


def test_validate_dss_date_format_invalid_month():
    """Test that invalid month values raise ValueError."""
    # Month = 0
    with pytest.raises(ValueError, match="invalid month"):
        iwfm.validate_dss_date_format('00/31/1973_24:00', 'test_date')

    # Month = 13
    with pytest.raises(ValueError, match="invalid month"):
        iwfm.validate_dss_date_format('13/31/1973_24:00', 'test_date')


def test_validate_dss_date_format_invalid_ranges():
    """Test that out-of-range values raise ValueError."""
    # Invalid day (0)
    with pytest.raises(ValueError, match="invalid day"):
        iwfm.validate_dss_date_format('10/00/1973_24:00', 'test_date')

    # Invalid day (32)
    with pytest.raises(ValueError, match="invalid day"):
        iwfm.validate_dss_date_format('10/32/1973_24:00', 'test_date')

    # Invalid hour (25)
    with pytest.raises(ValueError, match="invalid hour"):
        iwfm.validate_dss_date_format('10/31/1973_25:00', 'test_date')

    # Invalid minute (60)
    with pytest.raises(ValueError, match="invalid minute"):
        iwfm.validate_dss_date_format('10/31/1973_24:60', 'test_date')

    # Invalid year (too early)
    with pytest.raises(ValueError, match="invalid year"):
        iwfm.validate_dss_date_format('10/31/1700_24:00', 'test_date')

    # Invalid year (too late)
    with pytest.raises(ValueError, match="invalid year"):
        iwfm.validate_dss_date_format('10/31/6000_24:00', 'test_date')


def test_validate_dss_date_format_not_string():
    """Test that non-string input raises ValueError."""
    with pytest.raises(ValueError, match="must be a string"):
        iwfm.validate_dss_date_format(20200101, 'test_date')


# ============================================================================
# Test edge cases
# ============================================================================

def test_validate_date_format_with_whitespace():
    """Test that dates with leading/trailing whitespace are handled."""
    month, day, year = iwfm.validate_date_format('  01/15/2020  ', 'test_date')
    assert month == 1
    assert day == 15
    assert year == 2020


def test_safe_parse_date_with_whitespace():
    """Test that dates with whitespace are parsed correctly."""
    dt = iwfm.safe_parse_date('  01/15/2020  ', 'test_date')
    assert dt == datetime.datetime(2020, 1, 15)


def test_validate_dss_date_format_with_whitespace():
    """Test that DSS dates with leading/trailing whitespace are handled."""
    month, day, year, hour, minute = iwfm.validate_dss_date_format('  10/31/1973_24:00  ', 'test_date')
    assert month == 10
    assert day == 31
    assert year == 1973
    assert hour == 24
    assert minute == 0


# ============================================================================
# Test custom parameter names in error messages
# ============================================================================

def test_validate_date_format_custom_param_name():
    """Test that custom parameter name appears in error message."""
    with pytest.raises(ValueError, match="my_custom_date"):
        iwfm.validate_date_format('invalid', 'my_custom_date')


def test_safe_parse_date_custom_param_name():
    """Test that custom parameter name appears in error message."""
    with pytest.raises(ValueError, match="my_custom_date"):
        iwfm.safe_parse_date('invalid', 'my_custom_date')


def test_validate_dss_date_format_custom_param_name():
    """Test that custom parameter name appears in error message."""
    with pytest.raises(ValueError, match="my_custom_dss_date"):
        iwfm.validate_dss_date_format('invalid', 'my_custom_dss_date')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
