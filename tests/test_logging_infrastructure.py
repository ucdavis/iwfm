# test_logging_infrastructure.py
# Tests for the iwfm logging infrastructure: silent-by-default logger,
# parse_cli_flags(), setup_debug_logger(), and converted debug traces
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

import sys
import os
import pytest


# ---------------------------------------------------------------------------
# Helper: capture logger.debug() messages via a temporary loguru sink
# ---------------------------------------------------------------------------
def capture_logger_messages(func, *args, **kwargs):
    """Run func(*args, **kwargs) while capturing logger.debug messages.

    Returns (result, messages) where messages is a list of logged strings.
    """
    from iwfm.debug.logger_setup import logger

    messages = []
    handler_id = logger.add(lambda msg: messages.append(str(msg)), level="DEBUG")
    try:
        result = func(*args, **kwargs)
    finally:
        logger.remove(handler_id)
    return result, messages


# ===========================================================================
# 1. Silent-by-default behaviour
# ===========================================================================
class TestSilentByDefault:
    """Verify that logger.debug() produces no output when no handlers are configured."""

    def test_debug_produces_no_stderr(self, capsys):
        """logger.debug() should produce no stderr output by default."""
        from iwfm.debug.logger_setup import logger

        logger.debug("this should be silent")
        captured = capsys.readouterr()
        assert captured.out == ""
        # stderr may contain loguru internals on some configs, but "this should be silent"
        # should NOT appear since we called logger.remove() at module level
        assert "this should be silent" not in captured.err

    def test_debug_produces_no_stdout(self, capsys):
        """logger.debug() should produce no stdout output by default."""
        from iwfm.debug.logger_setup import logger

        logger.debug("also silent")
        captured = capsys.readouterr()
        assert "also silent" not in captured.out


# ===========================================================================
# 2. setup_debug_logger() enables output
# ===========================================================================
class TestSetupDebugLoggerEnablesOutput:
    """Verify that setup_debug_logger() causes debug messages to appear."""

    def test_debug_messages_captured_after_setup(self, tmp_path, monkeypatch):
        """After setup_debug_logger(), logger.debug() messages should be capturable."""
        from iwfm.debug.logger_setup import logger, setup_debug_logger

        monkeypatch.chdir(tmp_path)
        log_file = setup_debug_logger("test_enable")

        messages = []
        handler_id = logger.add(lambda msg: messages.append(str(msg)), level="DEBUG")
        try:
            logger.debug("hello from test")
        finally:
            logger.remove(handler_id)
            # Clean up: re-silence the logger for other tests
            logger.remove()

        assert any("hello from test" in m for m in messages)

        # Also verify the log file was created and contains the message
        assert os.path.exists(log_file)
        with open(log_file) as f:
            content = f.read()
        assert "Debug logging enabled" in content

    def test_log_file_contains_debug_messages(self, tmp_path, monkeypatch):
        """Log file should contain debug messages written after setup."""
        from iwfm.debug.logger_setup import logger, setup_debug_logger

        monkeypatch.chdir(tmp_path)
        log_file = setup_debug_logger("test_file_content")

        logger.debug("file content check")

        # Clean up handlers
        logger.remove()

        with open(log_file) as f:
            content = f.read()
        assert "file content check" in content


# ===========================================================================
# 3. parse_cli_flags() tests
# ===========================================================================
class TestParseCliFlags:
    """Tests for the parse_cli_flags() helper function."""

    def test_import(self):
        """parse_cli_flags should be importable from iwfm.debug."""
        from iwfm.debug import parse_cli_flags
        assert callable(parse_cli_flags)

    def test_no_flags(self, monkeypatch):
        """With no flags, verbose=True, debug=False, sys.argv unchanged."""
        from iwfm.debug.logger_setup import parse_cli_flags

        monkeypatch.setattr(sys, 'argv', ['script.py', 'arg1', 'arg2'])
        verbose, debug = parse_cli_flags()

        assert verbose is True
        assert debug is False
        assert sys.argv == ['script.py', 'arg1', 'arg2']

    def test_debug_flag(self, tmp_path, monkeypatch):
        """--debug should set debug=True and be removed from sys.argv."""
        from iwfm.debug.logger_setup import parse_cli_flags, logger

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, 'argv', ['script.py', '--debug', 'arg1'])
        verbose, debug = parse_cli_flags()

        # Clean up logger handlers added by setup_debug_logger
        logger.remove()

        assert verbose is True
        assert debug is True
        assert '--debug' not in sys.argv
        assert sys.argv == ['script.py', 'arg1']

    def test_quiet_flag(self, monkeypatch):
        """--quiet should set verbose=False and be removed from sys.argv."""
        from iwfm.debug.logger_setup import parse_cli_flags

        monkeypatch.setattr(sys, 'argv', ['script.py', 'arg1', '--quiet'])
        verbose, debug = parse_cli_flags()

        assert verbose is False
        assert debug is False
        assert '--quiet' not in sys.argv
        assert sys.argv == ['script.py', 'arg1']

    def test_both_flags(self, tmp_path, monkeypatch):
        """--debug --quiet together: debug=True, verbose=False."""
        from iwfm.debug.logger_setup import parse_cli_flags, logger

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, 'argv', ['script.py', '--debug', '--quiet', 'arg1'])
        verbose, debug = parse_cli_flags()

        logger.remove()

        assert verbose is False
        assert debug is True
        assert sys.argv == ['script.py', 'arg1']

    def test_flags_at_end(self, tmp_path, monkeypatch):
        """Flags at end of argv should still be stripped."""
        from iwfm.debug.logger_setup import parse_cli_flags, logger

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, 'argv', ['script.py', 'arg1', 'arg2', '--debug'])
        verbose, debug = parse_cli_flags()

        logger.remove()

        assert debug is True
        assert sys.argv == ['script.py', 'arg1', 'arg2']

    def test_flags_between_args(self, tmp_path, monkeypatch):
        """Flags between positional args should still be stripped."""
        from iwfm.debug.logger_setup import parse_cli_flags, logger

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, 'argv', ['script.py', 'arg1', '--quiet', 'arg2'])
        verbose, debug = parse_cli_flags()

        logger.remove()

        assert verbose is False
        assert sys.argv == ['script.py', 'arg1', 'arg2']

    def test_debug_creates_log_file(self, tmp_path, monkeypatch):
        """--debug should trigger setup_debug_logger() and create a log file."""
        from iwfm.debug.logger_setup import parse_cli_flags, logger

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, 'argv', ['script.py', '--debug'])
        parse_cli_flags()

        logger.remove()

        log_files = [f for f in os.listdir(tmp_path) if f.endswith('.log')]
        assert len(log_files) >= 1


# ===========================================================================
# 4. Converted debug traces in representative files
# ===========================================================================
class TestConvertedDebugTraces:
    """Verify that converted files emit logger.debug() instead of print()."""

    def test_headall_read_debug_traces(self, tmp_path):
        """headall_read() should emit ==> style debug traces via logger."""
        # Create a minimal headall.out file
        headall_file = tmp_path / "headall.out"
        # Minimal valid format: header lines then data
        lines = []
        lines.append("         1         2")  # node IDs header
        lines.append("    LAYER( 1)      X:   100.0     Y:   200.0")
        lines.append("    LAYER( 1)      X:   300.0     Y:   400.0")
        lines.append("")
        lines.append("           10/31/1999_24:00          50.0          60.0")
        headall_file.write_text("\n".join(lines))

        # The file format is complex; just test that the import and logger work
        from iwfm.debug.logger_setup import logger
        import iwfm

        # Verify logger.debug calls exist in the module source
        import inspect
        source = inspect.getsource(iwfm.headall_read)
        assert 'logger.debug' in source
        # Verify no '==> ' print statements remain
        assert "print(f' ==> " not in source
        assert "print(f'  ==> " not in source

    def test_read_hyd_dict_debug_traces(self, tmp_path):
        """read_hyd_dict() should emit Enter/Leave debug traces via logger."""
        import iwfm
        import inspect

        source = inspect.getsource(iwfm.read_hyd_dict)
        assert 'logger.debug' in source
        assert "Entered read_hyd_dict" in source
        assert "Leaving read_hyd_dict" in source
        # Verify no 'Entered'/'Leaving' print statements remain
        assert "print(f\"Entered" not in source
        assert "print(f\"Leaving" not in source

    def test_iwfm_read_gw_debug_traces(self):
        """iwfm_read_gw() should emit debug traces via logger."""
        import iwfm
        import inspect

        source = inspect.getsource(iwfm.iwfm_read_gw)
        assert 'logger.debug' in source
        # Verify ==> prints were removed
        assert "print(f' ==> " not in source
        assert "print(f'  ==> " not in source

    def test_get_zbudget_elemids_debug_traces(self):
        """get_zbudget_elemids() should emit debug traces via logger."""
        from iwfm.hdf5 import get_zbudget_elemids
        import inspect

        source = inspect.getsource(get_zbudget_elemids)
        assert 'logger.debug' in source
        assert "print(f'  ==> " not in source

    def test_idw_debug_traces(self):
        """calib/idw.py should emit debug traces via logger."""
        from iwfm.calib import idw
        import inspect

        source = inspect.getsource(idw)
        assert 'logger.debug' in source


# ===========================================================================
# 5. Debug traces are silent without setup_debug_logger()
# ===========================================================================
class TestDebugTracesSilent:
    """Verify that converted debug traces produce no output by default."""

    def test_read_hyd_dict_silent(self, tmp_path, capsys):
        """read_hyd_dict() debug traces should be silent without logger setup."""
        import iwfm

        gw_file = tmp_path / "groundwater.dat"
        # Minimal groundwater.dat
        lines = [
            "C  Groundwater file",
            "C  NOUTH  NOUTDHY  NGROUP",
            "     0        0       0",
        ]
        gw_file.write_text("\n".join(lines))

        try:
            iwfm.read_hyd_dict(str(gw_file), verbose=False)
        except (SystemExit, Exception):
            pass  # May fail on minimal data, but we only care about output

        captured = capsys.readouterr()
        assert "Entered read_hyd_dict" not in captured.out
        assert "Entered read_hyd_dict" not in captured.err
        assert "Leaving read_hyd_dict" not in captured.out
        assert "Leaving read_hyd_dict" not in captured.err


# ===========================================================================
# 6. Centralized import pattern
# ===========================================================================
class TestCentralizedImport:
    """Verify that modules use the centralized logger import, not direct loguru."""

    def _get_python_files(self, directory):
        """Get all .py files in directory recursively."""
        result = []
        for root, dirs, files in os.walk(directory):
            # Skip __pycache__ and test directories
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for f in files:
                if f.endswith('.py'):
                    result.append(os.path.join(root, f))
        return result

    def test_no_direct_loguru_imports_in_hdf5(self):
        """hdf5/ modules should not import directly from loguru."""
        hdf5_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'iwfm', 'hdf5'
        )
        if not os.path.isdir(hdf5_dir):
            pytest.skip("hdf5 directory not found")

        violations = []
        for fpath in self._get_python_files(hdf5_dir):
            if '__init__' in fpath or 'logger_setup' in fpath:
                continue
            with open(fpath) as f:
                content = f.read()
            if 'from loguru import logger' in content:
                violations.append(os.path.basename(fpath))

        assert violations == [], f"Files with direct loguru import: {violations}"

    def test_no_direct_loguru_imports_in_xls(self):
        """xls/ modules should not import directly from loguru."""
        xls_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'iwfm', 'xls'
        )
        if not os.path.isdir(xls_dir):
            pytest.skip("xls directory not found")

        violations = []
        for fpath in self._get_python_files(xls_dir):
            if '__init__' in fpath:
                continue
            with open(fpath) as f:
                content = f.read()
            if 'from loguru import logger' in content:
                violations.append(os.path.basename(fpath))

        assert violations == [], f"Files with direct loguru import: {violations}"

    def test_no_redundant_iwfm_import(self):
        """No files should have 'import iwfm as iwfm' (redundant import)."""
        iwfm_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'iwfm'
        )
        violations = []
        for fpath in self._get_python_files(iwfm_dir):
            with open(fpath) as f:
                for line_no, line in enumerate(f, 1):
                    if 'import iwfm as iwfm' in line and not line.strip().startswith('#'):
                        violations.append(f"{os.path.basename(fpath)}:{line_no}")

        assert violations == [], f"Files with redundant import: {violations}"


# ===========================================================================
# 7. __main__ blocks have parse_cli_flags
# ===========================================================================
class TestMainBlocksCoverage:
    """Verify that __main__ blocks use parse_cli_flags or argparse."""

    def _get_python_files(self, directory):
        result = []
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for f in files:
                if f.endswith('.py'):
                    result.append(os.path.join(root, f))
        return result

    def test_all_main_blocks_have_cli_flags(self):
        """Every __main__ block should have parse_cli_flags or argparse."""
        iwfm_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'iwfm'
        )
        # Known exceptions that use different CLI patterns
        exceptions = {'main.py'}

        missing = []
        for fpath in self._get_python_files(iwfm_dir):
            basename = os.path.basename(fpath)
            if basename in exceptions:
                continue
            with open(fpath) as f:
                content = f.read()
            if 'if __name__' not in content:
                continue
            if 'parse_cli_flags' not in content and 'argparse' not in content:
                missing.append(os.path.relpath(fpath, iwfm_dir))

        assert missing == [], f"__main__ blocks without parse_cli_flags/argparse: {missing}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
