
# Building a dictionary from the Airway Excel sheet.
# Looking up an airway and returning its points.


import pandas as pd


def build_airway_dictionary(airway_df):

    airway_dictionary = {}

    for _, row in airway_df.iterrows():

        airway_name = str(row[1]).strip()
        points = []

        for point in row[2:]:

            if pd.notna(point):
                points.append(point)

        airway_dictionary[airway_name] = points

    return airway_dictionary


def get_airway_points(airway_name, airway_dictionary):
    return airway_dictionary.get(airway_name)

# Check if a token is an airway.
def is_airway(token, airway_dictionary):
    return token in airway_dictionary