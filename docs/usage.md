# Create MicroJSON models

In this tutorial, we explain how a Python script is used to convert a pandas DataFrame into a MicroJSON FeatureCollection object.

## Example dataframe to MicroJSON conversion

::: microjson.examples.df_to_microjson.df_to_microjson
    :docstring:

Here's a breakdown of the steps involved:

1. **Initialize an empty list of Features**: A list `features` is initialized to hold `Feature` objects.

2. **Iterate over DataFrame rows**: The function iterates through each row of the DataFrame, performing the following operations for each row:

    - **Create a Geometry Object**: It dynamically generates a Geometry object based on the geometry type specified in the row.

    - **Create a Properties Object**: It then creates a `Properties` object to hold metadata about the feature like the name, value, and an array of values.

    - **Combine into a Feature**: It combines both the geometry and properties into a MicroJSON `Feature` object.

3. **Calculate Value Ranges**: For each numeric attribute, a range of values (min, max) is calculated.

4. **Create a FeatureCollection Object**: Finally, it aggregates all the features into a MicroJSON `FeatureCollection` object, including the calculated value ranges and other optional metadata.

## Example dataframe creation, conversion and MicroJSON output

Below, we convert a pandas DataFrame into a MicroJSON FeatureCollection object. It includes an example of creating a DataFrame with two features, one Point and one Polygon, and converting it into a FeatureCollection model using the `df_to_microjson` function as described above, and then serializing the model to a JSON string.

```python
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
    print(
        feature_collection_model.model_dump_json(indent=2, exclude_unset=True)
    )
```
