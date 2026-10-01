# Terminal Snake in Python

A complete, dependency-free Snake game for a terminal. The implementation separates game rules from rendering so the rules can be tested without opening a terminal UI.

## Run

```sh
python3 snake.py
```

Use arrow keys or WASD to steer. Press `p` to pause, `r` after game over to restart, and `q` to quit. Eat `*` to grow and score. Hitting a wall or your body ends the round. The game speeds up gradually as your score rises.

Run tests:

```sh
python3 -m unittest discover -s tests -v
```

Works in a terminal with Python 3.10+ and the standard-library `curses` module (macOS/Linux). Windows users can install `windows-curses` first. The game requires a terminal at least 40 columns by 18 rows. No account, cloud resource, or paid dependency is needed.

## Design

- `engine.py` contains movement, direction rules, food placement, score, collisions, and restart logic.
- `snake.py` owns terminal input, timing, and drawing.
- `tests/test_engine.py` checks the behavior of the engine, including an edge case where moving into the previous tail position is allowed if the tail vacates that cell.

This is a newly written portfolio implementation; it is not a recovered historical project or a CS50 submission.
