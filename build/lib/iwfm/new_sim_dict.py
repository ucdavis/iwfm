# new_sim_dict.py
# Creates and returns a dictionary of preprocessor file names from a basename
# Copyright (C) 2020-2021 University of California
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
    ''' new_sim_dict() - Create and return a dictionary of simulation file
        names from a basename

    Parameters
    ----------
    out_base_name : str
        base name of new simulation input files

    Returns
    -------
    sim_dict_new : dictionary
        dictionary of new simulation input file names

    '''
    sim_dict_new = {}
    sim_dict_new['preout']        = out_base_name + '_Preprocessor.bin'
    sim_dict_new['sim_name']      = out_base_name + '_Simulation.in'

    sim_dict_new['gw_file']       = out_base_name + '_Groundwater.dat'
    sim_dict_new['bc_file']       = out_base_name + '_BC.dat'
    sim_dict_new['spfl_file']     = out_base_name + '_SpecifiedFlowBC.dat'
    sim_dict_new['sphd_file']     = out_base_name + '_SpecifiedHeadBC.dat'
    sim_dict_new['ghd_file']      = out_base_name + '_GeneralHeadBC.dat'
    sim_dict_new['cghd_file']     = out_base_name + '_ConstrainedHeadBC.dat'
    sim_dict_new['tsbc_file']     = out_base_name + '_TimeSeriesBC.dat'

    sim_dict_new['pump_file']     = out_base_name + '_Pumping.dat'
    sim_dict_new['epump_file']    = out_base_name + '_ElemPump.dat'
    sim_dict_new['well_file']     = out_base_name + '_WellSpec.dat'
    sim_dict_new['prate_file']    = out_base_name + '_PumpRates.dat'
    
    sim_dict_new['sub_file']      = out_base_name + '_Subsidence.dat'
    sim_dict_new['drain_file']    = out_base_name + '_TileDrain.dat'

    sim_dict_new['stream_file']   = out_base_name + '_Streams.dat'
    sim_dict_new['stin_file']     = out_base_name + '_StreamInflow.dat'
    sim_dict_new['divspec_file']  = out_base_name + '_DiversionSpec.dat'
    sim_dict_new['bp_file']       = out_base_name + '_BypassSpec.dat'
    sim_dict_new['div_file']      = out_base_name + '_Diversions.dat'

    sim_dict_new['lake_file']     = out_base_name + '_Lakes.dat'
    sim_dict_new['lmax_file']     = out_base_name + '_MaxLakeElev.dat'

    sim_dict_new['root_file']     = out_base_name + '_Rootzone.dat'
    sim_dict_new['np_file']       = out_base_name + '_NonPondedCrop.dat'
    sim_dict_new['pc_file']       = out_base_name + '_PondedCrop.dat'
    sim_dict_new['ur_file']       = out_base_name + '_Urban.dat'
    sim_dict_new['nv_file']       = out_base_name + '_NativeVeg.dat'
    sim_dict_new['nva_file']      = out_base_name + '_NativeVeg_Area.dat'
    sim_dict_new['npa_file']      = out_base_name + '_NonPondedCrop_Area.dat'
    sim_dict_new['pca_file']      = out_base_name + '_PondedCrop_Area.dat'
    sim_dict_new['ura_file']      = out_base_name + '_Urban_Area.dat'

    sim_dict_new['swshed_file']   = out_base_name + '_SmallWatersheds.dat'
    sim_dict_new['unsat_file']    = out_base_name + '_Unsat.dat'

    return sim_dict_new
