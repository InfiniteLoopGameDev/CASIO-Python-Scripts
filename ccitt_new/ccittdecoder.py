import bitbuffer
import ccittmodes
import ccittcodes
import modecodes


class CCITTDecoder:
    reverse_color = True

    def __init__(self, width: int, bytes: bytes):
        self.width = width
        self.horizontal_codes = ccittcodes.HorizontalCodes()
        self.modeCodes = ccittmodes.GetModes()
        self.buffer = bitbuffer.BitBuffer(bytes)

    def decode(self) -> list:
        __lines = []
        __line = [0] * self.width
        __line_pos = 0
        __cur_line = 0
        __a0color = 0xff

        while self.buffer.has_data():
            if __line_pos > int(self.width) - 1:
                __lines.append(__line)
                __line = [0] * self.width
                __line_pos = 0
                __a0color = 0xff
                __cur_line += 1
                if end_of_block(self.buffer.buffer):
                  break

            __v, _ = self.buffer.peak_32()
            if __v == 0x00000000:
                break

            __mode = self.get_mode()
            self.buffer.flush_bits(__mode.bits_used)

            if __mode.type == modecodes.PASS:
                _, __b2 = find_b_values(get_previous_line(__lines, __cur_line, self.width), __line_pos, __a0color, False)
                for p in range(__line_pos, __b2):
                    __line[__line_pos] = __a0color
                    __line_pos += 1
            elif __mode.type == modecodes.HORIZONTAL:
                __is_white = __a0color == 0xff

                __length = [0, 0]
                __color = [127, 127]
                for i in range(0, 2):
                    __scan = True
                    while __scan:
                        __h = self.horizontal_codes.find_match_32(self.buffer.buffer, __is_white)
                        self.buffer.flush_bits(__h.bits_used)
                        __length[i] += __h.pixels
                        __color[i] = 0xff & abs(__h.c_color)

                        if __h.terminating:
                            __is_white = not __is_white
                            __scan = False

                for i in range(0 , 2):
                    for p in range(0, __length[i]):
                        if __line_pos < len(__line):
                            __line[__line_pos] = __color[i]
                        __line_pos += 1

            elif __mode.type == modecodes.VERTICAL_ZERO:
                pass
            elif __mode.type == modecodes.VERTICAL_L1:
                pass
            elif __mode.type == modecodes.VERTICAL_R1:
                pass
            elif  __mode.type == modecodes.VERTICAL_L2:
                pass
            elif  __mode.type == modecodes.VERTICAL_R2:
                pass
            elif  __mode.type == modecodes.VERTICAL_L3:
                pass
            elif  __mode.type == modecodes.VERTICAL_R3:
                __offset = __mode.get_vertical_offset()
                __b1, _ = find_b_values(get_previous_line(__lines, __cur_line, self.width), __line_pos, __a0color, True)

                for i in range(__line_pos, __b1+__offset):
                    if __line_pos < len(__line):
                        __line[__line_pos] = __a0color

                    __line_pos += 1

                __a0color = reverse_color(__a0color)

        if self.reverse_color:
            for i in range(0, len(__lines)):
                for x in range(0, len(__lines[i])):
                    __lines[i][x] = reverse_color(__lines[i][x])

        return __lines


def reverse_color(current: int) -> int:
    if current == 0:
        return 0xff
    else:
        return 0


def end_of_block(buffer: int) -> bool:
    return (buffer & 0xffffff00) == 0x00100100


def get_previous_line(lines: array, current_line: int, width: int) -> bytes:
    if current_line == 0:
        return b"\255" * width
    else:
        return lines[current_line - 1]

def find_b_values(refline: bytes, a0pos: int, a0color: int, justb1: bool) -> (int, int):
    b1 = 0
    b2 = 0
    other = reverse_color(a0color)
    start_pos = a0pos
    start_pos += 1 if start_pos != 0 else 0

    for i in range(start_pos, len(refline)):
        cur_color = bytes()
        last_color = bytes()
        if i == 0:
            cur_color = refline[0]
            last_color = b"\xff"
        else:
            cur_color = refline[i]
            last_color = refline[i-1]

        if b1 != 0:
            if cur_color == a0color and last_color == other:
                b2 = i
                return b1, b2

        if cur_color == other and last_color == a0color:
            b1 = i
            if b2 != 0 or justb1:
                b2 = i
                return b1, b2

    if b1 == 0:
        b1 = len(refline)
    else:
        b2 = len(refline)

    return b1, b2
          