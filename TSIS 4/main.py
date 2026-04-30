import pygame
import json
from game import SnakeGame
from db import get_top_10, get_best_score
from config import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Menu")

font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 22)


def draw_button(text, x, y, w, h):
    # рисует кнопку
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, GRAY, rect)

    label = font.render(text, True, WHITE)
    screen.blit(
        label,
        (
            x + (w - label.get_width()) // 2,
            y + (h - label.get_height()) // 2
        )
    )

    return rect


def username_input():
    # ввод имени игрока
    username = ""
    active = True

    while active:
        screen.fill(BLACK)

        title = font.render("Enter Username:", True, WHITE)
        name = font.render(username, True, GREEN)

        screen.blit(title, (180, 200))
        screen.blit(name, (200, 260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                # подтверждение имени
                if event.key == pygame.K_RETURN:
                    if username.strip():
                        return username

                # удаление символа
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    username += event.unicode


def leaderboard_screen():
    # экран лидеров
    running = True
    data = get_top_10()

    while running:
        screen.fill(BLACK)

        title = font.render("Leaderboard", True, WHITE)
        screen.blit(title, (220, 40))

        y = 120

        for i, row in enumerate(data):
            username, score, level, date = row

            text = small_font.render(
                f"{i+1}. {username} | {score} | lvl {level}",
                True,
                WHITE
            )

            screen.blit(text, (80, y))
            y += 40

        back = draw_button("Back", 220, 500, 160, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos):
                    running = False


def settings_screen():
    # экран настроек
    running = True

    with open("settings.json", "r") as f:
        settings = json.load(f)

    # доступные цвета змейки
    colors = [
        [0, 200, 0],
        [255, 0, 0],
        [0, 0, 255]
    ]

    if settings["snake_color"] in colors:
        color_index = colors.index(settings["snake_color"])
    else:
        color_index = 0

    while running:
        screen.fill(BLACK)

        title = font.render("Settings", True, WHITE)
        screen.blit(title, (230, 50))

        grid_btn = draw_button(
            f"Grid: {settings['grid']}",
            180, 150, 240, 50
        )

        sound_btn = draw_button(
            f"Sound: {settings['sound']}",
            180, 240, 240, 50
        )

        color_btn = draw_button(
            f"Color: {settings['snake_color']}",
            180, 330, 240, 50
        )

        save_btn = draw_button(
            "Save & Back",
            180, 450, 240, 50
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # включение/выключение сетки
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]

                # включение/выключение звука
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                    if settings["sound"]:
                        pygame.mixer.music.load("assets/background.wav")
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()

                # смена цвета змейки
                if color_btn.collidepoint(event.pos):
                    color_index += 1

                    if color_index >= len(colors):
                        color_index = 0

                    settings["snake_color"] = colors[color_index]

                # сохранение настроек
                if save_btn.collidepoint(event.pos):
                    with open("settings.json", "w") as f:
                        json.dump(settings, f)

                    running = False


def game_over_screen(username, score, level):
    # экран окончания игры
    running = True
    best = get_best_score(username)

    while running:
        screen.fill(BLACK)

        over = font.render("Game Over", True, RED)

        score_text = small_font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        level_text = small_font.render(
            f"Level: {level}",
            True,
            WHITE
        )

        best_text = small_font.render(
            f"Best: {best}",
            True,
            WHITE
        )

        screen.blit(over, (220, 100))
        screen.blit(score_text, (220, 180))
        screen.blit(level_text, (220, 220))
        screen.blit(best_text, (220, 260))

        retry = draw_button("Retry", 180, 360, 240, 50)
        menu = draw_button("Main Menu", 180, 440, 240, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry.collidepoint(event.pos):
                    return True

                if menu.collidepoint(event.pos):
                    return False


def main_menu():
    # главное меню
    while True:
        screen.fill(BLACK)

        title = font.render("Snake Game", True, GREEN)
        screen.blit(title, (210, 80))

        play_btn = draw_button("Play", 200, 180, 200, 50)
        leaderboard_btn = draw_button("Leaderboard", 200, 260, 200, 50)
        settings_btn = draw_button("Settings", 200, 340, 200, 50)
        quit_btn = draw_button("Quit", 200, 420, 200, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # запуск игры
                if play_btn.collidepoint(event.pos):
                    username = username_input()

                    while True:
                        game = SnakeGame(username)
                        game.run()

                        retry = game_over_screen(
                            username,
                            game.score,
                            game.level
                        )

                        if not retry:
                            break

                # таблица лидеров
                if leaderboard_btn.collidepoint(event.pos):
                    leaderboard_screen()

                # настройки
                if settings_btn.collidepoint(event.pos):
                    settings_screen()

                # выход
                if quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()


main_menu()