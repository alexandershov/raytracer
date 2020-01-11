import filecmp
import os.path

import pytest

from raytracer import main


@pytest.mark.skip(reason="slow")
def test_scene():
    main.render()._image.save(_full_path("test.png"))
    assert filecmp.cmp(
        _full_path("test.png"), _full_path("raytracer.png"), shallow=False
    )
    os.unlink(_full_path("test.png"))


def _full_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)
