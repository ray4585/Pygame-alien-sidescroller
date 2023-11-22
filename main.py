import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player
player_size = 50
player_speed = 5
bullet_speed = 7
initial_shooting_speed = 10  # Initial shooting speed

# Alien
alien_size = 50
alien_speed = 3

# Power-up
powerup_size = 30
powerup_speed = 5

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Guardian")

# Load images
player_image = pygame.Surface((player_size, player_size))
player_image.fill(WHITE)

alien_image = pygame.Surface((alien_size, alien_size))
alien_image.fill(WHITE)

bullet_image = pygame.Surface((5, 10))
bullet_image.fill(WHITE)

powerup_image = pygame.Surface((powerup_size, powerup_size))
powerup_image.fill((255, 0, 0))  # Power-up color (red)

# Set up the clock
clock = pygame.time.Clock()

# Game variables
running = True
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
score = 0
shooting_speed = initial_shooting_speed
powerup_active = False

aliens = []
bullets = []
powerups = []

def spawn_alien():
    x = random.randint(0, WIDTH - alien_size)
    y = random.randint(-alien_size, -10)
    score_multiplier = random.choice([1, 2, 3])
    aliens.append([x, y, score_multiplier])

def spawn_powerup():
    x = random.randint(0, WIDTH - powerup_size)
    y = random.randint(-powerup_size, -10)
    powerups.append([x, y])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not powerup_active:
            bullets.append([player_x + player_size // 2 - 2, player_y])
    
    keys = pygame.key.get_pressed()
    player_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed

    # Update bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Update power-ups
    for powerup in powerups:
        powerup[1] += powerup_speed
        if powerup[1] > HEIGHT:
            powerups.remove(powerup)
            spawn_powerup()

    # Update aliens
    for alien in aliens:
        alien[1] += alien_speed
        if alien[1] > HEIGHT:
            aliens.remove(alien)
            spawn_alien()

    # Spawn new aliens
    if random.random() < 0.02:
        spawn_alien()

    # Spawn new power-ups
    if random.random() < 0.01 and not powerup_active:
        spawn_powerup()

    # Collision detection for bullets and aliens
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
        for alien in aliens:
            alien_rect = pygame.Rect(alien[0], alien[1], alien_size, alien_size)
            if bullet_rect.colliderect(alien_rect):
                score += alien[2]
                print(f"Score: {score}")
                bullets.remove(bullet)
                aliens.remove(alien)
                spawn_alien()

    # Collision detection for player and power-ups
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for powerup in powerups:
        powerup_rect = pygame.Rect(powerup[0], powerup[1], powerup_size, powerup_size)
        if player_rect.colliderect(powerup_rect):
            powerups.remove(powerup)
            shooting_speed += 2  # Increase shooting speed
            powerup_active = True
            pygame.time.set_timer(pygame.USEREVENT, 5000)  # Set a timer to deactivate power-up after 5 seconds

    # Power-up deactivation event
    if powerup_active and pygame.event.get(pygame.USEREVENT):
        powerup_active = False
        shooting_speed = initial_shooting_speed  # Reset shooting speed

    # Drawing
    screen.fill(BLACK)
    screen.blit(player_image, (player_x, player_y))
    for alien in aliens:
        screen.blit(alien_image, (alien[0], alien[1]))
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))
    for powerup in powerups:
        screen.blit(powerup_image, (powerup[0], powerup[1]))

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
