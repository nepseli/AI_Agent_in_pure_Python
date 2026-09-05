"""Utility functions for the Snake game."""
import random
from typing import List, Tuple

from .constants import GRID_WIDTH, GRID_HEIGHT

Position = Tuple[int, int]


def random_food_position(snake: List[Position]) -> Position:
    """Return a random grid position not occupied by the snake."""
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos
