# shp_epsg.py
# Read the projection file of a shapefile and return EPSG value
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


def shp_epsg(filename):
    """shp_epsg() reads the projection file and returns the EPSG value"""
    from urllib.parse import urlencode
    from urllib.request import urlopen
    import json

    if filename[-4:] != ".prj":
        filename = filename + ".prj"
    with open(filename, "r") as f:
        q = urlencode({"exact": True, "error": True, "mode": "wkt", "terms": f.read()})
        r = urlopen("http://prj2epsg.org/search.json", q.encode())
        j = json.loads(r.read().decode())
    return int(j["codes"][0]["code"])
