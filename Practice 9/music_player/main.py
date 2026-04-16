import pygame
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((800, 400))
font = pygame.font.SysFont("Arial", 28)
player = MusicPlayer("music")

running = True
while running:
    screen.fill((25, 25, 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.previous()
            elif event.key == pygame.K_q:
                running = False

    # визуализация
    track_text = font.render(f"Track: {player.get_current_track_name()}", True, (255,255,255))
    status_text = font.render(f"Status: {'Playing' if player.playing else 'Stopped'}", True, (200,200,200))
    time_text = font.render(f"Time: {player.get_position()} sec", True, (180,180,180))

    screen.blit(track_text, (50, 100))
    screen.blit(status_text, (50, 150))
    screen.blit(time_text, (50, 200))

    pygame.display.flip()

pygame.quit()