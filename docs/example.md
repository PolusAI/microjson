# Sample MicroJSON File
This JSON file demonstrates how MicroJSON can be used to define and describe complex structures related to microscopy, such as cells and their nuclei, including their spatial relationships, identifiers, labels, and color representations.

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
                ],
                "coordinatesystem": {
                    "axes": [
                        "x",
                        "y"
                    ],
                    "units": [
                        "micrometer",
                        "micrometer"
                    ],
                    "pixelsPerUnit": [
                        0.5,
                        0.5
                    ]
                }
            },
            "properties": {
                "name": "Reference Point",
                "description": "Specific point of interest",
                "color": "red"
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
                ],
                "coordinatesystem": {
                    "axes": [
                        "x",
                        "y"
                    ],
                    "units": [
                        "micrometer",
                        "micrometer"
                    ],
                    "pixelsPerUnit": [
                        0.5,
                        0.5
                    ]
                }
            },
            "properties": {
                "name": "Cell Path",
                "description": "Path traced within a cell",
                "color": "blue"
            },
            "id": "2"
        }
    ],
    "coordinatesystem": {
        "axes": [
            "x",
            "y"
        ],
        "units": [
            "micrometer",
            "micrometer"
        ],
        "pixelsPerUnit": [
            0.5,
            0.5
        ]
    }
}

```