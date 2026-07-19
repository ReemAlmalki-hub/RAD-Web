from Backend.normalizer import normalize


def validate_route(expanded_points, validation_dictionary):

    invalid_points = []

    for point in expanded_points:

        point = normalize(point)

        if not point:
            continue

        if len(point) != 5:
            continue

        if point not in validation_dictionary:
            invalid_points.append(point)

    return ", ".join(invalid_points)