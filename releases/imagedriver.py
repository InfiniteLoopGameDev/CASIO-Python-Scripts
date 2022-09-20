import casioplot
from images import *


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
    decode_image(infinity)
    casioplot.show_screen()
