# Sample MicroJSON File
This JSON file demonstrates how MicroJSON can be used to define and describe complex structures related to microscopy, such as cells and their nuclei, including their spatial relationships, identifiers, labels, and color representations.

```json
{
  "coordinatesystem": {
    "axes": [
      "x",
      "y",
      "z"
    ],
    "units": [
      "micrometer",
      "micrometer",
      "micrometer"
    ],
    "pixelsPerUnit": [
      0.5,
      0.5,
      2
    ],    
  },
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "id": "cell-1",
        "type": "cell",
        "label": "Cell A",
        "color": "red"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [10, 10],
            [10, 50],
            [50, 50],
            [50, 10],
            [10, 10]
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "id": "cell-2",
        "type": "cell",
        "label": "Cell B",
        "color": "blue"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [60, 60],
            [60, 100],
            [100, 100],
            [100, 60],
            [60, 60]
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "id": "nucleus-1",
        "type": "nucleus",
        "label": "Nucleus A",
        "parentCell": "cell-1"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [30, 30]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "id": "nucleus-2",
        "type": "nucleus",
        "label": "Nucleus B",
        "parentCell": "cell-2"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [80, 80]
      }
    }
  ]
}
```