#!/usr/bin/env python

import sys
from pygbif import occurrences
import pandas as pd
import argparse

def parser_arguments():
    # captura os argumentos de linha de comando
    #   --specie
    #   --bbox (bound box com 4 valores float)
    #   --limit
    #   --begin_date
    #   --end_date
    #   --out_csv (arquivo de saída dos dados)

    parser = argparse.ArgumentParser()

    parser.add_argument("--specie", required=True)
    parser.add_argument("--limit", required=True, type=int, default="100")
    parser.add_argument("--begin_date", required=True)
    parser.add_argument("--end_date", required=True)
    parser.add_argument("--out_csv", required=True, default="gbfier_out.csv")
    parser.add_argument("--bbox", nargs=4, type=float,  required=True)

    return parser.parse_args()

#########################
# separar em função main?
args = parser_arguments()

# separa os argumentos --bbox para lat_max, lat_min, lon_max, lon_min
# constroi as strings para o pygbif

lat_max, lat_min, lon_max, lon_min = args.bbox

lat = f"{lat_min},{lat_max}"
lon = f"{lon_min},{lon_max}"

# usa --begin_date e --end_date para montar string
# no formato yyyy-MM-dd,yyyy-MM-dd
eventDate_str = f"{args.begin_date},{args.end_date}"

# faz a busca na API do GBIF usando a biblioteca pygbif
# https://pygbif.readthedocs.io/en/latest/modules/occurrence.html

gbif_data = occurrences.search(
    scientificName = args.specie,
    decimalLatitude = lat,
    decimalLongitude = lon,
    eventDate = eventDate_str,
    limit = args.limit,
    hasCoordinate = True
)

# cria DataFrame com os dados recebidos
data_df = pd.DataFrame(gbif_data["results"])


# filtra as colunas
gbif_cols = data_df.columns.tolist()
final_cols = ["decimalLongitude", "decimalLatitude", "year", "day", "month"]
data_df_selected = data_df[[c for c in final_cols if c in gbif_cols]]

# salva em .csv
data_df_selected.to_csv(args.out_csv, index=False)