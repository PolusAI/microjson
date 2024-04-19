# MicroJSON Specification

## Introduction

MicroJSON is a format, inspired by [GeoJSON](https://geojson.org), for encoding a variety of data structures related to microscopy images, including reference points, regions of interest, and other annotations. These data structures are represented using the widely adopted JSON format, making it easy to work with in various programming languages and applications. It is fully backwards compatible with the [GeoJSON Specification, RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946), since any GeoJSON also is accepted as a MicroJSON. As GeoJSON supports foreign top level properties, a MicroJSON is also a valid GeoJSON. This specification describes briefly the objects that exist in GeoJSON, and then in more detail describes the additional objects that are part of MicroJSON. For a more detailed description of the GeoJSON objects, please see the [GeoJSON Specification, RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946).

## Objects

### MicroJSON Object

A MicroJSON object is a JSON object that represents a geometry, feature, or collection of features, or more precisely, be either of type (having value of top level field `type` as) `"Geometry"`, `"Feature"`, or `"Featurecollection"`, that is, the same as for GeoJSON. What separates MicroJSON from GeoJSON is that it MAY have a member `"multiscale"` in a Feature or FeatureCollection object:  

- `"multiscale"`: (Optional) A multiscale object as defined in the section [Multiscale object](#multiscale-object). If this property is not present, the default coordinate system is assumed to be the same as the image coordinate system, using cartesian coordinates and pixels as units. It is recommended to define this property at the top level of the MicroJSON object, but it MAY also be defined at the level of a Feature or Geometry object, in which case it overrides the top level coordinate system.

A MicroJSON object MAY have a `"bbox"` property":

- `"bbox"`: (Optional) Bounding Box of the feature represented as an array of length 4 (2D) or length 6 (3D).


### Geometry Object

A geometry object is a JSON object where the `type` member's value is one of the following strings: `"Point"`, `"MultiPoint"`, `"LineString"`, `"MultiLineString"`, `"Polygon"`, `"Rectangle"`, `"MultiPolygon"`, or `"GeometryCollection"`.

Each geometry object MUST have a `"coordinates"` member with an array value. The structure of the coordinates array depends on the geometry type.

- **Point**: The coordinates array must contain two or three (if 3D) numbers representing the X and Y (and Z) coordinates of the point in the image. A “Point” Geometry MAY have a radius, if indicating a circular object, with the value in pixels, specified as a member `“radius”` of the Geometry object.

- **MultiPoint**: The coordinates array must be an array of point coordinates.

- **LineString**: The coordinates array must be an array of two or more point coordinates forming a continuous line. A “LineString” Geometry MAY have a radius, with the value in pixels, specified as a member “radius” of the Geometry object.

- **MultiLineString**: The coordinates array must be an array of LineString coordinate arrays.

- **Polygon**: The coordinates array must be an array of linear ring coordinate arrays, where the first linear ring represents the outer boundary and any additional rings represent holes within the polygon.

    - A subtype of “Polygon” is the “Rectangle” geometry: A polygon with an array of four 2D point coordinates representing the corners of the rectangle in a counterclockwise order. It has the property subtype with the value `“Rectangle”`.

- **MultiPolygon**: The coordinates array must be an array of Polygon coordinate arrays.

### GeometryCollection

A GeometryCollection is an array of geometries (Point, multipoint, LinesString, MultiLineString, Polygon, MultiPolygon). It is possible for this array to be empty.

### Feature Object

A feature object represents a spatially bounded entity associated with properties specific to that entity. A feature object is a JSON object with the following members, required unless otherwise noted:

- `"type"`: A string with the value `"Feature"`.
- `"geometry"`: A geometry object as defined in the section above or a JSON null value.
- `"properties"`: (Optional) A JSON object containing properties and metadata specific to the feature, or a JSON null value. It MAY have the following sub-properties:
    - `"string"`: (Optional) A list with key-value pairs, with string keys and string values, e.g. `{"color": "red", "size": "large"}`.
    - `"numeric"`: (Optional) A list with key-value pairs, with string keys and numerical values, e.g. `{"area": 123.45, "volume": 678.90}`.
    - `"multiNumeric"`: (Optional) A list with key-value pairs, with string keys and list of numerical values, e.g. `{"area": [123.45, 234.56], "volume": [678.90, 789.01]}`.
- `"id"`: (Optional) A unique identifier for this feature.
- `"ref"`: (Optional) A reference to an external resource, e.g. URI to a zarr strcture, e.g. "s3://zarr-demo/store/my_array.zarr".


#### Special Feature Objects

- **Image**: An image MUST have the following key-value pairs in its “properties” object:

    - `"type"`: A string with the value “Image”

    - `"URI"`: A string with the image URI, e.g. “./image_1.tif"

    An Image MUST also have a geometry object (as its “geometry” member) of type "Polygon", subtype “Rectangle”, indicating the shape of the image. An Image MAY have the following additional key-value pairs in its “properties” object:
    - `"correction"`: A list of coordinates indicating the relative correction of the image, e.g. `[1, 2]` indicating a correction of 1 units in the x direction and 2 units in the y direction, with units as defined by the coordinate system. If the coordinate system is not defined, the units are pixels.

### FeatureCollection Object

A FeatureCollection object is a JSON object representing a collection of feature objects. A FeatureCollection object has a member with the name `"features"`. The value of `"features"` is a JSON array. Each element of the array is a Feature object as defined above. It is possible for this array to be empty. Additionally, it MAY have the following members:
- `"stringFields"`: (Optional) A list of strings, indicating the descriptive fields of the features in the collection, e.g. `["color", "size"]`.
- `"valueRange"`: (Optional) A list of key-value pairs, with string keys and as keys another object with the fields:
    * `"min"`: The minimum value of the field in the key (both `"numeric"` and `"multiNumeric"`) of the features in the collection, e.g. `{"area": 123.45, "volume": 678.90}`.
    * `"max"`: The maximum value as above.
- `"properties"`: (Optional) A JSON object containing properties and metadata specific to the feature collection, and which apply to all features of the collection, or a JSON null value. It has the same structure as the `"properties"` member of a Feature object.

#### Special FeatureCollection Objects

- **StitchingVector**: Represents a stitching vector, and MUST have the following key-value pairs in its “properties” object:

    - `"type"`: A string with the value “StitchingVector”

    Any object of a StitchingVector “features” array MUST be an “Image” special type of features object.

### Multiscale Object

A multiscale object represents the choice of axes (2-5D) and potentially their transformations that should be applied to the numerical data in order to arrive to the actual size of the object described. It MUST have the following properties:

- `"axes"`: Representing the choice of axes as an Axis object.

It MAY contain either of, but NOT both of the following properties:
- `"coordinateTransformations"`: Representing the set of coordinate transformations that should be applied to the numerical data in order to arrive to the actual size of the object described. It MUST be an array of objects, each object representing a coordinate transformation. Each object MUST have properties as follows:
    - `"type"`: Representing the type of the coordinate transformation. Currently supported types are `"identity"`, `"scale"`, and `"translate"`. If the type is `"scale"`, the object MUST have the property `"scale"`, representing the scaling factor. It MUST be an array of numbers, with the number of elements equal to the number of axes in the coordinate system. If the type is `"translate"`, the object MUST have the property `"translate"`, representing the translation vector. It MUST be an array of numbers, with the number of elements equal to the number of axes in the coordinate system. If the type is `"identity"`, the object MUST NOT have any other properties.
- `"transformationMatrix"`: Representing the transformation matrix from the coordinate system of the image to the coordinate system of the MicroJSON object. It MUST be an array of arrays of numbers, with the number of rows equal to the number of axes in the coordinate system, and the number of columns equal to the number of axes in the image coordinate system. The transformation matrix MUST be invertible.


### Axis Object

An axis object represents the choice of axes (2D or 3D). It MUST have the following properties:
- `"name"`: Representing the name of the axis. It MUST be a string.
It MAY contain the following properties:
- `"unit"`: Representing the units of the corresponding axis in the axes property. It MUST be an array with the elements having any of the following values: `[“angstrom", "attometer", "centimeter", "decimeter", "exameter", "femtometer", "foot", "gigameter", "hectometer", "inch", "kilometer", "megameter", "meter", "micrometer", "mile", "millimeter", "nanometer", "parsec", "petameter", "picometer", "terameter", "yard", "yoctometer", "yottameter", "zeptometer", "zettameter“]`
- `"description"`: A string describing the axis.


