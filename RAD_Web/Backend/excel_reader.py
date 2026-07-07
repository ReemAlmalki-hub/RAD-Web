import pandas as pd


def load_airway_dictionary():

    return pd.read_excel(
        r"Data\Airway_Dictionary.xlsx",
        header=None
    )


def load_rad_routes():

    return pd.read_excel(
        r"Data\RAD_V17.1.xlsx",
        header=1
    )