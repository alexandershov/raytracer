import pytest

from raytracer.interval import Interval


@pytest.mark.parametrize(
    "interval, value, expected",
    [
        (Interval(min=0), 5, True),
        (Interval(min=0), 0, True),
        (Interval(min=0), -1, False),
    ],
)
def test_contains(interval, value, expected):
    assert (value in interval) is expected
