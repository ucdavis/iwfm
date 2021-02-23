# shp_to_utm_pts.py
# Reproject a shapefile to UTM with PyShp
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


def shp_to_utm_pts(infile, outfile, debug=0):
    """Reproject a point shapefile to UTM"""
    import shapefile  # PyShp

    zone = 0
    shp = shapefile.Reader(infile)  # open shapefile Reader
    if debug:
        print("  {} records".format(shp_recno(shp)))
    with shapefile.Writer(
        outfile, shapeType=shp.shapeType
    ) as w:  # open shapefile Writer
        # w.shapeType = shp.shapeType
        w.fields = shp.fields[1:]  # skip Deletion field
        for s in shp.iterShapeRecords():
            w.record(*s.record)
            # w.shape(s.shape)                 # this would make a copy
        for s in shp.iterShapes():  # this reprojects
            lon, lat = s.points[0]
            x, y, zone, band = utm.from_latlon(lat, lon)
            w.point(x, y)
    # the zone variable will tell which UTM zone this shapefile is in
    if debug:
        print("  zone {} ".format(zone))
    prj = urlopen(
        "http://spatialreference.org/ref/epsg/269" + str(zone) + "/esriwkt/"
    )  # for UTM 1N-29N
    with open(outfile + ".prj", "w") as f:
        f.write(str(prj.read()))
    return 0
