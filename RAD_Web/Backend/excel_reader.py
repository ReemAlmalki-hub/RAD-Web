import pandas as pd
import os

# Folder where excel_reader.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level (to RAD_Web) then into Data
DATA_DIR = os.path.join(BASE_DIR, "..", "Data")


def load_airway_dictionary():

    return pd.read_excel(
        os.path.join(DATA_DIR, "Airway_Dictionary.xlsx"),
        header=None
    )


def load_rad_routes():

    return pd.read_excel(
        os.path.join(DATA_DIR, "RAD_V17.1.xlsx"),
        header=1
    )
