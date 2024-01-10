# Working with MicroJSON and GeoJSON Files in Python

In this tutorial, we'll explore how to validate MicroJSON and GeoJSON files using the `microjson` package, which leverages Pydantic for data validation. Validation ensures that your JSON files adhere to the specified structure and constraints.

## Requirements

- Python 3.9 or higher
- `microjson` package

## Code Explanation

Before we dive into the code, let's understand what it aims to accomplish:

1. **Load JSON File**: Reads a JSON file into a Python object.
2. **Validate JSON Structure**: Utilizes Pydantic models to validate the structure of the JSON object.
3. **Print Result**: Prints the validated Pydantic object to the console.

Now let's look at the code itself.

```python
import microjson.model as mj
import json

# load the microjson file
with open('tests/json/microjson/valid/fullexample.json') as f:
    data = json.load(f, strict=True)

# validate the microjson file
microjsonobj = mj.MicroJSON.model_validate(data)
print("done validating: {}".format(microjsonobj))

# load the geojson file
with open('tests/json/geojson/valid/featurecollection/basic.json') as f:
    data = json.load(f, strict=True)

# validate the geojson file
geojsonobj = mj.GeoJSON.model_validate(data)

print("done validating: {}".format(geojsonobj))
```

### Step by Step Explanation

1. **Import Modules**: The script imports required modules from the `microjson` package and Python's built-in `json` library.

2. **Read and Validate MicroJSON**:
    - Opens a MicroJSON file in read mode.
    - Uses `json.load()` to parse the JSON content.
    - Calls `model_validate()` from the `microjson` package to validate the JSON against the MicroJSON Pydantic model.

3. **Read and Validate GeoJSON**:
    - Similar to the MicroJSON validation but validates against the GeoJSON Pydantic model.

4. **Output**: If the validation is successful, the script will print the validated objects.

By following this approach, you can validate the structure of any MicroJSON or GeoJSON file against their respective Pydantic models.
