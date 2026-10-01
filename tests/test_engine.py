import unittest
from random import Random

from engine import DOWN, LEFT, RIGHT, UP, SnakeGame


class SnakeGameTests(unittest.TestCase):
    def setUp(self):
        self.game = SnakeGame(8, 6, Random(7))

    def test_food_never_starts_on_snake(self):
        self.assertNotIn(self.game.food, self.game.snake)

    def test_moves_without_growth(self):
        self.game.food = (0, 0)
        original_length = len(self.game.snake)
        self.game.tick()
        self.assertEqual(self.game.snake[0], (5, 3))
        self.assertEqual(len(self.game.snake), original_length)

    def test_food_grows_and_scores(self):
        self.game.food = (5, 3)
        self.game.tick()
        self.assertEqual(self.game.score, 1)
        self.assertEqual(len(self.game.snake), 4)
        self.assertNotIn(self.game.food, self.game.snake)

    def test_reversal_is_ignored(self):
        self.game.turn(LEFT)
        self.assertEqual(self.game.direction, RIGHT)

    def test_wall_ends_round(self):
        self.game.snake = [(7, 3), (6, 3), (5, 3)]
        self.game.tick()
        self.assertTrue(self.game.over)

    def test_body_collision_ends_round(self):
        self.game.snake = [(3, 3), (3, 4), (4, 4), (4, 3), (5, 3)]
        self.game.food = (0, 0)
        self.game.tick()
        self.assertTrue(self.game.over)

    def test_vacating_tail_is_safe(self):
        self.game.snake = [(3, 3), (3, 4), (4, 4), (4, 3)]
        self.game.food = (0, 0)
        self.game.tick()
        self.assertFalse(self.game.over)
        self.assertEqual(self.game.snake[0], (4, 3))

    def test_restart_resets_state(self):
        self.game.over = True
        self.game.score = 9
        self.game.restart()
        self.assertFalse(self.game.over)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.snake), 3)


if __name__ == "__main__":
    unittest.main()
