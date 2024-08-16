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

AI_DIFFICULTY = {"easy": 0.5, "medium": 1.0, "hard": 1.5}

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
power_up_type = ""
power_up_time = 0
power_up_pos = None
round_number = 1
game_paused = False
sound_enabled = True
ai_enabled = False
ai_difficulty = "medium"
special_move_active = False
special_move_time = 0
weather_effect = None
wind_direction = 0

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
    global marker_pos, player1_stamina, player2_stamina, game_over, difficulty, start_game, power_up_active, power_up_pos, power_up_time, ai_enabled, special_move_active, special_move_time, weather_effect, wind_direction
    marker_pos = MARKER_START_POS
    player1_stamina = MAX_STAMINA
    player2_stamina = MAX_STAMINA
    game_over = False
    difficulty = 1
    power_up_active = False
    power_up_pos = None
    power_up_time = 0
    ai_enabled = False
    special_move_active = False
    special_move_time = 0
    weather_effect = None
    wind_direction = 0

def get_stamina_color(stamina):
    if stamina > MAX_STAMINA // 2:
        return STAMINA_BAR_COLOR_FULL
    else:
        return STAMINA_BAR_COLOR_LOW

def spawn_power_up():
    types = ["stamina_boost", "speed_boost", "invincibility"]
    return random.randint(100, SCREEN_WIDTH - 100), SCREEN_HEIGHT // 2, random.choice(types)

def apply_power_up(player):
    global player1_stamina, player2_stamina, power_up_type
    if power_up_type == "stamina_boost":
        if player == 1:
            player1_stamina = min(MAX_STAMINA, player1_stamina + 30)
        else:
            player2_stamina = min(MAX_STAMINA, player2_stamina + 30)
    elif power_up_type == "speed_boost":
        global BASE_MARKER_SPEED
        BASE_MARKER_SPEED *= 1.5
        pygame.time.set_timer(pygame.USEREVENT + 1, POWER_UP_DURATION)
    elif power_up_type == "invincibility":
        if player == 1:
            player1_stamina = MAX_STAMINA
        else:
            player2_stamina = MAX_STAMINA
        pygame.time.set_timer(pygame.USEREVENT + 2, POWER_UP_DURATION)

def apply_special_move(player):
    global special_move_active, special_move_time, player1_stamina, player2_stamina
    special_move_active = True
    special_move_time = pygame.time.get_ticks()
    if player == 1:
        player1_stamina = MAX_STAMINA
    else:
        player2_stamina = MAX_STAMINA

def ai_behavior():
    if ai_difficulty == "easy":
        if player2_stamina > 50:
            return True if random.random() > 0.5 else False
    elif ai_difficulty == "medium":
        if player2_stamina > 30:
            return True if random.random() > 0.3 else False
    elif ai_difficulty == "hard":
        if player2_stamina > 10:
            return True if random.random() > 0.1 else False
    return False

def apply_weather_effect():
    global wind_direction
    if weather_effect == "wind":
        wind_direction = random.choice([-1, 1])
        pygame.time.set_timer(pygame.USEREVENT + 3, 10000)  # Wind lasts for 10 seconds

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_paused = not game_paused
            if event.key == pygame.K_m:
                sound_enabled = not sound_enabled
            if event.key == pygame.K_a:
                ai_enabled = not ai_enabled
            if event.key == pygame.K_s and not special_move_active:
                apply_special_move(1)
        if event.type == pygame.USEREVENT + 1:
            BASE_MARKER_SPEED /= 1.5
        if event.type == pygame.USEREVENT + 2:
            if player1_stamina == MAX_STAMINA:
                player1_stamina = MAX_STAMINA
            else:
                player2_stamina = MAX_STAMINA
        if event.type == pygame.USEREVENT + 3:
            wind_direction = 0

    if game_paused:
        screen.fill(BG_COLOR_START)
        draw_text("Game Paused", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, TEXT_COLOR)
        draw_text("Press P to Resume", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40, TEXT_COLOR)
        pygame.display.flip()
        continue

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
        if ai_enabled:
            player2_stamina = update_stamina(player2_stamina, ai_behavior())
        else:
            player2_stamina = update_stamina(player2_stamina, keys[pygame.K_l])

        if keys[pygame.K_a] and player1_stamina > 0:
            marker_pos -= BASE_MARKER_SPEED * difficulty * (player1_stamina / MAX_STAMINA) + wind_direction
        if (ai_enabled and ai_behavior()) or (keys[pygame.K_l] and player2_stamina > 0):
            marker_pos += BASE_MARKER_SPEED * difficulty * (player2_stamina / MAX_STAMINA) - wind_direction

        if not power_up_active and random.random() < 0.001:
            power_up_pos = spawn_power_up()
            power_up_active = True
            power_up_type = power_up_pos[2]

        if power_up_active:
            power_up_color = POWER_UP_COLOR
            if power_up_type == "stamina_boost":
                power_up_color = (0, 255, 255)
            elif power_up_type == "speed_boost":
                power_up_color = (255, 0, 255)
            elif power_up_type == "invincibility":
                power_up_color = (255, 255, 0)
            pygame.draw.circle(screen, power_up_color, power_up_pos[:2], 10)
            if marker_pos >= power_up_pos[0] - 10 and marker_pos <= power_up_pos[0] + 10:
                apply_power_up(1 if marker_pos < SCREEN_WIDTH // 2 else 2)
                power_up_active = False
                power_up_time = pygame.time.get_ticks()

        if not weather_effect and random.random() < 0.001:
            weather_effect = random.choice(["wind"])
            apply_weather_effect()

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
