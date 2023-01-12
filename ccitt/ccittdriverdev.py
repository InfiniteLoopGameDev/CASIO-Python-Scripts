from PIL import Image
import casioplot

import ccittdecoder

# Checks if running on calculator
# If so, displays available images and imports it
if not "casioplot_settings" in dir(casioplot):
    import image
    print("Available images:")
    for image_name in dir(image):
        if not image_name.startswith("__"):
            print(image_name)
    del image
    image_name = input("Enter image name: ")
    exec("from image import " + image_name + " as img_data")


if __name__ == "__main__":
    casioplot.casioplot_settings.casio_graph_90_plus_e()
    casioplot.casioplot_settings.set(width=129)
    casioplot.casioplot_settings.set(height=65)
    casioplot.casioplot_settings.set(top_margin=0)
    casioplot.casioplot_settings.set(image_format="bmp")
    casioplot.casioplot_settings.set(filename="casioplot.bmp")
    file_data = open("images/frame2.bin", "rb").read()
    width = file_data[0]
    img_data = file_data[1:]
    del file_data
    decoder = ccittdecoder.CCITTDecoder(width, img_data)
    decoder.decode_to_image()
    casioplot.show_screen()
    img = Image.open("casioplot.bmp")
    newImage = img.crop((0, 0, 128, 64))
    newImage.save("casioplot.bmp")
