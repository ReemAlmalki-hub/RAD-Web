from Backend.translators.airport_translator import translate_airports
from Backend.translators.airway_translator import translate_airways


# Route Expansion Pipeline
def expand_route(tokens, airway_dictionary, airport_dictionary):

    # Airway Translation
    tokens = translate_airways(tokens, airway_dictionary)

    # Airport Translation
    tokens = translate_airports(tokens, airport_dictionary)

    return tokens