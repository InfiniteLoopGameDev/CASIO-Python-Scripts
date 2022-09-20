from PIL import Image
from sys import argv


def imageFormat(file):
    img = Image.open(file)

    max_size = 128, 64
    img.thumbnail(max_size)
    new_image = Image.new("RGBA", max_size)
    box = tuple((n - o) // 2 for n, o in zip(max_size, img.size))
    new_image.paste(img, box)
    new_image = new_image.convert("1")

    return new_image


def imageToArray(img):

    imgW, imgH = img.size

    img_array = []
    line_string = ""

    for i in range(1, imgW):
        for j in range(1, imgH):
            pix_val = img.getpixel((i, j))
            if pix_val == 255:
                line_string += "0"
            else:
                line_string += "1"

        encoded_list = []
        i = 0
        while i <= len(line_string) - 1:
            count = 1
            ch = line_string[i]
            j = i
            while j < len(line_string):
                try:
                    similar = line_string[j] == line_string[j + 1]
                except IndexError:
                    similar = False
                if similar:
                    count += 1
                    j += 1
                else:
                    break
            encoded_list.append((count, ch))
            i = j + 1

        img_array.append(encoded_list)
        line_string = ""

    return img_array


def arrayToPython(array, file_location):
    file_name = file_location.split(".")[0]
    file = open(f"{file_location}", 'a')
    file.write(f"{file_name} = ")
    print(array, file=file)
    file.close()


if __name__ == "__main__":
    arguments = argv
    arguments.pop(0)
    if len(arguments) > 1:
        raise Exception()
    elif len(arguments) == 0:
        file = "convert.png"
    else:
        file = arguments[0]
    image = imageFormat(file)
    imgArray = imageToArray(image)
    arrayToPython(imgArray, file)
    image.show()
