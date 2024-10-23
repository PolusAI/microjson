# Pydantic Models for MicroJSON and GeoJSON

## Introduction

This document describes the Pydantic models used for GeoJSON and MicroJSON objects. These models leverage Python's type hinting and Pydantic's validation mechanisms, making it robust and efficient to work with complex GeoJSON and MicroJSON objects.

## Models

::: microjson.model

### Base Objects


### Geometry Types
Uses geojson-pydantic models for GeoJSON geometry types, included here for reference. Please refer to the [geojson-pydantic documentation](https://developmentseed.org/geojson-pydantic/) for more information.

#### Point

Represents a GeoJSON Point object.

#### MultiPoint

Represents a GeoJSON MultiPoint object.

#### LineString

Represents a GeoJSON LineString object.

#### MultiLineString

Represents a GeoJSON MultiLineString object.

#### Polygon

Represents a GeoJSON Polygon object.

#### MultiPolygon

Represents a GeoJSON MultiPolygon object.


### Compound Objects

#### Multiscale

A coordinate system for MicroJSON features or feature collections.

::: microjson.model.Multiscale

#### GeometryCollection

A coordinate system for MicroJSON features or feature collections.

::: microjson.model.Multiscale

#### GeometryCollection

A collection of multiple geometries. From geojson-pydantic(https://developmentseed.org/geojson-pydantic/), included here for reference.

#### Feature

Represents a GeoJSON feature object, from geojson-pydantic(https://developmentseed.org/geojson-pydantic/), included here for reference.

#### FeatureCollection

Represents a GeoJSON feature collection, from geojson-pydantic(https://developmentseed.org/geojson-pydantic/), included here for reference.

#### GeoJSON

The root object of a GeoJSON file.

::: microjson.model.GeoJSON

### MicroJSON Extended Models

#### MicroFeature

A MicroJSON feature, which is an extension of a GeoJSON feature.

::: microjson.model.MicroFeature

#### MicroFeatureCollection

A MicroJSON feature collection, which is an extension of a GeoJSON feature collection.

::: microjson.model.MicroFeatureCollection

#### MicroJSON

The root object of a MicroJSON file.

::: microjson.model.MicroJSON
