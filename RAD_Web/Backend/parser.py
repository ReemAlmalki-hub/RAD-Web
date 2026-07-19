from Backend.normalizer import normalize

# Tokenize Route
def tokenize_route(route):
    return route.split()


# Clean Tokenss
def clean_tokens(tokens):
    cleaned_tokens = []
    for token in tokens:
        token = normalize(token)
        if token:
            cleaned_tokens.append(token)

    return cleaned_tokens