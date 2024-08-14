import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
BG_COLOR = (200, 200, 255)
LINE_COLOR = (0, 0, 0)
MARKER_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)
MARKER_START_POS = SCREEN_WIDTH // 2
MARKER_SPEED = 5
FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tug of War")

marker_pos = MARKER_START_POS
player1_score = 0
player2_score = 0
game_over = False
winner = ""

clock = pygame.time.Clock()

def draw_text(text, x, y, color):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_a]:
            marker_pos -= MARKER_SPEED
        if keys[pygame.K_l]:
            marker_pos += MARKER_SPEED

    screen.fill(BG_COLOR)
    pygame.draw.line(screen, LINE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)
    pygame.draw.circle(screen, MARKER_COLOR, (marker_pos, SCREEN_HEIGHT // 2), 20)

    draw_text(f"Player 1 (A): {player1_score}", 50, 20, TEXT_COLOR)
    draw_text(f"Player 2 (L): {player2_score}", SCREEN_WIDTH - 200, 20, TEXT_COLOR)

    if marker_pos <= 0:
        player1_score += 1
        winner = "Player 1 Wins!"
        game_over = True
    elif marker_pos >= SCREEN_WIDTH:
        player2_score += 1
        winner = "Player 2 Wins!"
        game_over = True

    if game_over:
        draw_text(winner, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, TEXT_COLOR)
        pygame.display.flip()
        pygame.time.wait(2000)
        marker_pos = MARKER_START_POS
        game_over = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
