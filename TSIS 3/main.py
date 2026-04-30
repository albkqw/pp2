import pygame
from racer import run_game
from ui import (
    main_menu,
    leaderboard_screen,
    settings_screen,
    game_over_screen,
    username_screen
)
from persistence import (
    load_settings,
    save_settings
)

pygame.init()
pygame.mixer.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

settings = load_settings()

# background music
pygame.mixer.music.load(
    "assets/sounds/background.wav"
)
pygame.mixer.music.set_volume(0.4)

if settings["sound"]:
    pygame.mixer.music.play(-1)

username = ""

state = "username"
game_result = None

running = True

colors = ["red", "blue", "green"]
difficulties = ["easy", "medium", "hard"]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_settings(settings)
            running = False

        # USERNAME SCREEN
        if state == "username":
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if username.strip():
                        state = "menu"

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    if len(username) < 15:
                        username += event.unicode

        # MENU
        elif state == "menu":
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    game_result = run_game(
                        screen,
                        username,
                        settings
                    )
                    state = "game_over"

                elif event.key == pygame.K_2:
                    state = "leaderboard"

                elif event.key == pygame.K_3:
                    state = "settings"

                elif event.key == pygame.K_4:
                    save_settings(settings)
                    running = False

        # LEADERBOARD
        elif state == "leaderboard":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"

        # SETTINGS
        elif state == "settings":
            if event.type == pygame.KEYDOWN:

                # изменить звук
                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]

                    if settings["sound"]:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()

                # поменять цвет машины
                elif event.key == pygame.K_c:
                    current = colors.index(
                        settings["car_color"]
                    )

                    settings["car_color"] = colors[
                        (current + 1) % len(colors)
                    ]

                # смена сложности игры
                elif event.key == pygame.K_d:
                    current = difficulties.index(
                        settings["difficulty"]
                    )

                    settings["difficulty"] = difficulties[
                        (current + 1) % len(difficulties)
                    ]

                # сохранение и возврат в меню
                elif event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    state = "menu"

        # GAME OVER
        elif state == "game_over":
            if event.type == pygame.KEYDOWN:

                # retry
                if event.key == pygame.K_r:
                    game_result = run_game(
                        screen,
                        username,
                        settings
                    )

                # возврат в меню
                elif event.key == pygame.K_ESCAPE:
                    state = "menu"

    # отрисовка
    if state == "username":
        username_screen(screen, username)

    elif state == "menu":
        main_menu(screen)

    elif state == "leaderboard":
        leaderboard_screen(screen)

    elif state == "settings":
        settings_screen(screen, settings)

    elif state == "game_over":
        game_over_screen(screen, game_result)

    pygame.display.update()

pygame.quit()