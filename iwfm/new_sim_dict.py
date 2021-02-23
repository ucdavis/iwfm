# new_sim_dict.py
# Creates and returns a dictionary of preprocessor file names from a basename
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


def new_sim_dict(out_base_name):
    """new_sim_dict() creates and returns a dictionary of simulation file
    names from a basename

    Parameters:
      out_base_name   (str):  Base name of new simulation input files

    Returns:
      sim_dict_new    (dict): Dictionary of new simulation input file names

    """
    sim_dict_new = {}
    sim_dict_new['sim_name']    = out_base_name + '_Simulation.in'
    sim_dict_new['preout']      = out_base_name + '_Preprocessor.bin'
    sim_dict_new['gw_file']     = out_base_name + '_Groundwater.dat'
    sim_dict_new['stream_file'] = out_base_name + '_Streams.dat'
    sim_dict_new['lake_file']   = out_base_name + '_Lakes.dat'
    sim_dict_new['root_file']   = out_base_name + '_Rootzone.dat'
    sim_dict_new['swshed_file'] = out_base_name + '_SmallWatersheds.dat'
    sim_dict_new['unsat_file']  = out_base_name + '_Unsat.dat'
    return sim_dict_new
