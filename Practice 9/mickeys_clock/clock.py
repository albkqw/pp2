import pygame
import time

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.center = (400, 300)

        # загрузка изображений
        self.clock_img = pygame.image.load('images/clock_face.png')
        self.clock_img = pygame.transform.scale(self.clock_img, (800, 600))

        self.hand = pygame.image.load('images/hand.png')
        self.hand = pygame.transform.scale(self.hand, (300, 300))

    def rotate_center(self, image, angle, center):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=center)
        return rotated_image, new_rect

    def draw(self):
        # текущее время
        current_time = time.localtime()
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        # углы
        minute_angle = -(minutes * 6)
        second_angle = -(seconds * 6)

        # вращение
        minute_hand, minute_rect = self.rotate_center(self.hand, minute_angle, self.center)
        second_hand, second_rect = self.rotate_center(self.hand, second_angle, self.center)

        # рисуем
        self.screen.blit(self.clock_img, (0, 0))
        self.screen.blit(minute_hand, minute_rect.topleft)
        self.screen.blit(second_hand, second_rect.topleft)