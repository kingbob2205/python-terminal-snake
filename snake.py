"""Curses front end for the Snake engine."""

from __future__ import annotations

import curses
import time

from engine import DOWN, LEFT, RIGHT, UP, SnakeGame

WIDTH = 38
HEIGHT = 14


def draw(screen: curses.window, game: SnakeGame, paused: bool) -> None:
    screen.erase()
    screen.addstr(0, 0, f" SNAKE  Score: {game.score}  |  Arrows/WASD move ")
    screen.addstr(1, 0, "+" + "-" * WIDTH + "+")
    for y in range(HEIGHT):
        screen.addstr(y + 2, 0, "|" + " " * WIDTH + "|")
    screen.addstr(HEIGHT + 2, 0, "+" + "-" * WIDTH + "+")
    if game.food is not None:
        x, y = game.food
        screen.addch(y + 2, x + 1, "*")
    for index, (x, y) in enumerate(game.snake):
        screen.addch(y + 2, x + 1, "@" if index == 0 else "o")
    if game.over:
        message = "You win!" if game.won else "Game over!"
        screen.addstr(HEIGHT + 3, 0, f" {message} Press R to restart or Q to quit.")
    elif paused:
        screen.addstr(HEIGHT + 3, 0, " Paused. Press P to resume, Q to quit.")
    else:
        screen.addstr(HEIGHT + 3, 0, " P pause | Q quit")
    screen.refresh()


def run(screen: curses.window) -> None:
    curses.curs_set(0)
    screen.keypad(True)
    screen.nodelay(True)
    game = SnakeGame(WIDTH, HEIGHT)
    paused = False
    last_tick = time.monotonic()
    keys = {
        curses.KEY_UP: UP, curses.KEY_DOWN: DOWN,
        curses.KEY_LEFT: LEFT, curses.KEY_RIGHT: RIGHT,
        ord("w"): UP, ord("s"): DOWN, ord("a"): LEFT, ord("d"): RIGHT,
    }
    while True:
        rows, cols = screen.getmaxyx()
        if rows < HEIGHT + 4 or cols < WIDTH + 2:
            screen.erase()
            screen.addstr(0, 0, "Resize terminal to at least 40x18. Q quits.")
            screen.refresh()
            if screen.getch() in (ord("q"), ord("Q")):
                break
            time.sleep(0.05)
            continue
        key = screen.getch()
        if key in (ord("q"), ord("Q")):
            break
        if key in (ord("p"), ord("P")) and not game.over:
            paused = not paused
            last_tick = time.monotonic()
        if key in (ord("r"), ord("R")) and game.over:
            game.restart()
            paused = False
            last_tick = time.monotonic()
        if key in keys and not paused and not game.over:
            game.turn(keys[key])
        delay = max(0.075, 0.18 - game.score * 0.005)
        now = time.monotonic()
        if not paused and not game.over and now - last_tick >= delay:
            game.tick()
            last_tick = now
        draw(screen, game, paused)
        time.sleep(0.015)


if __name__ == "__main__":
    try:
        curses.wrapper(run)
    except KeyboardInterrupt:
        pass
