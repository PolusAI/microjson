# MicroJSON

MicroJSON is a JSON-based format inspired by [GeoJSON](https://geojson.org), designed to encode a variety of data structures related to microscopy images. It can handle representations of reference points, regions of interest, and other annotations, making it an ideal solution for conveying complex microscopy data in a straightforward, easy-to-use format.

## Features

MicroJSON offers a range of features designed to meet the needs of microscopy data representation:

- **Flexible Data Structures:** MicroJSON can represent diverse data structures, including geometries (such as points, multipoints, linestrings, polygons), features (individual entities with specific properties), feature collections (groups of features), and coordinate systems.

- **Standardized Format:** MicroJSON uses the widely adopted JSON format, ensuring compatibility with a wide range of programming languages and tools.

- **Extensibility:** MicroJSON can handle additional properties associated with specific features, such as metadata relating to microscopy images.

## Additional Functions
There are two additional functionalities added which supports binary images.
**BinaryMicrojsonModel:** Converts objects in a binary image into polygon coordinates (rectangle, encoding) and save them in json file format using microjson package.
**MicrojsonBinaryModel:** Reconstruct binary images using polygon coordinates from json file.

## Usage

MicroJSON can be used with any application or tool that can process JSON data. Due to its design, it is particularly suited to applications related to the analysis, visualization, and manipulation of microscopy images.

## External Resources

The GeoJSON test files are copied from the [GeoJSON Schema GitHub repository](https://github.com/geojson/schema), and are Copyright (c) 2018 Tim Schaub under MIT License.

## Contribution

We welcome contributions to the development and enhancement of MicroJSON. Whether you're reporting bugs, suggesting enhancements, or contributing to the code, your input is highly appreciated.

## License

MicroJSON is licensed under MIT License, (c) 2023 Polus AI & Nextonic Solutions LLC.

## Authors
Bengt Ljungquist [bengt.ljungquist@nextonicsolutions.com](bengt.ljungquist@nextonicsolutions.com)


---

This project is maintained by Polus AI. For any queries or further discussion, please contact the author on email address above.
