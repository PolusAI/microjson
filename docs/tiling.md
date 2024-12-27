# Integration of TileJSON with MicroJSON

## Purpose

This specification outlines how to use TileJSON to integrate tiled MicroJSON data, both in json form as well as binary form. It provides examples of how TileJSON can be used to specify the tiling scheme and zoom levels for MicroJSON data and its binary equievalent. It is based on the [TileJSON 3.0.0 specification](https://github.com/mapbox/tilejson-spec/blob/master/3.0.0/README.md), but extends it by recommending additional properties to enable integration of MicroJSON data and fit purposes of microscopy imaging. The recommendations provided here are not intrinsic to the original TileJSON specification but have been tailored to suit the needs of microscopy metadata annotation and integration with MicroJSON. However, all suggestions are designed to maintain compatibility with the original TileJSON specification.

## Background of TileJSON

[TileJSON](https://github.com/mapbox/tilejson-spec/) is a widely-used format in mapping applications for specifying tilesets. Developed to streamline the integration of different map layers, TileJSON is essential for ensuring consistency across mapping platforms. It describes tilesets through a JSON object, detailing properties like tile URLs, zoom levels, and spatial coverage.

## TileJSON for MicroJSON Object Structure

- **`tilejson`:** Specifies the version of the TileJSON spec being used. Required for all TileJSON objects.
- **`name`:** The name of the tileset. Optional but recommended.
- **`description`:** Provide a brief description of the tileset. Optional but recommended.
- **`version`:** The version of the tileset. Optional but recommended.
- **`attribution`:** A link to the data source or other attribution information, e.g. organisational origin. Optional but recommended.
- **`tiles`:** Required. The URL pattern for accessing the vector tiles. The  `urlbase/{zlvl}/{t}/{c}/{z}/{x}/{y}` is the recommended default naming pattern for the tiles, in this order, where `urlbase` is the base URL (e.g. `http://example.com/tiles`), `{zlvl}` is the zoom level, `{t}` is the tileset timestamp, `{c}` is the channel, `{z}` is the z coordinate, and `{x}` and `{y}` are the x and y coordinates, respectively. If not using a timestamp, channel, or z coordinate, these can be omitted. The zoom level should always be first.
- **`minzoom` and `maxzoom`:** Defines the range of zoom levels for which the tiles are available.
- **`bounds`:** Optional. Specifies the geometrical bounds included in the tileset. Specified as an array of minimum four numbers in the order `[minX, minY, maxX, maxY]`, but may include up to a further six numbers for a total of ten, `[minT, minC, minZ, minX, minY, maxT, maxC, maxZ, maxX, maxY]`, where `minT` is the minimum tileset timestamp, `minC` is the minimum channel, `minZ` is the minimum z coordinate, `minX` and `minY` are the minimum x and y coordinates, `maxT` is the maximum tileset timestamp, `maxC` is the maximum channel, `maxZ` is the maximum z coordinate, and `maxX` and `maxY` are the maximum x and y coordinates.
- **`center`:** Optional. Indicates the center and suggested default view of the tileset. Minimum of three numbers in the order `[x, y, zoom]`, but may include up to a further three numbers for a total of six, `[t,c,z,x,y,zoom]`, where `t` is the tileset timestamp, `c` is the channel, `z` is the z coordinate, `x` and `y` are the x and y coordinates, and `zoom` is the zoom level. Zoom level should be last.
- **`vector_layers`:**  Required. Describes each layer within the vector tiles, and has the following structure:

  - **`id`:** Required. A unique identifier for the layer. Required for each layer.
  - **`fields`:** Required. A list of fields (attributes) and their data types. For MicroJSON, this can either be an empty list, or a simple datatype indicator, that is either of `String`, `Number`, or `Bool`. Complex data types, such as arrays or objects are not allowed.  Required for each layer.
  - **`fieldranges`:** Optional. A dictionary of field names and their ranges. For example, `{"label": [0,100], "channel": [0,10]}`. Optional.
  - **`fieldenums`:** Optional. A dictionary of field names and their possible values. For example, `{"plate": ["A1", "A2", "B1", "B2"], "image": ["image1.tif", "image2.tif", "image3.tif"]}`. Optional.
  - **`fielddescriptions`:** Optional. A dictionary of field names and their descriptions. For example, `{"plate": "Well plate identifier", "image": "Image filename", "label": "Label identifier", "channel": "Channel identifier"}`. Optional.
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

::: microjson.tilemodel.TileJSON

### TileModel

::: microjson.tilemodel.TileModel

### TileLayer

::: microjson.tilemodel.TileLayer

## General tiling requirements

This specification is designed to be compatible with the [Vector Tile Specification](https://github.com/mapbox/vector-tile-spec/blob/master/2.1/README.md) and the [TileJSON 3.0.0 specification](https://github.com/mapbox/tilejson-spec/blob/master/3.0.0/README.md). The Vector Tile Specification specifically requires vector tiles to be agnostic of the global coordinate system, and thus followingly each tile has a relative coordinate system, which instead is defined in the TileJSON. Our ambitions in general are to follow the same principles.

One difference is that we here recommend that the file ending for binary tiles is `.pbf` instead of `.mvt` to avoid confusion with the Mapbox Vector Tile format. The binary tiles should be encoded in the [Protobuf format](https://developers.google.com/protocol-buffers) as defined in the Vector Tile Specification.

## MicroJSON2vt

The MicroJSON2vt module is a helper module that can be used to convert MicroJSON objects to vector tiles. It is designed to be used in conjunction with the TileJSON for MicroJSON specification, and can be used to generate vector tiles from MicroJSON objects. The module is designed to be compatible with the Vector Tile Specification, and can be used to generate vector tiles in the intermediate vector tile JSON-format, which then, using `vt2pbf` may be transformed into protobuf. The module is included in the `microjson` package, and its wrapper function can be imported using the following code:

```python
from microjson import microjson2vt
```

The module:
::: microjson.microjson2vt.microjson2vt.MicroJsonVt
    :docstring:

## Tilewriter module

The Tilewriter module is a helper module that can be used to generate binary tiles from a large MicroJSON file, my utilizing both microjson2vt and vt2pbf.
::: microjson.tilewriter
    :docstring:

## TileJSON for MicroJSON example with Vector Layers

The below example illustrates a TileJSON for a MicroJSON tileset multiple layers of detail. The tileset has a single vector layer, `image_layer` id of `vector_layers`, which contains a single vector layer describing images. The `fields` property of the this layer specifies the attributes of the layer, including the data types of the attributes. The `tiles` property specifies the URL pattern for accessing the vector tiles, which in this case is a 2D data set (no channels, time or z-axis) with zoom level.

This file is located in the `examples/tiles` directory of the repository, and is named `tiled_example.json`. It has a corresponding MicroJSON file for each tile, located in the `examples/tiles/tiled_example` directory of the repository. The MicroJSON files are organized according to the tiling scheme, with the directory structure `zlvl/x/y.json` where `zlvl` is the zoom level, `x` is the x coordinate, and `y` is the y coordinate. The MicroJSON files contain the MicroJSON objects for the corresponding tiles, and are named according to the tiling scheme. For example, the MicroJSON object for the tile at zoom level 1, tile at (0,1) in the tiling scheme is located at `examples/tiles/tiled_example/1/0/1.json`. Examples for MicroJSON objects at zoom levels 0, 1, and 2 are provided below.

```json
{
    {
    "tilejson": "3.0.0",
    "name": "2D Data Example",
    "description": "A tileset showing 2D data with multiple layers of detail.",
    "version": "1.0.0",
    "attribution": "<a href='http://example.com'>Example</a>",
    "tiles": [
        "http://example.com/tiled_example/{zlvl}/{x}/{y}.json"
    ],
    "minzoom": 0,
    "maxzoom": 10,
    "bounds": [0, 0, 24000, 24000],
    "center": [12000, 12000, 0],
    "vector_layers": [
        {
            "id": "Tile_layer",
            "description": "Tile layer",
            "minzoom": 0,
            "maxzoom": 10,
            "fields": {
              "plate": "String",
              "image": "String",
              "label": "Number",
              "channel": "Number"
            }
        }
    ],
    "fillzoom": 3
}
```

## Tiled binary TileJSON

In addition to json format, tiles may be encoded in a binary protobuf format. Below follows a similar example to the one above, but with binary tiles. The `tiles` property specifies the URL pattern for accessing the binary tiles, which in this case is a 2D data set (no channels, time or z-axis) with zoom level. The `fillzoom` property specifies the zoom level from which to generate overzoomed tiles, which in this case starts at level 3, after the last specified layer.

```json
{
    "tilejson": "3.0.0",
    "name": "2D Data Example",
    "description": "A tileset showing 2D data with multiple layers of detail.",
    "version": "1.0.0",
    "attribution": "<a href='http://example.com'>Example</a>",
    "tiles": [
        "http://example.com/tiled_example/{zlvl}/{x}/{y}.pbf"
    ],
    "minzoom": 0,
    "maxzoom": 10,
    "bounds": [0, 0, 24000, 24000],
    "center": [12000, 12000, 0],
    "vector_layers": [
        {
            "id": "tile_layer",
            "description": "Tile layer",
            "minzoom": 0,
            "maxzoom": 10,
            "fields": {
              "plate": "String",
              "image": "String",
              "label": "Number",
              "channel": "Number",
            },
            "fieldranges": {
              "label": [0,100],
              "channel": [0,10]
            },
            "fieldenums": {
              "plate": ["A1", "A2", "B1", "B2"],
              "image": ["image1.tif", "image2.tif", "image3.tif"],
            }
            "fielddescriptions": {
              "plate": "Well plate identifier",
              "image": "Image filename",
              "label": "Label identifier",
              "channel": "Channel identifier"
            }
        }
    ],
    "fillzoom": 3
}
```

## Tiled binary example

The examples folder contains an example of how to generate binary tiles from one large MicroJSON file. It uses a helper module that generates a large random polygon grid, as could be expected in an imaging setting, using typical imaging coordinates. It is also included below for reference.

### Example of creating binary tiles from a large MicroJSON file

::: microjson.examples.tiling.main
    :docstring:

## Tiled MicroJSON Example

### Level 0

The following is an example of a MicroJSON object at zoom level 0, tile at (0,0) in the tiling scheme. Example URL: `http://example.com/tiles/0/0/0.json`

```json
{
    "tilejson": "3.0.0",
    "name": "2D Data Example",
    "description": "A tileset showing 2D data with multiple layers of detail.",
    "version": "1.0.0",
    "attribution": "<a href='http://example.com'>Example</a>",
    "tiles": [
        "http://example.com/tiled_example/{zlvl}/{x}/{y}.json"
    ],
    "minzoom": 0,
    "maxzoom": 10,
    "bounds": [0, 0, 24000, 24000],
    "center": [12000, 12000, 0],
    "format": "json",
    "vector_layers": [
        {
            "id": "image_layer",
            "description": "Image layer",
            "minzoom": 0,
            "maxzoom": 10,
            "fields": {
              "plate": "String",
              "image": "String",
              "label": "Number",
              "channel": "Number"
            }
        }
    ],
    "fillzoom": 3
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
        "label": 3
      }
    }
  ],
  "multiscale": {
    "axes": [
      {
        "name": "x",
        "type": "space",
        "unit": "micrometer",
        "description": "x-axis"
      },
      {
        "name": "y",
        "type": "space",
        "unit": "micrometer",
        "description": "y-axis"
      }
    ]
  },
  "properties": {
    "plate": "label",
    "image": "x00_y01_p01_c1.ome.tif",
    "channel": 1.0
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
              5000,
              15000
            ],
            [
              10000,
              15000
            ],
            [
              10000,
              20000
            ],
            [
              5000,
              20000
            ],
            [
              5000,
              15000
            ]
          ]
        ]
      },
      "properties": {
        "label": 13
      }
    }
  ],
  "multiscale": {
    "axes": [
      {
        "name": "x",
        "type": "space",
        "unit": "micrometer",
        "description": "x-axis"
      },
      {
        "name": "y",
        "type": "space",
        "unit": "micrometer",
        "description": "y-axis"
      }
    ]
  },
  "properties": {
    "plate": "label",
    "image": "x00_y01_p01_c1.ome.tif",
    "channel": 1.0
  }
}
```
