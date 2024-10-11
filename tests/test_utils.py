"""Test fixtures.

Set up all data used in tests.
"""
import shutil
import tempfile
from pathlib import Path
from typing import Union
import numpy as np
from pydantic import ValidationError
import pytest
import skimage as sk
HAS_BFIO = False
try:
    import bfio
    HAS_BFIO = True
except ImportError:
    pass


# Marker registration
def pytest_configure(config):  # Function to register marker
    config.addinivalue_line("markers", "requires_extra(name): mark test as needing an extra")


@pytest.fixture(autouse=True)
def skip_if_extra_not_installed(request):
    marker = request.node.get_closest_marker("requires_extra")
    if marker:
        extra_name = marker.args[0]
        try:
            __import__(extra_name)
        except ImportError:
            pytest.skip(f"Skipping test because '{extra_name}' extra is not installed.")


@pytest.fixture()
def inp_dir() -> Union[str, Path]:
    """Create directory for saving intensity images."""
    return Path(tempfile.mkdtemp(dir=Path.cwd()))

@pytest.fixture()
def output_directory() -> Union[str, Path]:
    """Create output directory."""
    output_dir = Path(tempfile.mkdtemp(dir=Path.cwd()))
    yield output_dir
    shutil.rmtree(output_dir)


@pytest.fixture(params=[512, 1024, 2048])
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
    yield inp_dir
    shutil.rmtree(inp_dir)


@pytest.fixture(params=["rectangle", "encoding"])
def get_params(request: pytest.FixtureRequest) -> pytest.FixtureRequest:
    """To get the parameter of the ome to json."""
    return request.param

@pytest.mark.skipif(
        not HAS_BFIO,
        reason="Skipping test because 'bfio' extra is not installed.")
def test_OmeMicrojsonModel(synthetic_images: Path, output_directory: Path, get_params) -> None:
    from microjson.utils import OmeMicrojsonModel
    """Testing of converting binary images to microjson of objects polygon
    coordinates."""
    
    inp_dir = synthetic_images
    for file in Path(inp_dir).iterdir():
        try:
            model = OmeMicrojsonModel(
                out_dir=output_directory,
                file_path=file,
                polygon_type=get_params,
            )
            model.write_single_json()
        except Exception as e:
            print(e)

    if get_params == "encoding":
        assert len(list(output_directory.rglob('*encoding*.json'))) == 5
    else:
        assert len(list(output_directory.rglob('*rectangle*.json'))) == 5


@pytest.mark.skipif(not HAS_BFIO, reason="Skipping test because 'bfio' extra is not installed.")
def test_MicrojsonBinaryModel(synthetic_images: Path, output_directory: Path, get_params:list[str]) -> None:
    from microjson.utils import OmeMicrojsonModel, MicrojsonBinaryModel
    """Testing of converting microjson of polygon coordinates of objects back to binary images."""
    
    inp_dir = synthetic_images
    for file in Path(inp_dir).iterdir():
        model = OmeMicrojsonModel(
            out_dir=output_directory,
            file_path=file,
            polygon_type=get_params,
        )
        model.write_single_json()

    for file in Path(output_directory).iterdir():
        model = MicrojsonBinaryModel(
            out_dir=output_directory,
            file_path=file
        )
        model.microjson_to_binary()

    assert len(list(output_directory.rglob('*tif'))) == 5
    assert len(np.unique(sk.io.imread(list(output_directory.rglob('*tif'))[0]))) == 2


def XOR(x, y):
    return x ^ y

@pytest.mark.skipif(not HAS_BFIO, reason="Skipping test because 'bfio' extra is not installed.")
def test_roundtrip(synthetic_images: Path, output_directory: Path) -> None:
    from microjson.utils import OmeMicrojsonModel, MicrojsonBinaryModel
    """Testing of reconstructed images from polygon coordinates with original images."""
    
    inp_dir = synthetic_images
    for file in Path(inp_dir).iterdir():
        model = OmeMicrojsonModel(
            out_dir=output_directory,
            file_path=file,
            polygon_type="encoding",
        )
        model.write_single_json()

    for file in Path(output_directory).iterdir():
        model = MicrojsonBinaryModel(
            out_dir=output_directory,
            file_path=file,
        )
        model.microjson_to_binary()

    for inp, rec in zip(inp_dir.iterdir(), output_directory.iterdir()):
        if inp.name == rec.name:
            inpimage = sk.io.imread(inp)
            inpimage = inpimage.astype(np.uint8)
            recimage = sk.io.imread(rec)
            ## Testing bitwise operation and return 1 if the two array are unique while 0 if they are similar
            byt_test = XOR(inpimage, recimage)
            assert np.unique(byt_test)[0]== 0
