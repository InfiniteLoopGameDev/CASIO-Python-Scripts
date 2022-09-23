from PIL import Image
import casioplot

import ccittdecoder


if __name__ == "__main__":
    casioplot.casioplot_settings.casio_graph_90_plus_e()
    casioplot.casioplot_settings.set(width=129)
    casioplot.casioplot_settings.set(height=65)
    casioplot.casioplot_settings.set(top_margin = 0)
    casioplot.casioplot_settings.set(image_format="bmp")
    casioplot.casioplot_settings.set(filename="../casioplot.bmp")
    file_data = open("../frame.bin", "rb").read()
    decoder = ccittdecoder.CCITTDecoder(128, file_data)
    decoder.decode_to_image()
    casioplot.show_screen()
    img = Image.open("../casioplot.bmp")
    newImage = img.crop((0, 0, 1, 63))
    newImage.save("casioplot.bmp")