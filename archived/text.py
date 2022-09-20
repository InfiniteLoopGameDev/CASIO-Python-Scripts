import casioplot as casio
import math
str = input("Input text: ")
lines = []
index = 0
tmpStr = ""
characterNum = round(128 / 13)
linesNum = len(str) / characterNum
linesNum = math.ceil(linesNum)
for i in range(0, linesNum):
    for j in range(0, characterNum):
        try:
            tmpStr += str[index + j]
        except IndexError:
            pass
    lines.append(tmpStr)
    tmpStr = ""
    index += characterNum
for i in range(0, len(lines)):
    casio.draw_string(0, (i * 17), lines[i])
casio.show_screen()