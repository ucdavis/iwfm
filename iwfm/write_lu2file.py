# write_lu2file.py
# Write IWFM land use to file
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


def write_lu2file(
    out_table,
    out_file,
    in_year,
    date_head_tail=['09/30/', '_24:00'],
    verbose=False,
    lu_type = '',
):
    """ write_lu2file() - Write IWFM land use to file

    Parameters:
      out_table       (list): IWFM land use information
      out_file        (str):  Name of output file
      in_year         (str):  Calendar year 
      date_head_tail  (list): Strings to convert in_year to DSS format
      verbose         (bool): Turn command-line output on or off
      lu_type         (str):  Land use type for verbose output

    Returns:
      nothing
    """
    date = date_head_tail[0] + str(in_year) + date_head_tail[1]  # date in DSS format
    with open(out_file, 'w') as f:
        for j in range(0, len(out_table)):
            if j == 0:  # start line with date in DSS format
                f.write(date)
            f.write('\t')
            f.write(str(j + 1) + '\t')  # elem number
            for word in out_table[j]:
                f.write(str(round(word, 2)) + '\t')
            f.write('\n')
    if verbose:
        print(f'  Wrote {lu_type} land use for {in_year} to {out_file}')
    return 
