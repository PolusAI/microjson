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
          "type": "Polygon",
          "coordinates": [[[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]]
        },
        "properties": {
            "well": "A1",
            "cellCount": 5,
            "ratioInfectivity": [0.1, 0.2, 0.3, 0.4, 0.5]
        }
      },
      {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates": [[[50.0, 0.0], [50.0, 50.0], [100.0, 50.0], [100.0, 0.0], [50.0, 0.0]]]
        },
        "properties": {
            "well": "A2",
            "cellCount": 10,
            "ratioInfectivity": [0.1, 0.2, 0.3, 0.4, 0.5]
        }
      }
    ],
    "valueRange": {
        "cellCount": {
            "min": 0,
            "max": 10
        },
        "ratioInfectivity": {
            "min": 0,
            "max": 1
        }
    },
    "descriptiveFields": ["well","imagename"],
    "multiscale": {
      "axes": [
          {
              "name": "x",
              "unit": "micrometer",
              "type": "space",
              "description": "x-axis"
          },
          {
              "name": "y",
              "unit": "micrometer",
              "type": "space",
              "description": "y-axis"
          }
      ],
      "transformationMatrix": [
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