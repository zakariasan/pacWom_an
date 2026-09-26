import random
from ..game.maze import Maze_gen
from ..parser.load_config import Config
import pygame


class Pacgums:
    def __init__(self, maze: Maze_gen, config: Config,
                 start: tuple[int, int]) -> None:
        self.maze = maze
        seed = config.seed
        count = config.pacgum
        self.config = config
        rows, cols = len(maze.grid), len(maze.grid[0])

        cells = [(x, y) for y in range(rows) for x in range(cols)
                 if maze.grid[y][x] != 15 and (x, y) != start]

        rng = random.Random(seed)
        self.gums = set(rng.sample(cells, min(count, len(cells))))

        corners = [(0, 0), (cols - 1, 0), (0, rows - 1),
                   (cols - 1, rows - 1)]
        self.gums.update(corners)
        self.supers = {c for c in corners if c in self.gums}

    def eat(self, x: float, y: float) -> int:
        """Remove the gum at Pac-Man's cell; return its points."""
        cell = (round(x), round(y))
        if cell not in self.gums:
            return 0
        self.gums.remove(cell)
        if cell in self.supers:
            self.supers.remove(cell)
            return self.config.points_per_super_pacgum
        return self.config.points_per_pacgum

    def draw(self, screen: pygame.Surface, origin: tuple[int, int]) -> None:
        """ draw the gums in the era of pacman """
        cs, half = self.maze.cell_size, self.maze.stroke // 2
        for x, y in self.gums:
            cx = origin[0] + half + x * cs + cs // 2
            cy = origin[1] + half + y * cs + cs // 2
            r = cs // 4 if (x, y) in self.supers else cs // 10
            pygame.draw.circle(screen, "peachpuff", (cx, cy), r)

