# test_ftp_fetch.py
# unit test for ftp_fetch function in the iwfm package
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
from pathlib import Path
from unittest.mock import Mock, patch, mock_open, MagicMock
import ftplib
import socket

import iwfm.util


# ============================================================================
# Test successful FTP download
# ============================================================================

def test_ftp_fetch_successful_download(tmp_path):
    '''Test successful file download via FTP.'''
    # Change to tmp directory for test
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Mock FTP connection
        mock_ftp = Mock(spec=ftplib.FTP)

        # Mock the file writing
        test_content = b'test file content'

        def mock_retrbinary(cmd, callback):
            callback(test_content)

        mock_ftp.retrbinary = mock_retrbinary

        with patch('ftplib.FTP', return_value=mock_ftp):
            iwfm.util.ftp_fetch('ftp.example.com', '/pub/data', 'test.txt', verbose=False)

        # Verify FTP methods were called
        mock_ftp.login.assert_called_once()
        mock_ftp.cwd.assert_called_once_with('/pub/data')
        mock_ftp.quit.assert_called()

        # Verify file was created
        output_file = tmp_path / 'test.txt'
        assert output_file.exists()
        assert output_file.read_bytes() == test_content

    finally:
        os.chdir(original_cwd)


def test_ftp_fetch_verbose_mode(tmp_path, capsys):
    '''Test that verbose mode produces output.'''
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        mock_ftp = Mock(spec=ftplib.FTP)

        def mock_retrbinary(cmd, callback):
            callback(b'test')

        mock_ftp.retrbinary = mock_retrbinary

        with patch('ftplib.FTP', return_value=mock_ftp):
            iwfm.util.ftp_fetch('ftp.example.com', '/pub', 'file.txt', verbose=True)

        captured = capsys.readouterr()
        assert 'Downloaded' in captured.out
        assert 'file.txt' in captured.out

    finally:
        os.chdir(original_cwd)


# ============================================================================
# Test connection errors
# ============================================================================

def test_ftp_fetch_connection_failed():
    '''Test error when FTP server connection fails.'''
    with patch('ftplib.FTP', side_effect=socket.gaierror('Name resolution failed')):
        with pytest.raises(ConnectionError, match='Failed to resolve FTP server address'):
            iwfm.util.ftp_fetch('invalid.server.com', '/pub', 'file.txt')


def test_ftp_fetch_connection_timeout():
    '''Test error when FTP server connection times out.'''
    with patch('ftplib.FTP', side_effect=socket.timeout('Connection timed out')):
        with pytest.raises(ConnectionError, match='Connection to FTP server .* timed out'):
            iwfm.util.ftp_fetch('ftp.example.com', '/pub', 'file.txt')


def test_ftp_fetch_connection_refused():
    '''Test error when FTP server refuses connection.'''
    with patch('ftplib.FTP', side_effect=OSError('Connection refused')):
        with pytest.raises(ConnectionError, match='Failed to connect to FTP server'):
            iwfm.util.ftp_fetch('ftp.example.com', '/pub', 'file.txt')


# ============================================================================
# Test authentication errors
# ============================================================================

def test_ftp_fetch_login_failed():
    '''Test error when FTP login fails.'''
    mock_ftp = Mock(spec=ftplib.FTP)
    mock_ftp.login.side_effect = ftplib.error_perm('530 Login incorrect')

    with patch('ftplib.FTP', return_value=mock_ftp):
        with pytest.raises(PermissionError, match='FTP login failed'):
            iwfm.util.ftp_fetch('ftp.example.com', '/pub', 'file.txt')

    # Verify cleanup was called
    mock_ftp.quit.assert_called()


# ============================================================================
# Test file/directory not found errors
# ============================================================================

def test_ftp_fetch_directory_not_found():
    '''Test error when FTP directory doesn't exist.'''
    mock_ftp = Mock(spec=ftplib.FTP)
    mock_ftp.cwd.side_effect = ftplib.error_perm('550 Directory not found')

    with patch('ftplib.FTP', return_value=mock_ftp):
        with pytest.raises(FileNotFoundError, match='FTP directory not found'):
            iwfm.util.ftp_fetch('ftp.example.com', '/invalid/path', 'file.txt')

    mock_ftp.quit.assert_called()


def test_ftp_fetch_file_not_found(tmp_path):
    '''Test error when FTP file doesn't exist.'''
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        mock_ftp = Mock(spec=ftplib.FTP)
        mock_ftp.retrbinary.side_effect = ftplib.error_perm('550 File not found')

        with patch('ftplib.FTP', return_value=mock_ftp):
            with pytest.raises(FileNotFoundError, match='FTP file not found'):
                iwfm.util.ftp_fetch('ftp.example.com', '/pub', 'missing.txt')

        mock_ftp.quit.assert_called()

    finally:
        os.chdir(original_cwd)


# ============================================================================
# Test local file write errors
# ============================================================================

def test_ftp_fetch_write_failed(tmp_path):
    '''Test error when local file write fails.'''
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        mock_ftp = Mock(spec=ftplib.FTP)

        # Mock open() to raise an error when trying to write file
        with patch('ftplib.FTP', return_value=mock_ftp):
            with patch('builtins.open', side_effect=PermissionError('Permission denied')):
                with pytest.raises(IOError, match='Failed to write file'):
                    iwfm.util.ftp_fetch('ftp.example.com', '/pub', 'file.txt')

        mock_ftp.quit.assert_called()

    finally:
        os.chdir(original_cwd)


# ============================================================================
# Test cleanup behavior (bare except clause fix)
# ============================================================================

def test_ftp_fetch_cleanup_on_success(tmp_path):
    '''Test that FTP connection is properly closed on success.'''
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        mock_ftp = Mock(spec=ftplib.FTP)

        def mock_retrbinary(cmd, callback):
            callback(b'test')

        mock_ftp.retrbinary = mock_retrbinary

        with patch('ftplib.FTP', return_value=mock_ftp):
            iwfm.util.ftp_fetch('ftp.example.com', '/pub', 'file.txt')

        # quit() should be called in finally block
        assert mock_ftp.quit.call_count >= 1

    finally:
        os.chdir(original_cwd)


def test_ftp_fetch_cleanup_handles_quit_errors(tmp_path):
    '''Test that errors during FTP quit are silently ignored.'''
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        mock_ftp = Mock(spec=ftplib.FTP)

        def mock_retrbinary(cmd, callback):
            callback(b'test')

        mock_ftp.retrbinary = mock_retrbinary

        # Make quit() raise an error in finally block
        mock_ftp.quit.side_effect = [None, ftplib.error_temp('421 Service not available')]

        with patch('ftplib.FTP', return_value=mock_ftp):
            # Should not raise exception even though quit() fails
            iwfm.util.ftp_fetch('ftp.example.com', '/pub', 'file.txt')

        # Verify file was still created
        assert (tmp_path / 'file.txt').exists()

    finally:
        os.chdir(original_cwd)


def test_ftp_fetch_cleanup_handles_eoferror(tmp_path):
    '''Test that EOFError during quit is handled gracefully.'''
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        mock_ftp = Mock(spec=ftplib.FTP)

        def mock_retrbinary(cmd, callback):
            callback(b'test')

        mock_ftp.retrbinary = mock_retrbinary
        mock_ftp.quit.side_effect = [None, EOFError('Connection closed')]

        with patch('ftplib.FTP', return_value=mock_ftp):
            iwfm.util.ftp_fetch('ftp.example.com', '/pub', 'file.txt')

        assert (tmp_path / 'file.txt').exists()

    finally:
        os.chdir(original_cwd)


# ============================================================================
# Test default parameter values
# ============================================================================

def test_ftp_fetch_default_filename(tmp_path):
    '''Test that default filename is used correctly.'''
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        mock_ftp = Mock(spec=ftplib.FTP)

        def mock_retrbinary(cmd, callback):
            callback(b'default content')

        mock_ftp.retrbinary = mock_retrbinary

        with patch('ftplib.FTP', return_value=mock_ftp):
            # Don't specify filename - should use default 'download.txt'
            iwfm.util.ftp_fetch('ftp.example.com', '/pub')

        # Verify default filename was used
        assert (tmp_path / 'download.txt').exists()

    finally:
        os.chdir(original_cwd)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
