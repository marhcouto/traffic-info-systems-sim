import math
import pytest

from src.position import Position

#!
# \brief Tests the Position.dist method.
@pytest.mark.parametrize(
        ("p1", "p2", "expected"),
        [
            (Position(0, 0), Position(0, 0), 0.0),
            (Position(0, 0), Position(1, 0), 1.0),
            (Position(0, 0), Position(0, 1), 1.0),
            (Position(0, 0), Position(1, 1), math.sqrt(2.0)),
            (Position(0, 0), Position(3, 4), 5.0),
            (Position(1, 2), Position(2, 3), math.sqrt(2.0)),
            (Position(3, 1), Position(2, 4), math.sqrt(10.0)),
            (Position(-2, 4), Position(-2, -4), 8.0),
            (Position(-3, 5), Position(1, 4), math.sqrt(17.0))
        ]
)
def test_position_dist(p1, p2, expected):
    assert p1.dist(p2) == expected