from sys import argv


class ArgumentError(Exception):
    super().__init__("Accepts a maximum of 2 argument")


def image_extract(source: bytes):
    data_end = int.from_bytes(source[4:7], "little")
    data = file[8:data_end]
    return data


def array_to_file(data: bytes, filename: str, image_name: str):
    file = open(f"{filename}", 'a')
    file.write(f"{image_name} = ")
    print(data, file=file)
    file.close()


if __name__ == "__main__":
    arguments = argv
    arguments.pop(0)
    if len(arguments) > 2:
        raise ArgumentError()
    elif len(arguments) == 0:
        file = "convert.tiff"
        destination = "images.py"
    else:
        file = arguments[0]
        try: destination = arguments[1]
        except IndexError: destination = "images.py"
    img = open(file, "rb")
    img_data = image_extract(img.read())
    img_name = file.split(".")[0]
    array_to_file(img_data, destination, img_name)

