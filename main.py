import pygame
import sys
from game import Game
from ai import best_move

pygame.init()

# Input
rows = int(input("Enter number of rows (5-10): "))
cols = int(input("Enter number of cols (5-10): "))

CELL_SIZE = 100
WIDTH, HEIGHT = cols * CELL_SIZE, rows * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman AI Escape")

clock = pygame.time.Clock()  # ✅ FPS control

# Colors
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,50,50)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Fonts
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 35)

# States
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

state = MENU
difficulty = 3

def reset_game():
    return Game(rows, cols)

game = reset_game()
result_text = ""

# -------- BUTTON POSITIONS (CENTERED) -------- #
center_x = WIDTH // 2 - 100

# MENU
start_btn  = pygame.Rect(center_x,200,200,50)
easy_btn   = pygame.Rect(center_x,260,200,50)
medium_btn = pygame.Rect(center_x,320,200,50)
hard_btn   = pygame.Rect(center_x,380,200,50)
menu_quit_btn = pygame.Rect(center_x,440,200,50)

# GAME OVER
restart_btn = pygame.Rect(center_x,360,200,50)
home_btn    = pygame.Rect(center_x,430,200,50)
over_quit_btn = pygame.Rect(center_x,500,200,50)

# -------- DRAW -------- #

def draw_button(text, rect):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Default color
    color = (100, 100, 255)

    # Hover effect
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, (180,180,255), rect.inflate(6,6), border_radius=14) 
        # Click effect
        if click[0]:  # left mouse button
            color = (70, 70, 200)  # darker when pressed

    pygame.draw.rect(screen, color, rect, border_radius=12)

    label = small_font.render(text, True, (255,255,255))
    screen.blit(label, (rect.x + 40, rect.y + 10)) 

def draw_walls():
    for (x, y) in game.walls:
        pygame.draw.rect(screen, BLUE,
            (y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE), border_radius=10)

def draw_goal():
    gx, gy = game.goal
    pygame.draw.circle(screen, GREEN,
        (gy*CELL_SIZE+CELL_SIZE//2, gx*CELL_SIZE+CELL_SIZE//2), 20)

def draw_players():
    px, py = game.pacman
    gx, gy = game.ghost

    emoji_font = pygame.font.SysFont("Segoe UI Emoji", 60)

    pacman = emoji_font.render("😄", True, (0,0,0))
    ghost = emoji_font.render("👻", True, (0,0,0))

    screen.blit(pacman, (py*CELL_SIZE+20, px*CELL_SIZE+20))
    screen.blit(ghost, (gy*CELL_SIZE+20, gx*CELL_SIZE+20))

# -------- LOOP -------- #

running = True
while running:
    screen.fill((20,20,40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- MENU --------
        if state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_btn.collidepoint(event.pos):
                    game = reset_game()
                    state = PLAYING

                elif easy_btn.collidepoint(event.pos):
                    difficulty = 2

                elif medium_btn.collidepoint(event.pos):
                    difficulty = 3

                elif hard_btn.collidepoint(event.pos):
                    difficulty = 5

                elif menu_quit_btn.collidepoint(event.pos):
                    running = False

        # -------- PLAYING --------
        elif state == PLAYING:
            if event.type == pygame.KEYDOWN:
                x, y = game.pacman

                if event.key == pygame.K_UP:
                    new = (x-1, y)
                elif event.key == pygame.K_DOWN:
                    new = (x+1, y)
                elif event.key == pygame.K_LEFT:
                    new = (x, y-1)
                elif event.key == pygame.K_RIGHT:
                    new = (x, y+1)
                else:
                    new = (x, y)

                if new in game.get_moves(game.pacman):
                    game.move_pacman(new)

                    # Eat dot
                    if game.pacman in game.dots:
                        game.dots.remove(game.pacman)
                        game.score += 1

                    # WIN
                    if game.is_pacman_win() or len(game.dots) == 0:
                        game.score += 50
                        result_text = "PACMAN WINS!"
                        state = GAME_OVER
                        continue  # ✅ STOP further actions

                    # Ghost move
                    game.move_ghost(best_move(game, game.pacman, game.ghost, difficulty))

                    # LOSE
                    if game.is_ghost_win():
                        game.score -= 10
                        result_text = "GHOST WINS!"
                        state = GAME_OVER
                        continue

        # -------- GAME OVER --------
        elif state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:

                if restart_btn.collidepoint(event.pos):
                    game = reset_game()
                    state = PLAYING

                elif home_btn.collidepoint(event.pos):
                    game = reset_game()
                    state = MENU

                elif over_quit_btn.collidepoint(event.pos):
                    running = False

    # -------- DRAW -------- #

    if state == MENU:
        title = font.render("PACMAN AI", True, YELLOW)
        rect = title.get_rect(center=(WIDTH//2, 100))
        screen.blit(title, rect)

        draw_button("START", start_btn)
        draw_button("EASY", easy_btn)
        draw_button("MEDIUM", medium_btn)
        draw_button("HARD", hard_btn)
        draw_button("QUIT", menu_quit_btn)

        diff_text = small_font.render(f"Difficulty: {difficulty}", True, WHITE)
        screen.blit(diff_text, (20, 20))

    elif state == PLAYING:
        screen.blit(small_font.render("PACMAN AI ESCAPE", True, WHITE), (20,10))
        screen.blit(small_font.render(f"Score: {game.score}", True, WHITE), (350,10))

        draw_walls()

        for (i,j) in game.dots:
            pygame.draw.circle(screen, (220,220,220),
                (j*CELL_SIZE+CELL_SIZE//2, i*CELL_SIZE+CELL_SIZE//2), 5)

        draw_goal()
        draw_players()

    elif state == GAME_OVER:
        text = font.render(result_text, True, RED)
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 120))
        screen.blit(text, rect)

        score = small_font.render(f"Final Score: {game.score}", True, WHITE)
        score_rect = score.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(score, score_rect)

        draw_button("RESTART", restart_btn)
        draw_button("HOME", home_btn)
        draw_button("QUIT", over_quit_btn)

    pygame.display.update()
    clock.tick(60)  # ✅ Smooth FPS

pygame.quit()
sys.exit()