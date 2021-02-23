# cdec2monthly.py
# Read CDEC observations, convert sub-monthly observations to the monthly average
# and write to a csv file
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


def cdec2monthly(input_file, output_file, verbose=0, debug=0):
    """Read CDEC observations, convert sub-monthly observations to the monthly average
    and write to a csv file"""
    import os
    import pandas as pd
    import numpy as np

    # read into pandas dataframe, replacing error codes with nan
    flow_data = (
        pd.read_csv(input_file)
        .replace(r"--", np.nan, regex=True)
        .replace(r"ART", np.nan, regex=True)
        .replace(r"BRT", np.nan, regex=True)
    )
    flow_data["DATE"] = pd.to_datetime(
        flow_data["DATE"], errors="coerce"
    )  # convert DATE to datetime objects
    flow_data["FLOW (CFS)"] = flow_data["FLOW (CFS)"].astype(
        float
    )  # convert FLOW to floats
    flow_data["FLOW (AF)"] = (
        flow_data["FLOW (CFS)"].astype(float) * 1.983
    )  # make new column with flow values in Acre-Feet/day

    flow_daily = flow_data.resample("D", on="DATE").mean()  # get daily mean value

    # the pandas dataframe was doing something weird, so ...
    flow_daily.to_csv("temp.txt")  # write it to a temporary output file ...
    flow_daily = pd.read_csv("temp.txt")  # read it back in ...
    os.remove("temp.txt")  # and delete the file

    flow_daily["DATE"] = pd.to_datetime(flow_daily["DATE"], errors="coerce")
    flow_daily["FLOW (CFS)"] = flow_daily["FLOW (CFS)"].astype(float)
    flow_daily["FLOW (AF)"] = flow_daily["FLOW (AF)"].astype(float)

    flow_monthly = flow_daily.resample(
        "M", on="DATE"
    ).sum()  # aggregate to monthly flows

    # write to output file
    header = ["FLOW (AF)"]
    flow_monthly.to_csv(output_file, columns=header)

    if verbose:
        print(
            "  Aggregated {} to monthly flows and wrote to {}".format(
                input_file, output_file
            )
        )
    return 1


if __name__ == "__main__":
    " Run cdec2monthly() from command line "
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:  # ask for file names from terminal
        input_file = input("CDEC daily data file name: ")
        output_file = input("Output monthly data file name: ")

    iwfm.file_test(input_file)

    idb.exe_time()  # initialize timer
    cdec2monthly(input_file, output_file, debug=0)  # set debug=1 to debug

    print("  Read {} and wrote {}".format(input_file, output_file))  # update cli
    idb.exe_time()  # print elapsed time
