# Author: Gabriel Cruz
# Date: 2025-04-09
# Description: This script uses the GBIF API to search for occurrences of a given species
# within a specified bounding box and date range.
# The results are saved to a CSV file.

# TO DO:
#   - Create functions for each step for better readability

import sys
from pygbif import occurrences
import pandas as pd
import argparse

def parser_arguments():
    # Get the arguments from the command line
    #   --specie
    #   --bbox (lat, long, 4 float values)
    #   --limit
    #   --begin_date
    #   --end_date
    #   --out_csv (output value)

    parser = argparse.ArgumentParser()

    parser.add_argument("--specie", required=True)
    parser.add_argument("--limit", required=True, type=int, default="100")
    parser.add_argument("--begin_date", required=True)
    parser.add_argument("--end_date", required=True)
    parser.add_argument("--out_csv", required=True, default="gbfier_out.csv")
    parser.add_argument("--bbox", nargs=4, type=float,  required=True)

    return parser.parse_args()

def main():
    args = parser_arguments()

    # Builds the string for the bounding box
    #   lat_max, lat_min, lon_max, lon_min
    lat_max, lat_min, lon_max, lon_min = args.bbox
    lat = f"{lat_min},{lat_max}"
    lon = f"{lon_min},{lon_max}"

    # Builds the string for the date range
    #  format: YYYY-MM-DD,YYYY-MM-DD
    eventDate_str = f"{args.begin_date},{args.end_date}"

    # Search for occurrences using the GBIF API
    # https://pygbif.readthedocs.io/en/latest/modules/occurrence.html
    gbif_data = occurrences.search(
        scientificName = args.specie,
        decimalLatitude = lat,
        decimalLongitude = lon,
        eventDate = eventDate_str,
        limit = args.limit,
        hasCoordinate = True
    )

    # Create dataframe from the results
    data_df = pd.DataFrame(gbif_data["results"])

    # Select the columns of interest
    #   decimalLongitude, decimalLatitude, year, day, month
    gbif_cols = data_df.columns.tolist()
    final_cols = ["decimalLongitude", "decimalLatitude", "year", "day", "month"]
    data_df_selected = data_df[[c for c in final_cols if c in gbif_cols]]

    # Save the dataframe to a CSV file
    data_df_selected.to_csv(args.out_csv, index=False)

if __name__ == "__main__":
    main()