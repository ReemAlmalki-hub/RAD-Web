def find_routes(
    routes_df,
    departure_fir=None,
    arrival_fir=None,
    entry_point=None,
    exit_point=None,
):

    # Search the RAD DataFrame and return all matching routes.

    matching_routes = []

    for _, row in routes_df.iterrows():

        # Check Departure FIR
        if departure_fir:
            if str(row["FIR/ADEP"]).strip().upper() != departure_fir.strip().upper():
                continue

        # Check Arrival FIR
        if arrival_fir:
            if str(row["FIR/ADES"]).strip().upper() != arrival_fir.strip().upper():
                continue

        # Check Entry Point
        if entry_point:
            if str(row["Entery Point"]).strip().upper() != entry_point.strip().upper():
                continue

        # Check Exit Point
        if exit_point:
            if str(row["Exit Point"]).strip().upper() != exit_point.strip().upper():
                continue

        # Save the whole matching row
        matching_routes.append(row)

    return matching_routes