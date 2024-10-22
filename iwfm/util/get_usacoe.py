# get_usacoe.py
# Save a data table from a USACOE website into a csv file
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

def get_usacoe(files):
    """ get_usacoe() - Save a data table from a USACOE website into a csv file

    Parameters
    ----------
    files : list
        List of information about each file in the form [Name, Data Source, url]
    
    Returns
    -------
    nothing
    """
    info = text_to_csv(files)
    format_file(info)


def add_data(lines, start, year):
    """ add_data() - Sort data by month in the months list.

    Parameters
    ----------
    lines : list of str
        The list of lines containing data to be added to the months.

    start : int
        The index representing the starting month in the months list. 
        It can be either 0 or 5, corresponding to the first or second set of months.

    Returns
    -------
    months : list of list
        A nested list containing six sublists, representing six consecutive months, 
        starting from the specified start index in the months list.
    """
    #  Months list, the first element in each sublist is the month number
    months = [[10], [11], [12], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
    
    #  Find the number of months with data entries in the table
    #  Only get data from months which have all data present
    if(start == 0):
        length = len(lines[32].split())
    else:
        length = len(lines[35].split())

    #  Determine number of days in February
    if is_leap_year(int(year)):
        feb_days = 29
    else:
        feb_days = 28
    
    #  Go line by line through the table, split to access different months' data
    for line in lines:
        this_line = line.split()

        #  Index for months list
        i = start

        #  If all months' data is present in the row, add each to its designated month's sublist
        if(len(this_line) >= length):
            for data in this_line[1:length]:
                months[i].append(data)
                i += 1
        #  If line 31, append data to months that have 31 days (skip months with 30 days)
        elif (len(this_line) == length - 2) and int(this_line[0]) == 31:
            for data in this_line[1:length]:
                #  If november, append to december instead
                if i == 1 or i == 4 or i == 6 or i == 8:
                    i += 1
                months[i].append(data)
                i += 1
        #  If line > days in February, append data to March instead
        elif start == 0 and (len(this_line) == length - 1) and int(this_line[0]) > feb_days:
            for data in this_line[1:length]:
                if(i == 4):
                    i += 1
                months[i].append(data)
                i += 1
    #  List of data sorted by month
    return months[start:start+6]

def format_file(info):
    """ format_file() - Read raw data file and write formatted data to new file.

    Parameters
    ----------
    info : list of tuples
        A list of tuples where each tuple contains two elements: 
        - file : str
            The file name of the raw data file extracted from the website table.
        - data_source : str
            The source of the data, such as the website name or any identifier.

    Returns
    -------
    nothing

    """
    import os

    #  Access each file separately
    for file, data_source in info:

        #  Create new file name for formatted data
        name = file.replace('raw', 'data')

        #  Read file contents
        with open(file, 'r') as raw:
            lines = raw.read().splitlines()
        
        #  Extract units, year, and data sets from file
        units = lines[3].split()[-1]
        year = lines[5].split()[2]
        line1 = lines[9:46]
        line2 = lines[70:107]
        
        #  Write to new file
        with open(name, 'w') as new_file:
                
            #  Header
            new_file.write("Date, Data, Units, Data Source\n")
            
            #  First 6 months (Oct - Mar)
            months1 = add_data(line1, 0, year)
            
            #  Second 6 months (Apr - Sep)
            months2 = add_data(line2, 6, year)

            #  Concatonate data into one list
            months = months1 + months2

            #  Write formatted data from months list into the new file in order of months (Oct - Sep)
            for list in months:
                month = list[0]
                for i, num in enumerate(list[1:]):
                    new_file.write(f"{month}/{i+1}/{year}, {num}, {units}, {data_source}\n")


        #  Delete old file of website table data
        os.remove(file)

        print(f"Data saved to {name}")

def is_leap_year(year):
    """ is_leap_yar() - Check if a given year is a leap year.

    Parameters
    ----------
    year : int
        The year to be checked for leap year.

    Returns
    -------
    bool
        True if the year is a leap year, False otherwise.
    """

    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        return True
    return False

def text_to_csv(files):
    """ text_to_csv() - Extract text from web pages and save as CSV files.

    Parameters
    ----------
    files : list of tuples
        A list of tuples where each tuple contains three elements:
        - File name for the CSV file to be saved (string).
        - Data source information (string).
        - URL of the web page from which text is to be extracted (string).

    Returns
    -------
    info : list of lists
        A list containing sublists with two elements each:
        - File name of the saved CSV file (string).
        - Data source information (string).

    Notes
    -----
    - The function may not work properly if the website structure changes or if the 'content' class is not found in the
      web page HTML.
    - The function uses the 'requests' library to fetch web pages. Ensure that the required library is installed in the
      Python environment.
    - The 'verify=False' parameter is used in the requests.get() method to bypass SSL certificate verification. This 
      may lead to potential security risks, and it's recommended to use the proper SSL certificate verification for 
      secure web pages.
    """
    import requests
    from bs4 import BeautifulSoup as bs4
    import csv

    #  List to store the file information for each processed web page
    info = []
    for file in files:

        #  Get url and create new file name, add (file name, data source) to info
        url = file[2]
        name = file[0].replace(' ', '_').lower() + "_raw.csv"
        info.append([name, file[1]])

        #  Send a GET request to the URL and fetch the web page content
        response = requests.get(url, verify = False)
        
        #  Check if the response status code is 200 (successful)
        if response.status_code == 200:
            #  Parse the HTML
            soup = bs4(response.text, 'html.parser')

            #  Find the element with 'content' class in the HTML
            content_element = soup.find('div', class_='content')
            
            #  Write the extracted text to a new CSV file
            if content_element:
                extracted_text = content_element.get_text(strip=True)
                with open(name, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([extracted_text])
                print(f"Text extracted and saved to {name}")
            else:
                print("No 'content' class found on the webpage.")
        else:
            print(f"Failed to fetch URL: {url}")
    return info

if __name__ == "__main__":

    # TODO: Add command line arguments
    
    """Run the main script to extract text from websites and save it to CSV files.
    
    WARNING: if 'Name' property is the same for any file(s), their output csv file will have the same name and be overwritten.

    NOTE: The 'files' list expects information about each website in the form of a list. Each sublist should contain 
    [name, data source, url]. This format could be changed. However, then each function/input probably would need to be changed as well. 

    It's essential to have the required dependencies (requests, csv, BeautifulSoup) installed to run this script 
    successfully. 

    """

    file_info1 = ["Chowchilla River", "Buchanan Reservoir releases (USACOE)", "https://www.spk-wc.usace.army.mil/fcgi-bin/annual.py?year=2023&res=Buchanan+Dam-H.V.+Eastman+Lake%2C+Chowchilla+River+Basin%2C+California&report=bucqt"]
    files = [file_info1]

    get_usacoe(files)


