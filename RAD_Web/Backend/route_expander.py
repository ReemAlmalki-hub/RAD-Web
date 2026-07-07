from Backend.airway_lookup import get_airway_points, is_airway
from Backend.route_trimmer import trim_airway


def expand_route(tokens, airway_dictionary):

    final_route = []

    for i in range(len(tokens)):

        current = tokens[i]

        # Handle non-airways
        if not is_airway(current, airway_dictionary):

            # Remove DCT
            if current != "DCT":
                final_route.append(current)

        # Handle airways
        else:

            # Airway must have a point before and after it
            if i == 0 or i == len(tokens) - 1:
                continue

            airway_points = get_airway_points(current, airway_dictionary)

            start_point = tokens[i - 1]
            end_point = tokens[i + 1]

            trimmed = trim_airway(
                airway_points,
                start_point,
                end_point,
            )

            # Skip if trimming failed
            if trimmed is None:
                continue

            # Add only intermediate points
            final_route.extend(trimmed[1:-1])

    return final_route