# geop_open.py
# Open file as a geopandas dataframe
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


def geop_open(infile):
    """ geop_open() - Open a file with geopandas and return geopandas object

    Parameters:
      infile          (str):  File name to save info from url

    Returns:
      gdf_file        (obj):  Geopandas object containing information from the infile

    """
    import geopandas

    gdf = geopandas.GeoDataFrame
    gdf_file = gdf.from_file(infile)
    return gdf_file
