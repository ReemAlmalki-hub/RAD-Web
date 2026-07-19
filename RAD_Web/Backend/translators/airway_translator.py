from Backend.route_trimmer import trim_airway


def translate_airways(tokens, airway_dictionary):

    translated_route = []
    
    for i, token in enumerate(tokens):

        # Skip first and last tokens (usually airports)
        if i == 0 or i == len(tokens) - 1:
            translated_route.append(token)
            continue

        start_point = tokens[i - 1]
        end_point = tokens[i + 1]

        airway = token.strip().upper()
       
        # Not an airway
        if airway not in airway_dictionary:
            translated_route.append(token)
            continue

        airway_points = airway_dictionary[airway]
        

        trimmed = trim_airway(
            airway_points,
            start_point,
            end_point
        )
        

        if trimmed:
            # Remove start and end because they already exist
            translated_route.extend(trimmed[1:-1])
        else:
            # Could not trim, keep the original airway
            translated_route.append(token)
       
        
    return translated_route