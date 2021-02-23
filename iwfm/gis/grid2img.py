# grid2img.py
# Convert an ASCII DEM to an image
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


def grid2img(source, target):
    """grid2img() Convert an ASCII DEM to an image"""
    import numpy as np
    from PIL import Image, ImageOps  # pip install pillow

    arr = np.loadtxt(source, skiprows=6)  # Load the ASCII DEM into a numpy array
    im = Image.fromarray(arr).convert("RGB")  # Convert array to numpy image
    im = ImageOps.equalize(im)  # Enhance the image: equalize and increase contrast
    im = ImageOps.autocontrast(im)
    im.save(target)
