from Backend.normalizer import normalize

def find_routes(
    routes_df,
    departure_fir=None,
    arrival_fir=None,
    entry_point=None,
    exit_point=None,
):

    # Search the RAD DataFrame and return all matching routes.
    matching_routes = []
    departure_fir = normalize(departure_fir)
    arrival_fir = normalize(arrival_fir)
    entry_point = normalize(entry_point)
    exit_point = normalize(exit_point)

    for _, row in routes_df.iterrows():

        if departure_fir and normalize(row["FIR/ADEP"]) != departure_fir:
            continue
        if arrival_fir and normalize(row["FIR/ADES"]) != arrival_fir:
            continue
        if entry_point and normalize(row["Entery Point"]) != entry_point:
            continue
        if exit_point and normalize(row["Exit Point"]) != exit_point:
            continue

        # Save the whole matching row
        matching_routes.append(row)

    return matching_routes