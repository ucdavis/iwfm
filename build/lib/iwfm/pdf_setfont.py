# pdf_setfont.py
# set font for a PDF instance
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


def pdf_setfont(pdf, font='Arial', style='B', size=20):
    ''' pdf_setfont() - Set the font for a PDF instance

    Parameters
    ----------
    pdf : PDF object
        PDF object to be modified
    
    font : str, default='Ariel'
        font name
    
    style : str, default='B'
        font style
    
    size : int, default=20
        font size in points

    Returns
    -------
    pdf : PDF object
        modified PDF object
    
    '''

    pdf.set_font(font, style, size)
    return pdf