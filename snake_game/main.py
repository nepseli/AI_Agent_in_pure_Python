"""
Simple Snake Game using pygame

Controls:
- Arrow keys or WASD to move
- R to restart after game over
- Q or ESC to quit

Install pygame: pip install pygame
Run: python main.py
"""

import random
import sys

try:
    import pygame
except ImportError:
    print("pygame not installed. Install with: pip install pygame")
    sys.exit(1)

# Configuration
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
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


def random_food_position(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 36)
        self.large_font = pygame.font.SysFont(None, 72)

        self.reset()

    def reset(self):
        mid_x = GRID_WIDTH // 2
        mid_y = GRID_HEIGHT // 2
        self.snake = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        self.direction = (1, 0)  # moving right
        self.next_direction = self.direction
        self.food = random_food_position(self.snake)
        self.score = 0
        self.game_over = False
        self.fps = FPS_START

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.set_direction((0, -1))
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.set_direction((0, 1))
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.set_direction((-1, 0))
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.set_direction((1, 0))
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit(0)

    def set_direction(self, new_dir):
        # Prevent reversing direction directly
        if (new_dir[0] == -self.direction[0] and new_dir[1] == -self.direction[1]):
            return
        self.next_direction = new_dir

    def update(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check collisions with walls
        x, y = new_head
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            self.game_over = True
            return

        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.score += 1
            # spawn new food
            self.food = random_food_position(self.snake)
            # Increase speed occasionally
            if self.score % FPS_INCREASE_EVERY == 0:
                self.fps += FPS_INCREASE_BY
        else:
            # remove tail
            self.snake.pop()

    def draw_cell(self, pos, color):
        x, y = pos
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def render(self):
        self.screen.fill(BLACK)

        # draw grid (optional subtle)
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))

        # draw food
        self.draw_cell(self.food, RED)

        # draw snake
        for i, segment in enumerate(self.snake):
            color = DARK_GREEN if i == 0 else GREEN
            self.draw_cell(segment, color)

        # draw score
        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (10, 10))

        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            go_text = self.large_font.render("Game Over", True, RED)
            go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(go_text, go_rect)

            info = self.font.render(f"Score: {self.score}    Press R to restart or Q to quit", True, WHITE)
            info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(info, info_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    Game().run()
