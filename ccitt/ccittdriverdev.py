import casioplot
from PIL import Image
import bitbuffer


class modeCode:
    BitsUsed = 0
    Value = 0
    Mask = 0
    Type = 0


modeCodes = [
    0x1, 4, 1,
    0x1, 3, 2,
    0x1, 1, 3,  # 1
    0x03, 3, 4,  # 011
    0x03, 6, 5,  # 0000 11
    0x03, 7, 6,  # 0000 011
    0x2, 3, 7,  # 010
    0x02, 6, 8,  # 0000 10
    0x02, 7, 9,  # 0000 010
    0x01, 7, 10,  # 0000 010
]


def getModes():
    modes = []
    for i in range(0, len(modeCodes) / 3):
        modes.append(0)

    for i in range(0, len(modeCodes) / 3):
        code = modeCode
        code.BitsUsed = modeCodes[i * 3 + 1]
        code.Value = modeCodes[i * 3] << (8 - code.BitsUsed)
        code.Mask = 0xff
        code.Mask = code.Mask << (8 - code.BitsUsed)
        code.Type = modeCodes[i * 3 + 2]
        modes[i] = code
    return modes


class CCITTDecoder:
    def __init__(self, width: int, bytes: bytes):
        width = width
        horizontal_codes = newHorizontalCodes()
        modeCodes = getModes()
        buffer = newBitBuffer(bytes)


if __name__ == "__main__":
    casioplot.casioplot_settings.casio_graph_90_plus_e()
    casioplot.casioplot_settings.set(width=129)
    casioplot.casioplot_settings.set(height=65)
    casioplot.casioplot_settings.set(image_format="bmp")
    casioplot.casioplot_settings.set(filename="../casioplot.bmp")
    decode_image(infinity)
    casioplot.show_screen()
    img = Image.open("../casioplot.bmp")
    newImage = img.crop((0, 24, 128, 88))
    newImage.save("casioplot.bmp")
