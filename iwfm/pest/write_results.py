# write_results.py
# write simulated and observed values to a text file
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


def write_results(name, date, meas, sim, start_date):
    """write_results(name,date,meas,sim,start_date) writes simulated and observed
    values for one observation well to a text file"""
    output_filename = name + "_obs.out"
    with open(output_filename, "w") as output_file:
        output_file.write("# Observations for well {}\n".format(name))
        output_file.write("# Date\tObserved\tModeled\n".format(name))
        for i in range(0, len(date)):
            output_file.write(
                "{}\t{}\t{}\n".format(
                    date_index(int(date[i]), start_date), meas[i], sim[i]
                )
            )
    return i
