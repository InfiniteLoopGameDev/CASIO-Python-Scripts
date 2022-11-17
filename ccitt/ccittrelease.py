#!/bin/python
import shutil
import os

import python_minifier

line_removal = ["casioplot_settings", "from PIL", "Image", "__name__"]
line_replace = [
    ["import ccittdecoder", "file_data = open("],
    ["import ccittdecoder\nfrom image import your_image_name as img_data", "file_data = bytes([int(img_data[i:i + 2],"
                                                                           "16) for i in range(0, len(img_data), "
                                                                           "2)])\ndel img_data\n"]
]

if __name__ == "__main__":
    if not os.path.exists("releases/ccitt/"):
        os.makedirs("releases/ccitt/")

    # Process ccittdriverdev.py
    final = []
    with open("ccitt/ccittdriverdev.py") as file:
        data = file.readlines()
    for line in data:
        newline = line
        newline = newline.replace('casioplot.casioplot_settings.get("width")', '128')
        newline = newline.replace("    ", "")
        newline = newline.replace("../", "")

        if any(x in newline for x in line_removal):
            continue
        if any(x in newline for x in line_replace[0]):
            match = line_replace[0].index(next((x for x in line_replace[0] if x in newline), False))
            final.append(line_replace[1][match])
            continue
        else:
            final.append(newline)

    with open("releases/ccitt/ccittdriver.py", "w+") as file:
        file.writelines(final)

    # Copy directory
    copy_list = ["ccittcodes.py", "ccittdecoder.py", "ccittmodes.py"]
    for i in copy_list:
        source = "ccitt/" + i
        destination = "releases/ccitt/" + i
        shutil.copy2(source, destination)

    # Minify
    all_files = os.listdir("releases/ccitt/")
    for file in all_files:
        with open("releases/ccitt/" + file, "r") as source_file:
            minified = python_minifier.minify(source_file.read())
        with open("releases/ccitt/" + file, "w") as destination_file:
            destination_file.write(minified)

    # Create empty images.py
    with open("releases/ccitt/image.py", "w+") as file:
        file.writelines(['your_image_name = "hexadecimal_string_output_here"'])