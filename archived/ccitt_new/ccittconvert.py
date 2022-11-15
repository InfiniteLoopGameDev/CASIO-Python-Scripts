from PIL import Image
from sys import argv


class ArgumentError(Exception):
    def __init__(self):
        self.__message = "Script takes in 1 or 2 arguments"
        super().__init__(self.__message)


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


def to_bin(data: bytes, width: int, output: str):
    bin_width = width.to_bytes(1, "little")
    bin_data = bin_width + data
    file = open(output, "wb")
    file.write(bin_data)


if __name__ == "__main__":
    arguments = argv
    arguments.pop(0)

    if len(arguments) < 1 or len(arguments) > 2:
        raise ArgumentError
    elif len(arguments) == 1:
        input_file = arguments[0]
        output_file = "".join((arguments[0].split(".")[0], ".bin"))
    else:
        input_file = arguments[0]
        output_file = arguments[1]

    img = open(input_file, "rb")
    img_data = image_extract(img.read())
    img_width = Image.open(input_file).size[0]
    to_bin(img_data, img_width, output_file)
