from enum import Enum


class Direction(Enum):
    UP = (0, -1, 1)
    RIGHT = (1, 0, 2)
    DOWN = (0, 1, 4)
    LEFT = (-1, 0, 8)

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    @property
    def wall(self) -> int:
        return self.value[2]
