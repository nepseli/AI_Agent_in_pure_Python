"""Configuration and constants for the Snake game."""

# Grid / screen
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# Game speed
FPS_START = 8
FPS_INCREASE_EVERY = 5  # increase fps every N points
FPS_INCREASE_BY = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (200, 30, 30)
GRAY = (40, 40, 40)
