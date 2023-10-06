import pandas as pd
from microjson import model as mj
from typing import List


def df_to_microjson(df: pd.DataFrame) -> mj.FeatureCollection:
    """
    Transforms a pandas DataFrame into a FeatureCollection model.

    This function is designed to convert geometries stored in a pandas
    DataFrame into a FeatureCollection model, based on the MicroJSON schema.

    Parameters:
    - df: The pandas DataFrame to transform. Each row should represent a
    feature.

    Returns:
    - A FeatureCollection object that aggregates the individual features.

    """
    # Initialize a list to hold the Feature objects
    features: List[mj.Feature] = []

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # Dynamically generate a Geometry object based on the row's
        # geometry type
        GeometryClass = getattr(mj, row["geometry_type"])
        geometry = GeometryClass(
            type=row["geometry_type"], coordinates=row["coordinates"]
        )

        # Create a Properties object to hold metadata about the feature
        properties = mj.Properties(
            string={"name": row["name"]},
            numeric={"value": row["value"]},
            multi_numeric={"values": row["values"]},
        )

        # Generate a Feature object that combines geometry and properties
        feature = mj.MicroFeature(
            type=row["type"], geometry=geometry, properties=properties
        )

        # Append this feature to the list of features
        features.append(feature)

    # Compute value ranges for numerical attributes
    value_range = {
        "value": {"min": df["value"].min(), "max": df["value"].max()},
        "values": {
            "min": df["values"].apply(min).min(),
            "max": df["values"].apply(max).max(),
        },
    }

    # Define which fields are to be considered as descriptive
    string_fields = ["name"]

    # Generate a FeatureCollection object to aggregate all features
    feature_collection = mj.MicroFeatureCollection(
        type="FeatureCollection",
        features=features,
        value_range=value_range,
        string_fields=string_fields,
        coordinatesystem={
            "axes": [
                {
                    "name": "x",
                    "type": "cartesian",
                    "unit": "meter",
                    "pixels_per_unit": 1,
                    "description": "The x-coordinate",
                },
                {
                    "name": "y",
                    "type": "cartesian",
                    "unit": "meter",
                    "pixels_per_unit": 1,
                    "description": "The y-coordinate",
                },
            ],
            "transformation_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        },
    )

    return feature_collection


if __name__ == "__main__":
    # Example DataFrame with two features: one Point and one Polygon
    data = [
        {
            "type": "Feature",
            "geometry_type": "Point",
            "coordinates": [0, 0],
            "name": "Point 1",
            "value": 1,
            "values": [1, 2, 3],
        },
        {
            "type": "Feature",
            "geometry_type": "Polygon",
            "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
            "name": "Polygon 1",
            "value": 2,
            "values": [4, 5, 6],
        },
    ]

    # Convert this list of dictionaries into a DataFrame
    df = pd.DataFrame(data)

    # Convert the DataFrame into a FeatureCollection model
    feature_collection_model = df_to_microjson(df)

    # Serialize the FeatureCollection model to a JSON string
    print(feature_collection_model.model_dump_json(indent=2, exclude_unset=True))
