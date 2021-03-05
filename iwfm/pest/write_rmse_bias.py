# write_rmse_bias.py
# write RMSE and bias values to a text file
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


def write_rmse_bias(output_filename, well_dict, well_name, rmse, bias, count):
    """ write_rmse_bias() - Writes the RMSE and Bias values plus well info
        (name,x,y,layer) for all observation wells to a text file

    Parameters:
      output_filemane (str):   Name of output data file
      well_dict       (obj):   Distionary, well_name = key
      well_name       (list):  List op dictionark keys, for example state well names
      rmse            (arr):   List of numpy array of rmse values for each well
      bias            (arr):   List of numpy array of bias values for each well
      count           (list):  No. obsercations for each well
    
    Return:
      nothing
        
    """
    with open(output_filename, "w") as output_file:
        output_file.write('Order\tWell_Name\tX\tY\tLayer\tRMSE\tBias\tCount\n')
        for i in range(0, len(well_name)):
            if well_dict.get(well_name[i]) is not None:
                info = well_dict.get(well_name[i])
                output_file.write(
                    "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                        i + 1,
                        well_name[i],
                        round(info[1], 2),
                        round(info[2], 2),
                        info[3],
                        round(rmse[i], 2),
                        round(bias[i], 2),
                        count[i],
                    )
                )
    return
