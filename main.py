import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
BG_COLOR = (200, 200, 255)
LINE_COLOR = (0, 0, 0)
MARKER_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)
POWER_BAR_COLOR = (0, 255, 0)
FONT = pygame.font.Font(None, 36)

MARKER_START_POS = SCREEN_WIDTH // 2
MARKER_SPEED = 5
MAX_POWER = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tug of War")

pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)
win_sound = pygame.mixer.Sound('win_sound.wav')

marker_pos = MARKER_START_POS
player1_power = MAX_POWER
player2_power = MAX_POWER
game_over = False
winner = ""
difficulty = 1

clock = pygame.time.Clock()

def draw_text(text, x, y, color):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_power_bar(player, power, x, y):
    pygame.draw.rect(screen, POWER_BAR_COLOR, (x, y, power, 20))
    draw_text(f"{player}: {power}", x, y - 25, TEXT_COLOR)

def reset_game():
    global marker_pos, player1_power, player2_power, game_over, difficulty
    marker_pos = MARKER_START_POS
    player1_power = MAX_POWER
    player2_power = MAX_POWER
    game_over = False
    difficulty += 0.5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_a]:
            marker_pos -= MARKER_SPEED * difficulty
            player1_power -= 1
        if keys[pygame.K_l]:
            marker_pos += MARKER_SPEED * difficulty
            player2_power -= 1

    screen.fill(BG_COLOR)
    pygame.draw.line(screen, LINE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)
    pygame.draw.circle(screen, MARKER_COLOR, (marker_pos, SCREEN_HEIGHT // 2), 20)

    draw_text("Tug of War", SCREEN_WIDTH // 2 - 100, 10, TEXT_COLOR)
    draw_power_bar("Player 1 (A)", player1_power, 50, SCREEN_HEIGHT - 50)
    draw_power_bar("Player 2 (L)", player2_power, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50)

    if player1_power <= 0:
        player1_power = 0
    if player2_power <= 0:
        player2_power = 0

    if marker_pos <= 0 or player1_power <= 0:
        winner = "Player 1 Wins!"
        win_sound.play()
        game_over = True
    elif marker_pos >= SCREEN_WIDTH or player2_power <= 0:
        winner = "Player 2 Wins!"
        win_sound.play()
        game_over = True

    if game_over:
        draw_text(winner, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, TEXT_COLOR)
        draw_text("Press R to Restart", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40, TEXT_COLOR)
        pygame.display.flip()
        if keys[pygame.K_r]:
            reset_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
