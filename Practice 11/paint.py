import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mini Paint")
    clock = pygame.time.Clock()

    # Холст (рисуем на нем)
    canvas = pygame.Surface((800, 600))
    canvas.fill((255, 255, 255))

    radius = 8
    mode = 'blue'
    tool = 'brush'

    drawing = False
    start_pos = None

    # Цвета
    colors = {
        'blue': (0, 0, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'white': (255, 255, 255)
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # инструменты
                if event.key == pygame.K_b:
                    tool = 'brush'
                elif event.key == pygame.K_x:
                    tool = 'eraser'
                elif event.key == pygame.K_r:
                    tool = 'rect'
                elif event.key == pygame.K_s:
                    tool = 'square'
                elif event.key == pygame.K_t:
                    tool = 'r_triangle'
                elif event.key == pygame.K_e:
                    tool = 'eq_triangle'
                elif event.key == pygame.K_h:
                    tool = 'rhombus'

                # цвета
                if event.key == pygame.K_1:
                    mode = 'red'
                elif event.key == pygame.K_2:
                    mode = 'green'
                elif event.key == pygame.K_3:
                    mode = 'blue'

            # НАЖАТИЕ МЫШИ
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos

            # ОТПУСКАНИЕ МЫШИ → рисуем фигуру
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    if tool == 'rect':
                        draw_rect(canvas, colors[mode], start_pos, end_pos)

                    elif tool == 'square':
                        draw_square(canvas, colors[mode], start_pos, end_pos)

                    elif tool == 'r_triangle':
                        draw_right_triangle(canvas, colors[mode], start_pos, end_pos)

                    elif tool == 'eq_triangle':
                        draw_equilateral_triangle(canvas, colors[mode], start_pos, end_pos)

                    elif tool == 'rhombus':
                        draw_rhombus(canvas, colors[mode], start_pos, end_pos)

            # ДВИЖЕНИЕ МЫШИ (кисть / ластик)
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'brush':
                        pygame.draw.circle(canvas, colors[mode], event.pos, radius)

                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, colors['white'], event.pos, radius * 2)

        # вывод холста
        screen.blit(canvas, (0, 0))

        # предпросмотр фигуры
        if drawing and tool not in ['brush', 'eraser']:
            current_pos = pygame.mouse.get_pos()

            if tool == 'rect':
                draw_rect(screen, colors[mode], start_pos, current_pos, 2)

            elif tool == 'square':
                draw_square(screen, colors[mode], start_pos, current_pos, 2)

            elif tool == 'r_triangle':
                draw_right_triangle(screen, colors[mode], start_pos, current_pos, 2)

            elif tool == 'eq_triangle':
                draw_equilateral_triangle(screen, colors[mode], start_pos, current_pos, 2)

            elif tool == 'rhombus':
                draw_rhombus(screen, colors[mode], start_pos, current_pos, 2)

        pygame.display.flip()
        clock.tick(60)


# Прямоугольник
def draw_rect(surface, color, start, end, width=0):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(surface, color, (x, y, w, h), width)


# Квадрат (равные стороны)
def draw_square(surface, color, start, end, width=0):
    size = min(abs(start[0] - end[0]), abs(start[1] - end[1]))
    x = start[0]
    y = start[1]
    pygame.draw.rect(surface, color, (x, y, size, size), width)


# Прямоугольный треугольник
def draw_right_triangle(surface, color, start, end, width=0):
    points = [
        start,
        (start[0], end[1]),
        end
    ]
    pygame.draw.polygon(surface, color, points, width)


# Равносторонний треугольник
def draw_equilateral_triangle(surface, color, start, end, width=0):
    side = abs(end[0] - start[0])
    height = side * math.sqrt(3) / 2

    p1 = (start[0], start[1])
    p2 = (start[0] + side, start[1])
    p3 = (start[0] + side / 2, start[1] - height)

    pygame.draw.polygon(surface, color, [p1, p2, p3], width)


# Ромб
def draw_rhombus(surface, color, start, end, width=0):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2

    points = [
        (cx, start[1]),  # верх
        (end[0], cy),    # право
        (cx, end[1]),    # низ
        (start[0], cy)   # лево
    ]

    pygame.draw.polygon(surface, color, points, width)


main()