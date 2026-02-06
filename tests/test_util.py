# test_util.py
# unit tests for utility functions in the iwfm.util package
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

import os
import tempfile
import zipfile
import pytest
from unittest.mock import patch, MagicMock


# --------------------------------------------------------------------------
# Tests for ftp_fetch
# --------------------------------------------------------------------------

def test_ftp_fetch_import():
    """Test that ftp_fetch can be imported from iwfm.util."""
    from iwfm.util import ftp_fetch
    assert callable(ftp_fetch)


def test_ftp_fetch_direct_import():
    """Test direct import from ftp_fetch module."""
    from iwfm.util.ftp_fetch import ftp_fetch
    assert callable(ftp_fetch)


@patch('ftplib.FTP')
def test_ftp_fetch_successful_download(mock_ftp_class, tmp_path, monkeypatch):
    """Test successful FTP download."""
    from iwfm.util.ftp_fetch import ftp_fetch

    # Setup mock FTP connection
    mock_ftp = MagicMock()
    mock_ftp_class.return_value = mock_ftp

    # Mock retrbinary to write test data to file
    def mock_retrbinary(cmd, callback):
        callback(b'test file content')
    mock_ftp.retrbinary.side_effect = mock_retrbinary

    monkeypatch.chdir(tmp_path)
    ftp_fetch('ftp.example.com', '/pub/data', 'test.txt')

    # Verify FTP methods were called
    mock_ftp_class.assert_called_once_with('ftp.example.com')
    mock_ftp.login.assert_called_once()
    mock_ftp.cwd.assert_called_once_with('/pub/data')

    # Verify file was created
    assert (tmp_path / 'test.txt').exists()
    with open(tmp_path / 'test.txt', 'rb') as f:
        assert f.read() == b'test file content'


@patch('ftplib.FTP')
def test_ftp_fetch_connection_error(mock_ftp_class):
    """Test FTP connection error handling."""
    from iwfm.util.ftp_fetch import ftp_fetch
    import socket

    mock_ftp_class.side_effect = socket.gaierror('Name resolution failed')

    with pytest.raises(ConnectionError) as exc_info:
        ftp_fetch('invalid.server.com', '/pub', 'test.txt')

    assert 'Failed to resolve FTP server address' in str(exc_info.value)


@patch('ftplib.FTP')
def test_ftp_fetch_permission_error(mock_ftp_class):
    """Test FTP login permission error."""
    from iwfm.util.ftp_fetch import ftp_fetch
    import ftplib

    mock_ftp = MagicMock()
    mock_ftp_class.return_value = mock_ftp
    mock_ftp.login.side_effect = ftplib.error_perm('530 Login incorrect')

    with pytest.raises(PermissionError) as exc_info:
        ftp_fetch('ftp.example.com', '/pub', 'test.txt')

    assert 'FTP login failed' in str(exc_info.value)


@patch('ftplib.FTP')
def test_ftp_fetch_directory_not_found(mock_ftp_class):
    """Test FTP directory not found error."""
    from iwfm.util.ftp_fetch import ftp_fetch
    import ftplib

    mock_ftp = MagicMock()
    mock_ftp_class.return_value = mock_ftp
    mock_ftp.cwd.side_effect = ftplib.error_perm('550 No such directory')

    with pytest.raises(FileNotFoundError) as exc_info:
        ftp_fetch('ftp.example.com', '/nonexistent', 'test.txt')

    assert 'FTP directory not found' in str(exc_info.value)


@patch('ftplib.FTP')
def test_ftp_fetch_file_not_found(mock_ftp_class, tmp_path, monkeypatch):
    """Test FTP file not found error."""
    from iwfm.util.ftp_fetch import ftp_fetch
    import ftplib

    mock_ftp = MagicMock()
    mock_ftp_class.return_value = mock_ftp
    mock_ftp.retrbinary.side_effect = ftplib.error_perm('550 File not found')

    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError) as exc_info:
        ftp_fetch('ftp.example.com', '/pub', 'nonexistent.txt')

    assert 'FTP file not found' in str(exc_info.value)


@patch('ftplib.FTP')
def test_ftp_fetch_verbose_output(mock_ftp_class, tmp_path, monkeypatch, capsys):
    """Test FTP fetch with verbose output."""
    from iwfm.util.ftp_fetch import ftp_fetch

    mock_ftp = MagicMock()
    mock_ftp_class.return_value = mock_ftp
    mock_ftp.retrbinary.side_effect = lambda cmd, cb: cb(b'content')

    monkeypatch.chdir(tmp_path)
    ftp_fetch('ftp.example.com', '/pub', 'test.txt', verbose=True)

    captured = capsys.readouterr()
    assert 'Downloaded' in captured.out
    assert 'test.txt' in captured.out


@patch('ftplib.FTP')
def test_ftp_fetch_default_filename(mock_ftp_class, tmp_path, monkeypatch):
    """Test FTP fetch with default filename."""
    from iwfm.util.ftp_fetch import ftp_fetch

    mock_ftp = MagicMock()
    mock_ftp_class.return_value = mock_ftp
    mock_ftp.retrbinary.side_effect = lambda cmd, cb: cb(b'content')

    monkeypatch.chdir(tmp_path)
    ftp_fetch('ftp.example.com', '/pub')

    # Default filename is 'download.txt'
    assert (tmp_path / 'download.txt').exists()


# --------------------------------------------------------------------------
# Tests for url_fetch
# --------------------------------------------------------------------------

def test_url_fetch_import():
    """Test that url_fetch can be imported from iwfm.util."""
    from iwfm.util import url_fetch
    assert callable(url_fetch)


def test_url_fetch_direct_import():
    """Test direct import from url_fetch module."""
    from iwfm.util.url_fetch import url_fetch
    assert callable(url_fetch)


@patch('requests.get')
def test_url_fetch_successful_download(mock_get):
    """Test successful URL download."""
    from iwfm.util.url_fetch import url_fetch

    # Setup mock response
    mock_response = MagicMock()
    mock_response.content = b'downloaded content'
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'test.txt')
        url_fetch('https://example.com/file.txt', filepath)

        # Verify request was made
        mock_get.assert_called_once()

        # Verify file was created
        assert os.path.exists(filepath)
        with open(filepath, 'rb') as f:
            assert f.read() == b'downloaded content'


def test_url_fetch_invalid_url():
    """Test url_fetch with invalid URL format."""
    from iwfm.util.url_fetch import url_fetch

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'test.txt')

        with pytest.raises(ValueError) as exc_info:
            url_fetch('not-a-valid-url', filepath)

        assert "url must start with" in str(exc_info.value)


def test_url_fetch_empty_url():
    """Test url_fetch with empty URL."""
    from iwfm.util.url_fetch import url_fetch

    with pytest.raises(ValueError) as exc_info:
        url_fetch('', 'test.txt')

    assert "url must be a non-empty string" in str(exc_info.value)


def test_url_fetch_empty_filename():
    """Test url_fetch with empty filename."""
    from iwfm.util.url_fetch import url_fetch

    with pytest.raises(ValueError) as exc_info:
        url_fetch('https://example.com/file.txt', '')

    assert "filename must be a non-empty string" in str(exc_info.value)


@patch('requests.get')
def test_url_fetch_timeout_error(mock_get):
    """Test url_fetch timeout handling."""
    from iwfm.util.url_fetch import url_fetch
    import requests

    mock_get.side_effect = requests.exceptions.Timeout()

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'test.txt')

        with pytest.raises(requests.exceptions.Timeout) as exc_info:
            url_fetch('https://example.com/file.txt', filepath, timeout=5)

        assert 'timed out' in str(exc_info.value)


@patch('requests.get')
def test_url_fetch_connection_error(mock_get):
    """Test url_fetch connection error handling."""
    from iwfm.util.url_fetch import url_fetch
    import requests

    mock_get.side_effect = requests.exceptions.ConnectionError('Connection refused')

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'test.txt')

        with pytest.raises(requests.exceptions.ConnectionError) as exc_info:
            url_fetch('https://example.com/file.txt', filepath)

        assert 'Failed to connect' in str(exc_info.value)


@patch('requests.get')
def test_url_fetch_http_error(mock_get):
    """Test url_fetch HTTP error handling."""
    from iwfm.util.url_fetch import url_fetch
    import requests

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.reason = 'Not Found'
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'test.txt')

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            url_fetch('https://example.com/notfound.txt', filepath)

        assert 'HTTP error 404' in str(exc_info.value)


@patch('requests.get')
def test_url_fetch_verbose_output(mock_get, capsys):
    """Test url_fetch with verbose output."""
    from iwfm.util.url_fetch import url_fetch

    mock_response = MagicMock()
    mock_response.content = b'content'
    mock_get.return_value = mock_response

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'test.txt')
        url_fetch('https://example.com/file.txt', filepath, verbose=True)

        captured = capsys.readouterr()
        assert 'Downloading from' in captured.out
        assert 'Saved to' in captured.out


# --------------------------------------------------------------------------
# Tests for zip_unzip
# --------------------------------------------------------------------------

def test_zip_unzip_import():
    """Test that zip_unzip can be imported from iwfm.util."""
    from iwfm.util import zip_unzip
    assert callable(zip_unzip)


def test_zip_unzip_direct_import():
    """Test direct import from zip_unzip module."""
    from iwfm.util.zip_unzip import zip_unzip
    assert callable(zip_unzip)


def test_zip_unzip_basic(tmp_path, monkeypatch):
    """Test basic zip file extraction."""
    from iwfm.util.zip_unzip import zip_unzip

    # Create a test zip file
    zip_path = tmp_path / 'test.zip'
    file1_content = b'content of file 1'
    file2_content = b'content of file 2'

    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr('file1.txt', file1_content)
        zf.writestr('file2.txt', file2_content)

    # Change to temp directory and extract
    monkeypatch.chdir(tmp_path)
    zip_unzip(str(zip_path))

    # Verify both files were extracted (this tests the fix for the [1:] bug)
    assert (tmp_path / 'file1.txt').exists(), "First file should be extracted"
    assert (tmp_path / 'file2.txt').exists(), "Second file should be extracted"

    with open(tmp_path / 'file1.txt', 'rb') as f:
        assert f.read() == file1_content
    with open(tmp_path / 'file2.txt', 'rb') as f:
        assert f.read() == file2_content


def test_zip_unzip_single_file(tmp_path, monkeypatch):
    """Test zip file with single file extraction."""
    from iwfm.util.zip_unzip import zip_unzip

    # Create a zip with single file
    zip_path = tmp_path / 'single.zip'
    file_content = b'single file content'

    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr('only_file.txt', file_content)

    # Extract
    monkeypatch.chdir(tmp_path)
    zip_unzip(str(zip_path))

    # Verify single file was extracted (would fail with old [1:] bug)
    assert (tmp_path / 'only_file.txt').exists(), "Single file should be extracted"
    with open(tmp_path / 'only_file.txt', 'rb') as f:
        assert f.read() == file_content


def test_zip_unzip_skips_directories(tmp_path, monkeypatch):
    """Test that zip_unzip skips directory entries."""
    from iwfm.util.zip_unzip import zip_unzip

    # Create a zip with a directory entry and file
    zip_path = tmp_path / 'with_dir.zip'

    with zipfile.ZipFile(zip_path, 'w') as zf:
        # Add a directory entry (ends with /)
        zf.writestr('subdir/', '')
        zf.writestr('file.txt', b'file content')

    monkeypatch.chdir(tmp_path)
    # Should not raise an error when encountering directory
    zip_unzip(str(zip_path))

    assert (tmp_path / 'file.txt').exists()


def test_zip_unzip_verbose(tmp_path, monkeypatch, capsys):
    """Test zip_unzip verbose output."""
    from iwfm.util.zip_unzip import zip_unzip

    zip_path = tmp_path / 'test.zip'

    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr('file.txt', b'content')

    monkeypatch.chdir(tmp_path)
    zip_unzip(str(zip_path), verbose=True)

    captured = capsys.readouterr()
    assert 'Unzipped' in captured.out
    assert 'test.zip' in captured.out


# --------------------------------------------------------------------------
# Tests for get_nwis
# --------------------------------------------------------------------------

def test_get_nwis_import():
    """Test that get_nwis can be imported from iwfm.util."""
    from iwfm.util import get_nwis
    assert callable(get_nwis)


def test_get_nwis_direct_import():
    """Test direct import from get_nwis module."""
    from iwfm.util.get_nwis import get_nwis
    assert callable(get_nwis)


def test_get_nwis_invalid_files_list():
    """Test get_nwis with invalid files list."""
    from iwfm.util.get_nwis import get_nwis

    with pytest.raises(ValueError) as exc_info:
        get_nwis([])

    assert "must be a non-empty list" in str(exc_info.value)


def test_get_nwis_invalid_files_type():
    """Test get_nwis with invalid files type."""
    from iwfm.util.get_nwis import get_nwis

    with pytest.raises(ValueError) as exc_info:
        get_nwis("not a list")

    assert "must be a non-empty list" in str(exc_info.value)


def test_parse_html_table():
    """Test parse_html_table function."""
    from iwfm.util.get_nwis import parse_html_table
    from bs4 import BeautifulSoup

    html = """
    <table>
        <tr><th>Date</th><th>Value</th></tr>
        <tr><td>2023-01</td><td>100</td></tr>
        <tr><td>2023-02</td><td>200</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    headers, rows = parse_html_table(table)

    assert headers == ['Date', 'Value']
    assert len(rows) == 2
    assert rows[0] == ['2023-01', '100']
    assert rows[1] == ['2023-02', '200']


def test_parse_html_table_empty():
    """Test parse_html_table with empty table."""
    from iwfm.util.get_nwis import parse_html_table
    from bs4 import BeautifulSoup

    html = "<table><tr><th>Header</th></tr></table>"
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    headers, rows = parse_html_table(table)

    assert headers == ['Header']
    assert rows == []


@patch('requests.get')
def test_get_nwis_skips_invalid_entries(mock_get, capsys):
    """Test that get_nwis skips invalid file entries."""
    from iwfm.util.get_nwis import get_nwis

    # Files list with invalid entry (missing URL)
    files = [
        ['Invalid Entry', 'Source'],  # Missing URL - should be skipped
    ]

    result = get_nwis(files)

    # Should return empty list since entry was skipped
    captured = capsys.readouterr()
    assert 'Skipping invalid' in captured.out


# --------------------------------------------------------------------------
# Tests for get_cdec
# --------------------------------------------------------------------------

def test_get_cdec_import():
    """Test that get_cdec can be imported from iwfm.util."""
    from iwfm.util import get_cdec
    assert callable(get_cdec)


def test_get_cdec_direct_import():
    """Test direct import from get_cdec module."""
    from iwfm.util.get_cdec import get_cdec
    assert callable(get_cdec)


def test_get_cdec_invalid_files_list():
    """Test get_cdec with invalid files list."""
    from iwfm.util.get_cdec import get_cdec

    with pytest.raises(ValueError) as exc_info:
        get_cdec([])

    assert "must be a non-empty list" in str(exc_info.value)


def test_get_cdec_invalid_files_type():
    """Test get_cdec with invalid files type."""
    from iwfm.util.get_cdec import get_cdec

    with pytest.raises(ValueError) as exc_info:
        get_cdec("not a list")

    assert "must be a non-empty list" in str(exc_info.value)


def test_cdec_parse_html_table():
    """Test parse_html_table function from get_cdec."""
    from iwfm.util.get_cdec import parse_html_table
    from bs4 import BeautifulSoup

    html = """
    <table>
        <tr><th>Date</th><th>Value</th></tr>
        <tr><td>2023-01-01</td><td>500</td></tr>
        <tr><td>2023-01-02</td><td>600</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    headers, rows = parse_html_table(table)

    assert headers == ['Date', 'Value']
    assert len(rows) == 2
    assert rows[0] == ['2023-01-01', '500']
    assert rows[1] == ['2023-01-02', '600']


# --------------------------------------------------------------------------
# Tests for get_usacoe
# --------------------------------------------------------------------------

def test_get_usacoe_import():
    """Test that get_usacoe can be imported from iwfm.util."""
    from iwfm.util import get_usacoe
    assert callable(get_usacoe)


def test_get_usacoe_direct_import():
    """Test direct import from get_usacoe module."""
    from iwfm.util.get_usacoe import get_usacoe
    assert callable(get_usacoe)


def test_get_usacoe_invalid_files_list():
    """Test get_usacoe with invalid files list."""
    from iwfm.util.get_usacoe import get_usacoe

    with pytest.raises(ValueError) as exc_info:
        get_usacoe([])

    assert "must be a non-empty list" in str(exc_info.value)


def test_get_usacoe_invalid_files_type():
    """Test get_usacoe with invalid files type."""
    from iwfm.util.get_usacoe import get_usacoe

    with pytest.raises(ValueError) as exc_info:
        get_usacoe("not a list")

    assert "must be a non-empty list" in str(exc_info.value)


def test_is_leap_year():
    """Test is_leap_year function."""
    from iwfm.util.get_usacoe import is_leap_year

    # Leap years
    assert is_leap_year(2000) is True   # divisible by 400
    assert is_leap_year(2004) is True   # divisible by 4, not by 100
    assert is_leap_year(2024) is True   # divisible by 4, not by 100

    # Non-leap years
    assert is_leap_year(1900) is False  # divisible by 100, not by 400
    assert is_leap_year(2001) is False  # not divisible by 4
    assert is_leap_year(2023) is False  # not divisible by 4


# --------------------------------------------------------------------------
# Tests for get_usbr
# --------------------------------------------------------------------------

def test_get_usbr_import():
    """Test that get_usbr can be imported from iwfm.util."""
    from iwfm.util import get_usbr
    assert callable(get_usbr)


def test_get_usbr_direct_import():
    """Test direct import from get_usbr module."""
    from iwfm.util.get_usbr import get_usbr
    assert callable(get_usbr)


def test_get_usbr_invalid_year():
    """Test get_usbr with invalid year format."""
    from iwfm.util.get_usbr import get_usbr

    with pytest.raises(ValueError) as exc_info:
        get_usbr('23', 'https://example.com/file.pdf')  # Not 4 digits

    assert "must be a 4-digit year" in str(exc_info.value)


def test_get_usbr_invalid_url():
    """Test get_usbr with invalid URL."""
    from iwfm.util.get_usbr import get_usbr

    with pytest.raises(ValueError) as exc_info:
        get_usbr('2023', 'not-a-url')

    assert "must start with 'http://'" in str(exc_info.value)


def test_get_usbr_empty_url():
    """Test get_usbr with empty URL."""
    from iwfm.util.get_usbr import get_usbr

    with pytest.raises(ValueError) as exc_info:
        get_usbr('2023', '')

    assert "must be a non-empty string" in str(exc_info.value)


def test_get_usbr_invalid_excel_filename():
    """Test get_usbr with invalid excel filename."""
    from iwfm.util.get_usbr import get_usbr

    with pytest.raises(ValueError) as exc_info:
        get_usbr('2023', 'https://example.com/file.pdf', excel_filename='')

    assert "excel_filename must be a non-empty string" in str(exc_info.value)


def test_is_year_in_list():
    """Test is_year_in_list function (from get_usbr module)."""
    from iwfm.util.get_usbr import is_year_in_list

    # Test when year is found
    string_list = ['Data for 2023', 'Other info', '2024 report']

    assert is_year_in_list('2023', string_list) == 0
    assert is_year_in_list('2024', string_list) == 2

    # Test when year is not found
    assert is_year_in_list('2025', string_list) == -1

    # Test with empty list
    assert is_year_in_list('2023', []) == -1


# --------------------------------------------------------------------------
# Tests for module-level imports
# --------------------------------------------------------------------------

def test_util_module_exports():
    """Test that iwfm.util exports all expected functions."""
    import iwfm.util as util

    # Check all expected exports are available
    assert hasattr(util, 'ftp_fetch')
    assert hasattr(util, 'url_fetch')
    assert hasattr(util, 'zip_unzip')
    assert hasattr(util, 'get_cdec')
    assert hasattr(util, 'get_nwis')
    assert hasattr(util, 'get_usacoe')
    assert hasattr(util, 'get_usbr')

    # Verify they are callable
    assert callable(util.ftp_fetch)
    assert callable(util.url_fetch)
    assert callable(util.zip_unzip)
    assert callable(util.get_cdec)
    assert callable(util.get_nwis)
    assert callable(util.get_usacoe)
    assert callable(util.get_usbr)


def test_util_docstrings():
    """Test that util functions have docstrings."""
    from iwfm.util import ftp_fetch, url_fetch, zip_unzip, get_cdec, get_nwis, get_usacoe, get_usbr

    assert ftp_fetch.__doc__ is not None
    assert url_fetch.__doc__ is not None
    assert zip_unzip.__doc__ is not None
    assert get_cdec.__doc__ is not None
    assert get_nwis.__doc__ is not None
    assert get_usacoe.__doc__ is not None
    assert get_usbr.__doc__ is not None


# --------------------------------------------------------------------------
# Tests for helper functions
# --------------------------------------------------------------------------

def test_save_table_as_csv():
    """Test save_table_as_csv function."""
    from iwfm.util.get_nwis import save_table_as_csv
    from bs4 import BeautifulSoup

    html = """
    <table>
        <tr><th>Date</th><th>Value</th></tr>
        <tr><td>2023-01</td><td>100</td></tr>
        <tr><td>2023-02</td><td>200</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'output.csv')
        save_table_as_csv(filepath, table)

        assert os.path.exists(filepath)
        with open(filepath, 'r') as f:
            content = f.read()
            assert 'Date' in content
            assert 'Value' in content
            assert '2023-01' in content


def test_save_table_as_csv_empty_table():
    """Test save_table_as_csv with empty table raises error."""
    from iwfm.util.get_nwis import save_table_as_csv
    from bs4 import BeautifulSoup

    html = "<table><tr><th>Header</th></tr></table>"
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'output.csv')

        with pytest.raises(ValueError) as exc_info:
            save_table_as_csv(filepath, table)

        assert "contains no data" in str(exc_info.value)


def test_add_data_function():
    """Test add_data function from get_usacoe."""
    from iwfm.util.get_usacoe import add_data

    # Create sample lines with data matching expected format
    # add_data expects specific line structure from USACOE reports
    # Lines at index 32 or 35 determine the length
    lines = [''] * 46  # Minimum 46 lines for add_data

    # For start=0, line[32] determines length
    lines[32] = "1  100  200  300  400  500  600"

    # Add data lines at positions 9-45 (line1 = lines[9:46])
    # add_data expects lines to have same format
    for i in range(9, 46):
        lines[i] = f"{i-8}  100  200  300  400  500  600"

    # Test with start=0 (Oct-Mar)
    result = add_data(lines[9:46], 0, "2024")

    assert isinstance(result, list)
    assert len(result) == 6  # 6 months


# --------------------------------------------------------------------------
# Tests for network error handling in get_nwis
# --------------------------------------------------------------------------

@patch('requests.get')
def test_get_nwis_network_timeout(mock_get, capsys):
    """Test get_nwis handles network timeout gracefully."""
    from iwfm.util.get_nwis import get_nwis
    import requests

    mock_get.side_effect = requests.exceptions.Timeout()

    files = [['Test', 'Source', 'https://example.com/data']]
    result = get_nwis(files)

    captured = capsys.readouterr()
    assert 'timed out' in captured.out


@patch('requests.get')
def test_get_nwis_connection_error(mock_get, capsys):
    """Test get_nwis handles connection error gracefully."""
    from iwfm.util.get_nwis import get_nwis
    import requests

    mock_get.side_effect = requests.exceptions.ConnectionError()

    files = [['Test', 'Source', 'https://example.com/data']]
    result = get_nwis(files)

    captured = capsys.readouterr()
    assert 'Connection error' in captured.out


@patch('requests.get')
def test_get_nwis_http_error(mock_get, capsys):
    """Test get_nwis handles HTTP error gracefully."""
    from iwfm.util.get_nwis import get_nwis
    import requests

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    files = [['Test', 'Source', 'https://example.com/data']]
    result = get_nwis(files)

    captured = capsys.readouterr()
    assert 'HTTP 500 error' in captured.out


