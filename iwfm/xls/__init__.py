# __init__.py for iwfm package
# Methods to read, write and modify Excel files for use with IWFM
# output files
# Copyright (C) 2018-2023 University of California
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

# -- Excel operations -------------------------------------
from iwfm.xls.excel_init import excel_init
from iwfm.xls.excel_new_workbook import excel_new_workbook
from iwfm.xls.excel_kill import excel_kill
from iwfm.xls.write_budget_to_xl import write_budget_to_xl

# -- older versions, deprecated but retained for backward compatibility
from iwfm.xls.bud2xl import bud2xl
from iwfm.xls.xl_open import xl_open
from iwfm.xls.xl_write_2d import xl_write_2d
from iwfm.xls.xl_save import xl_save
from iwfm.xls.xl_quit import xl_quit
from iwfm.xls.write_2_excel import write_2_excel
