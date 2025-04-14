# Author: Gabriel Cruz
# Date: 2025-04-09
# Description: This script uses the Copernicus Marine Toolbox to extract oceanographic data
# for a given set of coordinates and dates in a CSV file.
# The results are saved to a CSV file.

# TO DO:
#   - Create functions for each step for better readability

import argparse
import pandas as pd
import os
from dotenv import load_dotenv
import copernicusmarine
from datetime import date
import concurrent.futures

# Copernicus Marine Toolbox login
load_dotenv()
copernicus_user = os.getenv("COPERNICUS_USER")
copernicus_pass = os.getenv("COPERNICUS_PASS")
copernicusmarine.login(username=copernicus_user, password=copernicus_pass)

def parser_arguments():
    """
    Parses the arguments from the CLI.
    Args:
      --csv (str): name of the input CSV file
      --out_csv (str): name of the output CSV file
      --max_workers (int, optional): number of threads to use
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out_csv", required=True)
    parser.add_argument("--max_workers", type=int, default=5)

    return parser.parse_args()

def copernicus_get_data(linha, variable, client):
    """
    Retrieves the oceanographic data for a given location and date from the Copernicus Marine Toolbox.
    Args:
        linha (dict): line of the CSV file, containing the coordinates and date
        variable (str): variable to extract
        client: Copernicus Marine Toolbox client
    Returns:
        value (float): value of the variable
    """
    # Extracts the coordinates from the line
    #   decimalLongitude, decimalLatitude
    lon = linha['decimalLongitude']
    lat = linha['decimalLatitude']
    # Extracts the date from the line
    #   year, month, day
    date_time = date(int(linha['year']), int(linha['month']), int(linha['day'])).isoformat()
    # Extracts the variable from the Copernicus Marine Toolbox
    #   dataset_id, variable, lon, lat, date_time
    #   minimum_longitude, maximum_longitude, minimum_latitude, maximum_latitude
    #   start_datetime, end_datetime, minimum_depth, maximum_depth
    result = client.open_dataset(
        dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
        variables=[variable],
        minimum_longitude=lon,
        maximum_longitude=lon,
        minimum_latitude=lat,
        maximum_latitude=lat,
        start_datetime=date_time,
        end_datetime=date_time,
        minimum_depth=1,
        maximum_depth=2
    )
    # Extracts the value of the variable
    value = result[variable].isel(time=0, depth=0, latitude=0, longitude=0).values.item()
    return value

def extract_variables(line):
    """
    Extracts the oceanographic data for a given line of the CSV file. Uses the copernicus_get_data function
    to retrieve the data from the Copernicus Marine Toolbox.
    The function returns a dictionary with the variables extracted.
    Args:
        line (dict): line of the CSV file
    Returns:
        variables (dict): dictionary with the variables extracted
    """
    variables = {
        "thetao" : copernicus_get_data(line, 'thetao', copernicusmarine),
        "so" : copernicus_get_data(line, 'so', copernicusmarine)
    }
    return variables

def main():
    # Captures the cli arguments
    args = parser_arguments()

    # Reads the input .csv file and creates a DataFrame
    data_csv_df = pd.read_csv(args.csv)

    # Using threadPoolExecutor to parallelize the data extraction
    #   max_workers is the number of threads to use
    #   Call the extract_variables function for each line of the DataFrame and returns a list of results
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        result = list(executor.map(extract_variables, data_csv_df.to_dict(orient="records")))

    # Adds the results to the DataFrame
    #   thetao, so
    #   result is a list of dictionaries with the variables extracted
    data_csv_df["thetao"] = [r["thetao"] for r in result]
    data_csv_df["so"] = [r["so"] for r in result]

    # Removes all lines with NaN
    data_csv_df_clean = data_csv_df.dropna()

    # Writes the output .csv file
    data_csv_df_clean.to_csv(args.out_csv, index=False)

if __name__ == "__main__":
    main()