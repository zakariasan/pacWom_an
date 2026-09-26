import pygame

from .character import Character
from .directions import Direction
from ..game.maze import Maze_gen


def next_step(grid: list[list[int]], start: tuple[int, int],
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
    def __init__(self, maze: Maze_gen, x: int, y: int, color: str) -> None:
        super().__init__(maze, x, y, color)
        self.goal = (x, y)
        self.speed = 1.8

    def update(self, dt: float) -> None:
        """Follow the shortest path to goal, without turning back."""
        if (self.x, self.y) == self.target:
            back = next(d for d in Direction
                        if d.dx == -self.direction.dx
                        and d.dy == -self.direction.dy)
            d = next_step(self.maze.grid, self.target, self.goal, back)
            if d is None:
                d = next_step(self.maze.grid, self.target, self.goal)
            if d is not None:
                self.direction = d
        super().update(dt)

    def draw(self, screen: pygame.Surface, origin: tuple[int, int]) -> None:
        """A circle on top of a rectangle: a simple ghost shape."""
        cx, cy = self.center(origin)
        r = self.maze.cell_size // 3
        pygame.draw.circle(screen, self.color, (cx, cy), r)
        pygame.draw.rect(screen, self.color, (cx - r, cy, 2 * r, r))

    def choose_goal(self, pacman: Character) -> tuple[int, int]:
        """Default behavior: chase Pac-Man directly."""
        return (round(pacman.x), round(pacman.y))

    def _valid(self, x: float, y: float,
               pacman: Character) -> tuple[int, int]:
        """Clamp a goal into the maze; fall back to Pac-Man if closed."""
        rows, cols = len(self.maze.grid), len(self.maze.grid[0])
        cx = min(max(round(x), 0), cols - 1)
        cy = min(max(round(y), 0), rows - 1)
        if self.maze.grid[cy][cx] == 15:
            return (round(pacman.x), round(pacman.y))
        return (cx, cy)


class Blinky(Ghost):
    def __init__(self, maze: Maze_gen, x: int, y: int, color: str) -> None:
        super().__init__(maze, x, y, color)
        self.goal = (x, y)
        self.speed = 2.2


class Pinky(Ghost):
    def choose_goal(self, pacman: Character) -> tuple[int, int]:
        d = pacman.direction
        return self._valid(pacman.x + 4 * d.dx, pacman.y + 4 * d.dy, pacman)


class Inky(Ghost):
    def __init__(self, maze: Maze_gen, x: int, y: int, color: str,
                 blinky: Ghost) -> None:
        super().__init__(maze, x, y, color)
        self.blinky = blinky

    def choose_goal(self, pacman: Character) -> tuple[int, int]:
        d = pacman.direction
        ax, ay = pacman.x + 2 * d.dx, pacman.y + 2 * d.dy
        return self._valid(2 * ax - self.blinky.x,
                           2 * ay - self.blinky.y, pacman)


class Clyde(Ghost):
    def choose_goal(self, pacman: Character) -> tuple[int, int]:
        dist = abs(self.x - pacman.x) + abs(self.y - pacman.y)
        if dist > 8:
            return (round(pacman.x), round(pacman.y))
        return self.start
