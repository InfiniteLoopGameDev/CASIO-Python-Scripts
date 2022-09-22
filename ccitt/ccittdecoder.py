import casioplot

import bitbuffer
import ccittmodes
import ccittcodes
import modecodes

count = 0


class CCITTDecoder:
    reverse_color = True

    def __init__(self, width: int, bytes: bytes):
        self.width = width
        self.horizontal_codes = ccittcodes.HorizontalCodes()
        self.modeCodes = ccittmodes.getModes()
        self.buffer = bitbuffer.BitBuffer(bytes)

    def GetMode(self):
        b8, _ = self.buffer.Peak8()
        for i in range(0, len(self.modeCodes)):
            print(b8)
            print(self.modeCodes[i].Mask)
            print((0xff & b8) & (0xff & self.modeCodes[i].Mask))
            print(self.modeCodes[i].Value)
            if self.modeCodes[i].Matches(b8):
                global count
                count += 1
                print("end", count)
                return self.modeCodes[i]

    def Decode(self):
        lines = []
        line = []
        for i in range(0, self.width):
            line.append(0)
        line_pos = 0
        cur_line = 0
        a0Color = 255

        while self.buffer.HasData():
            print(self.buffer.buffer)
            print(lines)
            print(line)

            if line_pos > int(self.width) - 1:
                lines.append(line)
                line = []
                for i in range(0, self.width):
                    line.append(0)
                line_pos = 0
                a0Color = 255
                cur_line += 1
                if EndOfBlock(self.buffer.buffer):
                    break

            v = self.buffer.Peak32()
            if v == 0x00000000:
                break

            mode = self.GetMode()
            self.buffer.FlushBits(mode.BitsUsed)
            print(self.buffer.buffer)

            if mode.Type == modecodes.Pass:
                _, b2 = FindBValues(GetPreviousLine(lines, cur_line, self.width), line_pos, a0Color, False)
                for p in range(line_pos, b2):
                    line[line_pos] = a0Color
                    line_pos += 1
            elif mode.Type == modecodes.Horizontal:
                isWhite = a0Color == 255

                length = [0, 0]
                color = [127, 127]
                for i in range(0, 2):
                    scan = True
                    while scan:
                        h, err = self.horizontal_codes.FindMatch32(self.buffer.buffer, isWhite)
                        if err is not None:
                            return None, err
                        self.buffer.FlushBits(h.BitsUsed)
                        print(self.buffer.buffer)
                        length[i] += h.Pixels
                        color[i] = h.CColor
                        if h.Terminating:
                            isWhite = not isWhite
                            scan = False

                for i in range(0, 2):
                    for p in range(0, int(length[i])):
                        if line_pos < len(line):
                            line[line_pos] = color[i]
                        line_pos += 1
            elif mode.Type == modecodes.VerticalZero:
                pass
            elif mode.Type == modecodes.VerticalL1:
                pass
            elif mode.Type == modecodes.VerticalR1:
                pass
            elif mode.Type == modecodes.VerticalL2:
                pass
            elif mode.Type == modecodes.VerticalR2:
                pass
            elif mode.Type == modecodes.VerticalL3:
                pass
            elif mode.Type == modecodes.VerticalR3:
                offset = mode.GetVerticalOffset()
                b1, _ = FindBValues(GetPreviousLine(lines, cur_line, self.width), line_pos, a0Color, True)

                for i in range(line_pos, (b1 + offset)):
                    if line_pos < len(line):
                        line[line_pos] = a0Color
                    line_pos += 1

                a0Color = ReverseColor(a0Color)
            else:
                raise Exception()

        if self.reverse_color:
            for i in range(0, len(lines)):
                for x in range(0, len(lines[i])):
                    lines[i][x] = ReverseColor(lines[i][x])

        return lines

    def DecodeToImg(self):
        lines = self.Decode()
        for y in range(0, len(lines)):
            for x in range(0, int(self.width)):
                if len(lines[y]) > x:
                    casioplot.set_pixel(x, y, color=(0, 0, 0))


def ReverseColor(current: int):
    if current == 0:
        return 255
    else:
        return 0


def EndOfBlock(buffer: int):
    return (buffer & 0xffffff00) == 0x00100100


def GetPreviousLine(lines: list, currentLine: int, width: int):
    if currentLine == 0:
        whiteOut = []
        for i in range(0, width):
            whiteOut.append(bytes(255))
        return whiteOut
    else:
        return lines[currentLine - 1]


def FindBValues(refLine: bytes, a0pos: int, a0Color: int, justb1: bool):
    b1 = 0
    b2 = 0
    other = ReverseColor(a0Color)
    start_pos = a0pos
    if start_pos != 0:
        start_pos += 1

    for i in range(start_pos, len(refLine)):
        if i == 0:
            cur_color = bytes(refLine[0])
            last_color = bytes(255)
        else:
            cur_color = bytes(refLine[i])
            last_color = bytes(i - 1)

        if b1 != 0:
            if cur_color == a0Color and last_color == other:
                b2 = i
                return b1, b2

        if cur_color == other and last_color == a0Color:
            b1 = i
            return b1, b2

    if b1 == 0:
        b1 = len(refLine)
    else:
        b2 = len(refLine)
    return b1, b2
