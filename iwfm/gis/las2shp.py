# las2shp.py
# Convert an LAS LIDAR file to a shapefile
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


def las2shp(source, target, debug=0):
    ''' las2shp() - Convert an LAS LIDAR file to a shapefile by creating a
        3D triangle mesh using Delaunay Triangulation

    ** This function isn't working for the example LIDAR file **
    
    Parameters
    ----------
    source : str
        source LIDAR file name
    
    target : str
        output shapefile name
    
    debug : int, default=0
        level of CLI priniting for debugging (0 = none)

    Returns
    -------
    nothing

    
    '''
    import shapefile  # pyshp
    import pickle
    import numpy as np
    from scipy.spatial import Delaunay

    archive = 'triangles.p'  # Triangles archive

    # class Point:
    #  def __init__(self, x, y):
    #      self.px = x
    #      self.py = y
    #  def x(self):
    #      return self.px
    #  def y(self):
    #      return self.py

    # The triangle array holds tuples of 3 point indicies used to retrieve the points.
    # Load it from a pickle file or use the voronoi module to create the triangles.
    triangles = None
    las = file(source, mode='r')  # Open LIDAR LAS file
    points = []
    if debug:
        print('    - Assembling points...')
    for x, y in np.nditer((las.x, las.y)):  # Pull points from LAS file
        points.append([x, y])
    pts = np.array(points)
    if debug:
        print('        len(points): {}'.format(len(pts)))
    # print('  points:\n{}'.format(pts))

    if debug:
        print('    - Composing triangles...')
    # Delaunay Triangulation
    # triangles = voronoi.computeDelaunayTriangulation(points)
    # triangles = DelaunayTri(points)             # pyhull.delaunay of list
    # triangles = DelaunayTri(pts)                # pyhull.delaunay of np.array
    triangles = Delaunay(pts)  # scipy.spatial.Dalaunay
    if debug:
        print('        points: {}'.format(triangles.simplices))

    # Save the triangles to save time if we write more than one shapefile.
    f = open(archive, 'wb')
    pickle.dump(triangles, f, protocol=2)
    f.close()

    if debug:
        print('    - Creating shapefile...')
    # PolygonZ shapefile (x, y, z, m)
    w = shapefile.Writer(target, shapefile.POLYGONZ)
    w.field('X1', 'C', '40')
    w.field('X2', 'C', '40')
    w.field('X3', 'C', '40')
    w.field('Y1', 'C', '40')
    w.field('Y2', 'C', '40')
    w.field('Y3', 'C', '40')
    w.field('Z1', 'C', '40')
    w.field('Z2', 'C', '40')
    w.field('Z3', 'C', '40')

    # extract the Delaunay triangle coordinates to an np.array
    tri = triangles.simplices
    tris = len(tri)

    # for s in triangles.simplices:
    #  for data in itertools.combinations(s.coords,dim):
    #    tri.append(data)
    if debug:
        print(f'        len(tri): {len(tri)}')
        print(f'        points:\n{tri}')

    # Loop through shapes and track progress every 10 percent
    last_percent = 0
    count = 0
    for i in range(tris):
        # t = triangles[i]
        t = tri[i]
        if debug:
            print(f'        t[{i}]: {t}')
        pct = int((i / (tris * 1.0)) * 100.0)
        if pct % 10.0 == 0 and pct > last_percent:
            last_percent = pct
            if debug:
                print(f'        {pct} % done - Shape {i}/{tris} at {time.asctime()}')
        part = []
        x1 = las.x[t[0]]
        y1 = las.y[t[0]]
        z1 = las.z[t[0]]
        if debug:
            print(f'        x1,y1,z1: {x1},{x2},{x3}')
        x2 = las.x[t[1]]
        y2 = las.y[t[1]]
        z2 = las.z[t[1]]
        if debug:
            print(f'        x2,y2,z2: {x2},{y2},{z2}')
        x3 = las.x[t[2]]
        y3 = las.y[t[2]]
        z3 = las.z[t[2]]
        if debug:
            print(f'        x3,y3,z3: {x3},{y3},{z3}')
        # Check segments for large triangles along the convex hull which is a common
        # artificat in Delaunay triangulation
        max = 3
        if math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) > max:
            continue
        if math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2) > max:
            continue
        if math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2) > max:
            continue
        part.append([x1, y1, z1, 0])
        part.append([x2, y2, z2, 0])
        part.append([x3, y3, z3, 0])
        if debug:
            print(f'        part: {part}\n')
        w.polyz([part])
        w.record(x1, x2, x3, y1, y2, y3, z1, z2, z3)
        count += 1
    if count == 0:
        w = None
    if debug:
        print('    - Saving shapefile...')
        print('    - las2shp() done.')

    return 
