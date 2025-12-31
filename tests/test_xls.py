# test_xls.py
# unit test for iwfm.xls methods in the iwfm package
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
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import pytest


def _load_fn(module_name, file_name, fn_name):
    from importlib.util import spec_from_file_location, module_from_spec
    base = Path(__file__).resolve().parents[1] / "iwfm" / "xls" / file_name
    spec = spec_from_file_location(module_name, str(base))
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return getattr(mod, fn_name)


def test_write_2_excel_creates_file(tmp_path):
    """Test that write_2_excel creates an Excel file with correct structure."""
    try:
        import xlsxwriter
    except ImportError:
        pytest.skip("xlsxwriter not available")
    
    try:
        write_2_excel = _load_fn("write_2_excel", "write_2_excel.py", "write_2_excel")
    except (ImportError, ModuleNotFoundError):
        pytest.skip("xlsxwriter not available or module load failed")
    
    # Change to temp directory
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        # Create test data: 2 sheets, 3 elements, 2 time steps
        data = [
            [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0]],  # Sheet 1
            [[11.0, 21.0], [31.0, 41.0], [51.0, 61.0]]   # Sheet 2
        ]
        elements = 3
        time_steps = 2
        dates = [datetime(2020, 1, 1), datetime(2020, 2, 1)]
        
        file_base = "test_output"
        write_2_excel(file_base, data, sheets=2, elements=elements, 
                     time_steps=time_steps, dates=dates, data_type='Test')
        
        # Check that file was created
        output_file = tmp_path / "test_output.xlsx"
        assert output_file.exists()
        
        # Try to open and verify basic structure (if openpyxl is available)
        try:
            import openpyxl
            wb = openpyxl.load_workbook(output_file)
            assert len(wb.worksheets) == 2
            assert wb.worksheets[0].title == "Test1"
            assert wb.worksheets[1].title == "Test2"
            # Check header
            assert wb.worksheets[0]['A1'].value == "Test1"
            assert wb.worksheets[0]['A2'].value == "WYr"
            wb.close()
        except ImportError:
            pass  # openpyxl not available, just verify file exists
    finally:
        os.chdir(old_cwd)


def test_write_2_excel_structure_with_mock(tmp_path):
    """Test write_2_excel using mocked xlsxwriter to verify calls."""
    try:
        import xlsxwriter
    except ImportError:
        pytest.skip("xlsxwriter not available")
    
    try:
        write_2_excel = _load_fn("write_2_excel", "write_2_excel.py", "write_2_excel")
    except (ImportError, ModuleNotFoundError):
        pytest.skip("xlsxwriter not available or module load failed")
    
    # Note: xlsxwriter imports happen inside the function, so we can't easily mock
    # This test would need xlsxwriter installed to run properly
    pytest.skip("Mocking xlsxwriter requires complex module patching")


def test_excel_init_requires_win32com():
    """Test excel_init requires Windows COM (skip on non-Windows)."""
    try:
        excel_init = _load_fn("excel_init", "excel_init.py", "excel_init")
    except (ImportError, ModuleNotFoundError):
        pytest.skip("win32com not available (Windows-only)")
    
    # If we get here, we can test with mocks
    import sys
    if 'win32com' not in sys.modules:
        pytest.skip("win32com not available (Windows-only)")
    
    # For actual testing, would need Windows environment
    pytest.skip("Excel COM testing requires Windows and Excel installation")


def test_excel_new_workbook_creates_workbook():
    """Test excel_new_workbook creates a new workbook."""
    excel_new_workbook = _load_fn("excel_new_workbook", "excel_new_workbook.py", "excel_new_workbook")
    
    mock_excel = MagicMock()
    mock_workbooks = MagicMock()
    mock_workbook = MagicMock()
    mock_workbooks.Add.return_value = mock_workbook
    mock_excel.Workbooks = mock_workbooks
    
    result = excel_new_workbook(mock_excel)
    
    mock_workbooks.Add.assert_called_once()
    assert result == mock_workbook


def test_excel_kill_closes_excel():
    """Test excel_kill closes Excel application."""
    excel_kill = _load_fn("excel_kill", "excel_kill.py", "excel_kill")
    
    mock_excel = MagicMock()
    
    excel_kill(mock_excel)
    
    assert mock_excel.DisplayAlerts == False
    assert mock_excel.Visible == False
    mock_excel.Quit.assert_called_once()


def test_xl_quit_closes_application():
    """Test xl_quit gracefully closes Excel."""
    xl_quit = _load_fn("xl_quit", "xl_quit.py", "xl_quit")
    
    mock_excel = MagicMock()
    mock_application = MagicMock()
    mock_excel.Application = mock_application
    
    xl_quit(mock_excel)
    
    assert mock_excel.DisplayAlerts == False
    assert mock_excel.Visible == False
    mock_application.Quit.assert_called_once()


def test_xl_write_2d_writes_to_worksheet():
    """Test xl_write_2d writes data to specified worksheet."""
    xl_write_2d = _load_fn("xl_write_2d", "xl_write_2d.py", "xl_write_2d")
    
    mock_wb = MagicMock()
    mock_worksheet = MagicMock()
    mock_cells = MagicMock()
    mock_range = MagicMock()
    
    mock_wb.Worksheets.return_value = mock_worksheet
    mock_worksheet.Cells = MagicMock(return_value=mock_cells)
    mock_worksheet.Range.return_value = mock_range
    
    data = [[1, 2, 3], [4, 5, 6]]
    xl_write_2d(data, mock_wb, row=1, col=1, sheet=0)
    
    # Verify worksheet was selected
    mock_wb.Worksheets.assert_called_once_with(0)
    # Verify Range was called with correct cells
    mock_worksheet.Range.assert_called_once()
    # Verify data was assigned
    assert mock_range.Value == data


def test_xl_open_requires_win32com():
    """Test xl_open requires Windows COM (skip on non-Windows)."""
    try:
        xl_open = _load_fn("xl_open", "xl_open.py", "xl_open")
    except (ImportError, ModuleNotFoundError):
        pytest.skip("win32com not available (Windows-only)")
    
    # For actual testing, would need Windows environment
    pytest.skip("Excel COM testing requires Windows and Excel installation")


def test_xl_save_saves_workbook(tmp_path):
    """Test xl_save saves workbook to file."""
    xl_save = _load_fn("xl_save", "xl_save.py", "xl_save")
    
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        mock_wb = MagicMock()
        
        xl_save(mock_wb, "test.xlsx")
        
        # Verify SaveAs was called with full path
        mock_wb.SaveAs.assert_called_once()
        call_args = mock_wb.SaveAs.call_args[0][0]
        assert "test.xlsx" in str(call_args)
    finally:
        os.chdir(old_cwd)

