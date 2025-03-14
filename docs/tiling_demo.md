# MicroJSON Tiling Demo

This notebook demonstrates how to use the MicroJSON tiling functionality to create vector tiles from MicroJSON data. Vector tiles are a way to efficiently store and serve geospatial data for web mapping applications.

## Overview

In this demo, we will:
1. Generate sample polygon data (or use existing MicroJSON data)
2. Create a TileJSON specification
3. Generate vector tiles from the MicroJSON data
4. Save the tiles and metadata for use in web mapping applications

## Import Required Libraries

First, let's import the necessary libraries for tiling MicroJSON data.


```python
from microjson.tilewriter import (
    TileWriter,
    getbounds,
    extract_fields_ranges_enums
)
from pathlib import Path
from microjson.tilemodel import TileJSON, TileModel, TileLayer
import os
from microjson.polygen import generate_polygons
import json
```

## Option 1: Generate Sample Polygon Data

If you don't have existing MicroJSON data, we can generate sample polygon data using the `generate_polygons` function.


```python
# Parameters for generating polygons
GRID_SIZE = 10000  # Size of the grid
CELL_SIZE = 100    # Size of each cell in the grid
MIN_VERTICES = 10  # Minimum number of vertices per polygon
MAX_VERTICES = 100 # Maximum number of vertices per polygon

# Metadata types and options
meta_types = {
    "num_vertices": "int",
}
meta_values_options = {
    "polytype": ["Type1", "Type2", "Type3", "Type4"]
}

# Output file path
microjson_data_path = "example_generated.json"

# Generate polygons
generate_polygons(
    GRID_SIZE,
    CELL_SIZE,
    MIN_VERTICES,
    MAX_VERTICES,
    meta_types,
    meta_values_options,
    microjson_data_path
)

print(f"Generated polygon data saved to {microjson_data_path}")
```

    Generated polygon data saved to example_generated.json


## Option 2: Use Existing MicroJSON Data

Alternatively, you can use existing MicroJSON data. Uncomment and modify the following cell to use your own data.


```python
# microjson_data_path = "path/to/your/data.json"
# print(f"Using existing MicroJSON data from {microjson_data_path}")
```

## Visualize the MicroJSON Data

Let's take a look at the structure of our MicroJSON data.


```python
# Load and display the first few features of the MicroJSON data
with open(microjson_data_path, 'r') as f:
    data = json.load(f)

# Display basic information about the data
print(f"Number of features: {len(data.get('features', []))}")

# Display the first feature (truncated for readability)
if 'features' in data and len(data['features']) > 0:
    first_feature = data['features'][0]
    print("\nSample feature:")
    print(json.dumps(first_feature, indent=2)[:500] + "...")
```

    Number of features: 10000
    
    Sample feature:
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              62.7619624272948,
              9.7445327252005
            ],
            [
              66.55786998050925,
              10.453250162004622
            ],
            [
              86.82803641255592,
              51.64994084555056
            ],
            [
              77.93853896392383,
              68.85236038607228
            ],
            [
              67.57602296868663,
              78.79357410969412
            ],
            [
              4...


## Extract Fields, Ranges, and Enums

For existing MicroJSON data, we can extract field information, value ranges, and enumeration values.


```python
# Extract fields, ranges, and enums from the MicroJSON data
field_names, field_ranges, field_enums = extract_fields_ranges_enums(microjson_data_path)

print("Extracted field names:")
print(field_names)

print("\nExtracted field ranges:")
print(field_ranges)

print("\nExtracted field enums:")
print(field_enums)
```

    Extracted field names:
    {'num_vertices': 'Number', 'polytype': 'String'}
    
    Extracted field ranges:
    {'num_vertices': [10, 24]}
    
    Extracted field enums:
    {'polytype': {'Type3', 'Type2', 'Type1', 'Type4'}}


## Define Vector Layers

Now, let's define the vector layers for our tiles. We'll use the extracted field information.


```python
# Create a TileLayer using the extracted fields
vector_layers = [
    TileLayer(
        id="polygon-layer",
        fields=field_names,
        minzoom=0,
        maxzoom=10,
        description="Layer containing polygon data",
        fieldranges=field_ranges,
        fieldenums=field_enums,
    )
]

print("Vector layer defined with the following properties:")
print(f"ID: {vector_layers[0].id}")
print(f"Fields: {vector_layers[0].fields}")
print(f"Zoom range: {vector_layers[0].minzoom} - {vector_layers[0].maxzoom}")
```

    Vector layer defined with the following properties:
    ID: polygon-layer
    Fields: {'num_vertices': 'Number', 'polytype': 'String'}
    Zoom range: 0 - 10


## Get Bounds and Center

Next, we'll calculate the bounds of our data to properly configure the tile model.


```python
# Get bounds of the data (square=True ensures the bounds form a square)
maxbounds = getbounds(microjson_data_path, square=True)
print(f"Bounds: {maxbounds}")

# Calculate the center of the bounds
center = [0, (maxbounds[0] + maxbounds[2]) / 2, (maxbounds[1] + maxbounds[3]) / 2]
print(f"Center: {center}")
```

    Bounds: [5.352408515784582, 5.049442955279417, 9995.190828709661, 9994.887863149157]
    Center: [0, 5000.271618612723, 4999.9686530522185]


## Create the Tile Model

Now, let's create the TileModel that will define our tile set.


```python
# Create output directory for tiles
os.makedirs("tiles", exist_ok=True)

# Instantiate TileModel with our settings
tile_model = TileModel(
    tilejson="3.0.0",
    tiles=[Path("tiles/{z}/{x}/{y}.pbf")],  # Local path or URL
    name="Example Tile Layer",
    description="A TileJSON example incorporating MicroJSON data",
    version="1.0.0",
    attribution="Polus AI",
    minzoom=0,
    maxzoom=7,
    bounds=maxbounds,
    center=center,
    vector_layers=vector_layers
)

# Create the root model with our TileModel instance
tileobj = TileJSON(root=tile_model)

# Display the TileJSON specification
print("TileJSON specification:")
print(tileobj.model_dump_json(indent=2))
```

    TileJSON specification:
    {
      "tilejson": "3.0.0",
      "tiles": [
        "tiles/{z}/{x}/{y}.pbf"
      ],
      "name": "Example Tile Layer",
      "description": "A TileJSON example incorporating MicroJSON data",
      "version": "1.0.0",
      "attribution": "Polus AI",
      "template": null,
      "legend": null,
      "scheme": null,
      "grids": null,
      "data": null,
      "minzoom": 0,
      "maxzoom": 7,
      "bounds": [
        5.352408515784582,
        5.049442955279417,
        9995.190828709661,
        9994.887863149157
      ],
      "center": [
        0.0,
        5000.271618612723,
        4999.9686530522185
      ],
      "fillzoom": null,
      "vector_layers": [
        {
          "id": "polygon-layer",
          "fields": {
            "num_vertices": "Number",
            "polytype": "String"
          },
          "minzoom": 0,
          "maxzoom": 10,
          "description": "Layer containing polygon data",
          "fieldranges": {
            "num_vertices": [
              10,
              24
            ]
          },
          "fieldenums": {
            "polytype": [
              "Type3",
              "Type2",
              "Type1",
              "Type4"
            ]
          },
          "fielddescriptions": null
        }
      ],
      "multiscale": null,
      "scale_factor": null
    }


## Export TileJSON Metadata

Let's export the TileJSON metadata to a file.


```python
# Export to tilejson
with open("tiles/metadata.json", "w") as f:
    f.write(tileobj.model_dump_json(indent=2))

print("TileJSON metadata exported to tiles/metadata.json")
```

    TileJSON metadata exported to tiles/metadata.json


## Generate Vector Tiles

Finally, let's generate the vector tiles from our MicroJSON data.


```python
# Initialize the TileWriter
handler = TileWriter(tile_model, pbf=True)

# Convert MicroJSON to tiles
handler.microjson2tiles(microjson_data_path, validate=False)

print("Vector tiles generated successfully!")

# List the generated tile directories to verify
tile_dirs = [d for d in os.listdir("tiles") if os.path.isdir(os.path.join("tiles", d))]
print(f"Generated tile zoom levels: {tile_dirs}")
```

    Vector tiles generated successfully!
    Generated tile zoom levels: ['7', '2', '0', 'tiled_example', '1', '5', '3', '4', '6']


## Conclusion

In this notebook, we've demonstrated how to:

1. Generate or use existing MicroJSON data
2. Extract field information from the data
3. Define vector layers for our tiles
4. Calculate bounds and center for our tile set
5. Create a TileJSON specification
6. Generate vector tiles from MicroJSON data

These vector tiles can now be used in web mapping applications like Mapbox GL JS, Leaflet, or OpenLayers to display the data interactively.
