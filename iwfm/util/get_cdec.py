

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
    

def download_data_table(files):
    """ download_data_table() - Save a data table from a website into a csv file. Prints status.

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
        table = soup.find("table")

        #  Save the last table as a CSV file
        if table:
            save_table_as_csv(name, table)
        else:
            print(f"No tables found on {url}")

    return info


def format_file(info):
    """ download_data_table() - Save a data table from a website into a csv file. Prints status.

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

            #  Write to new file
            with open(name, 'w', newline='') as new_file:
                csv_writer = csv.writer(new_file)

                # Write the header to the new CSV file
                csv_writer.writerow(["Date", " Data", " Units", " Data Source"])

                for line_number, line in enumerate(csv_reader, start=0):
                    # Get units from the first line
                    if line_number == 0:
                        labels = line[1].split()
                        units = labels[1]

                    # Process data starting from the fourth line
                    if line_number >= 1:
                        year, data = line[0:2]
                        csv_writer.writerow([year, data, units, data_source])

        #  Delete old file of website table data
        os.remove(file)
        print(f"Data saved to {name}")



if __name__ == "__main__":
    """Run the main script to extract text from websites and save it to CSV files.
    
    WARNING: if 'Name' property is the same for any file(s), their output csv file will have the same name and be overwritten.

    NOTE: The 'files' list expects information about each website in the form of a list. Each sublist should contain 
    [name, data source, url]. This format could be changed. However, then each function/input probably would need to be changed as well. 

    It's essential to have the required dependencies (requests, csv, BeautifulSoup) installed to run this script 
    successfully. 

    """
    
    file_info1 = ["Feather River", "CDEC Kelly Ridge Powerplant Release", "https://cdec.water.ca.gov/dynamicapp/selectQuery?Stations=KLL&SensorNums=23&dur_code=D&Start=2021-10-01&End=2022-09-30"]
    files = [file_info1]
    
    print("WARNING: if 'Name' property is the same for any file(s), their output csv file will have the same name and be overwritten")
    info = download_data_table(files)
    format_file(info)

