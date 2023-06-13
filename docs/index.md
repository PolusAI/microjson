# MicroJSON Specification

## Introduction

MicroJSON is a format, inspired by [GeoJSON](https://geojson.org), for encoding a variety of data structures related to microscopy images, including reference points, regions of interest, and other annotations. These data structures are represented using the widely adopted JSON format, making it easy to work with in various programming languages and applications. It is fully backwards compatible with the [GeoJSON Specification, RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946), since any GeoJSON also is accepted as a MicroJSON. As GeoJSON supports foreign top level properties, a MicroJSON is also a valid GeoJSON. This specification describes briefly the objects that exist in GeoJSON, and then in more detail describes the additional objects that are part of MicroJSON. For a more detailed description of the GeoJSON objects, please see the [GeoJSON Specification, RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946).

## Objects

### MicroJSON Object

A MicroJSON object is a JSON object that represents a geometry, feature, or collection of features, or more precisely, be either of type (having value of top level field `type` as) `"Geometry"`, `"Feature"`, or `"Featurecollection"`, that is, the same as for GeoJSON. What separates MicroJSON from GeoJSON is that it MAY have of a top level property `"coordinatesystem"`:  

- `"coordinatesystem"`: (Optional) A coordinate system object as defined in the section [Coordinates object](#coordinates-object). If this property is not present, the default coordinate system is assumed to be the same as the image coordinate system, using cartesian coordinates and pixels as units.

A MicroJSON object MAY have a `"bbox"` property":

- `"bbox"`: (Optional) Bounding Box of the feature represented as an array of length 4 (2D) or length 6 (3D).


### Geometry Object

A geometry object is a JSON object where the `type` member's value is one of the following strings: `"Point"`, `"MultiPoint"`, `"LineString"`, `"MultiLineString"`, `"Polygon"`, `"Rectangle"`, `"MultiPolygon"`, or `"GeometryCollection"`.

Each geometry object must have a `"coordinates"` member with an array value. The structure of the coordinates array depends on the geometry type.

- **Point**: The coordinates array must contain two or three (if 3D) numbers representing the X and Y (and Z) coordinates of the point in the image. A “Point” Geometry MAY have a radius, if indicating a circular object, with the value in pixels, specified as a member `“radius”` of the Geometry object.

- **MultiPoint**: The coordinates array must be an array of point coordinates.

- **LineString**: The coordinates array must be an array of two or more point coordinates forming a continuous line. A “LineString” Geometry MAY have a radius, with the value in pixels, specified as a member “radius” of the Geometry object.

- **MultiLineString**: The coordinates array must be an array of LineString coordinate arrays.

- **Polygon**: The coordinates array must be an array of linear ring coordinate arrays, where the first linear ring represents the outer boundary and any additional rings represent holes within the polygon.

    - A subtype of “Polygon” is the “Rectangle” geometry: A polygon with an array of four 2D point coordinates representing the corners of the rectangle in a counterclockwise order. It has the property subtype with the value `“Rectangle”`.

    - A subtype of “Polygon” is the “Cuboid”: A polygon with an array of eight 3D point coordinates representing the corners of the rectangle in a counterclockwise order in the X-Y plane, starting with the plane with the lowest Z value. It has the property subtype with the value `“Cuboid”`.

- **MultiPolygon**: The coordinates array must be an array of Polygon coordinate arrays.

### GeometryCollection

A GeometryCollection is an array of geometries (Point, multipoint, LinesString, MultiLineString, Polygon, MultiPolygon). It is possible for this array to be empty.

### Feature Object

A feature object represents a spatially bounded entity associated with properties specific to that entity. A feature object is a JSON object with the following members, required unless otherwise noted:

- `"type"`: A string with the value `"Feature"`.
- `"geometry"`: A geometry object as defined in the section above or a JSON null value.
- `"properties"`: (Optional) A JSON object containing properties specific to the feature, or a JSON null value.
- `"id"`: (Optional) A unique identifier for this feature.


#### Special Feature Objects

- **Image**: An image MUST have the following key-value pairs in its “properties” object:

    - `"type"`: A string with the value “Image”

    - `"URI"`: A string with the image URI, e.g. “./image_1.tif"

    An Image MUST also have a geometry object (as its “geometry” member) of type “Rectangle”, indicating the shape of the image.

### FeatureCollection Object

A FeatureCollection object is a JSON object representing a collection of feature objects. A FeatureCollection object has a member with the name `"features"`. The value of `"features"` is a JSON array. Each element of the array is a Feature object as defined above. It is possible for this array to be empty.

#### Special FeatureCollection Objects

- **StitchingVector**: Represents a stitching vector, and MUST have the following key-value pairs in its “properties” object:

    - `"type"`: A string with the value “StitchingVector”

    Any object of a StitchingVector “features” array MUST be an “Image” special type of features object.

### Coordinates Object

A coordinates object represents the choice of axes (2D or 3D) and potentially their scale. It MUST have the following properties:

- `"axes"`: Representing the choice of axes. It MUST contain an array of length two from either of the following: `[“x“, ”y”, “z“]`, `[“r“, ”theta”, “z“]`, or `[“r“, ”theta”, “phi“]`.

It MAY contain the following properties:

- `"units"`: Representing the units of the corresponding axis in the axes property. It MUST be an array with the elements having any of the following values: `[“pixel“, “meter”, ”decimeter”, “centimeter“, “millimeter”, “micrometer”, “nanometer”, “picometer“, “radian“, “degree“]`
- `"pixelsPerUnit"`: A decimal value, except for angles, where it SHOULD have the value “0”.


