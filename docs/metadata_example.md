# Metadata Usage in MicroJSON Example

This guide demonstrates how to designate metadata in MicroJSON using the `properties` field in the `Feature` class. The `properties` field is used to store metadata related to a feature. This guide provides examples of how to populate these fields in both JSON and Python.

## Properties Class Overview

In MicroJSON, metadata related to a feature is stored in the `Properties` class. This class has 

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
example_properties = {
  "name": "Sample Polygon",
  "description": "This is a sample rectangular polygon.",
  "cellCount": 5000,
  "ratioInfectivity": [0.2, 0.5, 0.8]
}

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
