# get_usbr.py
# Save a data table from a USBR website into a csv file. Prints status
# Copyright (C) 2023 University of California
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

def get_usbr(year, pdf_url, excel_filename='temp.xlsx'):
   """ get_usbr() - Save a data table from a USBR website into a csv file

    Parameters
    ----------
    year : int
        Year of the data to be extracted.

    pdf_url : str
        The URL of the online PDF containing tables.

    excel_filename : str
        The name of the Excel file to save the extracted tables.
    
    Returns
    -------
    nothing
    """
    import os

    #  Extract tables from pdf and save to Excel file
    pdf_to_excel(pdf_url, excel_filename)

    #  Create a csv file for each table in the pdf (4 total)
    extract_data_to_csv(excel_filename)

    #  Delete created excel file
    os.remove(excel_filename)


# Function to read tables from an online PDF and save to Excel
def pdf_to_excel(pdf_url, excel_filename):
    """pdf_to_excel() - Read tables from an online PDF and save them to an Excel file.

    Parameters
    ----------
    pdf_url : str
        The URL of the online PDF containing tables.

    excel_filename : str
        The name of the Excel file to save the extracted tables.

    Returns
    -------
    nothing
    """

    import tabula
    import pandas as pd

    # Read tables from the online PDF
    tables = tabula.read_pdf(pdf_url, pages='all', multiple_tables=True)
    
    # Initialize an Excel writer
    excel_writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
    
    # Loop through each table and save it to the Excel file
    for i, table in enumerate(tables):
        sheet_name = f'Table_{i+1}'
        table_df = pd.DataFrame(table)
        table_df.to_excel(excel_writer, sheet_name=sheet_name, index=False)
        
    # Close the Excel writer
    excel_writer.close()
    
    print(f"Tables from {pdf_url} have been extracted and saved to {excel_filename}.")

def is_year_in_list(year, string_list):
    """is_year_in_list() - Check if a given year is present in any of the strings in a list.

    Parameters
    ----------
    year : str
        The year to check for in the strings.

    string_list : list of str
        A list of strings to search for the given year.

    Returns
    -------
    int or -1
        If the year is found in any of the strings, it returns the index (integer) of the first occurrence.
        If the year is not found in any of the strings, it returns -1.
    """

    for i, string in enumerate(string_list):
        # Split the string by whitespace to get individual words
        words = str(string).split()
        
        # Iterate through the words to check if the year is present
        for word in words:
            if year in word:
                return i
    
    # If the year is not found in any of the strings, return False
    return -1

def get_data(df, table_number, year):
    """get_data() - Extract data for a given year from a DataFrame.

    Parameters
    ----------
    df : pandas DataFrame
        The DataFrame containing the data.

    i : int
        An integer representing the table number.

    year : int or str
        The year for which data needs to be extracted from the DataFrame.

    Returns
    -------
    list
        A list containing the data for the given year. If the year is not found, an empty list is returned.
    """

    #  Account for different format in recent year's (2022) pdf
    if int(year) > 2021 and table_number < 3:
        start = 0
    else:
        start = 1

    #  Convert DataFrame to list
    data = df.values.tolist()

    #  Search for year in header line
    index = is_year_in_list(year, data[0])

     #  For new file format (years > 2021), header may be in this line instead
    index0 = is_year_in_list(year, df.columns.tolist())

    #  If year not found in header, might be in other line checked
    if(index == -1):
        index = index0

    #  If year is found, form list of data in its column
    if(index != -1):
        datas = []
        for list in data[start:]:
            #  If element is not NaN, add to list
            if(str(list[index]) != 'nan'):
                datas.append(list[index])
            #  For years > 2021, sometimes excel sheet creates 2 columns / header
            #  Data is then offest 1 to right
            elif int(year) > 2021:
                datas.append(list[index + 1])
    return datas

def get_names(df, table_number, year):
    """get_names() - Extract reservoir names from a DataFrame.

    Parameters
    ----------
    df : pandas DataFrame
        The DataFrame containing the data.

    table_number : int
        The table number for which reservoir names need to be extracted.

    year : int or str
        The year for which reservoir names need to be extracted.

    Returns
    -------
    list
        A list of reservoir names extracted from the DataFrame.
    """

    #  Account for different format in recent year's (2022) pdf
    if int(year) > 2021:
        start = 0
    else:
        start = 1

    #  Get first column of DataFrame with names
    names = df.iloc[start:, 0].tolist()


    #  Add names of correct format to list
    resivoir_names = []
    j = 0
    while j < len(names):
        if (str(names[j]) != 'nan'):
            #  When converting pdf to excel, error in splitting names at " AT". This fixes it.
            if (" AT" in str(names[j])):
                new_name = names[j] + " " + names[j + 1]
                resivoir_names.append(new_name)
                j += 1
            else:
                resivoir_names.append(names[j])
        j += 1    

    #  For first table, concatonate each dam name to the reservoir name     
    if(table_number == 0):
        #  Get dam names
        dam_names = df.iloc[2:,1].tolist()

        #  Concatonate each name pairing
        for k, dam in enumerate(dam_names):
            resivoir_names[k] = resivoir_names[k] + ' AT ' + dam + " DAM"
    return resivoir_names


def extract_data_to_csv(excel_file):
    """extract_data_to_csv() - Extract data from an Excel file and save it into 4 separate csv files.

    Parameters
    ----------
    excel_file : str
        The path to the Excel file from which data needs to be extracted.

    Returns
    -------
    nothing
    """
    #  Get year
    year = excel_file[-9:-5]

    #  Units for tables 1-4
    units = ["Cubic Feet/Second", "Thousands of Acre-Feet", "Thousands of Acre-Feet", "Inches", "IDK"]
    
    #  Titles for tables 1-4
    titles = ["Reservoir Releases", "Storage in Major Resevoirs", "Accumulated Inflow", "Accumulated Precipitation"]

    # Read all sheets of the Excel file into a dictionary of DataFrames
    xls = pd.read_excel(excel_file, sheet_name=None)

    #  Create list of formatted file names
    file_names = []
    for title in titles:
        file_names.append(f"{title.replace(' ', '_').lower()}_{year}_uwbr.csv")
        
    #  Go through each DataFrame, one per table
    i = 0
    for _, df in xls.items():
        #  Open the corresponding file
        with open(file_names[i], 'w') as f:
            #  Write header
            f.write("Date, Data, Units, Data Source Location\n")

            #  Get names and dates
            names = get_names(df, i, year)
            datas = get_data(df, i, year)

            #  Write formatted information to file        
            for n, dat in enumerate(datas):
                f.write(f"{year}, {dat}, {units[i]}, {names[n]}\n")      
        print(f"{title} data saved into {file_names[i]}")
        #  Increment to keep track of table number
        i += 1


if __name__ == "__main__":

    year = input("Which year's CVP END OF WATER YEAR REPORT would you like? ")

    pdf_url = f'https://www.usbr.gov/mp/cvo/vungvari/dayrpt09_{year}.pdf'
    
    excel_filename = f'CVP_{year}.xlsx'

    get_usbr(year, pdf_url, excel_filename)


