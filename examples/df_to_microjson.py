import pandas as pd
from microjson import model as mj
from typing import List


def df_to_microjson(df: pd.DataFrame) -> mj.FeatureCollection:
    """
    Transforms a pandas DataFrame into a FeatureCollection model.

    :param df: The pandas DataFrame to transform.
    :return: The transformed FeatureCollection model.
    """
    # Initialize a list to hold the Feature objects
    features: List[mj.Feature] = []

    # Iterate over the rows in the DataFrame
    for _, row in df.iterrows():
        # Create a new Geometry object dynamically
        GeometryClass = getattr(mj, row['geometry_type'])
        geometry = GeometryClass(
            type=row['geometry_type'],
            coordinates=row['coordinates']
        )

        # create a new properties object dynamically
        properties = mj.Properties(
            string={'name': row['name']},
            numeric={'value': row['value']},
            multi_numeric={'values': row['values']}
        )

        # Create a new Feature object
        feature = mj.MicroFeature(
            type=row['type'],
            geometry=geometry,
            properties=properties
        )

        # Add the Feature object to the list
        features.append(feature)

    # Create a value range object
    value_range = {
        'value': {
            'min': df['value'].min(),
            'max': df['value'].max()
        },
        'values': {
            'min': df['values'].apply(min).min(),
            'max': df['values'].apply(max).max()
        }
    }

    # Create a list of descriptive fields
    string_fields = ['name']


    # Create a new FeatureCollection object
    feature_collection = mj.MicroFeatureCollection(
        type='FeatureCollection',
        features=features,
        value_range=value_range,
        string_fields=string_fields,
        coordinatesystem={
            'axes': [
                {
                    'name': 'x',
                    'type': 'cartesian',
                    'unit': 'meter',
                    'pixels_per_unit': 1,
                    'description': 'The x-coordinate'
                },
                {
                    'name': 'y',
                    'type': 'cartesian',
                    'unit': 'meter',
                    'pixels_per_unit': 1,
                    'description': 'The y-coordinate'
                }
            ],
            'transformation_matrix': [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ],
        }
    )

    return feature_collection


# Example usage:
# Create a list of dictionary
data = [{
    'type': 'Feature',
    'geometry_type': 'Point',
    'coordinates': [0, 0],
    'name': 'Point 1',
    'value': 1,
    'values': [1, 2, 3]
}, {
    'type': 'Feature',
    'geometry_type': 'Polygon',
    'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
    'name': 'Polygon 1',
    'value': 2,
    'values': [4, 5, 6]
}]

df = pd.DataFrame(data)
feature_collection_model = df_to_microjson(df)
print(feature_collection_model.model_dump_json(indent=2, exclude_unset=True))
