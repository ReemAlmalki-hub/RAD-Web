import pandas as pd

def build_airport_dictionary(sheet):
    airport_dictionary = {}

    for _, row in sheet.iterrows():
        if pd.isna(row[0]) or pd.isna(row[1]):
            continue

        airport = str(row[0]).strip().upper()
        equivalent = str(row[1]).strip().upper()
        airport_dictionary[airport] = equivalent

    return airport_dictionary