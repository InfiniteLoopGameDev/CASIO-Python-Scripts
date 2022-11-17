#!/bin/python

from PIL import Image
import argparse


class FileTypeError(Exception):
    def __init__(self):
        self.__message = "File is not of TIFF format"
        super().__init__(self.__message)


def image_extract(source: bytes):
    if source[0] == 0x49:
        order = "little"
    elif source[0] == 0x4D:
        order = "big"
    else:
        raise FileTypeError
    data_end = int.from_bytes(source[4:7], order)
    data = source[8:data_end]
    return data


if __name__ == "__main__":
    # Argument Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Source (.tiff) file location")
    parser.add_argument("destination", nargs="?", help="Output (.bin) file location")
    parser.add_argument("-H", "--hexdump", help="Output to terminal directly", action="store_true")
    args = parser.parse_args()

    # Set destination to be source if not empty
    if not args.destination:
        dest = args.source
        dest = "".join(dest.split(".")[:-1])
        dest += ".bin"
    else:
        dest = args.destination

    # Extract data from source file
    with open(args.source, "rb") as file:
        file_data = file.read()

    width = Image.open(args.source).size[0].to_bytes(1, "little")
    raw_data = image_extract(file_data)
    full_data = width + raw_data

    if args.hexdump:
        # Hexdump
        print(full_data.hex().upper())
        exit(0)
    else:
        # Write to destination
        with open(dest, "wb") as file:
            file.write(full_data)
