import random

import pygame

from .character import Character
from .directions import Direction
from ..game.maze import Maze_gen

OPPOSITE = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


def path_to(grid: list[list[int]], start: tuple[int, int],
            goal: tuple[int, int],
            avoid: Direction | None = None) -> Direction | None:
    """First direction on the shortest path, never starting with avoid."""
    queue = [start]
    first: dict[tuple[int, int], Direction | None] = {start: None}
    while queue:
        x, y = queue.pop(0)
        if (x, y) == goal:
            return first[(x, y)]
        for d in Direction:
            if grid[y][x] & d.wall:
                continue
            if (x, y) == start and d == avoid:
                continue
            nxt = (x + d.dx, y + d.dy)
            if nxt not in first:
                first[nxt] = d if first[(x, y)] is None else first[(x, y)]
                queue.append(nxt)
    return None


class Ghost(Character):
    """Moves toward its goal; each subclass picks a different goal."""

    def __init__(self, maze: Maze_gen, x: int, y: int, color: str) -> None:
        super().__init__(maze, x, y, color)
        self.goal = (x, y)
        self.speed = 2.5

    def choose_goal(self, pacman: Character) -> tuple[int, int]:
        """Default: Pac-Man's cell."""
        return (round(pacman.x), round(pacman.y))

    def update(self, dt: float) -> None:
        """On each cell center, pick a direction; then move."""
        if (self.x, self.y) == self.target:
            back = OPPOSITE[self.direction]
            d = path_to(self.maze.grid, self.target, self.goal, back)
            if d is None:                       # no path: wander
                options = [o for o in Direction
                           if self.can_move(o) and o != back]
                d = random.choice(options or [back])
            self.direction = d
        super().update(dt)

    def draw(self, screen: pygame.Surface, origin: tuple[int, int]) -> None:
        """A circle on top of a rectangle: a simple ghost shape."""
        cx, cy = self.center(origin)
        r = self.maze.cell_size // 3
        pygame.draw.circle(screen, self.color, (cx, cy), r)
        pygame.draw.rect(screen, self.color, (cx - r, cy, 2 * r, r))


class Blinky(Ghost):
    """Red: chases Pac-Man directly (default goal)."""


class Pinky(Ghost):
    """Pink: aims up to 4 cells in front of Pac-Man."""

    def choose_goal(self, pacman: Character) -> tuple[int, int]:
        x, y = round(pacman.x), round(pacman.y)
        d = pacman.direction
        for _ in range(4):
            if self.maze.grid[y][x] & d.wall:
                break
            x, y = x + d.dx, y + d.dy
        return (x, y)


class Inky(Ghost):
    """Cyan: wanders randomly."""
    def choose_goal(self, pacman: Character) -> tuple[int, int]:
        dist = abs(self.x - pacman.x) + abs(self.y - pacman.y)
        if dist > 2:
            return (round(pacman.x), round(pacman.y))
        return self.start


class Clyde(Ghost):
    """Orange: chases when far, goes home when close."""

    def choose_goal(self, pacman: Character) -> tuple[int, int]:
        dist = abs(self.x - pacman.x) + abs(self.y - pacman.y)
        if dist > 8:
            return (round(pacman.x), round(pacman.y))
        return self.start
