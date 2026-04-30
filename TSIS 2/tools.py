import pygame
import math
from datetime import datetime
from collections import deque


def draw_pencil(surface, color, start, end, width):
    pygame.draw.line(surface, color, start, end, width)


def draw_line(surface, color, start, end, width):
    pygame.draw.line(surface, color, start, end, width)


def draw_rect(surface, color, start, end, width):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(surface, color, (x, y, w, h), width)


def draw_square(surface, color, start, end, width):
    size = min(abs(start[0] - end[0]), abs(start[1] - end[1]))
    pygame.draw.rect(surface, color, (start[0], start[1], size, size), width)


def draw_circle(surface, color, start, end, width):
    radius = int(math.dist(start, end))
    pygame.draw.circle(surface, color, start, radius, width)


def draw_right_triangle(surface, color, start, end, width):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start, end, width):
    side = abs(end[0] - start[0])
    height = side * math.sqrt(3) / 2
    points = [
        (start[0], start[1]),
        (start[0] + side, start[1]),
        (start[0] + side // 2, start[1] - height)
    ]
    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, start, end, width):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    points = [(cx, start[1]), (end[0], cy), (cx, end[1]), (start[0], cy)]
    pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, fill_color, width, height):
    target_color = surface.get_at(start_pos)

    # если цвет уже такой же — ничего не делаем
    if target_color == fill_color:
        return

    queue = deque([start_pos])

    while queue:
        x, y = queue.popleft()

        # проверка границ
        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        # если цвет другой — пропускаем
        if surface.get_at((x, y)) != target_color:
            continue

        # закрашиваем пиксель
        surface.set_at((x, y), fill_color)

        # добавляем соседей
        queue.extend([
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1)
        ])


def save_canvas(surface):
    filename = datetime.now().strftime('drawing_%Y%m%d_%H%M%S.png')
    pygame.image.save(surface, filename)
    print(f'Saved: {filename}')


# финальный рендер текста
def render_text(surface, text, pos, color, font):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)


# временный предпросмотр текста
def preview_text(surface, text, pos, color, font):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)


# выбор нужной фигуры
def draw_shape(tool, surface, color, start, end, width):
    if tool == 'line':
        draw_line(surface, color, start, end, width)
    elif tool == 'rect':
        draw_rect(surface, color, start, end, width)
    elif tool == 'circle':
        draw_circle(surface, color, start, end, width)
    elif tool == 'square':
        draw_square(surface, color, start, end, width)
    elif tool == 'r_triangle':
        draw_right_triangle(surface, color, start, end, width)
    elif tool == 'eq_triangle':
        draw_equilateral_triangle(surface, color, start, end, width)
    elif tool == 'rhombus':
        draw_rhombus(surface, color, start, end, width)
