# test_debug_module.py
# Tests for the debug module structure and package-level imports
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


class TestDebugModuleStructure:
    """Tests for debug module structure."""

    def test_debug_package_exists(self):
        """Test that iwfm.debug package exists."""
        import iwfm.debug
        assert iwfm.debug is not None

    def test_debug_has_check_key(self):
        """Test that debug module exports check_key."""
        import iwfm.debug as debug
        assert hasattr(debug, 'check_key')

    def test_debug_has_exe_time(self):
        """Test that debug module exports exe_time."""
        import iwfm.debug as debug
        assert hasattr(debug, 'exe_time')

    def test_debug_has_print_dict(self):
        """Test that debug module exports print_dict."""
        import iwfm.debug as debug
        assert hasattr(debug, 'print_dict')

    def test_debug_has_print_env(self):
        """Test that debug module exports print_env."""
        import iwfm.debug as debug
        assert hasattr(debug, 'print_env')

    def test_debug_has_print_exe_time(self):
        """Test that debug module exports print_exe_time."""
        import iwfm.debug as debug
        assert hasattr(debug, 'print_exe_time')

    def test_debug_has_test_dict(self):
        """Test that debug module exports test_dict."""
        import iwfm.debug as debug
        assert hasattr(debug, 'test_dict')

    def test_debug_has_this_python(self):
        """Test that debug module exports this_python."""
        import iwfm.debug as debug
        assert hasattr(debug, 'this_python')

    def test_debug_has_this_sys(self):
        """Test that debug module exports this_sys."""
        import iwfm.debug as debug
        assert hasattr(debug, 'this_sys')

    def test_debug_has_this_sys_version(self):
        """Test that debug module exports this_sys_version."""
        import iwfm.debug as debug
        assert hasattr(debug, 'this_sys_version')


class TestDebugFunctionsCallable:
    """Tests that all debug functions are callable."""

    def test_check_key_callable(self):
        """Test that check_key is callable."""
        import iwfm.debug as debug
        assert callable(debug.check_key)

    def test_exe_time_callable(self):
        """Test that exe_time is callable."""
        import iwfm.debug as debug
        assert callable(debug.exe_time)

    def test_print_dict_callable(self):
        """Test that print_dict is callable."""
        import iwfm.debug as debug
        assert callable(debug.print_dict)

    def test_print_env_callable(self):
        """Test that print_env is callable."""
        import iwfm.debug as debug
        assert callable(debug.print_env)

    def test_print_exe_time_callable(self):
        """Test that print_exe_time is callable."""
        import iwfm.debug as debug
        assert callable(debug.print_exe_time)

    def test_test_dict_callable(self):
        """Test that test_dict is callable."""
        import iwfm.debug as debug
        assert callable(debug.test_dict)

    def test_this_python_callable(self):
        """Test that this_python is callable."""
        import iwfm.debug as debug
        assert callable(debug.this_python)

    def test_this_sys_callable(self):
        """Test that this_sys is callable."""
        import iwfm.debug as debug
        assert callable(debug.this_sys)

    def test_this_sys_version_callable(self):
        """Test that this_sys_version is callable."""
        import iwfm.debug as debug
        assert callable(debug.this_sys_version)


class TestDebugSubmodules:
    """Tests for debug submodules."""

    def test_check_key_module(self):
        """Test that check_key module exists."""
        import iwfm.debug.check_key
        assert iwfm.debug.check_key is not None

    def test_exe_time_module(self):
        """Test that exe_time module exists."""
        import iwfm.debug.exe_time
        assert iwfm.debug.exe_time is not None

    def test_logger_setup_module(self):
        """Test that logger_setup module exists."""
        import iwfm.debug.logger_setup
        assert iwfm.debug.logger_setup is not None

    def test_print_dict_module(self):
        """Test that print_dict module exists."""
        import iwfm.debug.print_dict
        assert iwfm.debug.print_dict is not None

    def test_print_env_module(self):
        """Test that print_env module exists."""
        import iwfm.debug.print_env
        assert iwfm.debug.print_env is not None

    def test_print_exe_time_module(self):
        """Test that print_exe_time module exists."""
        import iwfm.debug.print_exe_time
        assert iwfm.debug.print_exe_time is not None

    def test_test_dict_module(self):
        """Test that test_dict module exists."""
        import iwfm.debug.test_dict
        assert iwfm.debug.test_dict is not None

    def test_timer_module(self):
        """Test that timer module exists."""
        import iwfm.debug.timer
        assert iwfm.debug.timer is not None

    def test_this_python_module(self):
        """Test that this_python module exists."""
        import iwfm.debug.this_python
        assert iwfm.debug.this_python is not None

    def test_this_sys_module(self):
        """Test that this_sys module exists."""
        import iwfm.debug.this_sys
        assert iwfm.debug.this_sys is not None

    def test_this_sys_version_module(self):
        """Test that this_sys_version module exists."""
        import iwfm.debug.this_sys_version
        assert iwfm.debug.this_sys_version is not None


class TestDebugIntegration:
    """Integration tests for debug functions working together."""

    def test_system_info_functions(self):
        """Test that system info functions work together."""
        import iwfm.debug as debug
        
        python_version = debug.this_python()
        os_name = debug.this_sys()
        os_version = debug.this_sys_version()
        
        assert isinstance(python_version, str)
        assert isinstance(os_name, str)
        assert isinstance(os_version, str)

    def test_dictionary_functions(self, capsys):
        """Test that dictionary functions work together."""
        import iwfm.debug as debug
        
        d = {"key1": "value1", "key2": "value2"}
        
        # Check key presence
        assert debug.check_key(d, "key1") is True
        assert debug.check_key(d, "missing") is False
        
        # Print dictionary
        debug.print_dict(d)
        captured = capsys.readouterr()
        assert "key1" in captured.out
        
        # Test dictionary value
        debug.test_dict("test_d", d, "key1")
        captured = capsys.readouterr()
        assert "value1" in captured.out


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
