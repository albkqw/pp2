import pygame
from clock import MickeyClock

pygame.init()

screen = pygame.display.set_mode((800, 600))
mickey_clock = MickeyClock(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # рисуем часы
    mickey_clock.draw()

    pygame.display.flip()

pygame.quit()