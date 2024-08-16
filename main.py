import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
BG_COLOR_START = (200, 200, 255)
LINE_COLOR = (0, 0, 0)
MARKER_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)
STAMINA_BAR_COLOR_FULL = (0, 255, 0)
STAMINA_BAR_COLOR_LOW = (255, 0, 0)
POWER_UP_COLOR = (255, 255, 0)
FONT = pygame.font.Font(None, 36)
MARKER_START_POS = SCREEN_WIDTH // 2
BASE_MARKER_SPEED = 5
MAX_STAMINA = 100
STAMINA_DECREASE = 1
STAMINA_REGEN = 0.5
POWER_UP_DURATION = 5000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tug of War")

marker_pos = MARKER_START_POS
player1_stamina = MAX_STAMINA
player2_stamina = MAX_STAMINA
game_over = False
start_game = False
winner = ""
difficulty = 1
rounds_won_p1 = 0
rounds_won_p2 = 0
player1_name = ""
player2_name = ""
power_up_active = False
power_up_time = 0
power_up_pos = None
round_number = 1

clock = pygame.time.Clock()

def draw_text(text, x, y, color):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_stamina_bar(stamina, x, y, color):
    pygame.draw.rect(screen, color, (x, y, stamina, 20))

def update_stamina(current_stamina, key_pressed):
    if key_pressed:
        current_stamina -= STAMINA_DECREASE
    else:
        current_stamina += STAMINA_REGEN
    return min(max(current_stamina, 0), MAX_STAMINA)

def reset_game():
    global marker_pos, player1_stamina, player2_stamina, game_over, difficulty, start_game, power_up_active, power_up_pos, power_up_time
    marker_pos = MARKER_START_POS
    player1_stamina = MAX_STAMINA
    player2_stamina = MAX_STAMINA
    game_over = False
    difficulty = 1
    power_up_active = False
    power_up_pos = None
    power_up_time = 0

def get_stamina_color(stamina):
    if stamina > MAX_STAMINA // 2:
        return STAMINA_BAR_COLOR_FULL
    else:
        return STAMINA_BAR_COLOR_LOW

def spawn_power_up():
    return random.randint(100, SCREEN_WIDTH - 100), SCREEN_HEIGHT // 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not start_game:
        screen.fill(BG_COLOR_START)
        draw_text("Enter Player 1 Name:", SCREEN_WIDTH // 2 - 150, 100, TEXT_COLOR)
        draw_text("Enter Player 2 Name:", SCREEN_WIDTH // 2 - 150, 200, TEXT_COLOR)
        draw_text("Press ENTER to Start", SCREEN_WIDTH // 2 - 120, 300, TEXT_COLOR)
        
        if keys[pygame.K_RETURN]:
            player1_name = "Player 1" if not player1_name else player1_name
            player2_name = "Player 2" if not player2_name else player2_name
            start_game = True

        pygame.display.flip()
        continue

    if not game_over:
        player1_stamina = update_stamina(player1_stamina, keys[pygame.K_a])
        player2_stamina = update_stamina(player2_stamina, keys[pygame.K_l])

        if keys[pygame.K_a] and player1_stamina > 0:
            marker_pos -= BASE_MARKER_SPEED * difficulty * (player1_stamina / MAX_STAMINA)
        if keys[pygame.K_l] and player2_stamina > 0:
            marker_pos += BASE_MARKER_SPEED * difficulty * (player2_stamina / MAX_STAMINA)

        if not power_up_active and random.random() < 0.001:
            power_up_pos = spawn_power_up()
            power_up_active = True

        if power_up_active:
            pygame.draw.circle(screen, POWER_UP_COLOR, power_up_pos, 10)
            if marker_pos >= power_up_pos[0] - 10 and marker_pos <= power_up_pos[0] + 10:
                if marker_pos < SCREEN_WIDTH // 2:
                    player1_stamina += 20
                else:
                    player2_stamina += 20
                power_up_active = False
                power_up_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - power_up_time > POWER_UP_DURATION:
            power_up_active = False

    bg_color_dynamic = (
        255 - int((marker_pos / SCREEN_WIDTH) * 100),
        200 + int((marker_pos / SCREEN_WIDTH) * 55),
        255 - int((marker_pos / SCREEN_WIDTH) * 55)
    )
    screen.fill(bg_color_dynamic)
    pygame.draw.line(screen, LINE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)
    pygame.draw.circle(screen, MARKER_COLOR, (marker_pos, SCREEN_HEIGHT // 2), 20)

    draw_stamina_bar(player1_stamina, 50, SCREEN_HEIGHT - 50, get_stamina_color(player1_stamina))
    draw_stamina_bar(player2_stamina, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, get_stamina_color(player2_stamina))

    if marker_pos <= 0 or player1_stamina <= 0:
        winner = f"{player1_name} Wins!"
        rounds_won_p1 += 1
        game_over = True
    elif marker_pos >= SCREEN_WIDTH or player2_stamina <= 0:
        winner = f"{player2_name} Wins!"
        rounds_won_p2 += 1
        game_over = True

    if game_over:
        draw_text(winner, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, TEXT_COLOR)
        draw_text("Press R to Restart or Q to Quit", SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 40, TEXT_COLOR)
        draw_text(f"Rounds: {rounds_won_p1} - {rounds_won_p2}", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 80, TEXT_COLOR)
        pygame.display.flip()

        if keys[pygame.K_r]:
            round_number += 1
            reset_game()
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
    else:
        difficulty += 0.001

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
