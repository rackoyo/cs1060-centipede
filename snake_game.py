import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Initialize font
pygame.font.init()
game_font = pygame.font.SysFont('Arial', 36)

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = (1, 0)  # Start moving right
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (
            (head[0] + self.direction[0]) % GRID_COUNT,
            (head[1] + self.direction[1]) % GRID_COUNT
        )
        
        if new_head in self.body:
            return False  # Game over - snake hit itself
            
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

def spawn_food():
    while True:
        food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
        if food not in snake.body:
            return food

def show_game_over_screen(score, high_score):
    screen.fill(BLACK)
    
    # Game Over text
    game_over_text = game_font.render('GAME OVER', True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//3))
    screen.blit(game_over_text, game_over_rect)
    
    # Score text
    score_text = game_font.render(f'Score: {score}', True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
    screen.blit(score_text, score_rect)
    
    # High Score text
    high_score_text = game_font.render(f'High Score: {high_score}', True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 + 50))
    screen.blit(high_score_text, high_score_rect)
    
    # Play Again text
    play_again_text = game_font.render('Press SPACE to Play Again', True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 + 120))
    screen.blit(play_again_text, play_again_rect)
    
    pygame.display.flip()

# Game setup
snake = Snake()
food = spawn_food()
score = 0
high_score = 0
game_active = True

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_active:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
            else:
                if event.key == pygame.K_SPACE:
                    # Reset game
                    snake.reset()
                    food = spawn_food()
                    score = 0
                    game_active = True

    if game_active:
        # Move snake
        if not snake.move():
            game_active = False
            high_score = max(score, high_score)
            continue

        # Check for food collision
        if snake.body[0] == food:
            snake.grow = True
            food = spawn_food()
            score += 1

        # Drawing game screen
        screen.fill(BLACK)
        
        # Draw food
        pygame.draw.rect(screen, RED, (
            food[0] * GRID_SIZE,
            food[1] * GRID_SIZE,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        ))
        
        # Draw snake
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            ))

        # Draw current score
        score_text = game_font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        # Show game over screen
        show_game_over_screen(score, high_score)

    pygame.display.flip()
    clock.tick(10)  # Control game speed

pygame.quit()
sys.exit()
