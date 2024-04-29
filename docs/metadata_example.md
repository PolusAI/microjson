# Metadata Usage in MicroJSON Example

This guide demonstrates how to populate the `string`, `numeric`, and `multiNumeric` fields under the 'properties' field as per the MicroJSON specification using a rectangular polygon as the geometry.

## Properties Class Overview

In MicroJSON, metadata related to a feature is stored in the `Properties` class. This class encompasses three fields:

- `string`: A dictionary containing string metadata. This can include textual information such as the name and description of the feature.
- `numeric`: A dictionary containing numeric metadata. This field can be used to store quantifiable data related to the feature, like the cell count in a microscopic image.
- `multiNumeric`: A dictionary where each entry is a list of numeric values. This can be useful for storing data with multiple numeric values under a single key, such as ratio of infectivity over time.

Now, let's explore an example to understand how these fields can be populated in both JSON and Python.

### JSON Example

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [100.0, 0.0],
        [101.0, 0.0],
        [101.0, 1.0],
        [100.0, 1.0],
        [100.0, 0.0]
      ]
    ]
  },
  "properties": {
    "string": {
      "name": "Sample Polygon",
      "description": "This is a sample rectangular polygon."
    },
    "numeric": {
      "cellCount": 5000
    },
    "multiNumeric": {
      "ratioInfectivity": [0.2, 0.5, 0.8]
    }
  }
}
```

### Python Example

```python
from microjson.model import MicroFeature, Properties

# Usage
example_properties = Properties(
    string={"name": "Sample Polygon", "description": "This is a sample rectangular polygon."},
    numeric={"cellCount": 5000},
    multiNumeric={"ratioInfectivity": [0.2, 0.5, 0.8]}
)

example_feature = MicroFeature(
    type="Feature",
    geometry={
        "type": "Polygon",
        "coordinates": [
            [
                [100.0, 0.0],
                [101.0, 0.0],
                [101.0, 1.0],
                [100.0, 1.0],
                [100.0, 0.0]
            ]
        ]
    },
    properties=example_properties
)
# print json
print(example_feature.model_dump_json(indent=2, exclude_unset=True))

```

---

In this example, a MicroJSON feature is defined with a rectangular polygon geometry, and the `Properties` class from the `microjson.model` module is employed to encapsulate string, numeric, and multiNumeric metadata associated with the feature. The JSON representation offers a clear formatting of the data, while the Python script showcases how to instantiate the `Properties` and `MicroFeature` classes to encapsulate the same data.
