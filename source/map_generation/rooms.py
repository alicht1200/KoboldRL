from __future__ import annotations
from typing import Tuple, Iterator

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    @property
    def center(self) -> Tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return center_x, center_y

    @property
    def center_column(self)-> Tuple[int, slice]:
        return (self.x1 + self.x2) // 2, slice(self.y1 + 1, self.y2)

    @property
    def center_row(self) -> Tuple[slice, int]:
        return slice(self.x1 + 1, self.x2), (self.y1 + self.y2) // 2

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

    @property
    def center_column_iterator(self) -> Iterator[Tuple[int, int]]:
        for y in range(self.y1 + 1, self.y2):
            yield (self.x1 + self.x2) // 2, y

    @property
    def center_row_iterator(self) -> Iterator[Tuple[int, int]]:
        for x in range(self.x1 + 1, self.x2):
            yield x, (self.y1 + self.y2) // 2

    @property
    def perimeter_iterator(self) -> Iterator[Tuple[int, int]]:
        north = [(x, self.y1) for x in range(self.x1, self.x2+1)]
        south = [(x, self.y2) for x in range(self.x1, self.x2 + 1)]
        east = [(self.x1, y) for y in range(self.y1, self.y2+1)]
        west = [(self.x2, y) for y in range(self.y1, self.y2 + 1)]
        perimeter = north + south + east + west
        for tile in perimeter:
            yield tile
