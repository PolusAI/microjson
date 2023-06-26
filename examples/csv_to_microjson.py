import pandas as pd
import microjson.model as mj
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

        # Create a new Feature object
        feature = mj.Feature(
            type=row['type'],
            geometry=geometry,
            properties={},  # Add an empty properties dictionary
            coordinatesystem=mj.Coordinatesystem(
                axes=row['coordinatesystem_axes'],
                units=row['coordinatesystem_units']
            )
        )

        # Add the Feature object to the list
        features.append(feature)

    # Create a new FeatureCollection object
    feature_collection = mj.FeatureCollection(
        type='FeatureCollection',
        features=features
    )

    return feature_collection


# Example usage:
# Create a list of dictionary
data = [{
    'type': 'Feature',
    'geometry_type': 'Point',
    'coordinates': [0, 0],
    'coordinatesystem_axes': ['x', 'y'],
    'coordinatesystem_units': ['pixel', 'pixel']
}, {
    'type': 'Feature',
    'geometry_type': 'Polygon',
    'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
    'coordinatesystem_axes': ['x', 'y'],
    'coordinatesystem_units': ['pixel', 'pixel']
}]

df = pd.DataFrame(data)
feature_collection_model = df_to_microjson(df)
print(feature_collection_model.json(indent=2))
