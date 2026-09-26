from .directions import Direction
from ..game.maze import Maze_gen
import pygame

MOVES = {
        Direction.UP: (0, -1, 1),
        Direction.RIGHT: (1, 0, 2),
        Direction.DOWN: (0, 1, 4),
        Direction.LEFT: (-1, 0, 8),
        }


def approach(value: float, target: int, step: float) -> float:
    if abs(target - value) <= step:
        return float(target)
    return value + step if target > value else value - step


class Character:
    def __init__(self, maze: Maze_gen, x: int, y: int, color: str) -> None:
        self.maze = maze
        self.x, self.y = float(x), float(y)
        self.target = (x, y)
        self.start = (x, y)

        self.color = color
        self.direction = Direction.RIGHT
        self.speed = 4

    def can_move(self, direction: Direction) -> bool:
        tx, ty = self.target
        return not self.maze.grid[ty][tx] & MOVES[direction][2]

    def update(self, dt: float) -> None:
        if (self.x, self.y) == self.target:
            if not self.can_move(self.direction):
                return
            dx, dy, _ = MOVES[self.direction]
            self.target = (self.target[0] + dx, self.target[1] + dy)

        step = self.speed * dt
        self.x = approach(self.x, self.target[0], step)
        self.y = approach(self.y, self.target[1], step)

    def draw(self, screen: pygame.Surface, origin: tuple[int, int]) -> None:
        cs = self.maze.cell_size
        half = self.maze.stroke // 2
        cx = origin[0] + half + int((self.x + 0.5) * cs)
        cy = origin[1] + half + int((self.y + 0.5) * cs)
        pygame.draw.circle(screen, self.color, (cx, cy), cs // 3)
    
    def center(self, origin: tuple[int, int]) -> tuple[int, int]:
        cs = self.maze.cell_size
        half = self.maze.stroke // 2
        return (origin[0] + half + int((self.x + 0.5) * cs),
                origin[1] + half + int((self.y + 0.5) * cs))
