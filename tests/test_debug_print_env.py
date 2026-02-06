# test_debug_print_env.py
# Tests for debug/print_env.py - Print environment variables
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


class TestPrintEnv:
    """Tests for print_env function."""

    def test_prints_environment_header(self, capsys):
        """Test that function prints 'Environment:' header."""
        from iwfm.debug.print_env import print_env
        
        print_env()
        
        captured = capsys.readouterr()
        assert "Environment:" in captured.out

    def test_prints_system_info(self, capsys):
        """Test that function prints system information."""
        from iwfm.debug.print_env import print_env
        
        print_env()
        
        captured = capsys.readouterr()
        assert "System:" in captured.out

    def test_prints_path(self, capsys):
        """Test that function prints PATH."""
        from iwfm.debug.print_env import print_env
        
        print_env()
        
        captured = capsys.readouterr()
        assert "PATH:" in captured.out

    def test_prints_pwd(self, capsys):
        """Test that function prints current working directory."""
        from iwfm.debug.print_env import print_env
        
        print_env()
        
        captured = capsys.readouterr()
        assert "pwd:" in captured.out

    def test_prints_pythonpath(self, capsys):
        """Test that function prints PYTHONPATH."""
        from iwfm.debug.print_env import print_env
        
        print_env()
        
        captured = capsys.readouterr()
        assert "PYTHONPATH:" in captured.out

    def test_returns_none(self):
        """Test that function returns None."""
        from iwfm.debug.print_env import print_env
        
        result = print_env()
        
        assert result is None

    def test_contains_version_info(self, capsys):
        """Test that output contains version information."""
        from iwfm.debug.print_env import print_env
        
        print_env()
        
        captured = capsys.readouterr()
        assert "version" in captured.out


class TestPrintEnvImports:
    """Tests for print_env imports."""

    def test_import_from_debug(self):
        """Test import from iwfm.debug."""
        from iwfm.debug import print_env
        assert callable(print_env)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.debug.print_env import print_env
        assert callable(print_env)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.debug.print_env import print_env
        
        assert print_env.__doc__ is not None
        assert 'environment' in print_env.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
