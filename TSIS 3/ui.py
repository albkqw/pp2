import pygame
from persistence import load_leaderboard


def get_font():
    # базовый шрифт
    return pygame.font.Font(None, 40)


def draw_text(screen, text, x, y):
    # рисуем текст на экране
    font = get_font()

    text_surface = font.render(
        text,
        True,
        (255, 255, 255)
    )

    screen.blit(text_surface, (x, y))


def main_menu(screen):
    # главное меню игры
    screen.fill((0, 0, 0))

    draw_text(screen, "1. Play", 130, 150)
    draw_text(screen, "2. Leaderboard", 130, 220)
    draw_text(screen, "3. Settings", 130, 290)
    draw_text(screen, "4. Quit", 130, 360)


def leaderboard_screen(screen):
    screen.fill((0, 0, 0))

    leaderboard = load_leaderboard()

    draw_text(screen, "TOP 10", 140, 40)

    y = 120

    for i, player in enumerate(leaderboard):
        draw_text(
            screen,
            f"{i+1}. {player['username']} - {player['score']}",
            40,
            y
        )
        y += 40


def settings_screen(screen, settings):
    screen.fill((0, 0, 0))

    draw_text(
        screen,
        f"Sound: {settings['sound']}",
        50,
        100
    )

    draw_text(
        screen,
        f"Car Color: {settings['car_color']}",
        50,
        180
    )

    draw_text(
        screen,
        f"Difficulty: {settings['difficulty']}",
        50,
        260
    )

    draw_text(
        screen,
        "S - Toggle Sound",
        50,
        360
    )

    draw_text(
        screen,
        "C - Change Color",
        50,
        410
    )

    draw_text(
        screen,
        "D - Change Difficulty",
        50,
        460
    )

    draw_text(
        screen,
        "ESC - Back",
        50,
        520
    )


def game_over_screen(screen, result):
    screen.fill((0, 0, 0))

    draw_text(screen, "GAME OVER", 120, 120)

    draw_text(
        screen,
        f"Score: {result['score']}",
        120,
        220
    )

    draw_text(
        screen,
        f"Coins: {result['coins']}",
        120,
        280
    )

    draw_text(
        screen,
        f"Distance: {result['distance']}",
        120,
        340
    )

    draw_text(
        screen,
        "R - Retry",
        120,
        430
    )

    draw_text(
        screen,
        "ESC - Menu",
        120,
        480
    )


def username_screen(screen, username):
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 50)

    title = font.render(
        "Enter username:",
        True,
        (255, 255, 255)
    )

    screen.blit(title, (70, 180))

    box = pygame.Rect(70, 280, 260, 60) # поле для ввода имени

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        box,
        2 # толщина
    )

    # отображаем введённый текст
    text = font.render(
        username,
        True,
        (255, 255, 255)
    )

    screen.blit(text, (80, 295))

    hint = pygame.font.Font(None, 30).render(
        "Press ENTER",
        True,
        (255, 255, 255)
    )

    screen.blit(hint, (130, 380))