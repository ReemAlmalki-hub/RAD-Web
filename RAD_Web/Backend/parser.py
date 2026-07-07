def tokenize_route(route: str) -> list[str]:

    return route.split()


def clean_tokens(tokens: list[str]) -> list[str]:

    cleaned_tokens = []

    for token in tokens:
        token = token.strip()

        if token:
            cleaned_tokens.append(token)

    return cleaned_tokens