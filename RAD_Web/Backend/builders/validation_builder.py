import pandas as pd
import re

# Normalize Point
def normalize_point(point):

    if pd.isna(point):
        return ""

    point = str(point)
    point = re.sub(r"\s+", "", point)

    return point.upper()


# Build Validation Set
def build_validation_dictionary(sheet):

    validation_set = set()

    for value in sheet.iloc[:, 0]:
        point = normalize_point(value)
        if point:
            validation_set.add(point)
    return validation_set