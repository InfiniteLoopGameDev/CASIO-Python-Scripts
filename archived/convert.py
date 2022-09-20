from PIL import Image


def makeNewFile(file):
    img = Image.open(file)

    maxSize = 128, 64
    img.thumbnail(maxSize)
    newImage = Image.new("RGBA", maxSize)
    box = tuple((n - o) // 2 for n, o in zip(maxSize, img.size))
    newImage.paste(img, box)
    newImage.show()
    newImage = newImage.convert("1")

    return newImage


def toArray(img):

    imgW, imgH = img.size

    imgArray = []
    lineArray = []

    for i in range(1, imgW):
        for j in range(1, imgH):
            pixVal = img.getpixel((i, j))
            if pixVal == 255:
                lineArray.append(0)
            else:
                lineArray.append(1)

        imgArray.append(lineArray)
        lineArray = []

    return imgArray


def arrayToPython(array):
    sample = open("../sample.txt")
    sampleData = sample.read()
    file = open("image.py", 'w')
    file.write("import casioplot\r\nimageArray = ")
    print(array, file=file)
    file.write(sampleData)


if __name__ == "__main__":
    # file = input("Enter file path / name: ")
    file = "../convert.png"
    image = makeNewFile(file)
    imgArray = toArray(image)
    arrayToPython(imgArray)
    image.show()



