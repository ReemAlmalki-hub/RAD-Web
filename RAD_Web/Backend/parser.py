from Backend.normalizer import normalize

# Tokenize Route
def tokenize_route(route):
    return route.split()


# Clean Tokens
def clean_tokens(tokens):
    cleaned_tokens = []

    for token in tokens:
        token = normalize(token)

        # Skip empty tokens and DCT
        if token and token != "DCT":
            cleaned_tokens.append(token)

    return cleaned_tokens
