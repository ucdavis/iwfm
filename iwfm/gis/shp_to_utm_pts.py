# shp_to_utm_pts.py
# Reproject a shapefile to UTM with PyShp
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


def shp_to_utm_pts(shape, outfile, verbose=False):
    ''' shp_to_utm_pts() - Reproject a point shapefile to UTM

    Parameters
    ----------
    shape : PyShp point shapefile
    
    outfile : str
        output point shapefile name
    
    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    tracks : list
        tracking points

    '''
    import shapefile  # PyShp
    import utm as utm

    zone = 0

    with shapefile.Writer(outfile, shapeType=shp.shapeType) as w:
        w.fields = shp.fields[1:]  # skip Deletion field
        for s in shp.iterShapeRecords():
            w.record(*s.record)
        for s in shp.iterShapes():  # this reprojects
            lon, lat = s.points[0]
            x, y, zone, band = utm.from_latlon(lat, lon)
            w.point(x, y)

    # for UTM 1N-29N
    # the zone variable will tell which UTM zone this shapefile is in
    prj = urlopen(f'http://spatialreference.org/ref/epsg/269{str(zone)}/esriwkt/')  

    with open(f'{outfile}.prj', 'w') as f:
        f.write(str(prj.read()))

    if verbose:
        print(f'  Wrote {outfile}, UTM Zone: {zone}')
    return
