# iwfm_read_sim.py
# Read IWFM Simulation main file
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

# -- IWFM simulation files ---
def iwfm_read_sim(sim_file, debug=0):
    """Function iwfm_read_sim(sim_file,debug = 0) reads an IWFM Simulation
    main input file, and returns a dictionary with the files called and some settings."""
    import iwfm as iwfm

    if debug:
        print("      --> Function iwfm_read_sim({})".format(sim_file))

    sim_lines = open(sim_file).read().splitlines()  # open and read input file

    # debugging
    if debug:
        print(" --> {}".format(sim_lines[13]))

    line_index = iwfm.skip_ahead(0, sim_lines, 3)  # skip comments

    # -- read input file names and create a dictionary ------------------
    sim_dict = {}
    preout = iwfm.file_get_path(sim_lines[line_index].split()[0])  # preproc output file
    sim_dict["preout"] = preout
    if debug:
        print("    --> {}: {}".format("preout", preout))

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    gw_file = iwfm.file_file_get_path(
        sim_lines[line_index].split()[0]
    )  # groundwater file
    sim_dict["gw"] = gw_file
    if debug:
        print("    --> {}: {}".format("gw_file", gw_file))

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    stream_file = iwfm.file_get_path(sim_lines[line_index].split()[0])  # stream file
    sim_dict["stream"] = stream_file
    if debug:
        print("    --> {}: {}".format("stream_file", stream_file))

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    temp = sim_lines[line_index].split()[0]  # lake file
    if temp[0] == "/":
        lake_file = ""
    else:
        lake_file = iwfm.file_get_path(temp)  # lake file
        if debug:
            print("    --> {}: {}".format("lake_file", lake_file))
    sim_dict["lake"] = lake_file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    rz_file = iwfm.file_get_path(sim_lines[line_index].split()[0])  # rootzone file
    sim_dict["rootzone"] = rz_file
    if debug:
        print("    --> {}: {}".format("rz_file", rz_file))

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    sw_file = iwfm.file_get_path(
        sim_lines[line_index].split()[0]
    )  # small watersheds file
    sim_dict["smallwatershed"] = sw_file
    if debug:
        print("    --> {}: {}".format("sw_file", sw_file))

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    us_file = iwfm.file_get_path(
        sim_lines[line_index].split()[0]
    )  # unsaturated zone file
    sim_dict["unsat"] = us_file
    if debug:
        print("    --> {}: {}".format("us_file", us_file))

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    if_file = iwfm.file_get_path(
        sim_lines[line_index].split()[0]
    )  # irrigation fractions file
    sim_dict["irrfrac"] = if_file
    if debug:
        print("    --> {}: {}".format("if_file", if_file))

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    sa_file = iwfm.file_get_path(
        sim_lines[line_index].split()[0]
    )  # supply adjustment file
    sim_dict["supplyadj"] = sa_file
    if debug:
        print("    --> {}: {}".format("sa_file", sa_file))

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    pc_file = sim_lines[line_index].split()[0]  # precipitation file
    sim_dict["precip"] = pc_file
    if debug:
        print("    --> {}: {}".format("pc_file", pc_file))

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    et_file = iwfm.file_get_path(
        sim_lines[line_index].split()[0]
    )  # unsaturated zone file
    sim_dict["et"] = et_file
    if debug:
        print("    --> {}: {}".format("et_file", et_file))

    # -- starting date
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    start = sim_lines[line_index].split()[0]  # starting date
    sim_dict["start"] = start
    if debug:
        print("    --> {}: {}".format("start", start))

    # -- time step
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 1)  # skip comments
    step = sim_lines[line_index].split()[0]  # time step
    sim_dict["step"] = step
    if debug:
        print("    --> {}: {}".format("step", step))

    # -- endng date
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    end = sim_lines[line_index].split()[0]  # ending date
    sim_dict["end"] = end
    if debug:
        print("    --> {}: {}".format("end", end))

    return sim_dict
