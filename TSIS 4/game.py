import pygame
import random
import json
from config import *
from db import *

pygame.init()
pygame.mixer.init()


class SnakeGame:
    def __init__(self, username):
        # создаем игру для конкретного пользователя
        self.username = username

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.load_settings()

        # звуки игры
        self.eat_sound = pygame.mixer.Sound("assets/eat.mp3")
        self.poison_sound = pygame.mixer.Sound("assets/poison.mp3")
        self.gameover_sound = pygame.mixer.Sound("assets/gameover.mp3")

        # включаем фоновую музыку
        if self.settings["sound"]:
            pygame.mixer.music.load("assets/background.wav")
            pygame.mixer.music.play(-1)

        self.reset()

    def load_settings(self):
        # загружаем настройки из файла
        with open("settings.json", "r") as f:
            self.settings = json.load(f)

    def save_settings(self):
        # сохраняем настройки
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

    def reset(self):
        # начальное состояние игры
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"

        self.score = 0
        self.level = 1
        self.speed = FPS

        # лучший результат игрока
        self.best_score = get_best_score(self.username)

        self.obstacles = []

        self.food = self.generate_food()
        self.poison = self.generate_poison()

        self.power_up = None
        self.power_up_timer = 0

        self.shield = False

    def move_direction(self):
        # возвращает смещение по текущему направлению
        if self.direction == "UP":
            return (0, -CELL)

        if self.direction == "DOWN":
            return (0, CELL)

        if self.direction == "LEFT":
            return (-CELL, 0)

        if self.direction == "RIGHT":
            return (CELL, 0)

    def generate_food(self):
        # создаем еду в свободной клетке
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)

            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                return {
                    "pos": (x, y),
                    "weight": random.choice([1, 2, 3]),  # сколько очков даст еда
                    "spawn": pygame.time.get_ticks()
                }

    def generate_poison(self):
        # создаем ядовитую еду
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)

            if (
                (x, y) not in self.snake
                and (x, y) != self.food["pos"]
                and (x, y) not in self.obstacles
            ):
                return (x, y)

    def generate_power_up(self):
        # создаем случайный бонус
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)

            if (
                (x, y) not in self.snake
                and (x, y) != self.food["pos"]
                and (x, y) != self.poison
                and (x, y) not in self.obstacles
            ):
                return {
                    "type": random.choice(["speed", "slow", "shield"]),
                    "pos": (x, y),
                    "spawn": pygame.time.get_ticks()
                }

    def generate_obstacles(self):
        # создаем препятствия по уровню
        self.obstacles = []

        for _ in range(self.level * 3):
            while True:
                x = random.randrange(0, WIDTH, CELL)
                y = random.randrange(0, HEIGHT, CELL)

                if (
                    (x, y) not in self.snake
                    and (x, y) != self.food["pos"]
                    and (x, y) != self.poison
                ):
                    self.obstacles.append((x, y))
                    break

    def game_over(self):
        # сохраняем результат и завершаем игру
        if self.settings["sound"]:
            self.gameover_sound.play()

        save_game(self.username, self.score, self.level)

        pygame.time.delay(1000)

        return False

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # управление змейкой
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"

                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"

                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"

                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"

            dx, dy = self.move_direction()

            # новая позиция головы
            head = (
                self.snake[0][0] + dx,
                self.snake[0][1] + dy
            )

            # столкновение со стеной
            if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
                if self.shield:
                    self.shield = False
                else:
                    running = self.game_over()

            # столкновение с собой
            if head in self.snake:
                if self.shield:
                    self.shield = False
                else:
                    running = self.game_over()

            # столкновение с препятствиями
            if head in self.obstacles:
                running = self.game_over()

            if not running:
                break

            self.snake.insert(0, head)

            # обычная еда
            if head == self.food["pos"]:
                if self.settings["sound"]:
                    self.eat_sound.play()

                self.score += self.food["weight"]
                self.food = self.generate_food()

                # каждые 5 очков новый уровень
                if self.score % 5 == 0:
                    self.level += 1
                    self.speed += 1

                    if self.level >= 3:
                        self.generate_obstacles()

            # ядовитая еда
            elif head == self.poison:
                if self.settings["sound"]:
                    self.poison_sound.play()

                # уменьшаем длину змеи
                for _ in range(2):
                    if len(self.snake) > 1:
                        self.snake.pop()

                if len(self.snake) <= 1:
                    running = self.game_over()

                self.poison = self.generate_poison()

            else:
                self.snake.pop()

            # создаем бонус если его нет
            if not self.power_up:
                self.power_up = self.generate_power_up()

            # бонус исчезает через 8 секунд
            if self.power_up:
                if pygame.time.get_ticks() - self.power_up["spawn"] > 8000:
                    self.power_up = None

            # подбор бонуса
            if self.power_up and head == self.power_up["pos"]:
                if self.power_up["type"] == "speed":
                    self.speed += 5
                    self.power_up_timer = pygame.time.get_ticks()

                elif self.power_up["type"] == "slow":
                    self.speed = max(3, self.speed - 3)
                    self.power_up_timer = pygame.time.get_ticks()

                elif self.power_up["type"] == "shield":
                    self.shield = True

                self.power_up = None

            # возвращаем скорость обратно через 5 сек
            if self.power_up_timer:
                if pygame.time.get_ticks() - self.power_up_timer > 5000:
                    self.speed = FPS + self.level
                    self.power_up_timer = 0

            self.draw()
            self.clock.tick(self.speed)

    def draw(self):
        # отрисовка всех объектов
        self.screen.fill(BLACK)

        # сетка
        if self.settings["grid"]:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))

            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

        # змейка
        for part in self.snake:
            pygame.draw.rect(
                self.screen,
                tuple(self.settings["snake_color"]),
                (*part, CELL, CELL)
            )

        # еда
        pygame.draw.rect(
            self.screen,
            RED,
            (*self.food["pos"], CELL, CELL)
        )

        # яд
        pygame.draw.rect(
            self.screen,
            DARK_RED,
            (*self.poison, CELL, CELL)
        )

        # препятствия
        for obs in self.obstacles:
            pygame.draw.rect(
                self.screen,
                BLUE,
                (*obs, CELL, CELL)
            )

        # бонус
        if self.power_up:
            pygame.draw.rect(
                self.screen,
                YELLOW,
                (*self.power_up["pos"], CELL, CELL)
            )

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        best_text = self.font.render(f"Best: {self.best_score}", True, WHITE)
        shield_text = self.font.render(
            f"Shield: {'ON' if self.shield else 'OFF'}",
            True,
            WHITE
        )

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(best_text, (10, 70))
        self.screen.blit(shield_text, (10, 100))

        pygame.display.flip()