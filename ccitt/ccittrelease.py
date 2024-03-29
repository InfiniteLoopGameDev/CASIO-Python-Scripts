#!/bin/python
import shutil
import os
import argparse
import copy

import python_minifier

line_removal = ["casioplot.casioplot_settings", "from PIL", "Image", "__name__"]
# noinspection SpellCheckingInspection
line_replace = [
    ["file_data = open("],
    ["file_data = bytes([int(img_data[i:i + 2],"
     "16) for i in range(0, len(img_data), "
     "2)])\ndel img_data\n"]
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--emulator", help="Shortens file names to be able to be imported into the emulator",
                        action="store_true")
    args = parser.parse_args()

    if not os.path.exists("releases/ccitt/"):
        os.makedirs("releases/ccitt/")

    # Process ccittdriverdev.py
    final = []
    with open("ccitt/ccittdriverdev.py") as file:
        data = file.readlines()
    past_main = False
    for line in data:
        newline = line
        newline = newline.replace('casioplot.casioplot_settings.get("width")', '128')
        if past_main:
            newline = newline.replace("    ", "")

        if "if __name__ == \"__main__\":" in newline:
            past_main = True

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
    copy_list = ["bitbuffer.py", "ccittcodes.py", "ccittdecoder.py", "ccittmodes.py", "modecodes.py"]
    for i in copy_list:
        source = "ccitt/" + i
        destination = "releases/ccitt/" + i
        shutil.copy2(source, destination)

    # Rename files if necessary
    if args.emulator:
        original_names = copy.deepcopy(os.listdir("releases/ccitt/"))
        for file in original_names:
            file = str(file).split(".")[0]
            with open("releases/ccitt/" + file + ".py", "r") as f:
                all_lines = f.read()
            for name in original_names:
                name = str(name).split(".")[0]
                print(name)
                all_lines = all_lines.replace(name, name[:8])
            with open("releases/ccitt/" + file + ".py", "w") as f:
                f.write(all_lines)
            os.rename("releases/ccitt/" + file + ".py", "releases/ccitt/" + file[:8] + ".py")

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
