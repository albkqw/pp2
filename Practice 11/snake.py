import pygame
import random
import time  

pygame.init()

# настройки экрана
WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (200, 200, 0)
BLACK = (0, 0, 0)

snake = [(100, 100), (80, 100), (60, 100)]
dx, dy = CELL, 0

def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:
            weight = random.choice([1, 2, 3])  # разный вес еды
            
            # время жизни еды (в секундах)
            lifetime = random.randint(5, 10)

            return {
                "pos": (x, y),
                "weight": weight,
                "spawn_time": time.time(),
                "lifetime": lifetime
            }

food = generate_food()

# счет и уровень
score = 0
level = 1
speed = 7

RUNNING = True

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL
            if event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL, 0
            if event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL, 0

    # Движение змейки
    head_x = snake[0][0] + dx
    head_y = snake[0][1] + dy
    new_head = (head_x, head_y)

    # выход за границы
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        print("Game Over (wall)")
        RUNNING = False

    # столкновение с собой
    if new_head in snake:
        print("Game Over (self)")
        RUNNING = False

    snake.insert(0, new_head)

    # Проверка еды
    if new_head == food["pos"]:
        score += food["weight"]  # учитываем вес еды
        food = generate_food()

        # повышение уровня
        if score % 5 == 0:
            level += 1
            speed += 1

    else:
        snake.pop()

    # Проверка таймера еды
    current_time = time.time()
    if current_time - food["spawn_time"] > food["lifetime"]:
        food = generate_food()  # еда исчезла — создаем новую

    screen.fill(BLACK)

    # змейка
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    # еда (цвет зависит от веса)
    if food["weight"] == 1:
        color = RED
    elif food["weight"] == 2:
        color = YELLOW
    else:
        color = WHITE

    pygame.draw.rect(screen, color, (*food["pos"], CELL, CELL))

    # текст
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()