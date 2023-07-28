# pdf_combine.py
# Combines all of the PDF files in a folder into one PDF file
# info and gwhyd_sim columns, and returns the dictionary
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


def pdf_combine(start_dir, save_dir, save_name):
    ''' PDF_combine() - Combine all of the PDF files in a folder into one PDF file
    modified from https://geektechstuff.com/2018/02/17/python-3-merge-multiple-pdfs-into-one-pdf/

    Parameters
    ----------
    start_dir : str
        Name of directory with PDF files to combine

    save_dir : str
        Name of output directory

    save_name : str
        Name of output file

    Returns
    -------
    count : int
        Number of PDFs combined

    '''
    import os, PyPDF2

    os.chdir(save_dir)  # change to PDFs folder
    count = 0
    mergelist = []
    for filename in os.listdir('.'):
        if filename.endswith('.pdf'):
            mergelist.append(filename)

    pdfWriter = PyPDF2.PdfFileWriter()

    # loop through all PDFs
    for filename in mergelist:
        count += 1
        pdfFileObj = open(filename, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        for pageNum in range(len(pdfReader.pages)):  
            pageObj = pdfReader.pages[pageNum]
            pdfWriter.add_page(pageObj)

    os.chdir(start_dir) 
    pdfOutput = open(save_name, 'wb') 
    pdfWriter.write(pdfOutput) 
    pdfOutput.close()  
    return count

if __name__ == '__main__':
    ' Run pdf_combine() from command line '
    import sys
    import iwfm as iwfm
    import iwfm.debug as idb

    # read arguments from command line
    if len(sys.argv) > 1:  # arguments are listed on the command line
        start_dir = sys.argv[1]         # Name of directory with PDF files to combine
        save_dir  = sys.argv[2]         # Name of output directory
        save_name = sys.argv[3]         # Name of output file

    else:  # get everything form the command line
        start_dir = input('Directory with individual PDF files: ')
        save_dir  = input('Output directory: ')
        save_name = input('Output file mname: ')


    idb.exe_time()  # initialize timer
    count = pdf_combine(start_dir, save_dir, save_name)
    print(f'  Combined {count} PDF files')  # update cli
    idb.exe_time()  # print elapsed time
