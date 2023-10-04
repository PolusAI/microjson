import os
import errno
import ast
import json
import logging
from itertools import chain
from pathlib import Path
from typing import Any
import microjson.model as mj
import numpy as np
import scipy
import vaex
import skimage as sk

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def gather_example_files(directory):
    files = []
    # Walk through the directory
    for dirpath, _, filenames in os.walk(directory):
        # Filter to just the .json files
        example_files = [os.path.join(dirpath, f)
                         for f in filenames if f.endswith('.json')]
        files.extend(example_files)
    return files

class BinaryMicrojsonModel:
    """Generate JSON of segmentations polygon using microjson python package.

    Args:
        polygon_type: Type of polygon (Rectangular, Encodings).
        out_dir: Path to output directory.
        file_name: Binary image filename
    """

    def __init__(
        self,
        out_dir: Path,
        file_path: str,
        polygon_type: str,
    ) -> None:
        """Convert each object polygons (series of points, rectangle) to microjson."""
        self.out_dir = out_dir
        self.file_path = file_path
        self.polygon_type = polygon_type
        self.image = sk.io.imread(self.file_path)
        self.min_unique_labels = 0
        self.max_unique_labels = 2
        if len(np.unique(self.image)) > self.max_unique_labels:
            msg = "Binary images are not detected!! Please do check images again"
            raise ValueError(msg)
        self.label_image = sk.morphology.label(self.image)
        self.mask = np.zeros((self.image.shape[0], self.image.shape[1]))


    def segmentations_encodings(
        self,
    ) -> tuple[Any, list[list[list[Any]]]]:
        """Calculate object boundries as series of vertices/points forming a polygon."""
        label, coordinates= [], []
        for i in np.unique(self.label_image):
            self.mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
            self.mask[(self.label_image == i)] = 1 
            contour_thresh = 0.8
            contour = sk.measure.find_contours(self.mask, contour_thresh)
            if (
                len(contour) > self.min_unique_labels
                and len(contour) < self.max_unique_labels
            ):
                contour = np.flip(contour, axis=1)
                seg_encodings = contour.ravel().tolist()
                poly = [[x, y] for x, y in zip(seg_encodings[1::2], seg_encodings[::2])]
                label.append(i)
                coordinates.append(poly)

        x_dimension = np.repeat(self.image.shape[0], len(label))
        y_dimension = np.repeat(self.image.shape[1], len(label))
        if len(self.image.shape) == 3:
            channel = np.repeat(self.image.shape[2], len(label))
        else:
            channel = np.repeat(1, len(label))
        filename = Path(self.file_path)
        image_name = np.repeat(filename.name, len(label))
        plate_name = np.repeat(Path(filename.parent).name, len(label))
        encodings = list(chain.from_iterable(coordinates))
        encoding_length = np.repeat(len(encodings), len(label))
        coordinates = [str(cor) for cor in coordinates]

        data = vaex.from_arrays(
            Plate=plate_name,
            Image=image_name,
            X=x_dimension,
            Y=y_dimension,
            Channel=channel,
            Label=label,
            Encoding_length=encoding_length,
            Coordinates=coordinates,
        )
        data["geometry_type"] = np.repeat("Polygon", data.shape[0])
        data["type"] = np.repeat("Feature", data.shape[0])
        return data

    def rectangular_polygons(
        self,
    ) -> vaex.DataFrame:
        """Calculate Rectangular polygon for each object."""
        objects = scipy.ndimage.measurements.find_objects(self.label_image)
        label, coordinates = [], []
        for i, obj in enumerate(objects):
            if obj is not None:
                height = int(obj[0].stop - obj[0].start)
                width = int(obj[1].stop - obj[1].start)
                ymin = obj[0].start
                xmin = obj[1].start
                poly = str(
                    [
                        [xmin, ymin],
                        [xmin + width, ymin],
                        [xmin + width, ymin + height],
                        [xmin, ymin + height],
                        [xmin, ymin],
                    ],
                )
            else:
                poly = str([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
            coordinates.append(poly)
            label.append(i + 1)

        x_dimension = np.repeat(self.image.shape[0], len(label))
        y_dimension = np.repeat(self.image.shape[1], len(label))
        if len(self.image.shape) == 3:
            channel = np.repeat(self.image.shape[2], len(label))
        else:
            channel = np.repeat(1, len(label))

        image_name = np.repeat(Path(self.file_path).name, len(label))
        plate_name = np.repeat(Path(Path(self.file_path).parent).name, len(label))
        encodings = list(chain.from_iterable(coordinates))
        encoding_length = np.repeat(len(encodings), len(label))
        coordinates = [str(cor) for cor in coordinates]

        data = vaex.from_arrays(
            Plate=plate_name,
            Image=image_name,
            X=x_dimension,
            Y=y_dimension,
            Channel=channel,
            Label=label,
            Encoding_length=encoding_length,
            Coordinates=coordinates,
        )
        data["geometry_type"] = np.repeat("Polygon", data.shape[0])
        data["type"] = np.repeat("Feature", data.shape[0])

        return data

    def get_method(self) -> vaex.DataFrame:
        """Get data and corrdinates based on polygon type."""
        methods = {
            "encoding": self.segmentations_encodings,
            "rectangle": self.rectangular_polygons,
        }
        data = methods[self.polygon_type]()  # type: ignore[index]

        return data
    
    def polygons_to_microjson(self) -> None:
        """Create microjson overlays in JSON Format."""
        data = self.get_method()

        varlist = [
            "Plate",
            "Image",
            "X",
            "Y",
            "Channel",
            "Label",
            "Encoding_length",
            "Coordinates",
            "geometry_type",
            "type"
        ]

        if list(data.columns) != varlist:
            msg = "Invalid vaex dataframe!! Please do check path again"
            raise ValueError(msg)

        if data.shape[0] == 0:
            msg = "Invalid vaex dataframe!! Please do check path again"
            raise ValueError(msg)

        des_columns = [
            feature
            for feature in data.get_column_names()
            if data.data_type(feature) == str
        ]
        des_columns = list(
            filter(
                lambda feature: feature not in ["geometry_type", "type", "Coordinates"],
                des_columns,
            ),
        )
        int_columns = [
            feature
            for feature in data.get_column_names()
            if data.data_type(feature) == int or data.data_type(feature) == float
        ]

        if len(int_columns) == 0:
            msg = "Features with integer datatype do not exist"
            raise ValueError(msg)

        if len(des_columns) == 0:
            msg = "Descriptive features do not exist"
            raise ValueError(msg)

        features: list[mj.Feature] = []
        for (_, row) in data.iterrows():
            desc = [{key: row[key]} for key in des_columns]
            numerical = [{key: row[key]} for key in int_columns]

            descriptive_dict = {}
            for sub_dict in desc:
                descriptive_dict.update(sub_dict)

            numeric_dict = {}
            for sub_dict in numerical:
                numeric_dict.update(sub_dict)

            GeometryClass = getattr(mj, row["geometry_type"])  # noqa: N806
            cor_value =list(ast.literal_eval(row['Coordinates']))
            geometry = GeometryClass(type=row["geometry_type"], coordinates=[cor_value])

            # create a new properties object dynamically
            properties = mj.Properties(
                string=descriptive_dict,
                numeric=numeric_dict,
            )

            # Create a new Feature object
            feature = mj.MicroFeature(
                type=row["type"],
                geometry=geometry,
                properties=properties,
            )
            features.append(feature)

        valrange = [
            {i: {"min": data[i].min(), "max": data[i].max()}} for i in int_columns
        ]
        valrange_dict = {}
        for sub_dict in valrange:
            valrange_dict.update(sub_dict)

        # Create a list of descriptive fields
        descriptive_fields = des_columns

        # Create a new FeatureCollection object
        feature_collection = mj.MicroFeatureCollection(
            type="FeatureCollection",
            features=features,
            value_range=valrange_dict,
            descriptive_fields=descriptive_fields,
            coordinatesystem={
                "axes": [
                    {
                        "name": "x",
                        "unit": "micrometer",
                        "type": "cartesian",
                        "pixelsPerUnit": 1,
                        "description": "x-axis",
                    },
                    {
                        "name": "y",
                        "unit": "micrometer",
                        "type": "cartesian",
                        "pixelsPerUnit": 1,
                        "description": "y-axis",
                    },
                ],
                "origo": "top-left",
            },
        )

        outname = str(data["Image"].values[0]).split(".ome")[0] + "_" + str(self.polygon_type) + ".json"


        if len(feature_collection.model_dump_json()) == 0:
            msg = "JSON file is empty"
            raise ValueError(msg)
        if len(feature_collection.model_dump_json()) > 0:
            out_name = Path(self.out_dir, outname)
            with Path.open(out_name, "w") as f:
                f.write(
                    feature_collection.model_dump_json(indent=2, exclude_unset=True),
                )
                logger.info(f"Saving overlay json file: {out_name}")


class MicrojsonBinaryModel:
    """Generate binary masks from polygons stored in microjson format.

    Args:
        polygon_type: Type of polygon (Rectangular, Encodings).
        out_dir: Path to output directory.
        file_path: Microjson file path
    """

    def __init__(
        self,
        out_dir: Path,
        file_path: str,
        polygon_type: str,
    ) -> None:
        """Convert each object polygons (series of points, rectangle) to binary mask."""
        self.out_dir = out_dir
        if not self.out_dir.exists():
            self.out_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = file_path
        self.polygon_type = polygon_type
        if not self.file_path.name.endswith(".json"):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.file_path)
        self.data = json.load(Path.open(self.file_path))
        
    def parsing_microjson(self) -> tuple[Any, int, int, str]:
        """Parsing microjson to get polygon coordinates, image name and dimesions."""
        poly = [self.data['features'][i]['geometry']['coordinates'] for i in range(len(self.data['features']))]
        image_name = self.data['features'][0]['properties']['string']['Image']
        x = int(self.data['features'][0]['properties']['numeric']['X'])
        y = int(self.data['features'][0]['properties']['numeric']['Y'])
        return poly, image_name, x, y
    
    def convert_microjson_to_binary(self) -> None:
        """Convert polygon coordinates (series of points, rectangle) of all objects to binary mask"""
        poly, image_name, x, y = self.parsing_microjson()
        final_mask = np.zeros((x, y), dtype=np.uint16)
        image = final_mask.copy()
        for i, _ in enumerate(poly):
            pol = np.array(poly[i][0])
            mask = sk.draw.polygon2mask((x, y), pol)
            image[mask == True] = 1
            image[mask == False] = 0
            final_mask += image 
        final_mask = np.rot90(final_mask)
        final_mask = np.flipud(final_mask)
        outname = Path(self.out_dir, image_name)
        sk.io.imsave(outname, final_mask)
        return