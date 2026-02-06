# test_cli_module.py
# Tests for CLI __main__ module entry point
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
import importlib


class TestCLIModule:
    """Tests for the CLI module structure."""

    def test_cli_package_exists(self):
        """Test that iwfm.cli package exists."""
        import iwfm.cli
        assert iwfm.cli is not None

    def test_cli_main_module_exists(self):
        """Test that iwfm.cli.main module exists."""
        import iwfm.cli.main
        assert iwfm.cli.main is not None

    def test_cli_context_module_exists(self):
        """Test that iwfm.cli.context module exists."""
        import iwfm.cli.context
        assert iwfm.cli.context is not None

    def test_cli_dunder_main_exists(self):
        """Test that iwfm.cli.__main__ module exists."""
        # This allows `python -m iwfm.cli` to work
        spec = importlib.util.find_spec('iwfm.cli.__main__')
        assert spec is not None


class TestCLIEntryPoint:
    """Tests for CLI entry point."""

    def test_run_function_importable(self):
        """Test that run function can be imported from main."""
        from iwfm.cli.main import run
        assert callable(run)

    def test_app_importable(self):
        """Test that app can be imported from main."""
        from iwfm.cli.main import app
        assert app is not None


class TestCLIPackageStructure:
    """Tests for CLI package structure and exports."""

    def test_context_exports_user_level(self):
        """Test that context module exports UserLevel."""
        from iwfm.cli.context import UserLevel
        assert UserLevel is not None

    def test_main_exports_app(self):
        """Test that main module exports app."""
        from iwfm.cli.main import app
        assert app is not None

    def test_main_exports_run(self):
        """Test that main module exports run."""
        from iwfm.cli.main import run
        assert run is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
