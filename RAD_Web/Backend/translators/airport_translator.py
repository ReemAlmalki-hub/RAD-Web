
def translate_airports(tokens, airport_dictionary):
    
    #Translate airport codes only if they appearat the beginning or end of the route.

    translated_tokens = []
    last_index = len(tokens) - 1

    for index, token in enumerate(tokens):
        token = token.strip().upper()

        # Only first and last tokens can be airports
        if index == 0 or index == last_index:
            translated_tokens.append(
                airport_dictionary.get(token, token)
            )
        else:
            translated_tokens.append(token)
    return translated_tokens