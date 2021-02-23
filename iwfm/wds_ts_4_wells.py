# wds_ts_4_wells.py
# Write well data as time series
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


def wds_ts_4_wells(station_file, waterlevel_file, verbose=False):
    """ wds_ts_4_wells() - Write well data as time series

    Parameters:
      station_file    (str):  Name of well information file
      waterlevel_file (str):  Name of water levels file
      verbose         (bool): Turn command-line output on or off

    Returns:
      nothing
    """
    import csv

    station_file_base = station_file[0 : station_file.find('.')]  # basename
    station_file_ext = station_file[
        station_file.find('.') + 1 : len(station_file) + 1
    ]  # extention
    output_file = station_file_base + '_TS.out'

    # -- read stations into a dictionary
    file_lines = open(station_file).read().splitlines()  # open and read input file
    if verbose:
        print(
            'Read {:,} stations from {}'.format(len(file_lines), station_file)
        )  # update cli

    # -- build a dictionary
    mydict = {
        entry['STN_ID']: [entry['SITE_CODE'], entry['SWN']]
        for entry in csv.DictReader(file_lines, delimiter='\t')
    }

    # -- read and process each line of waterlevel_file
    lines_in = 0
    lines_out = 0
    with open(waterlevel_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write(
            'STN_ID,SITE_CODE,WLM_ID,MSMT_DATE,WLM_RPE,WLM_GSE,RDNG_WS,RDNG_RP,WSE,RPE_GSE,GSE_WSE,WLM_QA_DESC,WLM_DESC,WLM_ACC_DESC,WLM_ORG_ID,WLM_ORG_NAME,MSMT_CMT,COOP_AGENCY_ORG_ID,COOP_ORG_NAME\n'
        )
        for line in infile:
            lines_in = lines_in + 1
            items = line.split()
            if len(line) > 10:
                value = mydict.get(items[0][0 : line.find(',')])
                if value is not None:
                    outfile.write(line)
                    lines_out = lines_out + 1
    if verbose:
        print('Processed {:,} lines from {}'.format(lines_in, waterlevel_file))
        print('Wrote {:,} lines to {}'.format(lines_out, output_file))
    return
