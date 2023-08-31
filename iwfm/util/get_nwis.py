# get_nwis.py
# Save a data table from an NWIS website into a csv file. Prints status
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


def get_nwis(files):
    """ get_nwis() - Save a data table from an NWIS website into a csv file. Prints status.

    Parameters
    ----------
    files : list
        List of information about each file in the form [Name, Data Source, url]
    
    Returns
    -------
    info : list
        List of information about the saved files in the form [Name, Data Source]
    """
    import requests
    from bs4 import BeautifulSoup
    
    info = []

    #  Iterate through provided list
    for name, data_source, url in files:

        #  Form file name
        name = name.replace(' ', '_').lower() + '_raw.csv'
        info.append([name, data_source])

        #  Access url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        #  Extract all the data tables from the webpage
        tables = soup.find_all("table")

        #  Save the last table as a CSV file
        if tables:
            last_table = tables[-1]
            save_table_as_csv(name, last_table)
        else:
            print(f"No tables found on {url}")

    return info

def save_table_as_csv(name, table):
    """ save_table_as_csv() - Save a data table from a website into a csv file. Prints status.

    Parameters
    ----------
    name : string
        Name for new csv file.
    
    table : html
        Table collected from website.
    
    Returns
    -------
    nothing
    """
    import pandas as pd

    try:
        df = pd.read_html(str(table))[0]
        df.to_csv(f"{name}", index=False)
        print(f"Data table saved to {name}")
    except Exception as e:
        print(f"Failed to save table '{name}': {e}")
    

def format_file(info):
    """ format_file() - Save a data table from a website into a csv file. Prints status.

    Parameters
    ----------
    info : list
        List of information about the files to access in the form [Name, Data Source]
    
    Returns
    -------
    nothing
    """
    import csv
    import os

    #  Access each file separately
    for file, data_source in info:
        name = file.replace('raw', 'data')

        #  Read file contents
        with open(file, 'r') as raw:
            csv_reader = csv.reader(raw)
            next(csv_reader)  # Skip the first line (header)

            #  Write to new file
            with open(name, 'w', newline='') as new_file:
                csv_writer = csv.writer(new_file)

                # Write the header to the new CSV file
                csv_writer.writerow(["Date", "Data", "Units", "Data Source"])

                for line_number, line in enumerate(csv_reader, start=1):
                    # Get units from the second line
                    if line_number == 1:
                        index = line[1].index("Monthly mean in ") + 16
                        units = line[1][index:].split()[0]

                    # Process data starting from the fourth line
                    if line_number >= 4:
                        year = line[0]
                        for i, data in enumerate(line[1:13], start=1):
                            csv_writer.writerow([f"{i}/{year}", data, units, data_source])

        #  Delete old file of website table data
        os.remove(file)
        print(f"Data saved to {name}")



if __name__ == "__main__":

    file_info1 = ["Sacramento River", "USGS Gage 11370500 SACRAMENTO RIVER AT KESWICK, CA", "https://waterdata.usgs.gov/nwis/monthly?referred_module=sw&amp;site_no=11370500&amp;por_11370500_10158=2209233,00060,10158,1938-10,2022-11&amp;format=html_table&amp;date_format=YYYY-MM-DD&amp;rdb_compression=file&amp;submitted_form=parameter_selection_list"]
    file_info2 = ["Clear Creek", "USGS Gage 11372000 CLEAR C NR IGO CA", "https://waterdata.usgs.gov/nwis/monthly?referred_module=sw&amp;site_no=11372000&amp;por_11372000_10170=2209239,00060,10170,1940-10,2023-02&amp;format=html_table&amp;date_format=YYYY-MM-DD&amp;rdb_compression=file&amp;submitted_form=parameter_selection_list"]
    files = [file_info1, file_info2]
    
    print("WARNING: if 'Name' property is the same for any file(s), their output csv file will have the same name and be overwritten")
    info = get_nwis(files)
    format_file(info)

