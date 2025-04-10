import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
STONE = (100, 100, 100)
TEXT_COLOR = (255, 255, 0)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER = (80, 80, 80)
BALL_EMOJI = "🐣"

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lava Floor Pong 🏓")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40)

# Load background image (no fire emoji version)
lava_background = pygame.image.load("lava.png")
lava_background = pygame.transform.scale(lava_background, (WIDTH, HEIGHT))

# Draw button
def draw_button(text, x, y, w, h, mouse, clicked):
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, BUTTON_HOVER, (x, y, w, h), border_radius=10)
        if clicked:
            return True
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, w, h), border_radius=10)

    label = font.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return False

# Paddle class
class Paddle:
    def __init__(self):
        self.width = 120
        self.height = 20
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - 60
        self.speed = 10

    def draw(self):
        pygame.draw.rect(screen, STONE, (self.x, self.y, self.width, self.height), border_radius=10)

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x + self.width < WIDTH:
            self.x += self.speed

# Ball class
class Ball:
    def __init__(self):
        self.size = 40
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vx = random.choice([-4, 4])
        self.vy = -4
        self.emoji = BALL_EMOJI
        self.font = pygame.font.SysFont("Segoe UI Emoji", self.size)

    def draw(self):
        text = self.font.render(self.emoji, True, WHITE)
        screen.blit(text, (self.x, self.y))

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x <= 0 or self.x + self.size >= WIDTH:
            self.vx *= -1
        if self.y <= 0:
            self.vy *= -1

# Start screen
def show_start_screen():
    while True:
        clock.tick(FPS)
        screen.blit(lava_background, (0, 0))
        title = font.render("🔥 Lava Floor Pong 🔥", True, TEXT_COLOR)
        screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 2 - 100))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        if draw_button("Play", WIDTH // 2 - 100, HEIGHT // 2, 200, 60, mouse, click):
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# Game loop
def game():
    paddle = Paddle()
    ball = Ball()
    running = True
    game_over = False
    score = 0

    while running:
        clock.tick(FPS)
        screen.blit(lava_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        if not game_over:
            ball.move()
            # Paddle collision
            if paddle.y < ball.y + ball.size < paddle.y + paddle.height:
                if paddle.x < ball.x + ball.size // 2 < paddle.x + paddle.width:
                    ball.vy *= -1
                    score += 1

            if ball.y + ball.size >= HEIGHT:
                game_over = True

        paddle.draw()
        ball.draw()

        if game_over:
            over_text = font.render("Game Over!", True, TEXT_COLOR)
            score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(over_text, ((WIDTH - over_text.get_width()) // 2, HEIGHT // 2 - 80))
            screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2 - 30))

            if draw_button("Play Again", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 60, mouse, click):
                return game()
        else:
            # Score top-left
            score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_text, (20, 20))

        pygame.display.flip()

# Run the game
show_start_screen()
game()
