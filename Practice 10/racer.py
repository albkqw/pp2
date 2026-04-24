import pygame
import random

pygame.init()

RUNNING = True
FPS = 60
FramePerSecond = pygame.time.Clock()

# цвета
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ИНФО
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
SPEED = 5
PLAYER_HEIGHT = 750
PLAYER_SPEED = 15

DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURFACE.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('racer_images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
    
    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('racer_images/hero.png')
        self.rect = self.image.get_rect()
        self.rect.center = (160, PLAYER_HEIGHT)
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-PLAYER_SPEED, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(PLAYER_SPEED, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('racer_images/coin.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 40), PLAYER_HEIGHT)
    
    def move(self):
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

    def respawn(self):
        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 40),
            random.randint(-100, -40)  # чуть выше экрана
        )

# Sprites
Player1 = Player()
Enemy1 = Enemy()
Coin1 = Coin()
Coin2 = Coin()
Coin3 = Coin()

# Sprites Groups
enemies = pygame.sprite.Group(Enemy1)
coins = pygame.sprite.Group(Coin1, Coin2)
all_sprites = pygame.sprite.Group(Player1, Enemy1, Coin1, Coin2, Coin3)

# добавление нового User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

point = 0
font = pygame.font.Font(None, 36)
point_surface = font.render(str(point), True, (0, 0, 0))

while RUNNING:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED = min(SPEED + 1, 20)
        if event.type == pygame.QUIT:
            RUNNING = False
    
    DISPLAYSURFACE.fill(WHITE)
    
    # движение и рисовка всех Sprites
    for entity in all_sprites:
        DISPLAYSURFACE.blit(entity.image, entity.rect)
        entity.move()

    # столкновение Player и Enemy
    if pygame.sprite.spritecollideany(Player1, enemies):
        pygame.mixer.Sound("racer_sounds/crash.wav").play()
        DISPLAYSURFACE.fill(RED) 
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        game_over_font = font.render("Game Over", True, (0, 0, 0))
        game_over_rect = game_over_font.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        DISPLAYSURFACE.blit(game_over_font, game_over_rect)

        pygame.display.update()
        pygame.time.delay(1000) 
        pygame.quit()
        RUNNING = False

    collected_coins = pygame.sprite.spritecollide(Player1, coins, False)
    for coin in collected_coins:
        pygame.mixer.Sound("racer_sounds/bell.wav").play()
        coin.respawn()
        point += 1
        point_surface = font.render(str(point), True, (0, 0, 0))
    
    DISPLAYSURFACE.blit(point_surface, (SCREEN_WIDTH-30, 20))
    pygame.display.update()
    FramePerSecond.tick(FPS)