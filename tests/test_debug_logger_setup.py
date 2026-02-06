# test_debug_logger_setup.py
# Tests for debug/logger_setup.py - Setup loguru logger
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
import os
from datetime import datetime


class TestSetupDebugLogger:
    """Tests for setup_debug_logger function."""

    def test_function_exists(self):
        """Test that setup_debug_logger function exists."""
        from iwfm.debug.logger_setup import setup_debug_logger
        
        assert callable(setup_debug_logger)

    def test_returns_log_filename(self, tmp_path, monkeypatch):
        """Test that function returns a log filename."""
        from iwfm.debug.logger_setup import setup_debug_logger
        
        # Change to temp directory to avoid cluttering
        monkeypatch.chdir(tmp_path)
        
        result = setup_debug_logger("test_prefix")
        
        assert isinstance(result, str)
        assert result.endswith('.log')

    def test_filename_contains_prefix(self, tmp_path, monkeypatch):
        """Test that filename contains the specified prefix."""
        from iwfm.debug.logger_setup import setup_debug_logger
        
        monkeypatch.chdir(tmp_path)
        
        result = setup_debug_logger("my_custom_prefix")
        
        assert "my_custom_prefix" in result

    def test_filename_contains_timestamp(self, tmp_path, monkeypatch):
        """Test that filename contains a timestamp."""
        from iwfm.debug.logger_setup import setup_debug_logger
        
        monkeypatch.chdir(tmp_path)
        
        before = datetime.now().strftime("%Y%m%d")
        result = setup_debug_logger("test")
        
        # Should contain date portion of timestamp
        assert before in result

    def test_creates_log_file(self, tmp_path, monkeypatch):
        """Test that function creates a log file."""
        from iwfm.debug.logger_setup import setup_debug_logger
        
        monkeypatch.chdir(tmp_path)
        
        log_filename = setup_debug_logger("test_create")
        
        assert os.path.exists(log_filename)

    def test_auto_prefix_when_none(self, tmp_path, monkeypatch):
        """Test that function auto-detects prefix when None."""
        from iwfm.debug.logger_setup import setup_debug_logger
        
        monkeypatch.chdir(tmp_path)
        
        # Should not raise error
        result = setup_debug_logger(None)
        
        assert isinstance(result, str)
        assert result.endswith('.log')


class TestLoggerImport:
    """Tests for logger import."""

    def test_logger_importable(self):
        """Test that logger can be imported."""
        from iwfm.debug.logger_setup import logger
        
        assert logger is not None

    def test_logger_has_methods(self):
        """Test that logger has standard logging methods."""
        from iwfm.debug.logger_setup import logger
        
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'critical')


class TestLoggerSetupImports:
    """Tests for logger_setup module imports."""

    def test_import_setup_debug_logger(self):
        """Test importing setup_debug_logger."""
        from iwfm.debug.logger_setup import setup_debug_logger
        assert callable(setup_debug_logger)

    def test_import_logger(self):
        """Test importing logger."""
        from iwfm.debug.logger_setup import logger
        assert logger is not None

    def test_import_from_debug_package(self):
        """Test importing from iwfm.debug."""
        from iwfm.debug import logger_setup
        assert hasattr(logger_setup, 'setup_debug_logger')
        assert hasattr(logger_setup, 'logger')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
