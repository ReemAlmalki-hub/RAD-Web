from pathlib import Path
import pandas as pd


# Data folder
DATA_FOLDER = Path("Data")

# File locations
DICTIONARY_FILE = DATA_FOLDER / "Dictionary.xlsx"
RAD_FILE = DATA_FOLDER / "RAD.xlsx"


# Dictionary Workbook
def load_dictionary():
   
    # Load all sheets from the Dictionary workbook.
   

    if not DICTIONARY_FILE.exists():
        return None

    workbook = pd.ExcelFile(DICTIONARY_FILE)
    sheets = {}

    for sheet_name in workbook.sheet_names:
        sheets[sheet_name] = pd.read_excel(
            workbook,
            sheet_name=sheet_name,
            header=None
        )

    return sheets


# RAD Routes
def load_rad_routes():
    # Load the current RAD file.

    if not RAD_FILE.exists():
        return None

    return pd.read_excel(
        RAD_FILE,
        header=1
    )