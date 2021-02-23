# pdf_addimage.py
# add an image to a PDF instance
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


def pdf_addimage(pdf, image, ux=1, uy=1, width=6.5, height=9):
    """ pdf_cell() - Create a cell in a PDF instance

    Parameters:
      pdf             (PDF):   PDF object
      image           (obj):   Image object
      ux              (int):   X location of image
      uy              (int):   Y location of image
      width           (float): image width
      height          (float): image height

    Returns:
      pdf             (PDF):   PDF object
    """
    # upper left corner: ux, uy
    # width, height
    pdf.image(image, x=ux, y=uy, w=width, h=height)
    return pdf
