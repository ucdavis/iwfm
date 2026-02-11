# __init__.py for iwfm.xls package
# Excel file operations for IWFM
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

"""
Excel file operations for IWFM.

Uses openpyxl by default (cross-platform). Falls back to win32com
on Windows if openpyxl is not installed.

New API (recommended):
    create_workbook, open_workbook, save_workbook, close_workbook
    add_worksheet, get_worksheet, write_cells, write_budget_data

Legacy API (deprecated):
    excel_init, excel_new_workbook, excel_kill
    xl_open, xl_save, xl_quit, xl_write_2d
    bud2xl, write_budget_to_xl, write_2_excel
"""

import warnings
from loguru import logger

# -----------------------------------------------------------------------------
# Backend Selection
# -----------------------------------------------------------------------------

_BACKEND = None
_backend_module = None

try:
    from iwfm.xls import _openpyxl_backend as _backend_module
    _BACKEND = 'openpyxl'
    logger.debug("xls module using openpyxl backend")
except ImportError:
    try:
        warnings.warn(
            "openpyxl not installed. Falling back to win32com (Windows only). "
            "Install openpyxl for cross-platform support: pip install openpyxl",
            DeprecationWarning
        )
        from iwfm.xls import _win32com_backend as _backend_module
        _BACKEND = 'win32com'
        logger.warning("xls module falling back to win32com backend")
    except ImportError:
        raise ImportError(
            "No Excel backend available. Install openpyxl: pip install openpyxl"
        )


def _get_backend_module():
    """Return the active backend module."""
    return _backend_module


def get_backend():
    """Return name of active backend ('openpyxl' or 'win32com')."""
    return _BACKEND


# -----------------------------------------------------------------------------
# New Public API
# -----------------------------------------------------------------------------

create_workbook = _backend_module.create_workbook
open_workbook = _backend_module.open_workbook
save_workbook = _backend_module.save_workbook
close_workbook = _backend_module.close_workbook
add_worksheet = _backend_module.add_worksheet
get_worksheet = _backend_module.get_worksheet
write_cells = _backend_module.write_cells
write_budget_data = _backend_module.write_budget_data


# -----------------------------------------------------------------------------
# Deprecated Functions (backward compatibility)
# These issue warnings and delegate to the backend
# -----------------------------------------------------------------------------

from iwfm.xls.buds2xl import buds2xl
from iwfm.xls.excel_init import excel_init
from iwfm.xls.excel_new_workbook import excel_new_workbook
from iwfm.xls.excel_kill import excel_kill
from iwfm.xls.xl_open import xl_open
from iwfm.xls.xl_save import xl_save
from iwfm.xls.xl_quit import xl_quit
from iwfm.xls.xl_write_2d import xl_write_2d
from iwfm.xls.bud2xl import bud2xl
from iwfm.xls.write_budget_to_xl import write_budget_to_xl
from iwfm.xls.write_2_excel import write_2_excel
