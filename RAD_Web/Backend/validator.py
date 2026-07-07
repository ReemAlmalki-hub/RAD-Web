import pandas as pd
import re

  # Normalize waypoint names 
def normalize_point(point):

    if pd.isna(point):
        return ""

    point = str(point)
    point = re.sub(r"\s+", "", point)

    return point.upper()


def build_validation_set(validation_df):
    
  # Build a set of valid waypoint names from the validation file.
   

    valid_points = set()

    for value in validation_df.iloc[:, 0]:
        point = normalize_point(value)

        if point:
            valid_points.add(point)

    return valid_points


def validate_route(expanded_points, valid_points):

    invalid_points = []

    for point in expanded_points:

        point = normalize_point(point)

        if not point:
            continue

        # Ignore non-waypoints
        if len(point) != 5:
            continue

        if point not in valid_points:
            invalid_points.append(point)

    return ", ".join(invalid_points)