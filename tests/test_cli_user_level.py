# test_cli_user_level.py
# Tests for CLI UserLevel enum
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
from iwfm.cli.context import UserLevel


class TestUserLevelEnum:
    """Tests for the UserLevel enum."""

    def test_user_level_values(self):
        """Test that UserLevel enum has correct string values."""
        assert UserLevel.USER.value == "user"
        assert UserLevel.POWER.value == "power"
        assert UserLevel.DEV.value == "dev"

    def test_user_level_from_string(self):
        """Test creating UserLevel from string values."""
        assert UserLevel("user") == UserLevel.USER
        assert UserLevel("power") == UserLevel.POWER
        assert UserLevel("dev") == UserLevel.DEV

    def test_invalid_user_level(self):
        """Test that invalid string raises ValueError."""
        with pytest.raises(ValueError):
            UserLevel("invalid")

    def test_is_user_method(self):
        """Test is_user() method returns correct values."""
        assert UserLevel.USER.is_user() is True
        assert UserLevel.POWER.is_user() is False
        assert UserLevel.DEV.is_user() is False

    def test_is_power_method(self):
        """Test is_power() method returns correct values."""
        assert UserLevel.USER.is_power() is False
        assert UserLevel.POWER.is_power() is True
        assert UserLevel.DEV.is_power() is False

    def test_is_dev_method(self):
        """Test is_dev() method returns correct values."""
        assert UserLevel.USER.is_dev() is False
        assert UserLevel.POWER.is_dev() is False
        assert UserLevel.DEV.is_dev() is True

    def test_enum_members_count(self):
        """Test that there are exactly 3 user levels."""
        assert len(UserLevel) == 3

    def test_enum_iteration(self):
        """Test iterating over all user levels."""
        levels = list(UserLevel)
        assert UserLevel.USER in levels
        assert UserLevel.POWER in levels
        assert UserLevel.DEV in levels
