import pandas as pd

def build_airway_dictionary(sheet):

    airway_dictionary = {}

    for _, row in sheet.iterrows():

        # Skip empty airway names
        if pd.isna(row[1]):
            continue

        airway_name = str(row[1]).strip().upper()

        # Read all waypoints
        points = []
        for point in row[2:]:
            if pd.notna(point):
                points.append(str(point).strip().upper())

        airway_dictionary[airway_name] = points
    
    
    return airway_dictionary
