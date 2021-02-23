# iwfm_adj_crops.py
# Use change factors to modify IWFM land use files
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


def iwfm_adj_crops(
    in_year,
    in_zone_file,
    in_chg_file_NV,
    in_chg_file_UR,
    in_area_npag,
    in_area_nvrv,
    in_area_urban,
    out_basename,
    skip=4,
    date_head_tail=['09/30/', '_24:00'],
):
    """ iwfm_adj_crops() - Use change factors to modify an IWFM 
        land use files

    Parameters:
      in_year         (str):  Water year of output land use
      in_zone_file    (str):  Name of zones file
      in_chg_file_NV  (str):  Name of file with Ag to Native factors
      in_chg_file_UR  (str):  Name of file with Ag to Urban factors
      in_area_npag    (str):  Name of Non-Ponded Ag Area file
      in_area_nvrv    (str):  Name of Native and Riparian Area file
      in_area_urban   (str):  Name of Urban Area file
      out_basename    (str):  Basename of output land use files
      skip            (int):  Number of non-comment lines to skip in eac file
      verbose         (bool): Turn command-line output on or off

    Returns:
      nothing
    """
    import iwfm as iwfm

    # -- get the change zones
    elem_zones = iwfm.read_lu_change_zones(in_zone_file)

    # -- read land use input files
    npag_table = iwfm.read_lu_file(in_area_npag, skip)  # open and read ag land use file
    nvrv_table = iwfm.read_lu_file(in_area_nvrv, skip)  # open and read nv land use file
    urban_table = iwfm.read_lu_file(
        in_area_urban, skip
    )  # open and read ur land use file

    # -- get change factors
    changes_NV = iwfm.read_lu_change_factors(in_chg_file_NV)
    changes_UR = iwfm.read_lu_change_factors(in_chg_file_UR)

    # - get column index for NV and UR factor for water year
    chg_col_nv = iwfm.get_change_col(changes_NV, in_year, in_chg_file_NV)
    chg_col_ur = iwfm.get_change_col(changes_UR, in_year, in_chg_file_UR)

    # -- process changes for each element
    lu_rows = len(npag_table[0])  # number of rows in land use files

    for i in range(0, len(elem_zones) - 1):  # cycle through elements in zone list
        elem, zone = elem_zones[i][0], elem_zones[i][1]
        ag2nv, ag2ur = (
            1.0 - changes_NV[zone][chg_col_nv],
            1.0 - changes_UR[zone][chg_col_ur],
        )  # factors for this zone

        area_ag = round(sum(npag_table[elem]), 2)
        # reduce ag area and add to NV area
        if ag2nv < 1 and area_ag > 0:
            ag_start = sum(npag_table[elem])
            temp = [round(j * ag2nv, 2) for j in npag_table[elem]]
            npag_table[elem] = temp
            ag_change = ag_start - sum(npag_table[elem])
            nvrv_table[elem][0] = round(nvrv_table[elem][0] + ag_change, 2)

        # reduce ag area and add to Urban area
        if ag2ur < 1 and area_ag > 0:
            ag_start = sum(npag_table[elem])
            temp = [round(j * ag2ur, 2) for j in npag_table[elem]]
            npag_table[elem] = temp
            ag_change = ag_start - sum(npag_table[elem])
            urban_table[elem][0] = round(urban_table[elem][0] + ag_change, 2)

    # -- create the output file names
    out_file_ag = out_basename + '_AG_' + in_year + '.dat'
    out_file_nv = out_basename + '_NV_' + in_year + '.dat'
    out_file_ur = out_basename + '_UR_' + in_year + '.dat'

    # -- test if each output file exists, if so delete
    iwfm.file_delete(out_file_ag)
    iwfm.file_delete(out_file_nv)
    iwfm.file_delete(out_file_ur)

    # -- write out new data 
    iwfm.write_lu2file(
        npag_table, out_file_ag, in_year, npag_table, 'Ag', date_head_tail
    )
    iwfm.write_lu2file(
        nvrv_table, out_file_nv, in_year, nvrv_table, 'Native', date_head_tail
    )
    iwfm.write_lu2file(
        urban_table, out_file_ur, in_year, urban_table, 'Urban', date_head_tail
    )

    return 


if __name__ == '__main__':
    ' Run iwfm_adj_crops() from command line '
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        in_year = sys.argv[1]
        in_zone_file = sys.argv[2]
        in_chg_file_NV = sys.argv[3]
        in_chg_file_UR = sys.argv[4]
        in_area_npag = sys.argv[5]
        in_area_nvrv = sys.argv[6]
        in_area_urban = sys.argv[7]
        out_basename = sys.argv[8]
    else:  # ask for file names from terminal
        in_year        = input('Year: ')
        in_zone_file   = input('Zone file name: ')
        in_chg_file_NV = input('Ag to Native change factors file name: ')
        in_chg_file_UR = input('Ag to Urban change factors file name: ')
        in_area_npag   = input('Input Ag file name: ')
        in_area_nvrv   = input('Input Native file name: ')
        in_area_urban  = input('Input Urban file name: ')
        out_basename   = input('Output file base name: ')

    iwfm.file_test(in_zone_file)
    iwfm.file_test(in_chg_file_NV)
    iwfm.file_test(in_chg_file_UR)
    iwfm.file_test(in_area_npag)
    iwfm.file_test(in_area_nvrv)
    iwfm.file_test(in_area_urban)

    idb.exe_time()  # initialize timer
    iwfm_adj_crops(
        in_year,
        in_zone_file,
        in_chg_file_NV,
        in_chg_file_UR,
        in_area_npag,
        in_area_nvrv,
        in_area_urban,
        out_basename,
    )  # set debug=1 for debugging

    idb.exe_time()  # print elapsed time
