# MicroJSON Examples
## Basic MicroJSON
This JSON file demonstrates how MicroJSON can be used to define and describe different structures related to imaging, such as cells and their nuclei, including their spatial relationships, identifiers, labels, and color representations.

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    200.0,
                    150.0
                ]
            },
            "properties": {
                "name": "Reference Point",
                "description": "Specific point of interest",
                "color": "red",
                "property1": "value1"
            },
            "id": "1"
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        100.0,
                        100.0
                    ],
                    [
                        200.0,
                        200.0
                    ],
                    [
                        300.0,
                        100.0
                    ]
                ]
            },
            "properties": {
                "name": "Cell Path",
                "description": "Path traced within a cell",
                "color": "blue"
            },
            "id": "2",
            "ref": "s3://mybucket/myfile.tif"
        }
    ],
    "coordinatesystem": {
        "axes": [
            {
                "name": "x",
                "unit": "micrometer",
                "type": "cartesian",
                "pixelsPerUnit": 1,
                "description": "x-axis"
            },
            {
                "name": "y",
                "unit": "micrometer",
                "type": "cartesian",
                "pixelsPerUnit": 1,
                "description": "y-axis"
            }
        ],
        "transformation_matrix": [
            [
                1.0,
                0.0,
                0.0
            ],
            [
                0.0,
                1.0,
                0.0
            ],
            [
                0.0,
                0.0,
                0.0
            ]
        ]
    }
}

```

## Stitching Vector MicroJSON
This JSON file demonstrates how MicroJSON can be used to define and describe a stitching vector, which is used to describe the spatial relationship between multiple images that may be stitched together.
```json
{
    "type": "FeatureCollection",
    "coordinatesystem": {
      "axes": [
        {
          "name": "x"
        },
        {
          "name": "y"
        }
      ],
    },
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "subtype": "Rectangle",
          "coordinates": [[[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]]
        },
        "properties": {
          "type": "Image",
          "URI": "./image_1.tif"
        }
      },
      {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "subtype": "Rectangle",
          "coordinates": [[[50.0, 0.0], [50.0, 50.0], [100.0, 50.0], [100.0, 0.0], [50.0, 0.0]]]
        },
        "properties": {
          "type": "Image",
          "URI": "./image_2.tif"
        }
      }
    ],
    "properties": {
      "type": "StitchingVector"
    }
}
  
```