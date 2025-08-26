# MicroJSON

MicroJSON is a JSON-based format inspired by [GeoJSON](https://geojson.org), designed to encode a variety of data structures related to microscopy images. It can handle representations of reference points, regions of interest, and other annotations, making it an ideal solution for conveying complex microscopy data in a straightforward, easy-to-use format.

For more extensive documentation, please refer to the [online documentation](https://polusai.github.io/microjson/).


## Features

MicroJSON offers a range of features designed to meet the needs of microscopy data representation:

- **Flexible Data Structures:** MicroJSON can represent diverse data structures, including geometries (such as points, multipoints, linestrings, polygons), features (individual entities with specific properties), feature collections (groups of features), and coordinate systems.

- **Standardized Format:** MicroJSON uses the widely adopted JSON format, ensuring compatibility with a wide range of programming languages and tools.

- **Extensibility:** MicroJSON can handle additional properties associated with specific features, such as metadata relating to microscopy images.

## Additional Functions
There are two additional functionalities added which supports binary and label images.

- **OmeMicrojsonModel:** Converts objects in a binary or label images into polygon coordinates (rectangle, encoding) and save them in json file format using microjson package.

- **MicrojsonBinaryModel:** Reconstruct binary images using polygon coordinates from json file.

## Installation

To install MicroJSON, you can use the following command:

```bash 
pip install microjson
```
This will install the default version of MicroJSON with the basic functionalities and minimal dependencies. If you want to use the additional functionalities, such as provided by the ```utils``` module, you can install the package with the following command:

```bash
pip install microjson[all]
```


## Usage

MicroJSON is compatible with any application or tool that process JSON data. Its design makes it especially well-suited for applications involving analysis, visualization, and manipulation of microscopy images.

## Examples

Refer to the examples folder to see samples of MicroJSON files as well as a simple parsing example, or the [example in the documentation](docs/example.md)

## Specification

For more detailed information about the MicroJSON structure and its components, please refer to the [Specification](docs/index.md) file.

## External Resources

The GeoJSON test files are copied from the [GeoJSON Schema GitHub repository](https://github.com/geojson/schema), and are Copyright (c) 2018 Tim Schaub under MIT License.

## Contribution

We welcome contributions to the development and enhancement of MicroJSON. Whether you're reporting bugs, suggesting enhancements, or contributing to the code, your input is highly appreciated.

## License

MicroJSON is primarily licensed under the [MIT License](./LICENSE).

Portions of this project are derived from 'geojson2vt' and are located in 'src/microjson/microjson2vt'.
These portions are licensed under the [ISC License](./src/microjson/microjson2vt/LICENSE).

---

This project is maintained by NovaGen Research Fund. For any queries or further discussion, please contact [Novagen](info@novagenresearch.org).
