import pygame
import random
import sys
from enum import Enum
import time

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
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Initialize fonts
pygame.font.init()
game_font = pygame.font.SysFont('Arial', 36)
title_font = pygame.font.SysFont('Arial', 72)
menu_font = pygame.font.SysFont('Arial', 48)

class GameState(Enum):
    TITLE = 1
    PLAYING = 2
    GAME_OVER = 3

class PowerUpType(Enum):
    SPEED = 1  # Temporarily increases speed
    SLOW = 2   # Temporarily decreases speed
    GHOST = 3  # Allows passing through walls once
    SHRINK = 4 # Reduces snake length

class PowerUp:
    def __init__(self, position, type):
        self.position = position
        self.type = type
        self.spawn_time = time.time()
        self.duration = 5  # PowerUp disappears after 5 seconds

    def is_expired(self):
        return time.time() - self.spawn_time > self.duration

    def get_color(self):
        colors = {
            PowerUpType.SPEED: BLUE,
            PowerUpType.SLOW: YELLOW,
            PowerUpType.GHOST: PURPLE,
            PowerUpType.SHRINK: WHITE
        }
        return colors[self.type]

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = (1, 0)
        self.grow = False
        self.speed_multiplier = 1.0
        self.ghost_mode = False
        self.effects = {}  # Dictionary to store active power-up effects and their end times

    def move(self):
        head = self.body[0]
        new_head = (
            (head[0] + self.direction[0]) % GRID_COUNT,
            (head[1] + self.direction[1]) % GRID_COUNT
        )
        
        if not self.ghost_mode and new_head in self.body:
            return False

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def apply_power_up(self, power_up):
        effect_duration = 10  # Duration in seconds
        current_time = time.time()
        
        if power_up.type == PowerUpType.SPEED:
            self.speed_multiplier = 2.0
            self.effects['speed'] = current_time + effect_duration
        elif power_up.type == PowerUpType.SLOW:
            self.speed_multiplier = 0.5
            self.effects['speed'] = current_time + effect_duration
        elif power_up.type == PowerUpType.GHOST:
            self.ghost_mode = True
            self.effects['ghost'] = current_time + effect_duration
        elif power_up.type == PowerUpType.SHRINK:
            if len(self.body) > 1:
                self.body = self.body[:-3] if len(self.body) > 3 else self.body[:-1]

    def update_effects(self):
        current_time = time.time()
        for effect, end_time in list(self.effects.items()):
            if current_time > end_time:
                if effect == 'speed':
                    self.speed_multiplier = 1.0
                elif effect == 'ghost':
                    self.ghost_mode = False
                del self.effects[effect]

def spawn_food():
    while True:
        food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
        if food not in snake.body:
            return food

def spawn_power_up():
    if random.random() < 0.1:  # 10% chance to spawn a power-up
        while True:
            pos = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
            if pos not in snake.body:
                return PowerUp(pos, random.choice(list(PowerUpType)))
    return None

def show_title_screen():
    screen.fill(BLACK)
    
    # Title
    title_text = title_font.render('SNAKE GAME', True, GREEN)
    title_rect = title_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//4))
    screen.blit(title_text, title_rect)
    
    # Menu options
    start_text = menu_font.render('Press ENTER to Start', True, WHITE)
    start_rect = start_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
    screen.blit(start_text, start_rect)
    
    # Controls
    controls = [
        'Controls:',
        'Arrow Keys - Move Snake',
        'P - Pause Game',
        'ESC - Return to Title'
    ]
    
    y_offset = WINDOW_SIZE//2 + 100
    for control in controls:
        control_text = game_font.render(control, True, WHITE)
        control_rect = control_text.get_rect(center=(WINDOW_SIZE//2, y_offset))
        screen.blit(control_text, control_rect)
        y_offset += 40
    
    # Power-ups legend
    powerup_text = game_font.render('Power-ups:', True, WHITE)
    screen.blit(powerup_text, (50, WINDOW_SIZE - 150))
    
    powerups = [
        (BLUE, 'Speed Up'),
        (YELLOW, 'Slow Down'),
        (PURPLE, 'Ghost Mode'),
        (WHITE, 'Shrink')
    ]
    
    y_offset = WINDOW_SIZE - 100
    for color, description in powerups:
        pygame.draw.rect(screen, color, (50, y_offset, 20, 20))
        powerup_desc = game_font.render(description, True, WHITE)
        screen.blit(powerup_desc, (80, y_offset))
        y_offset += 30

def show_game_over_screen(score, high_score):
    screen.fill(BLACK)
    
    # Game Over text
    game_over_text = title_font.render('GAME OVER', True, RED)
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
    
    # Options
    space_text = game_font.render('Press SPACE to Play Again', True, WHITE)
    space_rect = space_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 + 120))
    screen.blit(space_text, space_rect)
    
    esc_text = game_font.render('Press ESC for Title Screen', True, WHITE)
    esc_rect = esc_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 + 170))
    screen.blit(esc_text, esc_rect)

# Game setup
snake = Snake()
food = spawn_food()
power_up = None
score = 0
high_score = 0
game_state = GameState.TITLE
paused = False
base_speed = 10

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == GameState.TITLE:
                if event.key == pygame.K_RETURN:
                    game_state = GameState.PLAYING
                    snake.reset()
                    food = spawn_food()
                    power_up = None
                    score = 0
                    paused = False
            
            elif game_state == GameState.PLAYING:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    game_state = GameState.TITLE
                elif not paused:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))
            
            elif game_state == GameState.GAME_OVER:
                if event.key == pygame.K_SPACE:
                    game_state = GameState.PLAYING
                    snake.reset()
                    food = spawn_food()
                    power_up = None
                    score = 0
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    game_state = GameState.TITLE

    if game_state == GameState.TITLE:
        show_title_screen()
    
    elif game_state == GameState.PLAYING and not paused:
        # Update snake effects
        snake.update_effects()
        
        # Move snake
        if not snake.move():
            game_state = GameState.GAME_OVER
            high_score = max(score, high_score)
            continue

        # Check for food collision
        if snake.body[0] == food:
            snake.grow = True
            food = spawn_food()
            score += 1
            if power_up is None:  # Only try to spawn a power-up if there isn't one
                power_up = spawn_power_up()

        # Check for power-up collision
        if power_up and snake.body[0] == power_up.position:
            snake.apply_power_up(power_up)
            power_up = None

        # Check if power-up expired
        if power_up and power_up.is_expired():
            power_up = None

        # Drawing
        screen.fill(BLACK)
        
        # Draw food
        pygame.draw.rect(screen, RED, (
            food[0] * GRID_SIZE,
            food[1] * GRID_SIZE,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        ))
        
        # Draw power-up if it exists
        if power_up:
            pygame.draw.rect(screen, power_up.get_color(), (
                power_up.position[0] * GRID_SIZE,
                power_up.position[1] * GRID_SIZE,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            ))
        
        # Draw snake
        for segment in snake.body:
            color = PURPLE if snake.ghost_mode else GREEN
            pygame.draw.rect(screen, color, (
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            ))

        # Draw score and active effects
        score_text = game_font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw active effects
        y_offset = 50
        if snake.speed_multiplier > 1:
            effect_text = game_font.render('Speed Boost!', True, BLUE)
            screen.blit(effect_text, (10, y_offset))
            y_offset += 40
        elif snake.speed_multiplier < 1:
            effect_text = game_font.render('Slowed!', True, YELLOW)
            screen.blit(effect_text, (10, y_offset))
            y_offset += 40
        if snake.ghost_mode:
            effect_text = game_font.render('Ghost Mode!', True, PURPLE)
            screen.blit(effect_text, (10, y_offset))
    
    elif game_state == GameState.PLAYING and paused:
        pause_text = title_font.render('PAUSED', True, WHITE)
        pause_rect = pause_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
        screen.blit(pause_text, pause_rect)
    
    elif game_state == GameState.GAME_OVER:
        show_game_over_screen(score, high_score)

    pygame.display.flip()
    clock.tick(base_speed * snake.speed_multiplier)

pygame.quit()
sys.exit()
