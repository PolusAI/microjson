## OME NGFF and MicroJSON

OME NGFF provides a clear, efficient, and extensible format for storing and interacting with bioimaging data. Its ability to incorporate high-dimensional data and the existing rich ecosystem of tools and libraries that support Zarr (the underlying storage format for OME NGFF) make it a robust choice for imaging applications.

MicroJSON, as a minimal geometric data interchange format, offers a concise and streamlined way to represent and communicate geometric information. Its lightweight nature and the ability to precisely describe geometric shapes and positions make it an attractive choice to enrich the OME NGFF with geometric metadata.

## MicroJSON within OME NGFF: A Proposal

There are several ways to integrate MicroJSON within the OME NGFF data hierarchy. Here are a few potential placements:

-   **Multiscales Metadata - dataset level:** The `multiscales` metadata section describes various scales of the data. In this context, it's conceivable that MicroJSON could be used to add geometry metadata to specific scale levels. If the MicroJSON data directly relates to specific datasets (i.e., it describes geometric properties of the data within these datasets), then it might make sense to include this data as part of the metadata for each dataset. This could be achieved by adding a new key (e.g., "microjson") within each "datasets" dictionary. The value of this key would be the MicroJSON data relevant to that dataset.

    A possible solution could be to create a new key, "microjson", in each dataset dictionary. Each "microjson" entry could be a list of MicroJSON objects that apply to the corresponding dataset. For instance, if a MicroJSON object represents a spatial feature identified in the image data, that object could be linked to the corresponding image dataset.

    In this way, the MicroJSON data would be directly correlated to the relevant datasets, allowing users to directly connect the geometric data with the image data it describes. This seems to align well with the intent of the "multiscales" metadata to provide detailed, contextual information about how to interpret and understand the underlying image data. In examples where axes and units are the same for the MicroJSON data and the dataset, the MicroJSON "coordinatesystem" object could be omitted.

    Here is an example of how this could look:

```json
{
    "multiscales": [
        {
            "version": "0.5-dev",
            "name": "example",
            "axes": [ ... ],
            "datasets": [
                {
                    "path": "0",
                    "coordinateTransformations": [ ... ],
                    "microjson": [
                        {
                            "type": "Polygon",
                            "coordinates": [ ... ],
                            "coordinatesystem": {
                                "axes": ["x", "y"],
                                "units": ["micrometer", "micrometer"]
                            }
                        }
                        // More MicroJSON objects...
                    ]
                },
                // More datasets...
            ],
            "coordinateTransformations": [ ... ],
            "type": "gaussian",
            "metadata": { ... }
        }
    ]
}
```

In this example, each dataset has a "microjson" field, which is a list of MicroJSON objects that provide geometric context for that dataset. This approach allows users to directly relate the MicroJSON geometric data to the image data it describes, providing a rich, contextual interpretation of the data.

- **Multiscales meta data - top level**: If the MicroJSON data is globally relevant , then it could be included as a new key (e.g., "microjson") at the top level of the "multiscales" metadata.
    
```json
{
    "multiscales": [
        {
            "version": "0.5-dev",
            "name": "example",
            "axes": [ ... ],
            "datasets": [ ... ],
            "coordinateTransformations": [ ... ],
            "type": "gaussian",
            "metadata": { ... }
        }
    ],
    "microjson": [
        {
            "type": "Polygon",
            "coordinates": [ ... ],
            "coordinatesystem": {
                "axes": ["x", "y"],
                "units": ["micrometer", "micrometer"]
            }
        }
        // More MicroJSON objects...
    ]
}
```
    

- **Root metadata level:** The root metadata section describes the overall structure of the data. If the MicroJSON data is relevant to the entire dataset, then it could be included as a new key (e.g., "microjson") at the top level of the root metadata, that is, in the top folder of the OME NGFF data hierarchy. This would for example be suitable for a stitching vector, which would be a MicroJSON object in the root metadata, under a key `stitchingVectors`:

```json
{
    "stitchingVectors": [
        {
            "type": "FeatureCollection",
            "properties": {
                "type": "StitchingVector"
            },
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [...],
                        "subtype": "Rectangle"
                    },
                    "properties": {
                        "type": "Image",
                        "URI": "./123.zarr",
                    }
                },
                // More images...
            ]
        }
        // More stitching vectors...
    ],
    // Other metadata...
}

```