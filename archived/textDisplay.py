import casioplot as casio
import math
from PIL import Image


def display_text(str, size="medium", mode="draw"):
    if mode == "draw":
        colour = (0, 0, 0)
    elif mode == "erase":
        colour = (255, 255, 255)
    lines = []
    index = 0
    tmpStr = ""
    characterNum = round(casio.casioplot_settings.get("width") / 13)
    linesNum = len(str) / characterNum
    linesNum = math.ceil(linesNum)
    for i in range(0, linesNum):
        for j in range(0, characterNum):
            try:
                tmpStr += str[index + j]
            except IndexError:
                pass
        lines.append(tmpStr)
        tmpStr = ""
        index += characterNum
    for i in range(0, len(lines)):
        casio.draw_string(0, (i * 17), lines[i], colour, size)


if __name__ == "__main__":
    casio.casioplot_settings.casio_graph_90_plus_e()
    casio.casioplot_settings.set(width=128)
    casio.casioplot_settings.set(height=64)
    casio.casioplot_settings.set(image_format="bmp")
    casio.casioplot_settings.set(filename="../casioplot.bmp")
    text = "will is a poopy head ur trash"
    display_text(text)
    casio.show_screen()
    img = Image.open("../casioplot.bmp")
    newImage = img.crop((0, 24, 128, 88))
    newImage.save("casioplot.bmp")
