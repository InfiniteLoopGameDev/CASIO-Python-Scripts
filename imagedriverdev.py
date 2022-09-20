import casioplot
from images import *
from PIL import Image


def decode_image(image_array):
    count_x = 0
    for line in image_array:
        count_y = 0
        for i in line:
            for j in range(0, i[0]):
                count_y += 1
                if i[1] == "1":
                    colour = (0, 0, 0)
                elif i[1] == "0":
                    colour = (255, 255, 255)
                else:
                    print("File Corrupted")
                    raise Exception
                casioplot.set_pixel(count_x, count_y, colour)
        count_x += 1


if __name__ == "__main__":
    casioplot.casioplot_settings.casio_graph_90_plus_e()
    casioplot.casioplot_settings.set(width=129)
    casioplot.casioplot_settings.set(height=65)
    casioplot.casioplot_settings.set(image_format="bmp")
    casioplot.casioplot_settings.set(filename="casioplot.bmp")
    decode_image(infinity)
    casioplot.show_screen()
    img = Image.open("casioplot.bmp")
    newImage = img.crop((0, 24, 128, 88))
    newImage.save("casioplot.bmp")
