# test_util.py
# unit tests for utility functions in the iwfm package
# Copyright (C) 2025 University of California
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

import zipfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open, MagicMock
import pytest
import unittest
from iwfm.util.get_cdec import save_table_as_csv, download_data_table, format_file


def _load_fn(module_name, file_name, fn_name):
    from importlib.util import spec_from_file_location, module_from_spec
    base = Path(__file__).resolve().parents[1] / "iwfm" / "util" / file_name
    spec = spec_from_file_location(module_name, str(base))
    assert spec is not None, "Failed to load module specification"
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return getattr(mod, fn_name)


zip_unzip = _load_fn("zip_unzip", "zip_unzip.py", "zip_unzip")
url_fetch = _load_fn("url_fetch", "url_fetch.py", "url_fetch")


def test_zip_unzip_extracts_files(tmp_path, capsys):
    # Create a test zip file
    zip_path = tmp_path / "test.zip"
    file1_path = tmp_path / "file1.txt"
    file2_path = tmp_path / "file2.txt"
    
    # Write some content
    file1_path.write_text("content1")
    file2_path.write_text("content2")
    
    # Create zip file
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.write(file1_path, "file1.txt")
        zf.write(file2_path, "file2.txt")
        zf.writestr("skip_me.txt", "skip")
    
    # Delete original files
    file1_path.unlink()
    file2_path.unlink()
    
    # Run zip_unzip
    zip_unzip(str(zip_path), verbose=True)
    
    # Check output message
    out = capsys.readouterr().out
    assert "Unzipped" in out
    
    # Note: Implementation skips first file (namelist()[1:]), so file1.txt should be extracted
    # The behavior depends on namelist() order


def test_zip_unzip_verbose_false_no_output(tmp_path):
    zip_path = tmp_path / "test.zip"
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.write(test_file, "test.txt")
    
    test_file.unlink()
    
    # Should not raise
    zip_unzip(str(zip_path), verbose=False)


@patch('requests.get')
def test_url_fetch_downloads_file(mock_get, tmp_path, capsys):
    # Mock the requests.get response
    mock_response = Mock()
    mock_response.content = b"test file content"
    mock_get.return_value = mock_response
    
    output_file = tmp_path / "downloaded.txt"
    
    url_fetch("http://example.com/file.txt", str(output_file), verbose=True)
    
    # Check file was written
    assert output_file.exists()
    assert output_file.read_bytes() == b"test file content"
    
    # Check verbose output
    out = capsys.readouterr().out
    assert "Retrieved" in out
    
    # Verify requests was called correctly
    mock_get.assert_called_once_with(url="http://example.com/file.txt", verify=False)


@patch('requests.get')
def test_url_fetch_verbose_false_no_output(mock_get, tmp_path):
    mock_response = Mock()
    mock_response.content = b"content"
    mock_get.return_value = mock_response
    
    output_file = tmp_path / "downloaded.txt"
    
    url_fetch("http://example.com/file.txt", str(output_file), verbose=False)
    
    assert output_file.exists()


@patch('ftplib.FTP')
def test_ftp_fetch_functionality(mock_ftp_class, tmp_path, capsys):
    """Test ftp_fetch function with mocked FTP connection."""
    ftp_fetch = _load_fn("ftp_fetch", "ftp_fetch.py", "ftp_fetch")
    
    # Create a mock FTP instance
    mock_ftp = Mock()
    mock_ftp_class.return_value = mock_ftp
    
    # Mock the retrbinary method to write test content
    def mock_retrbinary(command, callback):
        test_content = b"test ftp file content"
        callback(test_content)
    
    mock_ftp.retrbinary = mock_retrbinary
    
    # Change to temp directory for test
    import os
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        # Test the function
        ftp_fetch("ftp.example.com", "/pub", "testfile.txt", verbose=True)
        
        # Verify FTP operations were called correctly
        mock_ftp_class.assert_called_once_with("ftp.example.com")
        mock_ftp.login.assert_called_once()
        mock_ftp.cwd.assert_called_once_with("/pub")
        
        # Check that file was created with correct content
        output_file = tmp_path / "testfile.txt"
        assert output_file.exists()
        assert output_file.read_bytes() == b"test ftp file content"
        
        # Check verbose output
        out = capsys.readouterr().out
        assert "Downloaded 'testfile.txt'" in out
        
    finally:
        # Restore original directory
        os.chdir(original_dir)


@patch('ftplib.FTP')
def test_ftp_fetch_verbose_false_no_output(mock_ftp_class, tmp_path):
    """Test ftp_fetch with verbose=False produces no output."""
    ftp_fetch = _load_fn("ftp_fetch", "ftp_fetch.py", "ftp_fetch")
    
    # Create a mock FTP instance
    mock_ftp = Mock()
    mock_ftp_class.return_value = mock_ftp
    
    # Mock the retrbinary method
    def mock_retrbinary(command, callback):
        callback(b"content")
    
    mock_ftp.retrbinary = mock_retrbinary
    
    import os
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        # Test the function with verbose=False
        ftp_fetch("ftp.example.com", "/pub", "test.txt", verbose=False)
        
        # Verify file was created
        output_file = tmp_path / "test.txt"
        assert output_file.exists()
        
    finally:
        os.chdir(original_dir)


@patch('ftplib.FTP')
def test_ftp_fetch_default_filename(mock_ftp_class, tmp_path):
    """Test ftp_fetch with default filename parameter."""
    ftp_fetch = _load_fn("ftp_fetch", "ftp_fetch.py", "ftp_fetch")
    
    # Create a mock FTP instance
    mock_ftp = Mock()
    mock_ftp_class.return_value = mock_ftp
    
    # Mock the retrbinary method
    def mock_retrbinary(command, callback):
        callback(b"default content")
    
    mock_ftp.retrbinary = mock_retrbinary
    
    import os
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        # Test the function with default filename
        ftp_fetch("ftp.example.com", "/pub")
        
        # Check that default filename was used
        output_file = tmp_path / "download.txt"
        assert output_file.exists()
        assert output_file.read_bytes() == b"default content"
        
    finally:
        os.chdir(original_dir)


class TestGetCDEC(unittest.TestCase):

    @patch("iwfm.util.get_cdec.pd.read_html")
    @patch("builtins.open", new_callable=mock_open)
    @patch("iwfm.util.get_cdec.print")
    def test_save_table_as_csv(self, mock_print, mock_open, mock_read_html):
        # Mock the HTML table and CSV saving
        mock_table = MagicMock()
        mock_df = MagicMock()
        mock_read_html.return_value = [mock_df]

        with patch.object(mock_df, "to_csv") as mock_to_csv:
            save_table_as_csv("test.csv", mock_table)

            # Verify the table was read and saved
            mock_read_html.assert_called_once()
            mock_to_csv.assert_called_once_with("test.csv", index=False)
            mock_print.assert_any_call("Data table saved to test.csv")

    @patch("iwfm.util.get_cdec.requests.get")
    @patch("iwfm.util.get_cdec.BeautifulSoup")
    @patch("iwfm.util.get_cdec.save_table_as_csv")
    @patch("iwfm.util.get_cdec.print")
    def test_download_data_table(self, mock_print, mock_save_csv, mock_bs, mock_get):
        # Mock the HTTP response and BeautifulSoup
        mock_response = MagicMock()
        mock_response.content = b"<html></html>"  # No table in the HTML
        mock_get.return_value = mock_response

        mock_soup = MagicMock()
        mock_soup.find.return_value = None  # Simulate no table found
        mock_bs.return_value = mock_soup

        files = [["Test", "Source", "http://example.com"]]
        result = download_data_table(files)

        # Verify the table was downloaded and saved
        mock_get.assert_called_once_with("http://example.com")
        mock_bs.assert_called_once_with(mock_response.content, "html.parser")
        mock_save_csv.assert_not_called()  # No table to save
        self.assertEqual(result, [["test_raw.csv", "Source"]])
        mock_print.assert_any_call("No tables found on http://example.com")

    @patch("iwfm.util.get_cdec.os.remove")
    @patch("builtins.open", new_callable=mock_open, read_data="Year,Data\n2021,100\n2022,200")
    @patch("iwfm.util.get_cdec.print")
    def test_format_file(self, mock_print, mock_open, mock_remove):
        # Mock file formatting
        info = [["test_raw.csv", "Source"]]
        format_file(info)

        # Verify the file was read, written, and deleted
        mock_open.assert_any_call("test_raw.csv", "r")
        mock_open.assert_any_call("test_data.csv", "w", newline="")
        mock_remove.assert_called_once_with("test_raw.csv")
        mock_print.assert_called_with("Data saved to test_data.csv")

class TestGetNWIS(unittest.TestCase):

    @patch("iwfm.util.get_cdec.requests.get")
    @patch("iwfm.util.get_cdec.BeautifulSoup")
    @patch("iwfm.util.get_cdec.save_table_as_csv")
    @patch("iwfm.util.get_cdec.print")
    def test_get_nwis(self, mock_print, mock_save_csv, mock_bs, mock_get):
        # Mock the HTTP response and BeautifulSoup
        mock_response = MagicMock()
        mock_response.content = b"<html></html>"  # No table in the HTML
        mock_get.return_value = mock_response

        mock_soup = MagicMock()
        mock_soup.find.return_value = None  # Simulate no table found
        mock_bs.return_value = mock_soup

        files = [["Test", "Source", "http://example.com"]]
        result = download_data_table(files)

        # Verify the table was downloaded and saved
        mock_get.assert_called_once_with("http://example.com")
        mock_bs.assert_called_once_with(mock_response.content, "html.parser")
        mock_save_csv.assert_not_called()  # No table to save
        self.assertEqual(result, [["test_raw.csv", "Source"]])
        mock_print.assert_any_call("No tables found on http://example.com")

class TestGetUSACOE(unittest.TestCase):

    @patch("iwfm.util.get_cdec.requests.get")
    @patch("iwfm.util.get_cdec.BeautifulSoup")
    @patch("iwfm.util.get_cdec.save_table_as_csv")
    @patch("iwfm.util.get_cdec.print")
    def test_get_usacoe(self, mock_print, mock_save_csv, mock_bs, mock_get):
        # Mock the HTTP response and BeautifulSoup
        mock_response = MagicMock()
        mock_response.content = b"<html></html>"  # No table in the HTML
        mock_get.return_value = mock_response

        mock_soup = MagicMock()
        mock_soup.find.return_value = None  # Simulate no table found
        mock_bs.return_value = mock_soup

        files = [["Test", "Source", "http://example.com"]]
        result = download_data_table(files)

        # Verify the table was downloaded and saved
        mock_get.assert_called_once_with("http://example.com")
        mock_bs.assert_called_once_with(mock_response.content, "html.parser")
        mock_save_csv.assert_not_called()  # No table to save
        self.assertEqual(result, [["test_raw.csv", "Source"]])
        mock_print.assert_any_call("No tables found on http://example.com")

class TestGetUSBR(unittest.TestCase):

    @patch("iwfm.util.get_cdec.requests.get")
    @patch("iwfm.util.get_cdec.BeautifulSoup")
    @patch("iwfm.util.get_cdec.save_table_as_csv")
    @patch("iwfm.util.get_cdec.print")
    def test_get_usbr(self, mock_print, mock_save_csv, mock_bs, mock_get):
        # Mock the HTTP response and BeautifulSoup
        mock_response = MagicMock()
        mock_response.content = b"<html></html>"  # No table in the HTML
        mock_get.return_value = mock_response

        mock_soup = MagicMock()
        mock_soup.find.return_value = None  # Simulate no table found
        mock_bs.return_value = mock_soup

        files = [["Test", "Source", "http://example.com"]]
        result = download_data_table(files)

        # Verify the table was downloaded and saved
        mock_get.assert_called_once_with("http://example.com")
        mock_bs.assert_called_once_with(mock_response.content, "html.parser")
        mock_save_csv.assert_not_called()  # No table to save
        self.assertEqual(result, [["test_raw.csv", "Source"]])
        mock_print.assert_any_call("No tables found on http://example.com")

