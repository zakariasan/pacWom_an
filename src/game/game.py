import pygame
import sys
from .maze import Maze_gen
from ..graphic.pacman import Pacman
from ..graphic.ghosts import Ghost
from ..graphic.directions import Direction
from ..graphic.pacgums import Pacgums
from ..graphic.ghosts import Blinky, Clyde, Inky, Pinky

KEYS = {
    pygame.K_UP: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
}
GAP = 100


class Game:
    def __init__(self, config):
        """Luching the game form here"""
        self.config = config
        self.dt = 0
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("PacWooMAn")
        self.clock = pygame.time.Clock()
        sw, sh = self.screen.get_size()
        self.sw = sw
        self.sh = sh
        cell = min((sw - 2 * GAP)
            // config.width, (sh - 2 * GAP) // config.height)
        self.maze = Maze_gen(self.config, cell_size=cell)
        self.maze_pos = self.maze.surface.get_rect(
                center=self.screen.get_rect().center).topleft
        mid_x = len(self.maze.grid[0]) // 2
        mid_y = len(self.maze.grid) // 2
        if self.maze.grid[mid_x][mid_y] == 15:
            mid_x -= 1
        self.pacman = Pacman(self.maze, mid_x, mid_y)
        # self.pacman = Pacman(self.maze, cell[0], cell[1])

        self.gums = Pacgums(self.maze, self.config, (mid_x, mid_y))

        self.score = 0
        self.lives = self.config.lives
        self.lvl = 0
        self.time = self.config.level_max_time

        self.font = pygame.font.SysFont(None, 40)

        cols, rows = len(self.maze.grid[0]), len(self.maze.grid)
        cols, rows = len(self.maze.grid[0]), len(self.maze.grid)
        cols, rows = len(self.maze.grid[0]), len(self.maze.grid)
        self.ghosts = [
            Blinky(self.maze, 0, 0, "red"),
            Pinky(self.maze, cols - 1, 0, "pink"),
            Inky(self.maze, 0, rows - 1, "cyan"),
            Clyde(self.maze, cols - 1, rows - 1, "orange"),
            ]

    def _text(self, text: str, pos: tuple[int, int]) -> None:
        """Draw text centered at pos."""
        img = self.font.render(text, True, "white")
        self.screen.blit(img, img.get_rect(center=pos))

    def _handle_events(self):
        """Print in a nice way"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.running = False
                    print('Exit -_-')
                    sys.exit(0)
                elif event.key == pygame.K_SPACE:
                    print("Space bar pressed!")
                elif event.type == pygame.KEYDOWN and event.key in KEYS:
                    self.pacman.next_direction = KEYS[event.key]

    def _draw(self):
        """draw the game"""
        self.screen.fill("black")
        gap = 10
        w, y = self.screen.get_size()
        rect = pygame.Rect(gap, gap, w - gap * 2, y - gap * 2)
        pygame.draw.rect(self.screen, "blue", rect, width=3, border_radius=6)
        self.maze.draw(self.screen, self.maze_pos)
        self.gums.draw(self.screen, self.maze_pos)
        self.pacman.draw(self.screen, self.maze_pos)
        for ghost in self.ghosts:
            ghost.draw(self.screen, self.maze_pos)

        self._text(f"SCORES: {self.score}", (GAP + 50, 50))
        self._text(f"lives: {self.lives}", (self.sw - GAP, 50))
        self._text(f"LEVEL: {self.lvl}", (GAP + 500, 50))
        self._text(f"Time: {self.time:2f}", (GAP + 1000, 50))

    def run(self):
        """Runing the game Engine"""
        while self.running:
            # pygame.draw.rect(screen, RED, (100, 150, 200, 99))
            self.dt = self.clock.tick(60) / 1000.0
            self._handle_events()

            self.pacman.update(self.dt)
            pac_cell = (round(self.pacman.x), round(self.pacman.y))
            for ghost in self.ghosts:
                ghost.goal = ghost.choose_goal(self.pacman)
                ghost.update(self.dt)

            self.score += self.gums.eat(self.pacman.x, self.pacman.y)
            self.time -= self.dt
            if self.time <= 0:
                self.time = 0
            self._draw()
            pygame.display.flip()

        pygame.quit()
