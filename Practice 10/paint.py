import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    canvas = pygame.Surface((640, 480))
    canvas.fill((255, 255, 255))

    radius = 10
    mode = 'blue'
    tool = 'brush'

    drawing = False
    start_pos = None

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
                elif event.key == pygame.K_r:
                    tool = 'rect'
                elif event.key == pygame.K_c:
                    tool = 'circle'
                elif event.key == pygame.K_e:
                    tool = 'eraser'

                # цвета
                if event.key == pygame.K_1:
                    mode = 'red'
                elif event.key == pygame.K_2:
                    mode = 'green'
                elif event.key == pygame.K_3:
                    mode = 'blue'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    if tool == 'rect':
                        draw_rect(canvas, colors[mode], start_pos, end_pos)
                    elif tool == 'circle':
                        draw_circle(canvas, colors[mode], start_pos, end_pos)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'brush':
                        pygame.draw.circle(canvas, colors[mode], event.pos, radius)

                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, colors['white'], event.pos, radius * 2)

        # отрисовка
        screen.blit(canvas, (0, 0))

        # предпросмотр фигуры
        if drawing and tool in ['rect', 'circle']:
            current_pos = pygame.mouse.get_pos()
            if tool == 'rect':
                draw_rect(screen, colors[mode], start_pos, current_pos, 2)
            elif tool == 'circle':
                draw_circle(screen, colors[mode], start_pos, current_pos, 2)

        pygame.display.flip()
        clock.tick(60)


def draw_rect(surface, color, start, end, width=0):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(surface, color, (x, y, w, h), width)


def draw_circle(surface, color, start, end, width=0):
    radius = int(((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, width)


main()