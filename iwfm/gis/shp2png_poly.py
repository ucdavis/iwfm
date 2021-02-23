# shp2png_poly.py
# Save a shapefile as a raster filling in polygons
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


def shp2png_poly(shapefile, outfile, iwidth=800, iheight=600):
    """shp2png_poly() converts a shapefile to a raster and saves as a
    png file, filling in polygon holes"""
    import iwfm as iwfm
    import pngcanvas as pngcanvas

    r = iwfm.shp_read(shapefile)  # Open the shapefile
    # Setup the world to pixels conversion
    xdist = r.bbox[2] - r.bbox[0]
    ydist = r.bbox[3] - r.bbox[1]
    xratio = iwidth / xdist
    yratio = iheight / ydist
    polygons = []
    for shape in r.shapes():  # Loop through all shapes
        for i in range(
            len(shape.parts)
        ):  # Loop through all parts to catch polygon holes!
            pixels = []
            pt = None
            if i < len(shape.parts) - 1:
                pt = shape.points[shape.parts[i] : shape.parts[i + 1]]
            else:
                pt = shape.points[shape.parts[i] :]
            for x, y in pt:
                px = int(iwidth - ((r.bbox[2] - x) * xratio))
                py = int((r.bbox[3] - y) * yratio)
                pixels.append([px, py])
            polygons.append(pixels)
    c = pngcanvas.PNGCanvas(iwidth, iheight)  # Set up the output canvas
    for p in polygons:  # Loop through the polygons and draw them
        c.polyline(p)
    with open(outfile, "wb") as f:  # Save the image
        f.write(c.dump())
        f.close()
