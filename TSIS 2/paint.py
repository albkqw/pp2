import pygame
from tools import *

pygame.init()

# размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# отдельный слой для рисования
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# доступные цвета
colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255)
}

mode = 'blue'       # текущий цвет
tool = 'pencil'     # текущий инструмент

# размеры кисти
brush_sizes = {1: 2, 2: 5, 3: 10}
brush_size = brush_sizes[1]

drawing = False     # идет ли сейчас рисование
start_pos = None    # начальная точка фигуры
last_pos = None     # последняя точка для карандаша

# переменные для ввода текста
text_mode = False
text_pos = None
text_buffer = ""

running = True
while running:

    # обработка событий
    for event in pygame.event.get():

        # закрытие окна
        if event.type == pygame.QUIT:
            running = False

        # обработка клавиатуры
        if event.type == pygame.KEYDOWN:

            # ESC — выход или выход из режима текста
            if event.key == pygame.K_ESCAPE:
                if text_mode:
                    text_mode = False
                    text_buffer = ""
                else:
                    running = False

            # Ctrl + S — сохранить рисунок
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas(canvas)

            # смена размера кисти
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                brush_size = brush_sizes[int(event.unicode)]

            # выбор инструмента горячими клавишами
            tools_map = {
                pygame.K_p: 'pencil',
                pygame.K_l: 'line',
                pygame.K_r: 'rect',
                pygame.K_c: 'circle',
                pygame.K_q: 'square',
                pygame.K_t: 'r_triangle',
                pygame.K_e: 'eq_triangle',
                pygame.K_h: 'rhombus',
                pygame.K_f: 'fill',
                pygame.K_x: 'text',
                pygame.K_z: 'eraser',
                pygame.K_k: 'color_picker'
            }

            if event.key in tools_map:
                tool = tools_map[event.key]

            # ввод текста по символам
            if text_mode:
                if event.key == pygame.K_RETURN:
                    # окончательно рисуем текст
                    render_text(canvas, text_buffer, text_pos, colors[mode], font)
                    text_mode = False
                    text_buffer = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]

                else:
                    text_buffer += event.unicode

        # нажатие мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
            drawing = True
            last_pos = event.pos

            # заливка области
            if tool == 'fill':
                flood_fill(canvas, event.pos, colors[mode], WIDTH, HEIGHT)
                drawing = False

            # выбор цвета из палитры
            elif tool == 'color_picker':
                x, y = event.pos

                if 10 <= x <= 40 and 10 <= y <= 40:
                    mode = 'red'
                elif 50 <= x <= 80 and 10 <= y <= 40:
                    mode = 'green'
                elif 90 <= x <= 120 and 10 <= y <= 40:
                    mode = 'blue'

                drawing = False

            # запуск режима текста
            elif tool == 'text':
                text_mode = True
                text_pos = event.pos
                text_buffer = ""
                drawing = False

        # отпускание мыши = финальный рисунок фигуры
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos
            draw_shape(tool, canvas, colors[mode], start_pos, end_pos, brush_size)

        # движение мыши при рисовании
        if event.type == pygame.MOUSEMOTION and drawing:

            # свободное рисование
            if tool == 'pencil':
                draw_pencil(canvas, colors[mode], last_pos, event.pos, brush_size)
                last_pos = event.pos

            # ластик (рисует белым)
            elif tool == 'eraser':
                draw_pencil(canvas, (255, 255, 255), last_pos, event.pos, brush_size * 2)
                last_pos = event.pos

    # вывод холста на экран
    screen.blit(canvas, (0, 0))

    # палитра цветов
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 30, 30))
    pygame.draw.rect(screen, (0, 255, 0), (50, 10, 30, 30))
    pygame.draw.rect(screen, (0, 0, 255), (90, 10, 30, 30))

    # временный предпросмотр фигуры во время растягивания
    if drawing and tool in ['line', 'rect', 'circle', 'square', 'r_triangle', 'eq_triangle', 'rhombus']:
        temp = canvas.copy()
        current_pos = pygame.mouse.get_pos()
        draw_shape(tool, temp, colors[mode], start_pos, current_pos, brush_size)
        screen.blit(temp, (0, 0))

    # предпросмотр текста до Enter
    if text_mode:
        preview_text(screen, text_buffer, text_pos, colors[mode], font)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()