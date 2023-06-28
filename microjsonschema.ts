/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type Unit =
  | "angstrom"
  | "attometer"
  | "centimeter"
  | "decimeter"
  | "exameter"
  | "femtometer"
  | "foot"
  | "gigameter"
  | "hectometer"
  | "inch"
  | "kilometer"
  | "megameter"
  | "meter"
  | "micrometer"
  | "mile"
  | "millimeter"
  | "nanometer"
  | "parsec"
  | "petameter"
  | "picometer"
  | "terameter"
  | "yard"
  | "yoctometer"
  | "yottameter"
  | "zeptometer"
  | "zettameter"
  | "pixel"
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
  | Point
  | MultiPoint
  | LineString
  | MultiLineString
  | Polygon
  | MultiPolygon
  | GeometryCollection;

export interface Coordinatesystem {
  axes: ("x" | "y" | "z" | "r" | "theta" | "phi")[];
  units?: Unit[];
  pixelsPerUnit?: number[];
}
export interface Descriptive {
  descriptive?: {
    [k: string]: string;
  };
}
export interface Feature {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "Feature";
  /**
   * The geometry of the
   *                                    feature
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
  value_range?: {
    [k: string]: ValueRange;
  };
  descriptive_fields?: string[];
}
export interface ValueRange {
  min: number;
  max: number;
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
   * The geometry of the
   *                                    feature
   */
  geometry: Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon | GeometryCollection;
  properties: Properties;
  id?: string | number;
  coordinatesystem?: Coordinatesystem;
  ref?: string | number;
}
export interface Properties {
  descriptive?: Descriptive;
  numerical?: Numerical;
  multi_numerical?: MultiNumerical;
}
export interface Numerical {
  numerical?: {
    [k: string]: number;
  };
}
export interface MultiNumerical {
  multi_numerical?: {
    [k: string]: number[];
  };
}
export interface MicroFeatureCollection {
  /**
   * @minItems 4
   */
  bbox?: [number, number, number, number, ...number[]];
  type: "FeatureCollection";
  features: Feature[];
  value_range?: {
    [k: string]: ValueRange;
  };
  descriptive_fields?: string[];
  coordinatesystem?: Coordinatesystem;
}
