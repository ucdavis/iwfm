# getWKT_prj.py
# Return a WKT string containing projection information
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


def getWKT_prj(epsg_code, debug=0):
    """getWKT_prj() gets a WKT string containing PRJ info for <epsg_code>"""
    from urllib.request import urlopen

    wkt = urlopen(
        "http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code)
    )
    ans = "{}".format(wkt.read())  # convert bytecode to string
    output = (
        ans[1:].replace(" ", "").replace("\n", "").replace("\\", "").replace(",n", ",")
    )
    if debug:
        print(" wkt:   {}".format(output))
    return output
