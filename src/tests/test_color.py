from raytracer.image import Color


def test_color():
    assert Color(1, 2, 3) * 2 == Color(2, 4, 6)
