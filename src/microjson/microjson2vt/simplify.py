# Original code from geojson2vt
# Copyright (c) 2015, Mapbox
# ISC License terms apply; see LICENSE file for details.

# Modifications by PolusAI, 2024

def simplify(coords, sq_tolerance):
    """Simplifies a list of coordinates using the Ramer-Douglas-Peucker
    algorithm."""

    if len(coords) <= 2:
        return coords

    def get_sq_seg_dist(px, py, x, y, bx, by):
        """Calculates the square distance from a point to a segment."""
        dx = bx - x
        dy = by - y

        if dx != 0 or dy != 0:
            t = ((px - x) * dx + (py - y) * dy) / (dx * dx + dy * dy)

            if t > 1:
                x = bx
                y = by
            elif t > 0:
                x += dx * t
                y += dy * t

        dx = px - x
        dy = py - y

        return dx * dx + dy * dy

    first = 0
    last = len(coords) - 1
    max_sq_dist = 0
    index = None

    for i in range(1, last):
        sq_dist = get_sq_seg_dist(coords[i][0], coords[i][1],
                                  coords[first][0], coords[first][1],
                                  coords[last][0], coords[last][1])
        if sq_dist > max_sq_dist:
            index = i
            max_sq_dist = sq_dist

    if max_sq_dist > sq_tolerance:
        left_simplified = simplify(coords[:index+1], sq_tolerance)
        right_simplified = simplify(coords[index:], sq_tolerance)

        # Exclude the last point of the left as it's the first of the right.
        return left_simplified + right_simplified[1:]
    else:
        return [coords[first], coords[last]]
