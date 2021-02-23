# wdl_meas_stats.py
# Calculate water level statistics and write out to a file
# info and gwhyd_sim columns, and return the dictionary
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


def wdl_meas_stats(input_file, verbose=False):
    """ wdl_meas_stats() - Calculate water level statistics and write out 
        to a file

    Parameters:
      input_file      (str):  Name of input file
      verbose         (bool): Turn command-line output on or off

    Returns:
      nothing
    """
    import statistics

    output_file = input_file[0 : input_file.find('.')] + '_stats.out'

    # -- read and process each line of input_file
    lines_in, lines_out, count = 0, 0, 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write(
            'STN_ID\tMIN_DATE\tMAX_DATE\tCOUNT\tWL_AVG\tWL_MAX\tWL_MIN\tWL_SDV\n'
        )  # header
        first_date, first_well_id, start_date, last_date, wl = 0, '', '', '', []
        for line in infile:
            lines_in = lines_in + 1
            items = line.split()
            if lines_in == 2:
                first_well_id, start_date, last_date = items[0], items[1], items[1]
                wl.append(float(items[4]))
                count = 1
            elif lines_in > 2:
                this_well_id, this_date = items[0], items[1]
                if items[0] != first_well_id:
                    # write out info for this well
                    if count > 1:
                        stdev = int(statistics.stdev(wl) * 100) / 100
                    else:
                        stdev = -99.9
                    outfile.write(
                        '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                            first_well_id,
                            text_date(start_date),
                            text_date(last_date),
                            count,
                            int(statistics.mean(wl) * 100) / 100,
                            max(wl),
                            min(wl),
                            stdev,
                        )
                    )
                    lines_out = lines_out + 1
                    # - reset for the next well
                    first_well_id = this_well_id
                    first_date = this_date
                    start_date = items[1]
                    count = 1
                    wl = []
                    wl.append(float(items[4]))
                else:
                    wl.append(float(items[4]))
                    count = count + 1

                last_date = this_date

    if verbose:
        print('Processed {:,} lines from {}'.format(lines_in, input_file))
        print('Wrote {:,} lines to {}'.format(lines_out, output_file))
