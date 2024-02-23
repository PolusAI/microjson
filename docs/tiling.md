# Integration of TileJSON with MicroJSON
## Purpose
This specification outlines how to use TileJSON to integrate tiled MicroJSON data. It provides examples of how TileJSON can be used to specify the tiling scheme and zoom levels for MicroJSON data. It is based on the [TileJSON 3.0.0 specification](https://github.com/mapbox/tilejson-spec/blob/master/3.0.0/README.md), but extends it by recommending additional properties include the integration of MicroJSON data and fit purposes of microscopy data visualization. Recommendations made here are NOT part of the original TileJSON specification, but are made to fit the purposes of microscopy data visualization and integration with MicroJSON, although all recommendations are made to be compatible with the original TileJSON specification.

## Background of TileJSON

[TileJSON](https://github.com/mapbox/tilejson-spec/) is a widely-used format in mapping applications for specifying tilesets. Developed to streamline the integration of different map layers, TileJSON is essential for ensuring consistency across mapping platforms. It describes tilesets through a JSON object, detailing properties like tile URLs, zoom levels, and spatial coverage.


## TileJSON for MicroJSON Object Structure

- **`tilejson`:** Specifies the version of the TileJSON spec being used. Required for all TileJSON objects.
- **`name`:** The name of the tileset. Optional but recommended.
- **`description`:** Provide a brief description of the tileset. Optional but recommended.
- **`version`:** The version of the tileset. Optional but recommended.
- **`attribution`:** A link to the data source or other attribution information, e.g. organisational origin. Optional but recommended.
- **`tiles`:** Required. The URL pattern for accessing the vector tiles. The  `urlbase/{zlvl}/{t}/{c}/{z}/{x}/{y}` is the recommended default naming pattern for the tiles, in this order, where `urlbase` is the base URL (e.g. `http://example.com/tiles`), `{zlvl}` is the zoom level, `{t}` is the tileset timestamp, `{c}` is the channel, `{z}` is the z coordinate, and `{x}` and `{y}` are the x and y coordinates, respectively. 
- **`minzoom` and `maxzoom`:** Defines the range of zoom levels for which the tiles are available. 
- **`bounds`:** Optional. Specifies the geomoetrical bounds covered by the tileset. Specified as an array of four numbers in the order `[minX, minY, maxX, maxY]`.
- **`center`:** Optional. Indicates the center and suggested default view of the tileset.
- **`format`:** Required. The format of the tiles, for the purpose of this specification, we are currently using `json`, but are planning to extend this to binary vector format in the future.
- **`vector_layers`:**  Required. Describes each layer within the vector tiles, and has the following structure:

  - **`id`:** Required. A unique identifier for the layer. Required for each layer.
  - **`fields`:** Required. A list of fields (attributes) and their data types. For MicroJSON, this can either be an empty list, or any combination of `string`, `numerical`, and `multi-numeric`, attributes with their sub-attributes, as described in the MicroJSON specification. Required for each layer.
  - **`description`:** Optional. A brief description of the layer.
  - **`minzoom` and `maxzoom`:** Optional. The range of zoom levels at which the layer is visible.
- **`fillzoom`:** Optional. An integer specifying the zoom level from which to generate overzoomed tiles.
- **`legend`:** Optional. Contains a legend to be displayed with the tileset.

The following fields of TileJSON may be used if the use case requires it, and are included here for completeness:

- **`scheme`:** The tiling scheme of the tileset.
- **`grids`:** The URL pattern for accessing grid data.
- **`data`:** Optional. The URL pattern for accessing data. Used for GeoJSON originally, which in this specification is replaced by MicroJSON and used in the `tiles` field.
- **`template`:** Optional. Contains a mustache template to be used to format data from grids for interaction.

## Pydantic Model for TileJSON for MicroJSON
### TileJSON
::: microjson.tile.TileJSON
### TileModel
::: microjson.tile.TileModel
### TileLayer
::: microjson.tile.TileLayer

## TileJSON for MicroJSON example with Vector Layers
The below example shows a TileJSON object for a MicroJSON tileset with multiple layers of detail. The tileset has a single vector layer, `image_layer` id of `vector_layers`, which contains a single vector layer describing images. The `fields` property of the this layer specifies the attributes of the layer, including the data types of the attributes. The `tiles` property specifies the URL pattern for accessing the vector tiles, which in this case is a 2D data set (no channels, time or z-axis) with zoom level. The `fillzoom` property specifies the zoom level from which to generate overzoomed tiles, which in this case starts at level 3, after the last specified layer.

This file is located in the `examples/tiles` directory of the repository, and is named `tiled_example.json`. It has a corresponding MicroJSON file for each tile, located in the `examples/tiles/tiled_example` directory of the repository. The MicroJSON files are organized according to the tiling scheme, with the directory structure `zlvl/x/y.json` where `zlvl` is the zoom level, `x` is the x coordinate, and `y` is the y coordinate. The MicroJSON files contain the MicroJSON objects for the corresponding tiles, and are named according to the tiling scheme. For example, the MicroJSON object for the tile at zoom level 1, tile at (0,1) in the tiling scheme is located at `examples/tiles/tiled_example/1/0/1.json`. Examples for MicroJSON objects at zoom levels 0, 1, and 2 are provided below.

```json
{
    "tilejson": "3.0.0",
    "name": "2D Data Example",
    "description": "A tileset showing 2D data with multiple layers of detail.",
    "version": "1.0.0",
    "attribution": "<a href='http://example.com'>Example</a>",
    "tiles": [
        "http://example.com/tiles/{zlvl}/{x}/{y}.json"
    ],
    "minzoom": 0,
    "maxzoom": 10,
    "bounds": [0, 0, 24000, 24000],
    "center": [12000, 12000, 10],
    "format": "json",
    "vector_layers": [
        {
            "id": "image_layer",
            "description": "Image layer",
            "minzoom": 0,
            "maxzoom": 10,
            "fields": {
                "string": {
                    "Plate": "Plate ID",
                    "Image": "Image URI"
                },
                "numerical": {
                    "X": "X coordinate",
                    "Y": "Y coordinate",
                    "Channel": "Channel ID"
                }
            }
        }
    ],
    "fillzoom": 3
}
```

## Tiled MicroJSON Example
### Level 0
The following is an example of a MicroJSON object at zoom level 0, tile at (0,0) in the tiling scheme. Example URL: `http://example.com/tiles/0/0/0.json`
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              0,
              0
            ],
            [
              20000,
              0
            ],
            [
              20000,
              20000
            ],
            [
              0,
              20000
            ],
            [
              0,
              0
            ]
          ]
        ]
      },
      "properties": {
        "numeric": {
          "Label": 15.0,
          "Encoding_length": 3690.0
        }
      }
    }
  ],
  "coordinatesystem": {
    "axes": [
      {
        "name": "x",
        "type": "cartesian",
        "unit": "micrometer",
        "description": "x-axis"
      },
      {
        "name": "y",
        "type": "cartesian",
        "unit": "micrometer",
        "description": "y-axis"
      }
    ]
  },
  "value_range": {
    "Label": {
      "min": 1.0,
      "max": 35.0
    },
    "Encoding_length": {
      "min": 3690.0,
      "max": 3690.0
    }
  },
  "properties": {
    "string": {
      "Plate": "label",
      "Image": "x00_y01_p01_c1.ome.tif"
    },
    "numeric": {
      "Y": 1080.0,
      "X": 1080.0,
      "Channel": 1.0
    }
  }
}
```

### Level 1 
The following is an example of a MicroJSON object at zoom level 1, tile at (0,1) in the tiling scheme. Example URL: `http://example.com/tiles/1/0/1.json`
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              0,
              10000
            ],
            [
              10000,
              10000
            ],
            [
              10000,
              20000
            ],
            [
              0,
              20000
            ],
            [
              0,
              10000
            ]
          ]
        ]
      },
      "properties": {
        "numeric": {
          "Label": 10.0,
          "Encoding_length": 3690.0
        }
      }
    }
  ],
  "coordinatesystem": {
    "axes": [
      {
        "name": "x",
        "type": "cartesian",
        "unit": "micrometer",
        "description": "x-axis"
      },
      {
        "name": "y",
        "type": "cartesian",
        "unit": "micrometer",
        "description": "y-axis"
      }
    ]
  },
  "value_range": {
    "Label": {
      "min": 1.0,
      "max": 35.0
    },
    "Encoding_length": {
      "min": 3690.0,
      "max": 3690.0
    }
  },
  "properties": {
    "string": {
      "Plate": "label",
      "Image": "x00_y01_p01_c1.ome.tif"
    },
    "numeric": {
      "Y": 1080.0,
      "X": 1080.0,
      "Channel": 1.0
    }
  }
}
```

### Level 2
The following is an example of a MicroJSON object at zoom level 2, tile at (1,1) in the tiling scheme. Example URL: `http://example.com/tiles/2/1/3.json`
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              15000,
              15000
            ],
            [
              20000,
              15000
            ],
            [
              20000,
              20000
            ],
            [
              15000,
              20000
            ],
            [
              15000,
              15000
            ]
          ]
        ]
      },
      "properties": {
        "numeric": {
          "Label": 32.0,
          "Encoding_length": 3690.0
        }
      }
    }
  ],
  "coordinatesystem": {
    "axes": [
      {
        "name": "x",
        "type": "cartesian",
        "unit": "micrometer",
        "description": "x-axis"
      },
      {
        "name": "y",
        "type": "cartesian",
        "unit": "micrometer",
        "description": "y-axis"
      }
    ]
  },
  "value_range": {
    "Label": {
      "min": 1.0,
      "max": 35.0
    },
    "Encoding_length": {
      "min": 3690.0,
      "max": 3690.0
    }
  },
  "properties": {
    "string": {
      "Plate": "label",
      "Image": "x00_y01_p01_c1.ome.tif"
    },
    "numeric": {
      "Y": 1080.0,
      "X": 1080.0,
      "Channel": 1.0
    }
  }
}
```
