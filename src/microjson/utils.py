import os
import errno
import ast
import json
import logging
import numpy as np

import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from itertools import product

import skimage as sk
from skimage import measure
from skimage import morphology

from sys import platform
from pathlib import Path
from typing import Any
from typing import Union
import microjson.model as mj
from multiprocessing import cpu_count

import warnings
from microjson import MicroJSON
from pydantic import ValidationError
from microjson.model import Feature
from typing import Union
import pydantic

#define conditional imports
try:
    from bfio import BioReader
    import filepattern as fp
    from scipy import ndimage
    import vaex
except ImportError as e:
    print("""Packages bfio, filepattern, scipy, vaex not installed
          please install using pip install microjson[all]""")
    raise e


warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TILE_SIZE = 1024
if platform == "linux" or platform == "linux2":
    NUM_THREADS = len(os.sched_getaffinity(0))  # type: ignore
else:
    NUM_THREADS = max(cpu_count() // 2, 2)


class OmeMicrojsonModel:
    """Generate JSON of segmentations polygon using microjson python package.

    Args:
        out_dir: Path to output directory.
        file_path: Path of an image file
        polygon_type: Type of polygon (Rectangle, Encoding).
    """

    def __init__(
        self,
        out_dir: Path,
        file_path: str,
        polygon_type: str,
    ) -> None:
        """Convert each object polygons (series of points, rectangle) to
        microjson."""
        self.out_dir = out_dir
        self.file_path = file_path
        self.polygon_type = polygon_type
        self.min_label_length = 1
        self.min_unique_labels = 0
        self.max_unique_labels = 2
        self.br = BioReader(self.file_path)

    def _tile_read(self) -> None:
        """Reading of Image in a tile and compute encodings for it."""
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            idx = 0
            for i, (z, y, x) in enumerate(
                product(
                    range(self.br.Z),
                    range(0, self.br.Y, TILE_SIZE),
                    range(0, self.br.X, TILE_SIZE),
                ),
            ):
                y_max = min([self.br.Y, y + TILE_SIZE])
                x_max = min([self.br.X, x + TILE_SIZE])
                image = self.br[y:y_max, x:x_max, z : z + 1]

                unique_labels = len(np.unique(image))

                if unique_labels >= self.max_unique_labels:
                    if unique_labels == self.max_unique_labels:
                        msg = f"Binary image detected : tile {i}"
                        logger.info(msg)
                        label_image = morphology.label(image)
                    else:
                        msg = f"Label image detected : tile {i}"
                        label_image = image
                        logger.info(msg)

                    if self.polygon_type != "rectangle":
                        future = executor.submit(
                            self.segmentations_encodings,
                            label_image,
                            x,
                            y,
                        )
                        if as_completed(future):  # type: ignore
                            label, coordinates = future.result()
            
                            if len(label) and len(coordinates) > 0:
                                label = [i + idx for i in range(
                                    1, len(label) + 1)]
                                idx = 0
                                if len(label) == 1:
                                    idx += label[0]
                                else:
                                    idx += label[-1]
                                self.polygons_to_microjson(
                                    i, label, coordinates)

                    else:
                        future = executor.submit(
                            self.rectangular_polygons,  # type: ignore
                            label_image,
                            x,
                            y,
                        )
                        if as_completed(future):  # type: ignore
                            label, coordinates = future.result()
                            if len(label) and len(coordinates) > 0:
                                label = [i + idx for i in range(
                                    1, len(label) + 1)]
                                idx = 0
                                if len(label) == 1:
                                    idx += label[0]
                                else:
                                    idx += label[-1]
                                self.polygons_to_microjson(
                                    i, label, coordinates)

    def get_line_number(self, filename, target_string) -> int:
        line_number = 0
        with open(filename, 'r') as file:
            for line in file:
                line_number += 1
                if target_string in line:
                    return line_number
        return line_number
    
    def cleaning_directories(self):
        out_combined = Path(self.out_dir, "tmp")
        for file in out_combined.iterdir():
            if file.is_file():
                shutil.move(file, out_combined.parent)
        shutil.rmtree(out_combined)

    def write_single_json(self) -> None:
        """Combine microjsons from tiled images into combined json file."""
        self._tile_read()
        out_combined = Path(self.out_dir, "tmp")
        out_file = Path(self.file_path).name.split(
            ".")[0] + "_" + str(self.polygon_type) + ".json"
        if not out_combined.exists():
            out_combined.mkdir(exist_ok=True)
            
        fname = re.split(r"[\W']+", str(Path(self.file_path).name))[0]
        files = fp.FilePattern(self.out_dir, f"{fname}.*json")
        if len(files) > 1:
            with Path.open(Path(out_combined, out_file), "w") as fw:
                for i, fl in zip(range(1, len(files) + 1), files()):
                    file = fl[1][0]
                    line_number = self.get_line_number(
                        file,
                        "multiscale")
                    total_lines = len([line for line in open(file, 'r')])
                    index = (total_lines - line_number) + 3
                    outname = re.split(r"[_\.]+", file.name)[:-2]
                    outname = "_".join(outname) + ".json"  # type: ignore
                    df = Path.open(Path(file))
                    data = df.readlines()
                    if i == 1:
                        endline = data[-index].rstrip() + ","
                        sfdata = data[:-index] + [endline]
                    elif i > 1 and i < len(files):
                        endline = data[-index].rstrip() + ","
                        sfdata = data[3:-index] + [endline]
                    else:
                        sfdata = data[3:]
                    fw.writelines(sfdata)
                    Path(file).unlink()
        self.cleaning_directories()

    def segmentations_encodings(
        self,
        label_image: np.ndarray,
        x: int,
        y: int,
    ) -> tuple[Any, list[list[list[Any]]]]:
        """Calculate object boundries as series of vertices/points
        forming a polygon."""
        label, coordinates = [], []
        objects = ndimage.measurements.find_objects(label_image)
        for i in range(len(objects)+1):
            mask = np.zeros((label_image.shape[0], label_image.shape[1]))
            mask[(label_image == i)] = 1
            contour_thresh = 0.8
            contour = measure.find_contours(mask, contour_thresh)
            if (
                len(contour) > self.min_unique_labels
                and len(contour) < self.max_unique_labels
                and len(contour[0] > self.min_label_length)
            ):
                contour = np.flip(contour, axis=1)
                seg_encodings = contour.ravel().tolist()
                poly = [
                    [xi + x, yi + y]
                    for xi, yi in zip(seg_encodings[1::2], seg_encodings[::2])
                ]
                label.append(i)
                coordinates.append(poly)

        return label, coordinates

    def rectangular_polygons(
        self,
        label_image: np.ndarray,
        x: int,
        y: int,
    ) -> tuple[list[int], list[str]]:
        """Calculate Rectangular polygon for each object."""
        objects = ndimage.measurements.find_objects(label_image)
        label, coordinates = [], []
        for i, obj in enumerate(objects):
            if obj is not None:
                height = int(obj[0].stop - obj[0].start)
                width = int(obj[1].stop - obj[1].start)
                ymin = obj[0].start
                xmin = obj[1].start
                poly = str(
                    [
                        [x + xmin, y + ymin],
                        [x + xmin + width, y + ymin],
                        [x + xmin + width, y + ymin + height],
                        [x + xmin, y + ymin + height],
                        [x + xmin, y + ymin],
                    ],
                )

            else:
                poly = str([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
            coordinates.append(poly)
            label.append(i + 1)

        return label, coordinates

    def polygons_to_microjson(  # noqa: PLR0915
        self,
        i: int,
        label: list[int],
        coordinates: list[Any],
    ) -> None:  # : 183
        """Create microjson overlays in JSON Format."""
        x_dimension = np.repeat(self.br.X, len(label))
        y_dimension = np.repeat(self.br.Y, len(label))
        channel = np.repeat(self.br.C, len(label))
        filename = Path(self.file_path)
        image_name = np.repeat(filename.name, len(label))

        data = vaex.from_arrays(
            Image=image_name,
            X=x_dimension,
            Y=y_dimension,
            Channel=channel,
            Label=label,
        )
        data["geometry_type"] = np.repeat("Polygon", data.shape[0])
        data["type"] = np.repeat("Feature", data.shape[0])

        varlist = [
            "Image",
            "X",
            "Y",
            "Channel",
            "Label",
            "geometry_type",
            "type",
        ]

        if list(data.columns) != varlist:
            msg = "Invalid vaex dataframe!! Please do check path again"
            raise ValueError(msg)

        if data.shape[0] == 0:
            msg = "Invalid vaex dataframe!! Please do check path again"
            raise ValueError(msg)

        str_columns = list(
            filter(
                lambda feature: feature in ["Image", "X", "Y", "Channel"],
                data.get_column_names(),
            ),
        )
        int_columns = list(
            filter(
                lambda feature: feature in ["Label"],
                data.get_column_names(),
            ),
        )
        if len(int_columns) == 0:
            msg = "Features with integer datatype do not exist"
            raise ValueError(msg)

        features: list[mj.Feature] = []
        for (_, row), cor in zip(data.iterrows(), coordinates):  # type: ignore
            numerical = [{key: row[key]} for key in int_columns]

            numeric_dict = {}
            for sub_dict in numerical:
                numeric_dict.update(sub_dict)

            GeometryClass = getattr(mj, row["geometry_type"])  # noqa: N806
            if self.polygon_type == "rectangle":
                cor_value = list(ast.literal_eval(cor))
            else:
                cor_value = cor + [cor[0]]

            geometry = GeometryClass(type=row["geometry_type"],
                                     coordinates=[cor_value])

            # Create a new Feature object
            feature = mj.MicroFeature(
                type=row["type"],
                geometry=geometry,
                properties=numeric_dict,
            )
            features.append(feature)


        desc_meta = {key: f"{data[key].values[0]}" for key in str_columns}

        # Create a new FeatureCollection object
        feature_collection = mj.MicroFeatureCollection(
            type="FeatureCollection",
            properties=desc_meta,
            features=features,
            multiscale={
                "axes": [
                    {
                        "name": "x",
                        "unit": "micrometer",
                        "type": "space",
                        "description": "x-axis",
                    },
                    {
                        "name": "y",
                        "unit": "micrometer",
                        "type": "space",
                        "description": "y-axis",
                    },
                ],
                "origo": "top-left",
            },
        )
        fname = re.split(r"[\W']+", str(Path(self.file_path).name))[0]
        outname = (
            str(fname)
            + "_"
            + str(self.polygon_type)
            + "_"
            + str(i)
            + ".json"
        )
        if len(feature_collection.model_dump_json()) == 0:
            msg = "JSON file is empty"
            raise ValueError(msg)
        if len(feature_collection.model_dump_json()) > 0:
            out_name = Path(self.out_dir, outname)
            with Path.open(out_name, "w") as f:
                f.write(
                    feature_collection.model_dump_json(
                        indent=2, exclude_unset=True),
                )
                logger.info(f"Saving overlay json file: {out_name}")


class CustomValidation(pydantic.BaseModel):
    """Properties with validation."""
    out_dir: Union[str, Path]
    file_path: Union[str, Path]

    @pydantic.validator("out_dir", pre=True)
    @classmethod
    def validate_out_dir(cls, value):
        if not Path(value).exists():
            raise ValueError(f"{value} do not exist! Please do check it again")
        if isinstance(value, str):
            return Path(value)
        return value

    @pydantic.validator("file_path", pre=True)
    @classmethod
    def validate_file_path(cls, value):
        if not Path(value).exists():
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), value)
        if not MicroJSON.model_validate(json.load(Path.open(Path(value)))):
            raise ValidationError(f"Not a valid MicroJSON {value.name}")
        if isinstance(value, str):
            return Path(value)
        return value


class MicrojsonBinaryModel(CustomValidation):
    """Generate binary masks from polygons stored in microjson format.

    Args:
        out_dir: Path to output directory.
        file_path: Microjson file path
    """
    out_dir: Union[str, Path]
    file_path: Union[str, Path]

    def microjson_to_binary(self) -> None:
        """Convert polygon coordinates (series of points, rectangle) of all
        objects to binary mask"""
        logger.info(f"Converting microjson to binary mask: {self.file_path}")

        data = json.load(Path.open(Path(self.file_path)))
        items = [Feature(**item) for item in data['features']]
        poly = [i.geometry.coordinates for i in items]
        meta = data['properties']
        image_name = meta.get("Image")
        x = int(meta.get("X"))
        y = int(meta.get("Y"))
        fmask = np.zeros((x, y), dtype=np.uint8)
        for i, _ in enumerate(poly):
            image = fmask.copy()
            pol = np.array(poly[i][0])
            mask = sk.draw.polygon2mask((x, y), pol)
            image[mask == False] = 0
            image[mask == True] = 1
            fmask += image 
        fmask = np.rot90(fmask)
        fmask = np.flipud(fmask)
        outname = Path(self.out_dir, image_name)
        if len(np.unique(fmask)) == 3:
            tmp_mask = fmask.copy()
            tmp_mask[fmask == 2] = 1
            sk.io.imsave(outname, tmp_mask)
        else:
            sk.io.imsave(outname, fmask)
        return
