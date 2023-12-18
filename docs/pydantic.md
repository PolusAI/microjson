# Pydantic Models for MicroJSON and GeoJSON

## Introduction

This document describes the Pydantic models used for GeoJSON and MicroJSON objects. These models leverage Python's type hinting and Pydantic's validation mechanisms, making it robust and efficient to work with complex GeoJSON and MicroJSON objects.

## Models

::: microjson.model

### Base Models

#### GeoAbstract

::: microjson.model.GeoAbstract

#### ValueRange

A range of values for MicroJSON quantitative properties.

::: microjson.model.ValueRange

#### CoordinateSystem

A coordinate system for MicroJSON coordinates.

::: microjson.model.CoordinateSystem

#### Properties

Metadata properties of a MicroJSON feature.

::: microjson.model.Properties

### Geometry Types

#### Point

Represents a GeoJSON Point object.

::: microjson.model.Point

#### MultiPoint

Represents a GeoJSON MultiPoint object.

::: microjson.model.MultiPoint

#### LineString

Represents a GeoJSON LineString object.

::: microjson.model.LineString

#### MultiLineString

Represents a GeoJSON MultiLineString object.

::: microjson.model.MultiLineString

#### Polygon

Represents a GeoJSON Polygon object.

::: microjson.model.Polygon

#### MultiPolygon

Represents a GeoJSON MultiPolygon object.

::: microjson.model.MultiPolygon

### Compound Objects

#### GeometryCollection

A collection of multiple geometries.

::: microjson.model.GeometryCollection

#### Feature

Represents a GeoJSON feature object.

::: microjson.model.Feature

#### FeatureCollection

Represents a GeoJSON feature collection.

::: microjson.model.FeatureCollection

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
