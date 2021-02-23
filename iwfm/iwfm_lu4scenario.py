# iwfm_lu4scenario.py
# Modify IWFM land use files for a scenario
# Copyright (C) 2020-2021 Hydrolytics LLC
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


def iwfm_lu4scenario(
    out_base_name,
    in_npag_file,
    in_ponded_file,
    in_urban_file,
    in_nvrv_file,
    skip=4,
    verbose=False,
):
    """ iwfm_lu4scenario() - Modify IWFM land use files for a scenario

    Parameters:
      out_base_name   (str):  Base name of output files
      in_npag_file    (str):  Name of input Non-Ponded Ag Area file
      in_ponded_file  (str):  Name of input Ponded Ag Area File
      in_urban_file   (str):  Name of input Urban Area file
      in_nvrv_file    (str):  Name of input Native and Riparian Area input file
      skip            (int):  Number of non-comment lines to skip in eac file
      verbose         (bool): Turn command-line output on or off

    Returns:
      nothing

    To do:
      Each land use file is done in series. Can this be replaced with a function that
        does one land use file, and use the function for each land use file?
    """
    comments = 'Cc*#'

    # -- open and read Non-Ponded Area file ------------------------------------
    npag_data = open(in_npag_file).read().splitlines()  # open, read and close
    if verbose:
        print('   Read {:,} lines from {}'.format(len(npag_data), in_npag_file))

    # -- find the file line with the first elemen't data
    npag_index = 0
    while any(
        (c in comments) for c in npag_data[npag_index][0]
    ):  # skip lines that begin with 'C', 'c' or '*'
        npag_index += 1
    for i in range(0, skip):  # skip data spec rows
        npag_index += 1
    while any(
        (c in comments) for c in npag_data[npag_index][0]
    ):  # skip lines that begin with 'C', 'c' or '*'
        npag_index += 1

    # -- compile the data from the file 
    # the first line contains the date, elemeno, and land use data
    line = npag_data[npag_index].split()
    date = line.pop(0)
    elem = line.pop(0)
    npag_table = []
    npag_table.append(line)
    npag_index += 1
    npag_cols = len(line)  # including elem_no column
    # do the remaining lines
    while npag_index < len(npag_data):
        line = npag_data[npag_index].split()
        elem = line.pop(0)
        npag_table.append(line)
        npag_index += 1

    # -- open and read the Ponded Area file -----------------------------------
    pag_data = open(in_ponded_file).read().splitlines()  # open, read and close
    if verbose:
        print("   Read {:,} lines from {}".format(len(pag_data), in_ponded_file))

    # -- find the file line with the first elemen't data 
    pag_index = 0
    while any(
        (c in comments) for c in pag_data[pag_index][0]
    ):  # skip lines that begin with 'C', 'c' or '*'
        pag_index += 1
    for i in range(0, skip):  # skip data spec rows
        pag_index += 1
    while any(
        (c in comments) for c in pag_data[pag_index][0]
    ):  # skip lines that begin with 'C', 'c' or '*'
        pag_index += 1

    # -- compile the data from the file 
    # the first line contains the date, elemeno, and land use data
    line = pag_data[pag_index].split()
    date = line.pop(0)
    elem = line.pop(0)
    pag_table = []
    pag_table.append(line)
    pag_index += 1
    pag_cols = len(line)  # including elem_no column
    # do the remaining lines
    while pag_index < len(pag_data):
        line = pag_data[pag_index].split()
        elem = line.pop(0)
        pag_table.append(line)
        pag_index += 1

    # -- open and read the Urban Area file ------------------------------------
    urb_data = open(in_urban_file).read().splitlines()  # open, read and close
    if verbose:
        print("   Read {:,} lines from {}".format(len(urb_data), in_urban_file))

    # -- find the file line with the first elemen't data 
    urb_index = 0
    while any(
        (c in comments) for c in urb_data[urb_index][0]
    ):  # skip lines that begin with 'C', 'c' or '*'
        urb_index += 1
    for i in range(0, skip):  # skip data spec rows
        urb_index += 1
    while any(
        (c in comments) for c in urb_data[urb_index][0]
    ):  # skip lines that begin with 'C', 'c' or '*'
        urb_index += 1

    # -- compile the data from the file 
    # the first line contains the date, elemeno, and land use data
    line = urb_data[urb_index].split()
    date = line.pop(0)
    elem = line.pop(0)
    urb_table = []
    urb_table.append(line)
    urb_index += 1
    urb_cols = len(line)  # including elem_no column
    # do the remaining lines
    while urb_index < len(urb_data):
        line = urb_data[urb_index].split()
        elem = line.pop(0)
        urb_table.append(line)
        urb_index += 1

    # -- open and read the Native and Riparian Area file ----------------------
    nvrv_data = open(in_nvrv_file).read().splitlines()  # open, read and close
    if verbose:
        print("   Read {:,} lines from {}".format(len(nvrv_data), in_nvrv_file))

    # -- find the file line with the first elemen't data
    nvrv_index = 0
    while any(
        (c in comments) for c in nvrv_data[nvrv_index][0]
    ):  # skip lines that begin with 'C', 'c' or '*'
        nvrv_index += 1
    for i in range(0, skip):  # skip data spec rows
        nvrv_index += 1
    while any(
        (c in comments) for c in nvrv_data[nvrv_index][0]
    ):  # skip lines that begin with 'C', 'c' or '*'
        nvrv_index += 1

    # -- compile the data from the file 
    # the first line contains the date, elemeno, and land use data
    line = nvrv_data[nvrv_index].split()
    date = line.pop(0)
    elem = line.pop(0)
    nvrv_table = []
    nvrv_table.append(line)
    nvrv_index += 1
    nvrv_cols = len(line)  # including elem_no column
    # do the remaining lines
    while nvrv_index < len(nvrv_data):
        line = nvrv_data[nvrv_index].split()
        elem = line.pop(0)
        nvrv_table.append(line)
        nvrv_index += 1

    # -- build one table from the four data sets ------------------------------------
    import itertools

    land_use = []
    for i in range(0, len(npag_table)):
        npag = npag_table[i][0:20]
        pag = pag_table[i]
        urb = urb_table[i][0]
        nvrv = nvrv_table[i]
        x = []
        x.append([str(i + 1)])
        x.append(npag_table[i][0:20])
        x.append(pag_table[i][0:5])
        x.append(nvrv_table[i][0:2])
        y = list(itertools.chain.from_iterable(x))
        y.append(urb_table[i][0])
        land_use.append(y)

    # -- write to file ---------------------------------------------------------------
    outFileName = out_base_name + "_Landuse.dat"
    outFile = open(outFileName, "w", newline="")
    outFile.write("# Date: {}\n".format(date))
    outFile.write(
        "# Elem\tNPA1\tNPA2\tNPA3\tNPA4\tNPA5\tNPA6\tNPA7\tNPA8\tNPA9\tNPA10\tNPA11\tNPA12\tNPA13\tNPA14\tNPA15\tNPA16\tNPA17\tNPA18\tNPA19\tNPA20\tPA1\tPA2\tPA3\tPA4\tPA5\tNV\tRV\tUrb\n"
    )
    for i in range(0, len(npag_table)):
        outFile.write("\t".join(land_use[i]))
        outFile.write("\n")
    outFile.close
    if verbose:
        print("   Wrote land use data for {} to {}".format(date, outFileName))
    return
