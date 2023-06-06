/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type Unit =
  | "pixel"
  | "meter"
  | "decimeter"
  | "centimeter"
  | "millimeter"
  | "micrometer"
  | "nanometer"
  | "picometer"
  | "radian"
  | "degree";
/**
 * The root object of a GeoJSON file
 */
export type GeoJSON =
  | Feature
  | FeatureCollection
  | Point
  | MultiPoint
  | LineString
  | MultiLineString
  | Polygon
  | MultiPolygon
  | GeometryCollection;
/**
 * The root object of a MicroJSON file
 */
export type MicroJSON =
  | MicroFeature
  | MicroFeatureCollection
  | MicroPoint
  | MicroMultiPoint
  | MicroLineString
  | MicroMultiLineString
  | MicroPolygon
  | MicroMultiPolygon
  | MicroGeometryCollection;

export interface Coordinatesystem {
  /**
   * The coordinate system of the coordinates
   */
  axes: ("x" | "y" | "z" | "r" | "theta" | "phi")[];
  /**
   * The units of the coordinates
   */
  units: Unit[];
  /**
   * The number of pixels per unit
   */
  pixelsPerUnit: number[];
}
export interface Feature {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "Feature";
  /**
   * The geometric data
   *                                              of the feature
   */
  geometry: Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon | GeometryCollection;
  /**
   * Properties of the
   *                                        feature
   */
  properties: {
    [k: string]: unknown;
  };
  id?: string | number;
}
export interface Point {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "Point";
  /**
   * @minItems 2
   * @maxItems 3
   */
  coordinates: [number, number] | [number, number, number];
}
export interface MultiPoint {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "MultiPoint";
  coordinates: [number, number] | [number, number, number][];
}
export interface LineString {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "LineString";
  coordinates: [number, number] | [number, number, number][];
}
export interface MultiLineString {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "MultiLineString";
  coordinates: [number, number] | [number, number, number][][];
}
export interface Polygon {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "Polygon";
  coordinates: [number, number] | [number, number, number][][];
}
export interface MultiPolygon {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "MultiPolygon";
  coordinates: [number, number] | [number, number, number][][][];
}
export interface GeometryCollection {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "GeometryCollection";
  geometries: (Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon)[];
}
export interface FeatureCollection {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "FeatureCollection";
  features: Feature[];
}
export interface GeoAbstract {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
}
export interface MicroFeature {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "Feature";
  /**
   * The geometric data
   *                                              of the feature
   */
  geometry: Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon | GeometryCollection;
  /**
   * Properties of the
   *                                        feature
   */
  properties: {
    [k: string]: unknown;
  };
  id?: string | number;
  coordinatesystem?: Coordinatesystem;
}
export interface MicroFeatureCollection {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "FeatureCollection";
  features: Feature[];
  coordinatesystem?: Coordinatesystem;
}
export interface MicroGeometryCollection {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "GeometryCollection";
  geometries: (Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon)[];
  coordinatesystem?: Coordinatesystem;
}
export interface MicroPoint {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "Point";
  /**
   * @minItems 2
   * @maxItems 3
   */
  coordinates: [number, number] | [number, number, number];
  coordinatesystem?: Coordinatesystem;
}
export interface MicroMultiPoint {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "MultiPoint";
  coordinates: [number, number] | [number, number, number][];
  coordinatesystem?: Coordinatesystem;
}
export interface MicroLineString {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "LineString";
  coordinates: [number, number] | [number, number, number][];
  coordinatesystem?: Coordinatesystem;
}
export interface MicroMultiLineString {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "MultiLineString";
  coordinates: [number, number] | [number, number, number][][];
  coordinatesystem?: Coordinatesystem;
}
export interface MicroPolygon {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "Polygon";
  coordinates: [number, number] | [number, number, number][][];
  coordinatesystem?: Coordinatesystem;
}
export interface MicroMultiPolygon {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "MultiPolygon";
  coordinates: [number, number] | [number, number, number][][][];
  coordinatesystem?: Coordinatesystem;
}
