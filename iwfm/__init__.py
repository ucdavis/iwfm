# __init__.py for iwfm package
# Classes and methods to read, write and modify IWFM and IGSM files and
# associated data files
# Copyright (C) 2018-2023 University of California
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

# -- IWFM model class -------------------------------------
from iwfm.iwfm_model import iwfm_model
from iwfm.gw_well_lay_elev import gw_well_lay_elev
from iwfm.idw import idw

# -- IWFM model file ---------------------------------------
from iwfm.iwfm_read_model_file import iwfm_read_model_file
from iwfm.sim_info import sim_info

# -- IWFM preprocessor files -------------------------------
from iwfm.iwfm_read_preproc import iwfm_read_preproc
from iwfm.iwfm_read_elements import iwfm_read_elements
from iwfm.iwfm_read_nodes import iwfm_read_nodes
from iwfm.iwfm_read_chars import iwfm_read_chars
from iwfm.iwfm_read_lake import iwfm_read_lake
from iwfm.iwfm_read_streams import iwfm_read_streams
from iwfm.iwfm_read_strat import iwfm_read_strat

from iwfm.iwfm_strat_arrays import iwfm_strat_arrays
from iwfm.iwfm_lse import iwfm_lse
from iwfm.iwfm_aquifer_thickness import iwfm_aquifer_thickness
from iwfm.iwfm_aquifer_top import iwfm_aquifer_top
from iwfm.iwfm_aquifer_bottom import iwfm_aquifer_bottom
from iwfm.iwfm_aquitard_thickness import iwfm_aquitard_thickness
from iwfm.iwfm_aquitard_top import iwfm_aquitard_top
from iwfm.iwfm_aquitard_bottom import iwfm_aquitard_bottom

# -- IWFM simulation files -------------------------------
from iwfm.iwfm_read_gw import iwfm_read_gw

# -- create a submodel ------------------------------------
from iwfm.iwfm_sub_preproc import iwfm_sub_preproc
from iwfm.sub_pp_file import sub_pp_file
from iwfm.sub_pp_node_file import sub_pp_node_file
from iwfm.sub_pp_elem_file import sub_pp_elem_file
from iwfm.sub_pp_lake_file import sub_pp_lake_file
from iwfm.sub_pp_strat_file import sub_pp_strat_file
from iwfm.sub_pp_stream_file import sub_pp_stream_file
from iwfm.get_elem_list import get_elem_list
from iwfm.sub_pp_nodes import sub_pp_nodes
from iwfm.sub_pp_lakes import sub_pp_lakes
from iwfm.sub_pp_streams import sub_pp_streams
from iwfm.get_stream_list_42 import get_stream_list_42
from iwfm.new_pp_dict import new_pp_dict

from iwfm.iwfm_sub_sim import iwfm_sub_sim
from iwfm.iwfm_read_sim_file import iwfm_read_sim_file
from iwfm.sub_sim_file import sub_sim_file
from iwfm.sub_swhed_file import sub_swhed_file
from iwfm.sub_unsat_file import sub_unsat_file
from iwfm.sub_gw_file import sub_gw_file
from iwfm.sub_gw_bc_file import sub_gw_bc_file
from iwfm.sub_gw_bc_cghd_file import sub_gw_bc_cghd_file
from iwfm.sub_gw_pump_file import sub_gw_pump_file
from iwfm.sub_gw_pump_epump_file import sub_gw_pump_epump_file
from iwfm.sub_gw_pump_well_file import sub_gw_pump_well_file
from iwfm.sub_gw_td_file import sub_gw_td_file
from iwfm.sub_gw_subs_file import sub_gw_subs_file
from iwfm.sub_streams_file import sub_streams_file
from iwfm.sub_st_inflow_file import sub_st_inflow_file
from iwfm.sub_st_bp_file import sub_st_bp_file
from iwfm.sub_rootzone_file import sub_rootzone_file
from iwfm.sub_rz_npc_file import sub_rz_npc_file
from iwfm.sub_rz_pc_file import sub_rz_pc_file
from iwfm.sub_rz_urban_file import sub_rz_urban_file
from iwfm.sub_rz_nv_file import sub_rz_nv_file
from iwfm.sub_remove_items import sub_remove_items
from iwfm.sub_lu_file import sub_lu_file

from iwfm.new_sim_dict import new_sim_dict

# -- IWFM simulation files --------------------------------
from iwfm.iwfm_read_sim import iwfm_read_sim
from iwfm.simhyds import simhyds

# -- IWFM land use methods --------------------------------
from iwfm.iwfm_adj_crops import iwfm_adj_crops
from iwfm.iwfm_lu2sub import iwfm_lu2sub
from iwfm.read_lu_file import read_lu_file
from iwfm.write_lu2file import write_lu2file
from iwfm.lu2tables import lu2tables
from iwfm.lu2csv import lu2csv

# -- IWFM land use file changes for scenarios -------------
from iwfm.iwfm_lu4scenario import iwfm_lu4scenario
from iwfm.get_change_col import get_change_col
from iwfm.read_lu_change_zones import read_lu_change_zones
from iwfm.read_lu_change_factors import read_lu_change_factors
from iwfm.iwfm_precip_adj import iwfm_precip_adj

# -- igsm file methods ------------------------------------
from iwfm.igsm_read_elements import igsm_read_elements
from iwfm.igsm_read_nodes import igsm_read_nodes
from iwfm.igsm_read_chars import igsm_read_chars
from iwfm.igsm_read_strat import igsm_read_strat
from iwfm.igsm_read_lake import igsm_read_lake
from iwfm.igsm_read_streams import igsm_read_streams

# -- IWFM budget files ------------------------------------
from iwfm.budget_info import budget_info

# -- post-process IWFM results ----------------------------
from iwfm.write_results import write_results
from iwfm.simhyd_obs import simhyd_obs
from iwfm.wdl_meas_stats import wdl_meas_stats
from iwfm.wdl_ts_4_wells import wdl_ts_4_wells

# --- plotting methods --for IWFM output ------------------
from iwfm.read_obs_smp import read_obs_smp
from iwfm.read_sim_wells import read_sim_wells
from iwfm.read_sim_hyds import read_sim_hyds
from iwfm.hyd_diff import hyd_diff
from iwfm.gw_plot_draw import gw_plot_draw
from iwfm.gw_plot_noobs_draw import gw_plot_noobs_draw
from iwfm.gw_plot_noobs import gw_plot_noobs
from iwfm.gw_plot_obs_draw import gw_plot_obs_draw
from iwfm.gw_plot_obs import gw_plot_obs
from iwfm.gw_plot import gw_plot
from iwfm.write_smp import write_smp
from iwfm.draw_plot import draw_plot
from iwfm.read_obs import read_obs
from iwfm.pdf_combine import pdf_combine

# -- post-process headall.out file ------------------------
from iwfm.headall_read import headall_read
from iwfm.headall2csv import headall2csv
from iwfm.headall2dtw import headall2dtw
from iwfm.headall2table import headall2table
from iwfm.headall2ts import headall2ts
from iwfm.get_heads_4_date import get_heads_4_date

# -- finite-element methods -------------------------------
from iwfm.elem_poly_coords import elem_poly_coords
from iwfm.iwfm_nearest_nodes import iwfm_nearest_nodes
from iwfm.nearest_node import nearest_node
from iwfm.nearest import nearest
from iwfm.in_element import in_element

# -- text file methods -------------------------------------
from iwfm.write_2_dat import write_2_dat
from iwfm.skip_ahead import skip_ahead
from iwfm.pad_front import pad_front
from iwfm.pad_back import pad_back
from iwfm.pad_both import pad_both
from iwfm.print_to_string import print_to_string
from iwfm.file_2_list import file_2_list

# -- date and time methods --------------------------------
from iwfm.diff_dates import diff_dates
from iwfm.dss_date import dss_date
from iwfm.month import month
from iwfm.day import day
from iwfm.year import year
from iwfm.text_date import text_date
from iwfm.date2text import date2text
from iwfm.index_date import index_date
from iwfm.date_index import date_index
from iwfm.str2datetime import str2datetime
from iwfm.dts2days import dts2days
from iwfm.dates_diff import dates_diff
from iwfm.secs_between import secs_between
from iwfm.Unbuffered import Unbuffered

# -- dictionary methods -----------------------------------
from iwfm.file2dict import file2dict
from iwfm.file2dict_int import file2dict_int
from iwfm.hyd_dict import hyd_dict
from iwfm.inverse_dict import inverse_dict
from iwfm.list2dict import list2dict

# -- DBF methods ------------------------------------------
from iwfm.dbf_open import dbf_open
from iwfm.dbf_print_record import dbf_print_record

# -- PDF methods -- ---------------------------------------
from iwfm.pdf_create import pdf_create
from iwfm.pdf_addpages import pdf_addpages
from iwfm.pdf_setfont import pdf_setfont
from iwfm.pdf_cell import pdf_cell
from iwfm.pdf_addimage import pdf_addimage
from iwfm.pdf_save import pdf_save
from iwfm.pdf2csv import pdf2csv

# -- file system methods ----------------------------------
from iwfm.file_test import file_test
from iwfm.file_missing import file_missing
from iwfm.file_delete import file_delete
from iwfm.file_rename import file_rename
from iwfm.filename_ext import filename_ext
from iwfm.filename_base import filename_base
from iwfm.file_dir import file_dir
from iwfm.file_2_bak import file_2_bak
from iwfm.file_type_error import file_type_error
from iwfm.file_get_path import file_get_path

# -- unit conversion --------------------------------------
from iwfm.cfs2afd import cfs2afd

# -- math -------------------------------------------------
from iwfm.distance import distance
from iwfm.logtrans import logtrans
from iwfm.rmse_calc import rmse_calc
from iwfm.bias_calc import bias_calc
from iwfm.round import round
from iwfm.column_sum import column_sum

# -- data file methods ------------------------------------
from iwfm.cdec2monthly import cdec2monthly
from iwfm.vic_2_table import vic_2_table
from iwfm.detaw_2_table import detaw_2_table
from iwfm.dicu2table import dicu2table
from iwfm.write_flows import write_flows

# -- Excel methods -----------------------------------------
from iwfm.bud2xl import bud2xl
from iwfm.xl_open import xl_open
from iwfm.xl_write_2d import xl_write_2d
from iwfm.xl_save import xl_save
from iwfm.xl_quit import xl_quit
from iwfm.write_2_excel import write_2_excel


# -- multiprocessing --------------------------------------
from iwfm.multiproc import multiproc

# -- other methods -----------------------------------------
# from iwfm.meas_bounds import meas_bounds
