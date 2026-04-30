import pygame
import random
from persistence import add_score

WIDTH = 400
HEIGHT = 600

ROAD_LEFT = 50
ROAD_RIGHT = 350

WHITE = (255, 255, 255)

COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 120, 255),
    "green": (0, 255, 0)
}


# перекрашивание картинки 
def tint_image(image, color):
    tinted = image.copy()
    tinted.fill(color, special_flags=pygame.BLEND_MULT)
    return tinted


class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()

        base_image = pygame.image.load(
            "assets/images/player.png"
        ).convert_alpha()

        base_image = pygame.transform.scale(
            base_image,
            (50, 80)
        )

        self.image = tint_image(
            base_image,
            COLORS[color_name]
        )

        self.rect = self.image.get_rect()
        # начальная позиция игрока
        self.rect.center = (WIDTH // 2, HEIGHT - 100)

        self.speed = 7
        self.shield = False # защита от одного столкновения

    def move(self, keys):
        # Движение влево в пределах дороги
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= self.speed

        # Движение вправо в пределах дороги
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += self.speed


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.image = pygame.image.load(
            "assets/images/enemy.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (50, 80)
        )

        self.rect = self.image.get_rect()
        self.rect.center = (
            random.choice([100, 200, 300]),
            -100
        )

        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # разная ценности монеты
        self.value = random.choice([1, 2, 5])

        self.image = pygame.image.load(
            "assets/images/coin.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (30, 30)
        )

        self.rect = self.image.get_rect()
        self.rect.center = (
            random.choice([100, 200, 300]),
            -30
        )

        self.speed = 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.image = pygame.Surface((40, 40)) # ширина и высота
        self.image.fill((100, 100, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (
            random.choice([100, 200, 300]),
            -50
        )

        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Случайный тип бонуса
        self.kind = random.choice(
            ["nitro", "shield", "repair"]
        )

        self.image = pygame.Surface((35, 35))

        if self.kind == "nitro":
            self.image.fill((0, 255, 255))

        elif self.kind == "shield":
            self.image.fill((255, 255, 0))

        else:
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.center = (
            random.choice([100, 200, 300]),
            -50
        )

        self.speed = 5
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

        if pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()


def run_game(screen, username, settings):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    road = pygame.image.load(
        "assets/images/AnimatedStreet.png"
    )

    road = pygame.transform.scale(
        road,
        (WIDTH, HEIGHT)
    )

    if settings["sound"]:
        coin_sound = pygame.mixer.Sound(
            "assets/sounds/coin.wav"
        )

        crash_sound = pygame.mixer.Sound(
            "assets/sounds/crash.wav"
        )

        nitro_sound = pygame.mixer.Sound(
            "assets/sounds/nitro.mp3"
        )

    player = Player(
        settings["car_color"]
    )

    player_group = pygame.sprite.Group(player)
    traffic_group = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    powerup_group = pygame.sprite.Group()

    base_speed = 5
    game_speed = 5

    if settings["difficulty"] == "easy":
        spawn_delay = 1400 # машины появляются реже

    elif settings["difficulty"] == "medium":
        spawn_delay = 1000

    else:
        spawn_delay = 700 # машины появляются чаще

    score = 0
    coins = 0
    distance = 0

    active_powerup = None
    powerup_start = 0

    # Таймеры для контроля появления объектов
    traffic_timer = 0
    obstacle_timer = 0
    coin_timer = 0
    powerup_timer = 0

    running = True

    while running:
        screen.blit(road, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

        keys = pygame.key.get_pressed()
        player.move(keys)

        now = pygame.time.get_ticks()

        # Создаем новую машину через определенный интервал
        if now - traffic_timer > spawn_delay:
            traffic_group.add(
                TrafficCar(game_speed)
            )
            traffic_timer = now

        if now - obstacle_timer > 1500:
            obstacle_group.add(
                Obstacle(game_speed)
            )
            obstacle_timer = now

        if now - coin_timer > 1200:
            coin_group.add(Coin())
            coin_timer = now

        if now - powerup_timer > 7000:
            if len(powerup_group) == 0:
                powerup_group.add(PowerUp())

            powerup_timer = now

        traffic_group.update()
        obstacle_group.update()
        coin_group.update()
        powerup_group.update()

        collected_coins = pygame.sprite.spritecollide(
            player,
            coin_group,
            True
        )

        for coin in collected_coins:
            coins += coin.value
            score += coin.value * 10

            if settings["sound"]:
                coin_sound.play()

        collected_powerups = pygame.sprite.spritecollide(
            player,
            powerup_group,
            True
        )

        for powerup in collected_powerups:
            if active_powerup is None:
                active_powerup = powerup.kind

                if powerup.kind == "nitro":
                    game_speed += 5
                    powerup_start = now

                    if settings["sound"]:
                        nitro_sound.play()

                elif powerup.kind == "shield":
                    player.shield = True

                elif powerup.kind == "repair":
                    active_powerup = None

        if active_powerup == "nitro":
            if now - powerup_start > 5000:
                game_speed = base_speed
                active_powerup = None

        traffic_collision = pygame.sprite.spritecollide(
            player,
            traffic_group,
            True
        )

        obstacle_collision = pygame.sprite.spritecollide(
            player,
            obstacle_group,
            True
        )

        if traffic_collision or obstacle_collision:
            if player.shield:
                player.shield = False
                active_powerup = None

            else:
                if settings["sound"]:
                    crash_sound.play()

                pygame.time.delay(300)
                running = False

        distance += game_speed * 0.1
        score += 1

        # постепенное увеличение сложности игры
        if score % 50 == 0:
            base_speed += 1
            game_speed = base_speed

        player_group.draw(screen)
        traffic_group.draw(screen)
        obstacle_group.draw(screen)
        coin_group.draw(screen)
        powerup_group.draw(screen)

        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        coin_text = font.render(
            f"Coins: {coins}",
            True,
            WHITE
        )

        distance_text = font.render(
            f"Distance: {int(distance)}m",
            True,
            WHITE
        )

        screen.blit(score_text, (20, 20))
        screen.blit(coin_text, (20, 60))
        screen.blit(distance_text, (20, 100))

        if active_powerup:
            power_text = font.render(
                f"Power: {active_powerup}",
                True,
                WHITE
            )
            screen.blit(power_text, (20, 140))

        pygame.display.update()
        clock.tick(60)

    add_score(username, score, int(distance))

    return {
        "score": score,
        "coins": coins,
        "distance": int(distance)
    }