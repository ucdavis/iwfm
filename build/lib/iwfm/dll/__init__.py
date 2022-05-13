# __init__.py for iwfm.dll package
# Classes, methods and functions to interface with the IWFM DLL
# Copyright (C) 2021 University of California
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

# -- IWFM DLL methods -------------------------------------
from dll_init import dll_init
from seek_proc import seek_proc
from dll_open import dll_open
from date_time import date_time
from get_timesteps import get_timesteps
from get_timespecs import get_timespecs
from get_nnodes import get_nnodes
from get_node_ids import get_node_ids
from get_node_xy import get_node_xy
from get_nelem import get_nelem
from get_elem_ids import get_elem_ids
from get_elem_nodes import get_elem_nodes
