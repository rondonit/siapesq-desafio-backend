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

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out_csv", required=True)

    return parser.parse_args()

def copernicus_get_data(linha, variable, client):
    lon = linha['decimalLongitude']
    lat = linha['decimalLatitude']
    date_time = date(int(linha['year']), int(linha['month']), int(linha['day'])).isoformat()
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
    value = result[variable].isel(time=0, depth=0, latitude=0, longitude=0).values.item()
    return value

def extract_variables(line):
    variables = {
        "thetao" : copernicus_get_data(line, 'thetao', copernicusmarine),
        "so" : copernicus_get_data(line, 'so', copernicusmarine)
    }
    return variables

# captures the cli arguments
args = parser_arguments()

# reads input .csv file
data_csv_df = pd.read_csv(args.csv)

# using threadPoolExecutor to parallelize the data extraction
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    result = list(executor.map(extract_variables, data_csv_df.to_dict(orient="records")))

# extracting the results into the DataFrame
data_csv_df["thetao"] = [r["thetao"] for r in result]
data_csv_df["so"] = [r["so"] for r in result]

# removes lines with NaN
data_csv_df_clean = data_csv_df.dropna()

# writes the output .csv file
data_csv_df_clean.to_csv(args.out_csv, index=False)