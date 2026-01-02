# iwfm_read_rz_npc.py
# Read non-ponded crop data from a file and organize them into lists
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



def iwfm_read_rz_npc(file, verbose=False):
    """iwfm_read_rz_npc() - Read non-ponded crop data from a file and organize them into lists.

    Parameters
    ----------
    file : str
        The path of the file containing the non-ponded crop data.
  
    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------

    crops : list
        A list of crop codes
    
    params : list
        A list of parameters: [cn, et, wsp, ip, ms, ts, rf, ru, ic]

    files : list
        A list of file names: [npc_area_file, npc_bd_file, npc_zb_file, npc_rd_file, npc_ms_file, npc_ts_file, npc_md_file]

    """
    import iwfm as iwfm

    if verbose: print(f"Entered iwfm_read_rz_npc() with {file}")

    with open(file) as f:
        npc_lines = f.read().splitlines()                  # open and read input file

    line_index = iwfm.skip_ahead(0, npc_lines, 0)               # skip to number of crop types
    ncrop = int(npc_lines[line_index].split()[0])               # number of crop types

    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line
    fldmd = int(npc_lines[line_index].split()[0])               # soil moisture ocmputation method flag

    # read crop codes
    crops = []
    for i in range(ncrop):
        line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line
        crops.append(npc_lines[line_index].split()[0])              # crop code

    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line
    npc_area_file = npc_lines[line_index].split()[0]

    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line
    nbcrop = int(npc_lines[line_index].split()[0])               # soil moisture ocmputation method flag

    line_index = iwfm.skip_ahead(line_index + 1 + nbcrop, npc_lines, 0) # skip to budget file names
    npc_bd_file = npc_lines[line_index].split()[0]                   # read crop budget file name

    line_index = iwfm.skip_ahead(line_index + 1 + nbcrop, npc_lines, 0) # skip to budget file names
    npc_zb_file = npc_lines[line_index].split()[0]                   # read crop zbudget fractions file name

    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)          # skip budget file names
    npc_rd_file = npc_lines[line_index].split()[0]                   # read rooting depth fractions file name

    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line
    fact = float(npc_lines[line_index].split()[0])               # soil moisture ocmputation method flag

    # read rooting depths
    rd = []
    for i in range(ncrop):
        line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line
        t = []
        t.append(int(npc_lines[line_index].split()[0]))  
        t.append(float(npc_lines[line_index].split()[1]))
        t.append(int(npc_lines[line_index].split()[2]))  
        rd.append(t)

    # how many elements?
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line
    ne = 0
    while (line_index + ne < len(npc_lines) and
           npc_lines[line_index+(ne)].split()[0] != 'C'):
        ne += 1

    if line_index + ne >= len(npc_lines):
        raise ValueError(
            f"'C' marker not found while counting non-ponded crop elements at line {line_index}"
        )

    ne -= 2                                             # one to convert to zero index, one is extra

    # curve numbers
    cn, line_index = iwfm.iwfm_read_param_table_ints(npc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    # ET
    et, line_index = iwfm.iwfm_read_param_table_ints(npc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    # ag water supply requirement
    wsp, line_index = iwfm.iwfm_read_param_table_ints(npc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    # irrigation period
    ip, line_index = iwfm.iwfm_read_param_table_ints(npc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    # minimum soil moisture
    npc_ms_file = npc_lines[line_index].split()[0]                   # read minimum soil moisture file name
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    ms, line_index = iwfm.iwfm_read_param_table_ints(npc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    # target soil misture
    npc_ts_file = npc_lines[line_index].split()[0]                   # read target soil moisture file name
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    tsm, line_index = iwfm.iwfm_read_param_table_ints(npc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    # return flow fractions
    rf, line_index = iwfm.iwfm_read_param_table_ints(npc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    # reuse fractions
    ru, line_index = iwfm.iwfm_read_param_table_ints(npc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    # minimum deep perc fractions
    npc_md_file = npc_lines[line_index].split()[0]                   # read target soil moisture file name
    line_index = iwfm.skip_ahead(line_index + 1, npc_lines, 0)  # skip to next value line

    # initial condition
    ic, line_index = iwfm.iwfm_read_param_table_floats(npc_lines, line_index, ne)

    params = [cn, et, wsp, ip, ms, tsm, rf, ru, ic]
    files = [npc_area_file, npc_bd_file, npc_zb_file, npc_rd_file, npc_ms_file, npc_ts_file, npc_md_file]
         
    if verbose: print(f"Leaving iwfm_read_rz_npc()")

    return crops, params, files
