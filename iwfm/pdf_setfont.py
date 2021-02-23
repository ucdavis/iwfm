# pdf_setfont.py
# set font for a PDF instance
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


def pdf_setfont(pdf, font='Arial', style='B', size=20):
    """ pdf_setfont() - Set the font for a PDF instance

    Parameters:
      pdf             (PDF):  PDF object
      font            (str):  Font name
      style           (str):  Font style
      size            (int):  Font size

    Returns:
      pdf             (PDF):  PDF object
    """

    pdf.set_font(font, style, size)
    return pdf
