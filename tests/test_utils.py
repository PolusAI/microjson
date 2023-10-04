"""Test fixtures.

Set up all data used in tests.
"""
import shutil
import tempfile
from pathlib import Path
from typing import Union
import numpy as np
import pytest
import microjson.utils as ut
import skimage as sk

def clean_directories() -> None:
    """Remove all temporary directories."""
    for d in Path(".").cwd().iterdir():
        if d.is_dir() and d.name.startswith("tmp"):
            shutil.rmtree(d)


@pytest.fixture()
def inp_dir() -> Union[str, Path]:
    """Create directory for saving intensity images."""
    return Path(tempfile.mkdtemp(dir=Path.cwd()))


@pytest.fixture()
def output_directory() -> Union[str, Path]:
    """Create output directory."""
    return Path(tempfile.mkdtemp(dir=Path.cwd()))

@pytest.fixture(params=[512, 1024])
def image_sizes(request: pytest.FixtureRequest) -> pytest.FixtureRequest:
    """To get the parameter of the fixture."""
    return request.param


@pytest.fixture()
def synthetic_images(
    inp_dir: Union[str, Path],
    image_sizes: pytest.FixtureRequest,
) -> Union[str, Path]:
    """Generate random synthetic images."""
    for i in range(5):
        im = np.zeros((image_sizes, image_sizes))
        blobs = sk.data.binary_blobs(
            length=image_sizes, volume_fraction=0.02, blob_size_fraction=0.03

        )
        im[blobs > 0] = 1
        binary_img = f"x01_y01_r{i}_c1.tif"
        binary_img = Path(inp_dir, binary_img)  # type: ignore
        sk.io.imsave(binary_img, im)
    return inp_dir

@pytest.fixture(params=["rectangle", "encoding"])
def get_params(request: pytest.FixtureRequest) -> list[str]:
    """To get the parameter of the fixture."""
    return request.param


def test_BinaryMicrojsonModel(synthetic_images: Path, output_directory: Path, get_params) -> None:
    """Testing of converting binary images to microjson of objects polygon coordinates."""
    
    inp_dir = synthetic_images
    for file in Path(inp_dir).iterdir():
        model = ut.BinaryMicrojsonModel(
            out_dir=output_directory,
            file_path=file,
            polygon_type=get_params,
        )
        model.polygons_to_microjson()
    if get_params == "encoding":
        assert len(list(output_directory.rglob('*_encoding.json'))) == 5
    else:
        assert len(list(output_directory.rglob('*_rectangle.json'))) == 5

    clean_directories()

def test_MicrojsonBinaryModel(synthetic_images: Path, output_directory: Path, get_params:list[str]) -> None:
    """Testing of converting microjson of polygon coordinates of objects back to binary images."""
    
    inp_dir = synthetic_images
    for file in Path(inp_dir).iterdir():
        model = ut.BinaryMicrojsonModel(
            out_dir=output_directory,
            file_path=file,
            polygon_type=get_params,
        )
        model.polygons_to_microjson()

    for file in Path(output_directory).iterdir():
        model = ut.MicrojsonBinaryModel(
            out_dir=output_directory,
            file_path=file,
            polygon_type=get_params,
        )
        model.convert_microjson_to_binary()

    assert len(list(output_directory.rglob('*tif'))) == 5
    assert len(np.unique(sk.io.imread(list(output_directory.rglob('*tif'))[0]))) == 2
    clean_directories()

def XOR(x, y):
    return x ^ y

def test_roundtrip(synthetic_images: Path, output_directory: Path) -> None:
    """Testing of reconstructed images from polygon coordinates with original images."""
    
    inp_dir = synthetic_images
    for file in Path(inp_dir).iterdir():
        model = ut.BinaryMicrojsonModel(
            out_dir=output_directory,
            file_path=file,
            polygon_type="encoding",
        )
        model.polygons_to_microjson()

    for file in Path(output_directory).iterdir():
        model = ut.MicrojsonBinaryModel(
            out_dir=output_directory,
            file_path=file,
            polygon_type="encoding",
        )
        model.convert_microjson_to_binary()

    for inp, rec in zip(inp_dir.iterdir(), output_directory.iterdir()):
        if inp.name == rec.name:
            inpimage = sk.io.imread(inp)
            inpimage = inpimage.astype(np.uint8)
            recimage = sk.io.imread(rec)
            ## Testing bitwise operation and return 1 if the two array are unique while 0 if they are similar
            byt_test = XOR(inpimage, recimage)
            assert np.unique(byt_test)[0]== 0

    clean_directories()