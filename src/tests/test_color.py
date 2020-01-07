import pytest

from raytracer.image import Color


def test_color_mul():
    assert Color(1, 2, 3) * 2 == Color(2, 4, 6)
    assert Color(1, 2, 3) * 200 == Color(200, 255, 255)


@pytest.mark.parametrize('r, g, b', [
    (256, 255, 255),
])
def test_color_creation_failure(r, g, b):
    with pytest.raises(ValueError):
        Color(r, g, b)
