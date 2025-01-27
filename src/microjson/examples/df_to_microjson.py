import pandas as pd  # type: ignore
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
        GeometryClass = getattr(mj, row["geometryType"])
        geometry = GeometryClass(
            type=row["geometryType"], coordinates=row["coordinates"]
        )
        properties = {}
        for key in ["name", "value", "values"]:
            properties[key] = row[key]

        # Generate a Feature object that combines geometry and properties
        feature = mj.MicroFeature(
            type=row["type"], geometry=geometry, properties=properties
        )

        # Append this feature to the list of features
        features.append(feature)

    # Generate a FeatureCollection object to aggregate all features
    feature_collection = mj.MicroFeatureCollection(
        type="FeatureCollection",
        features=features,
        properties={"plate": "Example Plate"}
    )

    return feature_collection


if __name__ == "__main__":
    # Example DataFrame with two features: one Point and one Polygon
    data = [
        {
            "type": "Feature",
            "geometryType": "Point",
            "coordinates": [0, 0],
            "name": "Point 1",
            "value": 1,
            "values": [1, 2, 3],
        },
        {
            "type": "Feature",
            "geometryType": "Polygon",
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
    print(feature_collection_model.model_dump_json(
        indent=2, exclude_unset=True))
