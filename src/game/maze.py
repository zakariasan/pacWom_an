from mazegenerator import MazeGenerator
import pygame
from ..parser.load_config import Config


class Maze_gen:
    def __init__(self, config: Config, cell_size: int = 40, stroke:int = 4, color:str  = 'gray') -> None:
        """Get data from the game to draw"""
        maze_gen = MazeGenerator(
                    size=(config.width, config.height),
                    perfect=config.perfect,
                    seed=config.seed
                    )
        self.grid: list[list[int]] = maze_gen.maze
        self.cell_size = cell_size
        self.color = color
        self.stroke = stroke
        self.surface = self._render()

    def _render(self) -> pygame.Surface:
        """Draw wall of the maze"""
        cs , st = self.cell_size, self.stroke
        rows, cols = len(self.grid), len(self.grid[0])
        surf = pygame.Surface((cols * cs + st, rows * cs + st), pygame.SRCALPHA)

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                left, top = x * cs, y *cs

                if cell & 1:
                    self._wall(surf, left, top, cs + st, st)
                if cell & 4:
                    self._wall(surf, left, top + cs, cs+ st, st)
                if cell & 8:
                    self._wall(surf, left, top, st, cs + st)
                if cell & 2:
                    self._wall(surf, left+ cs, top, st, cs + st)

        return surf

    def _wall(self, surface, x, y, w, h):
        pygame.draw.rect(surface, self.color, (x, y, w, h))

    def draw(self, target, pos):
        target.blit(self.surface, pos)
