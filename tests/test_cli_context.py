# test_cli_context.py
# Tests for CLI context module
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
from enum import Enum


class TestUserLevelEnum:
    """Tests for the UserLevel enum."""

    def test_user_level_is_enum(self):
        """Test that UserLevel is an Enum."""
        from iwfm.cli.context import UserLevel
        
        assert issubclass(UserLevel, Enum)

    def test_user_level_values(self):
        """Test that UserLevel enum has correct string values."""
        from iwfm.cli.context import UserLevel
        
        assert UserLevel.USER.value == "user"
        assert UserLevel.POWER.value == "power"
        assert UserLevel.DEV.value == "dev"

    def test_user_level_from_string(self):
        """Test creating UserLevel from string values."""
        from iwfm.cli.context import UserLevel
        
        assert UserLevel("user") == UserLevel.USER
        assert UserLevel("power") == UserLevel.POWER
        assert UserLevel("dev") == UserLevel.DEV

    def test_invalid_user_level_raises_error(self):
        """Test that invalid string raises ValueError."""
        from iwfm.cli.context import UserLevel
        
        with pytest.raises(ValueError):
            UserLevel("invalid")

        with pytest.raises(ValueError):
            UserLevel("admin")

    def test_is_user_method(self):
        """Test is_user() method returns correct values."""
        from iwfm.cli.context import UserLevel
        
        assert UserLevel.USER.is_user() is True
        assert UserLevel.POWER.is_user() is False
        assert UserLevel.DEV.is_user() is False

    def test_is_power_method(self):
        """Test is_power() method returns correct values."""
        from iwfm.cli.context import UserLevel
        
        assert UserLevel.USER.is_power() is False
        assert UserLevel.POWER.is_power() is True
        assert UserLevel.DEV.is_power() is False

    def test_is_dev_method(self):
        """Test is_dev() method returns correct values."""
        from iwfm.cli.context import UserLevel
        
        assert UserLevel.USER.is_dev() is False
        assert UserLevel.POWER.is_dev() is False
        assert UserLevel.DEV.is_dev() is True

    def test_enum_members_count(self):
        """Test that there are exactly 3 user levels."""
        from iwfm.cli.context import UserLevel
        
        assert len(UserLevel) == 3

    def test_enum_iteration(self):
        """Test iterating over all user levels."""
        from iwfm.cli.context import UserLevel
        
        levels = list(UserLevel)
        assert UserLevel.USER in levels
        assert UserLevel.POWER in levels
        assert UserLevel.DEV in levels

    def test_enum_comparison(self):
        """Test that enum members can be compared."""
        from iwfm.cli.context import UserLevel
        
        assert UserLevel.USER == UserLevel.USER
        assert UserLevel.USER != UserLevel.POWER
        assert UserLevel.POWER != UserLevel.DEV

    def test_enum_hashable(self):
        """Test that enum members are hashable (can be used in sets/dicts)."""
        from iwfm.cli.context import UserLevel
        
        level_set = {UserLevel.USER, UserLevel.POWER, UserLevel.DEV}
        assert len(level_set) == 3

        level_dict = {UserLevel.USER: 'basic', UserLevel.DEV: 'advanced'}
        assert level_dict[UserLevel.USER] == 'basic'


class TestContextFunctions:
    """Tests for context helper functions."""

    def test_get_user_level_exists(self):
        """Test that get_user_level function exists."""
        from iwfm.cli.context import get_user_level
        
        assert callable(get_user_level)

    def test_is_power_exists(self):
        """Test that is_power function exists."""
        from iwfm.cli.context import is_power
        
        assert callable(is_power)

    def test_is_dev_exists(self):
        """Test that is_dev function exists."""
        from iwfm.cli.context import is_dev
        
        assert callable(is_dev)


class TestContextImports:
    """Tests for context module imports."""

    def test_import_user_level(self):
        """Test importing UserLevel."""
        from iwfm.cli.context import UserLevel
        assert UserLevel is not None

    def test_import_get_user_level(self):
        """Test importing get_user_level."""
        from iwfm.cli.context import get_user_level
        assert get_user_level is not None

    def test_import_is_power(self):
        """Test importing is_power."""
        from iwfm.cli.context import is_power
        assert is_power is not None

    def test_import_is_dev(self):
        """Test importing is_dev."""
        from iwfm.cli.context import is_dev
        assert is_dev is not None

    def test_import_from_cli_package(self):
        """Test importing from iwfm.cli package."""
        from iwfm.cli import context
        assert hasattr(context, 'UserLevel')
        assert hasattr(context, 'get_user_level')
        assert hasattr(context, 'is_power')
        assert hasattr(context, 'is_dev')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
