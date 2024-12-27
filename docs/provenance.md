# Provenance and Traceability in MicroJSON

## Background

For geospatial data, particularly with GeoJSON, there are no standardized methods for tracing data provenance. While GeoJSON offers a robust format for geographical features representation, it lacks mechanisms for tracking the workflows and processes that generate or modify these features. This document outlines an addition to MicroJSON, integrating a provenance model to bridge this gap.

## Design Motivations

The design introduces a traceability model that integrates seamlessly with MicroJSON, enhancing GeoJSON capabilities while maintaining full backward compatibility. Key motivations include:

- **Supporting Workflow Integration:** Linking MicroJSON objects to specific analytical workflows, thereby enabling reproducibility and transparency.
- **Enabling Flexible Provenance Tracking:** Providing detailed information about workflow steps, including input and output parameters, that led to the creation or modification of MicroJSON objects.
- **Facilitating Workflow and Artifact Linking:** Allowing references to specific workflows and artifacts, providing a comprehensive view of data processing and provenance tracking.
- **Adapting to Varied Use Cases:** Accommodating both structured and ad-hoc processes.

## Model Structure

The provenance model structure comprises `WorkflowCollection`, `Workflow`, `Artifact`, `ArtifactCollection`, `WorkflowProvenance`, and `MicroJSONLink` objects:

- **Workflow Collection Object:** Includes multiple workflows, acknowledging that a single MicroJSON object might result from various processes.
- **Workflow Object:** Captures essential workflow details, including identifiers and descriptive metadata. This metadata links MicroJSON objects to their respective workflows.
- **Artifact and Artifact Collection Objects:** Represent single files or directories and collections of these, respectively, providing a link between the physical data and the workflows.
- **Workflow Provenance Object:** Details specific instances of workflow runs, including run identifiers, duration, operator, and the input/output parameters.
Of these, Workflow, WorkflowCollection, Artifact, and ArtifactCollection can funtion as the top object in the provenance part of a MicroJSON file.
- **MicroJSON Link Object:** Provides a link to a specific MicroJSON object, specifying which parts of the object's properties are pertinent to the workflow run. While this object is required, and the id property is required, the specification of a field in the MicroJSON object is optional. If no field is specified, the entire MicroJSON object is considered to be pertinent to the workflow run or artifact.

## Data Provenance and MicroJSON Traceability Link

Under each workflow, the `WorkflowProvenance` object includes:

- **Properties** that describe the workflow run, in form of a dictionary, to enable flexible and scalable provenance tracking. Example of properties include run identifier, duration, operator, and input/output parameters.
- **Output Artifacts:** These artifacts are the result of the workflow run. These in turn has the `microjsonLinks` field, which is a list of MicroJSON objects that is pertinent to the workflow run:
  - **MicroJSON Traceability Links:** These links connect back to specific MicroJSON objects, specifying which parts of the object's properties are pertinent to the workflow run.

## Rationale for Structure

This structure is designed to:

- **Reflect Complex Data Relationships:** Multiple workflows can contribute to a single MicroJSON object.
- **Provide Comprehensive Traceability:** Offering a complete journey of the data from origin through processing steps.
- **Ensure Flexibility and Scalability:** Suitable for a wide range of scenarios and scalable in applications.
- **Capture Simple Provenance:** Allowing for simple provenance tracking, such as a single standalone workflow or even only an artifact or artifact collection.
This enhancement not only increases the utility of MicroJSON in various scientific and geospatial contexts but also fosters an environment of transparency and reproducibility.

## Examples MicroJSON Provenance and Traceability

***Example 1: MicroJSON with single Artifact only***

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "1",
            "geometry": {
                "type": "Polygon",
                "subtype": "Rectangle",
                "coordinates": [
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [
                            0.0,
                            50.0
                        ],
                        [
                            50.0,
                            50.0
                        ],
                        [
                            50.0,
                            0.0
                        ],
                        [
                            0.0,
                            0.0
                        ]
                    ]
                ]
            },
            "properties": {
                "string": {
                    "well": "A1"
                },
                "numeric": {
                    "cellCount": 5
                },
                "multiNumeric": {
                    "ratioInfectivity": [
                        [
                            0.1,
                            0.2,
                            0.3,
                            0.4,
                            0.5
                        ],
                        [
                            0.2,
                            0.3,
                            0.4,
                            0.5,
                            0.6
                        ]
                    ]
                }
            }
        },
        {
            "type": "Feature",
            "id": "2",
            "geometry": {
                "type": "Polygon",
                "subtype": "Rectangle",
                "coordinates": [
                    [
                        [
                            50.0,
                            0.0
                        ],
                        [
                            50.0,
                            50.0
                        ],
                        [
                            100.0,
                            50.0
                        ],
                        [
                            100.0,
                            0.0
                        ],
                        [
                            50.0,
                            0.0
                        ]
                    ]
                ]
            },
            "properties": {
                "string": {
                    "well": "A2"
                },
                "numeric": {
                    "cellCount": 10
                },
                "multiNumeric": {
                    "ratioInfectivity": [
                        [
                            0.1,
                            0.2,
                            0.3,
                            0.4,
                            0.5
                        ],
                        [
                            0.2,
                            0.3,
                            0.4,
                            0.5,
                            0.6
                        ]
                    ]
                }
            }
        }
    ],
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
    },
    "provenance": {
        "type": "Artifact",
        "id": "artifact_1",
        "uri": "file://path/to/image.tif",
        "properties": {
            "imageType": "TIFF",
            "analysisType": "Cell counting"
        },
        "microjsonLinks": [
            {
                "microjsonTd": "1",
                "microjsonField": "string.well"
            }
        ]
    }
}
```

***Example 2: MicroJSON with Workflow Collection***

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "1",
            "geometry": {
                "type": "Polygon",
                "subtype": "Rectangle",
                "coordinates": [
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [
                            0.0,
                            50.0
                        ],
                        [
                            50.0,
                            50.0
                        ],
                        [
                            50.0,
                            0.0
                        ],
                        [
                            0.0,
                            0.0
                        ]
                    ]
                ]
            },
            "properties": {
                "string": {
                    "well": "A1"
                },
                "numeric": {
                    "cellCount": 5
                },
                "multiNumeric": {
                    "ratioInfectivity": [
                        [
                            0.1,
                            0.2,
                            0.3,
                            0.4,
                            0.5
                        ],
                        [
                            0.2,
                            0.3,
                            0.4,
                            0.5,
                            0.6
                        ]
                    ]
                }
            }
        },
        {
            "type": "Feature",
            "id": "2",
            "geometry": {
                "type": "Polygon",
                "subtype": "Rectangle",
                "coordinates": [
                    [
                        [
                            50.0,
                            0.0
                        ],
                        [
                            50.0,
                            50.0
                        ],
                        [
                            100.0,
                            50.0
                        ],
                        [
                            100.0,
                            0.0
                        ],
                        [
                            50.0,
                            0.0
                        ]
                    ]
                ]
            },
            "properties": {
                "string": {
                    "well": "A2"
                },
                "numeric": {
                    "cellCount": 10
                },
                "multiNumeric": {
                    "ratioInfectivity": [
                        [
                            0.1,
                            0.2,
                            0.3,
                            0.4,
                            0.5
                        ],
                        [
                            0.2,
                            0.3,
                            0.4,
                            0.5,
                            0.6
                        ]
                    ]
                }
            }
        }
    ],
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
    },
    "provenance": {
        "type": "WorkflowCollection",
        "workflows": [
            {
                "type": "Workflow",
                "id": "workflow_1",
                "properties": {
                    "description": "Image processing workflow"
                },
                "sub_workflows": [],
                "workflow_provenance": {
                    "type": "WorkflowProvenance",
                    "output_artifacts": {
                        "type": "Artifact",
                        "id": "artifact_1",
                        "uri": "file://path/to/image.tif",
                        "properties": {
                            "imageType": "TIFF",
                            "analysisType": "Cell counting"
                        },
                        "microjsonLinks": [
                            {
                                "microjsonId": "1",
                                "microjsonField": "string.well"
                            }
                        ]
                    }
                }
            }
        ]
    }
}
```
