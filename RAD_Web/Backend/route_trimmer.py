def trim_airway(points, start_point, end_point):

    # Check if both points exist in the airway
    if start_point not in points or end_point not in points:
        return None

    start_index = points.index(start_point)
    end_index = points.index(end_point)

    # Normal direction
    if start_index <= end_index:
        return points[start_index:end_index + 1]

    # Reverse direction
    reversed_points = list(reversed(points))

    # Find the points again in the reversed airway
    start_index = reversed_points.index(start_point)
    end_index = reversed_points.index(end_point)

    return reversed_points[start_index:end_index + 1]