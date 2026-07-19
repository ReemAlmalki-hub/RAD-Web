import pandas as pd
import re


def normalize(value):

    if pd.isna(value):
        return ""

    value = str(value)

    value = re.sub(r"\s+", "", value)

    return value.upper()