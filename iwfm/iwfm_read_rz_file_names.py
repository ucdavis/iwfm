# iwfm_read_rz_file_names.py
# Read rootzone file names from the main rootzone file
# Copyright (C) 2020-2026 University of California
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


def iwfm_read_rz_file_names(rz_file_name, verbose=False):
    """iwfm_read_rz_file_names() - Read rootzone file names from the main rootzone file.

    Parameters
    ----------
    rz_file_name : str
        Path to the main IWFM Rootzone file

    verbose : bool, default = False
        If True, print status messages

    Returns
    -------
    rz_npc_file_name : str
        Non-ponded crop file name (AGNPFL)

    rz_pc_file_name : str
        Ponded crop file name (PFL)

    rz_ur_file_name : str
        Urban file name (URBFL)

    rz_nv_file_name : str
        Native and riparian vegetation file name (NVRVFL)

    """
    import iwfm
    import os
    from iwfm.file_utils import read_next_line_value

    if verbose: print(f"  Reading rootzone file names from {rz_file_name}")

    iwfm.file_test(rz_file_name)
    with open(rz_file_name) as f:
        rz_lines = f.read().splitlines()

    # Skip to the file names section (after RZCONV, RZITERMX, FACTCN, GWUPTK)
    # Read the four file names: AGNPFL, PFL, URBFL, NVRVFL
    rz_npc_file_name, line_index = read_next_line_value(rz_lines, -1, skip_lines=4)
    rz_pc_file_name, line_index = read_next_line_value(rz_lines, line_index)
    rz_ur_file_name, line_index = read_next_line_value(rz_lines, line_index)
    rz_nv_file_name, line_index = read_next_line_value(rz_lines, line_index)

    # Normalize path separators (convert backslashes to forward slashes)
    rz_npc_file_name = rz_npc_file_name.replace('\\', '/')
    rz_pc_file_name = rz_pc_file_name.replace('\\', '/')
    rz_ur_file_name = rz_ur_file_name.replace('\\', '/')
    rz_nv_file_name = rz_nv_file_name.replace('\\', '/')

    # Remove "RootZone/" prefix if present (case-insensitive)
    # Files are typically in the same directory as the main RZ file
    if rz_npc_file_name.lower().startswith('rootzone/'):
        rz_npc_file_name = rz_npc_file_name[9:]
    if rz_pc_file_name.lower().startswith('rootzone/'):
        rz_pc_file_name = rz_pc_file_name[9:]
    if rz_ur_file_name.lower().startswith('rootzone/'):
        rz_ur_file_name = rz_ur_file_name[9:]
    if rz_nv_file_name.lower().startswith('rootzone/'):
        rz_nv_file_name = rz_nv_file_name[9:]

    # Convert relative paths to absolute paths based on the rootzone file location
    rz_dir = os.path.dirname(rz_file_name)
    if rz_dir:
        rz_npc_file_name = os.path.normpath(os.path.join(rz_dir, rz_npc_file_name))
        rz_pc_file_name = os.path.normpath(os.path.join(rz_dir, rz_pc_file_name))
        rz_ur_file_name = os.path.normpath(os.path.join(rz_dir, rz_ur_file_name))
        rz_nv_file_name = os.path.normpath(os.path.join(rz_dir, rz_nv_file_name))

    if verbose:
        print(f"    Non-ponded crop file: {rz_npc_file_name}")
        print(f"    Ponded crop file: {rz_pc_file_name}")
        print(f"    Urban file: {rz_ur_file_name}")
        print(f"    Native & Riparian file: {rz_nv_file_name}")

    return rz_npc_file_name, rz_pc_file_name, rz_ur_file_name, rz_nv_file_name
