"""Pure game state and rules for terminal Snake."""

from __future__ import annotations

from dataclasses import dataclass, field
from random import Random

Point = tuple[int, int]
UP: Point = (0, -1)
DOWN: Point = (0, 1)
LEFT: Point = (-1, 0)
RIGHT: Point = (1, 0)


@dataclass
class SnakeGame:
    width: int = 38
    height: int = 14
    random: Random = field(default_factory=Random, repr=False)
    snake: list[Point] = field(init=False)
    direction: Point = field(init=False, default=RIGHT)
    food: Point | None = field(init=False, default=None)
    score: int = field(init=False, default=0)
    over: bool = field(init=False, default=False)
    won: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        if self.width < 6 or self.height < 4:
            raise ValueError("Board must be at least 6 by 4")
        self.restart()

    def restart(self) -> None:
        x, y = self.width // 2, self.height // 2
        self.snake = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = RIGHT
        self.score = 0
        self.over = False
        self.won = False
        self.food = self._new_food()

    def turn(self, direction: Point) -> None:
        if direction not in (UP, DOWN, LEFT, RIGHT):
            raise ValueError("Unknown direction")
        if direction != (-self.direction[0], -self.direction[1]):
            self.direction = direction

    def _new_food(self) -> Point | None:
        occupied = set(self.snake)
        free = [(x, y) for y in range(self.height) for x in range(self.width)
                if (x, y) not in occupied]
        return self.random.choice(free) if free else None

    def tick(self) -> None:
        if self.over:
            return
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        eating = new_head == self.food
        x, y = new_head
        if not (0 <= x < self.width and 0 <= y < self.height):
            self.over = True
            return
        # The tail moves away unless this tick grows the snake.
        body = self.snake if eating else self.snake[:-1]
        if new_head in body:
            self.over = True
            return
        self.snake.insert(0, new_head)
        if eating:
            self.score += 1
            self.food = self._new_food()
            if self.food is None:
                self.over = True
                self.won = True
        else:
            self.snake.pop()
