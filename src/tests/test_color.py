import pytest

from raytracer.image import Color


@pytest.mark.parametrize(
    "color, mul, expected",
    [(Color(1, 2, 3), 2, Color(2, 4, 6)), (Color(1, 2, 3), 200, Color(200, 255, 255)),],
)
def test_color_mul(color, mul, expected):
    assert color * mul == expected


@pytest.mark.parametrize("r, g, b", [(256, 255, 255), (255, -1, 255),])
def test_color_creation_failure(r, g, b):
    with pytest.raises(ValueError):
        Color(r, g, b)
