# choropleth.py
# Reads a shapefile and writes a chloropleth image
# Copyright (C) 2020-2025 University of California
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

def choropleth(infile,fieldname1,fieldname2,iwidth=600,
    iheight=400,denrat=80.0,savename=None):
    ''' choropleth() - Read a shapefile and write a chloropleth image

    Parameters
    ----------
    infile : str
        source shapefile name
    
    fieldname1 : str
        name of field for shading
    
    fieldname2 : str
        name of field for normalization
    
    iwidth : int, default=600
        image width in pixels
    
    iheight : int
        image height in pixels
    
    denrat : float, default=80.0
        density ratio
    
    savename : str, default=None
        image destination file name (None = not saved)

    Returns
    -------
    nothing

    '''
    import shapefile  # pyshp
    from PIL import Image, ImageDraw, ImageOps
    import iwfm as iwfm
    import math

    inShp = shapefile.Reader(infile)

    img = Image.new('RGB', (iwidth, iheight), (255, 255, 255))  
    draw = ImageDraw.Draw(img)  

    val_index1, val_index2 = None, None
    for i, f in enumerate(inShp.fields):  
        if f[0] == fieldname1:
            val_index1 = i - 1  # Account for the Deletion Flag field
        elif f[0] == fieldname2:
            val_index2 = i - 1  # Account for the Deletion Flag field

    for shp in inShp.shapeRecords():
        density = shp.record[val_index1] / shp.record[val_index2]
        weight = (min(math.sqrt(density / denrat), 1.0) * 50) 
        R, G, B = int(205 - weight), int(215 - weight), int(245 - weight)
        pixels = []
        for x, y in shp.shape.points:
            (px, py) = iwfm.gis.world2screen(inShp.bbox, iwidth, iheight, x, y)
            pixels.append((px, py))
        draw.polygon(pixels, outline=(255, 255, 255), fill=(R, G, B))
    if savename:
        img.save(savename)
    return
    