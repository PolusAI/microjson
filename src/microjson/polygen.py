import random
import math
import string
from shapely.geometry import MultiPoint
from shapely.geometry.polygon import orient
from typing import List
import microjson.model as mj


def generate_convex_polygon(x0, y0, x1, y1, num_vertices) -> List[float]:
    """
    Generates a convex polygon within the given bounding box.
    :param x0: x-coordinate of the bottom-left corner
    :param y0: y-coordinate of the bottom-left corner
    :param x1: x-coordinate of the top-right corner
    :param y1: y-coordinate of the top-right corner
    :param num_vertices: Number of vertices of the polygon
    :return: List of coordinates of the polygon
    """
    points = []
    center_x = (x0 + x1) / 2
    center_y = (y0 + y1) / 2
    max_radius_x = (x1 - x0) / 2 * 0.9  # To avoid touching cell edges
    max_radius_y = (y1 - y0) / 2 * 0.9

    # Generate sorted angles to maintain convexity
    angles = sorted(
        [random.uniform(
            0, 2 * math.pi
            ) for _ in range(num_vertices)])

    for angle in angles:
        # Random radius for each point
        r_x = random.uniform(max_radius_x * 0.5, max_radius_x)
        r_y = random.uniform(max_radius_y * 0.5, max_radius_y)
        x = center_x + r_x * math.cos(angle)
        y = center_y + r_y * math.sin(angle)
        points.append([x, y])

    # Close the polygon by appending the first point at the end
    points.append(points[0])

    # ensure the polygon is convex
    multipoint = MultiPoint(points)
    convex_hull = orient(multipoint.convex_hull, sign=1.0)

    return list(convex_hull.exterior.coords)


def assign_meta_types_and_values(n_keys, n_variants):
    """
    Randomly assigns a data type to each meta key ('meta1' to 'metan')
    and generates 4 random values for each key based on the assigned data type.
    : param n_keys: Number of meta keys
    : param n_variants: Number of possible values for each meta key

    Returns:
        meta_types: A dictionary where keys are 'meta1' to 'meta50' and values
        are the assigned data types.
        meta_values_options: A dictionary where keys are 'meta1' to 'meta50'
        and values are lists of 4 possible values.
    """
    meta_types = {}
    meta_values_options = {}
    for i in range(1, n_keys + 1):
        key = f"meta{i}"
        # Randomly choose a data type for each key
        value_type = random.choice(['int', 'float', 'string', 'bool'])
        meta_types[key] = value_type

        # Generate 4 random values of the assigned type
        values = []
        for _ in range(n_variants):
            if value_type == 'int':
                value = random.randint(0, 1000)
            elif value_type == 'float':
                value = round(random.uniform(0, 1000), 2)
            elif value_type == 'string':
                value = ''.join(random.choices(
                    string.ascii_letters + string.digits, k=8))
            elif value_type == 'bool':
                value = random.choice([True, False])
            values.append(value)
        meta_values_options[key] = values
    return meta_types, meta_values_options


def generate_meta_values(meta_values_options):
    """
    Generates a dictionary of meta values by randomly selecting one of the
    4 pre-generated values for each key.

    Args:
        meta_values_options: A dictionary where keys are 'meta1' to 'meta50'
        and values are lists of 4 possible values.

    Returns:
        A dictionary with meta keys and one of the 4 possible values for each.
    """
    meta_values = {}
    for key, options in meta_values_options.items():
        value = random.choice(options)
        meta_values[key] = value
    return meta_values


def generate_polygons(grid_size, cell_size, min_vertices, max_vertices,
                      meta_types, meta_values_options,
                      microjson_data_path) -> mj.MicroFeatureCollection:
    features = []
    num_cells = grid_size // cell_size
    for i in range(num_cells):
        for j in range(num_cells):
            # Cell boundaries
            x0 = i * cell_size
            y0 = j * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            # Random number of vertices for this polygon
            num_vertices = random.randint(min_vertices, max_vertices)

            dvx = 0
            hasmin = False
            # Generate a convex polygon within the cell
            while not hasmin:
                # Generate a convex polygon
                coordinates = [generate_convex_polygon(
                    x0, y0, x1, y1, num_vertices+dvx)]
                # Check if the polygon has the minimum number of vertices
                hasmin = len(coordinates[0]) >= min_vertices
                dvx += 1

            # Generate meta values by selecting from the 4 options
            meta_properties = generate_meta_values(meta_values_options)

            # Base properties
            base_properties = {
                "num_vertices": len(coordinates[0]),
            }

            # Combine base properties with meta properties
            properties = {**base_properties, **meta_properties}

            feature = mj.MicroFeature(
                type="Feature",
                geometry=mj.Polygon(
                    type="Polygon",
                    coordinates=coordinates  # type: ignore
                ),
                id=int(f"{i}{j}"),
                properties=properties
            )
            features.append(feature)
    # create microjson root object and validate it
    mjfc = mj.MicroFeatureCollection(
        properties={},
        type="FeatureCollection",
        features=features
    )
    mjfc.model_validate(mjfc)
    # write the microjson data to a file

    with open(microjson_data_path, "w") as f:
        f.write(mjfc.model_dump_json(indent=2))

    return mjfc
