from .character import Character
from .directions import Direction
from ..game.maze import Maze_gen
import pygame


class Pacman(Character):
    def __init__(self, maze: Maze_gen, x: int, y: int) -> None:
        super().__init__(maze, x, y, color='yellow')
        self.next_direction: Direction | None = None
        self.mouth_open = False
        self.mouth_time = 0.00

    def update(self, dt: float) -> None:
        """Turn to the remembered direction as soon as it's open."""
        on_center = (self.x, self.y) == self.target
        if on_center and self.next_direction is not None:
            if self.can_move(self.next_direction):
                self.direction = self.next_direction
                self.next_direction = None
        super().update(dt)

        if (self.x, self.y) != self.target:
            self.mouth_time += dt
            if self.mouth_time >= 0.1:
                self.mouth_open = not self.mouth_open
                self.mouth_time = 0.0

    def draw(self, screen: pygame.Surface, origin: tuple[int, int]) -> None:
        cx, cy = self.center(origin)
        r = self.maze.cell_size // 3
        pygame.draw.circle(screen, self.color, (cx, cy), r)

        if self.mouth_open:
            dx, dy = self.direction.dx, self.direction.dy
            p1 = (cx + r * (dx - dy), cy + r * (dy + dx))
            p2 = (cx + r * (dx + dy), cy + r * (dy - dx))
            pygame.draw.polygon(screen, "black", [(cx, cy), p1, p2]) 
