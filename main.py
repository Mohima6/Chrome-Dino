import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dino Clone without Clouds")

BG_COLOR = (255, 255, 255)
GROUND_COLOR = (50, 50, 50)
TEXT_COLOR = (0, 0, 0)
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

# Load dino running frames and flip to face right
dino_run1 = pygame.image.load("assets/dino_run1.png").convert_alpha()
dino_run2 = pygame.image.load("assets/dino_run2.png").convert_alpha()
dino_run1 = pygame.transform.flip(dino_run1, True, False)
dino_run2 = pygame.transform.flip(dino_run2, True, False)
dino_run1 = pygame.transform.scale(dino_run1, (80, 80))
dino_run2 = pygame.transform.scale(dino_run2, (80, 80))
dino_frames = [dino_run1, dino_run2]
dino_index = 0
dino_image = dino_frames[dino_index]
dino_rect = dino_image.get_rect(midbottom=(100, 350))

# Load cactus image and create different sizes
base_cactus = pygame.image.load("assets/cactus.png").convert_alpha()
cactus_sizes = [(35, 50), (50, 70), (25, 40)]  # small, big, smaller
cactus_images = [pygame.transform.scale(base_cactus, size) for size in cactus_sizes]

# Initialize first cactus
current_cactus_img = random.choice(cactus_images)
cactus_rect = current_cactus_img.get_rect(midbottom=(SCREEN_WIDTH + 300, 350))  # closer spawn

gravity = 1
velocity_y = 0
is_jumping = False

score = 0
game_active = False
game_over = False
dino_running = False

RUN_ANIM_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(RUN_ANIM_EVENT, 150)

def display_text(text, size, color, x, y):
    font_obj = pygame.font.SysFont(None, size)
    surface = font_obj.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

while True:
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect(0, 350, SCREEN_WIDTH, 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == RUN_ANIM_EVENT and game_active:
            dino_index = (dino_index + 1) % 2
            dino_image = dino_frames[dino_index]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active and not game_over:
                    game_active = True
                    dino_running = True
                    current_cactus_img = random.choice(cactus_images)
                    cactus_rect = current_cactus_img.get_rect(midbottom=(SCREEN_WIDTH + 300, 350))
                    score = 0
                elif game_active:
                    if not is_jumping and dino_rect.bottom >= 350:
                        is_jumping = True
                        velocity_y = -15
                elif game_over:
                    game_active = True
                    game_over = False
                    dino_running = True
                    current_cactus_img = random.choice(cactus_images)
                    cactus_rect = current_cactus_img.get_rect(midbottom=(SCREEN_WIDTH + 300, 350))
                    score = 0
                    dino_rect.bottom = 350
                    dino_rect.left = 100

    if game_active:
        # Dino running and moving forward if not jumping and not reached max x
        if dino_running and not is_jumping:
            if dino_rect.left < 300:
                dino_rect.x += 6

        # Jump physics
        if is_jumping:
            dino_rect.y += velocity_y
            velocity_y += gravity
            if dino_rect.bottom >= 350:
                dino_rect.bottom = 350
                is_jumping = False

        # Move cactus obstacle
        cactus_rect.x -= 8  # Increase speed for more challenge

        # Draw cactus
        screen.blit(current_cactus_img, cactus_rect)

        # When cactus goes off screen, respawn sooner with random cactus size
        if cactus_rect.right < 0:
            current_cactus_img = random.choice(cactus_images)
            cactus_rect = current_cactus_img.get_rect(midbottom=(SCREEN_WIDTH + random.randint(200, 400), 350))
            score += 1

        # Draw dino
        screen.blit(dino_image, dino_rect)

        # Collision detection with cactus
        if dino_rect.colliderect(cactus_rect.inflate(-10, -10)):
            game_active = False
            game_over = True
            dino_running = False

        # Draw score
        score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_surf, (10, 10))

    elif game_over:
        display_text("GAME OVER", 64, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        display_text(f"Final Score: {score}", 48, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
        display_text("Press SPACE to Restart", 36, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)

    else:
        # Before game start: dino stands still
        screen.blit(dino_frames[0], dino_rect)
        display_text("CHROME DINO CLONE", 48, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
        display_text("Press SPACE to Start", 36, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    pygame.display.update()
    clock.tick(60)
