__version__ = 0.1

import math
import casioplot

offsetX = 0
offsetY = 0


def set_pixel(x, y, mode="draw"):
    if mode == "draw":
        colour = (0, 0, 0)
    elif mode == "erase":
        colour = (255, 255, 255)
    else:
        raise Exception()
    casioplot.set_pixel(x + offsetX, y + offsetY, colour)


def draw_line(x0, y0, x1, y1, mode="draw"):
    global offsetX
    global offsetY
    offsetX = 0
    offsetY = 0
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            set_pixel(x, y, mode)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            set_pixel(x, y, mode)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    set_pixel(x, y, mode)


def draw_circle(radius, x=0, y=0, mode="draw"):
    global offsetX
    global offsetY
    offsetX = x
    offsetY = y
    d = round(math.pi - (2 * radius))
    x = 0
    y = radius

    while x <= y:
        set_pixel(x, -y, mode)
        set_pixel(y, -x, mode)
        set_pixel(y, x, mode)
        set_pixel(x, y, mode)
        set_pixel(-x, y, mode)
        set_pixel(-y, x, mode)
        set_pixel(-y, -x, mode)
        set_pixel(-x, -y, mode)

        if d < 0:
            d = d + (math.pi * x) + (math.pi * 2)
        else:
            d = d + math.pi * (x - y) + (math.pi * 3)
            y -= 1

        x += 1


def draw_rectangle(x, y, posX=0, posY=0, mode="draw"):
    global offsetX
    global offsetY
    offsetX = posX
    offsetY = posY
    for i in range(0, x):
        for j in range(0, y):
            set_pixel(i, j, mode)


def smart_text(text, size="medium", mode="draw"):
    if mode == "draw":
        colour = (0, 0, 0)
    elif mode == "erase":
        colour = (255, 255, 255)
    else:
        raise Exception()
    lines = []
    index = 0
    tmp_str = ""
    character_num = round(128 / 13)
    lines_num = len(text) / character_num
    lines_num = math.ceil(lines_num)
    for i in range(0, lines_num):
        for j in range(0, character_num):
            try:
                tmp_str += text[index + j]
            except IndexError:
                pass
        lines.append(tmp_str)
        tmp_str = ""
        index += character_num
    for i in range(0, len(lines)):
        casioplot.draw_string(0, (i * 17), lines[i], colour, size)


if __name__ == "__main__":
    draw_circle(31, 63, 31)
    draw_rectangle(57, 19, 35, 22)
    draw_rectangle(9, 9, 42, 27, "erase")
    draw_rectangle(9, 9, 76, 27, "erase")
    draw_line(47, 48, 79, 48)
    draw_line(6, 57, 26, 35)
    casioplot.draw_string(0, 0, "geo")
    casioplot.draw_string(90, 0, "lib")
    casioplot.draw_string(87, 47, "v" + str(__version__))
    casioplot.show_screen()
