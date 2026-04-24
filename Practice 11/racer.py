import pygame
import random

pygame.init()

RUNNING = True
FPS = 60
FramePerSecond = pygame.time.Clock()

# Цвета
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Настройки экрана
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

# Настройки игры
SPEED = 5  # Скорость врагов и монет
PLAYER_HEIGHT = 750
PLAYER_SPEED = 15

# Настройки увеличения сложности
COINS_FOR_SPEEDUP = 10  # Каждые N очков увеличивается скорость
MAX_SPEED = 20

DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('racer_images/hero.png')
        self.rect = self.image.get_rect()
        self.rect.center = (160, PLAYER_HEIGHT)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('racer_images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # Движение врага вниз
        self.rect.move_ip(0, SPEED)

        # Перемещение наверх при выходе за экран
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Случайный вес  монеты
        self.value = random.choice([1, 2, 5])

        # Размер зависит от ценности
        if self.value == 1:
            size = 60
        elif self.value == 2:
            size = 80
        else:
            size = 100

        # Загрузка и масштабирование изображения
        self.image = pygame.image.load('racer_images/coin.png')
        self.image = pygame.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()

        # Появление в случайной позиции чуть выше экрана
        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 40),
            random.randint(-100, -40)
        )

    def move(self):
        # Движение монеты вниз
        self.rect.move_ip(0, SPEED)

        # Если монета вышла за экран — переспавн
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

    def respawn(self):
        # Назначаем новую ценность и размер
        self.value = random.choice([1, 2, 5])

        if self.value == 1:
            size = 60
        elif self.value == 2:
            size = 80
        else:
            size = 100

        self.image = pygame.image.load('racer_images/coin.png')
        self.image = pygame.transform.scale(self.image, (size, size))

        # Новая случайная позиция
        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 40),
            random.randint(-100, -40)
        )


Player1 = Player()
Enemy1 = Enemy()

Coin1 = Coin()
Coin2 = Coin()
Coin3 = Coin()

# Sprite Groups
enemies = pygame.sprite.Group(Enemy1)
coins = pygame.sprite.Group(Coin1, Coin2, Coin3)
all_sprites = pygame.sprite.Group(Player1, Enemy1, Coin1, Coin2, Coin3)

# Очки
point = 0
font = pygame.font.Font(None, 36)


while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    DISPLAYSURFACE.fill(WHITE)

    # Движение и отрисовка всех спрайтов
    for entity in all_sprites:
        DISPLAYSURFACE.blit(entity.image, entity.rect)
        entity.move()

    # столкновение Player и Enemy
    if pygame.sprite.spritecollideany(Player1, enemies):
        pygame.mixer.Sound("racer_sounds/crash.wav").play()

        DISPLAYSURFACE.fill(RED)
        pygame.display.update()

        # Удаление всех объектов
        for entity in all_sprites:
            entity.kill()

        # Надпись Game Over
        game_over_font = font.render("Game Over", True, BLACK)
        game_over_rect = game_over_font.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        DISPLAYSURFACE.blit(game_over_font, game_over_rect)

        pygame.display.update()
        pygame.time.delay(1000)

        pygame.quit()
        RUNNING = False

    # столкновение Player и Coin
    collected_coins = pygame.sprite.spritecollide(Player1, coins, False)

    for coin in collected_coins:
        pygame.mixer.Sound("racer_sounds/bell.wav").play()

        # Добавляем очки с учётом ценности монеты
        point += coin.value

        coin.respawn()

        # Увеличение скорости каждые N очков
        if point % COINS_FOR_SPEEDUP == 0:
            SPEED = min(SPEED + 1, MAX_SPEED)

    # Отрисовка счёта
    point_surface = font.render(f"Score: {point}", True, BLACK)
    DISPLAYSURFACE.blit(point_surface, (SCREEN_WIDTH - 200, 20))

    pygame.display.update()
    FramePerSecond.tick(FPS)