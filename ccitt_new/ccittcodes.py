import math


class HorizontalCode:
    bits_used = 0
    mask = 0
    value = 0
    c_color = 0
    pixels = 0
    terminating = False

    def matches(self, data: int):
        print("matches", (0xffff & data) & self.mask, self.value)
        return (0xffff & data) & self.mask == self.value


class HorizontalCodes:
    white_codes = []
    black_codes = []

    def __init__(self):
        self.white_codes = load_white_codes()
        self.black_codes = load_black_codes()

    def find_match_32(self, data: int, white: bool) -> HorizontalCode:
        print("find_match_32", (0xffff & abs(data >> 16)), white)
        return self.find_match((0xffff & abs(data >> 16)), white)

    def find_match(self, data: int, white: bool) -> HorizontalCode:
        data = 0xffff & abs(data)
        print("find_match", data, white)
        if white:
            __lookup = self.white_codes
        else:
            __lookup = self.black_codes
        for i in range(0, len(__lookup)):
            if __lookup[i].matches(data):
                return __lookup[i]


black = 0x00
white = 0xff
both = 0x7f

white_term_codes = [
    0x35, 8, 0x07, 6, 0x07, 4, 0x08, 4, 0x0b, 4, 0x0c, 4, 0x0e, 4, 0x0f, 4,
    0x13, 5, 0x14, 5, 0x07, 5, 0x08, 5, 0x08, 6, 0x03, 6, 0x34, 6, 0x35, 6,
    0x2a, 6, 0x2b, 6, 0x27, 7, 0x0c, 7, 0x08, 7, 0x17, 7, 0x03, 7, 0x04, 7,
    0x28, 7, 0x2b, 7, 0x13, 7, 0x24, 7, 0x18, 7, 0x02, 8, 0x03, 8, 0x1a, 8,
    0x1b, 8, 0x12, 8, 0x13, 8, 0x14, 8, 0x15, 8, 0x16, 8, 0x17, 8, 0x28, 8,
    0x29, 8, 0x2a, 8, 0x2b, 8, 0x2c, 8, 0x2d, 8, 0x04, 8, 0x05, 8, 0x0a, 8,
    0x0b, 8, 0x52, 8, 0x53, 8, 0x54, 8, 0x55, 8, 0x24, 8, 0x25, 8, 0x58, 8,
    0x59, 8, 0x5a, 8, 0x5b, 8, 0x4a, 8, 0x4b, 8, 0x32, 8, 0x33, 8, 0x34, 8
]

white_makeup_codes = [
    0x1b, 5, 0x12, 5, 0x17, 6, 0x37, 7, 0x36, 8, 0x37, 8, 0x64, 8, 0x65, 8,
    0x68, 8, 0x67, 8, 0xcc, 9, 0xcd, 9, 0xd2, 9, 0xd3, 9, 0xd4, 9, 0xd5, 9,
    0xd6, 9, 0xd7, 9, 0xd8, 9, 0xd9, 9, 0xda, 9, 0xdb, 9, 0x98, 9, 0x99, 9,
    0x9a, 9, 0x18, 6, 0x9b, 9
]

common_makeup_codes = [
    0x08, 11, 0x0c, 11, 0x0d, 11, 0x12, 12, 0x13, 12, 0x14, 12, 0x15, 12, 0x16, 12,
    0x17, 12, 0x1c, 12, 0x1d, 12, 0x1e, 12, 0x1f, 12
]

black_term_codes = [
    0x37, 10, 0x02, 3, 0x03, 2, 0x02, 2, 0x03, 3, 0x03, 4, 0x02, 4, 0x03, 5,
    0x05, 6, 0x04, 6, 0x04, 7, 0x05, 7, 0x07, 7, 0x04, 8, 0x07, 8, 0x18, 9,
    0x17, 10, 0x18, 10, 0x08, 10, 0x67, 11, 0x68, 11, 0x6c, 11, 0x37, 11, 0x28, 11,
    0x17, 11, 0x18, 11, 0xca, 12, 0xcb, 12, 0xcc, 12, 0xcd, 12, 0x68, 12, 0x69, 12,
    0x6a, 12, 0x6b, 12, 0xd2, 12, 0xd3, 12, 0xd4, 12, 0xd5, 12, 0xd6, 12, 0xd7, 12,
    0x6c, 12, 0x6d, 12, 0xda, 12, 0xdb, 12, 0x54, 12, 0x55, 12, 0x56, 12, 0x57, 12,
    0x64, 12, 0x65, 12, 0x52, 12, 0x53, 12, 0x24, 12, 0x37, 12, 0x38, 12, 0x27, 12,
    0x28, 12, 0x58, 12, 0x59, 12, 0x2b, 12, 0x2c, 12, 0x5a, 12, 0x66, 12, 0x67, 12
]

black_makeup_codes = [
    0x0f, 10, 0xc8, 12, 0xc9, 12, 0x5b, 12, 0x33, 12, 0x34, 12, 0x35, 12, 0x6c, 13,
    0x6d, 13, 0x4a, 13, 0x4b, 13, 0x4c, 13, 0x4d, 13, 0x72, 13, 0x73, 13, 0x74, 13,
    0x75, 13, 0x76, 13, 0x77, 13, 0x52, 13, 0x53, 13, 0x54, 13, 0x55, 13, 0x5a, 13,
    0x5b, 13, 0x64, 13, 0x65, 13
]


def get_bits_used(code: HorizontalCode) -> int:
    return code.bits_used


def load_white_codes() -> list:
    total_codes = (len(black_term_codes) + len(white_term_codes) + len(white_makeup_codes) + len(
        black_makeup_codes) + len(common_makeup_codes)) / 2
    codes = [HorizontalCode()] * math.ceil(total_codes)
    c = 0

    # white
    for i in range(0, math.ceil(len(white_term_codes) / 2)):
        code = HorizontalCode()
        code.bits_used = 0xff & abs(white_term_codes[i * 2 + 1])
        code.value = 0xffff & abs(white_term_codes[i * 2] << (16 - code.bits_used))
        code.c_color = white
        code.mask = 0xffff
        code.mask = 0xffff & abs(code.mask << (16 - code.bits_used))
        code.pixels = 0xffff & abs(i)
        code.terminating = True
        codes[c] = code
        c += 1

    # white makeup
    for i in range(0, math.ceil(len(white_makeup_codes) / 2)):
        code = HorizontalCode()
        code.bits_used = 0xff & abs(white_makeup_codes[i * 2 + 1])
        code.value = 0xffff & abs(white_makeup_codes[i * 2] << (16 - code.bits_used))
        code.c_color = white
        code.mask = 0xffff
        code.mask = 0xffff & abs(code.mask << (16 - code.bits_used))
        code.pixels = 0xffff & abs((i + 1) * 64)
        codes[c] = code
        c += 1

    # common make up
    for i in range(0, math.ceil(len(common_makeup_codes) / 2)):
        code = HorizontalCode()
        code.bits_used = 0xff & abs(common_makeup_codes[i * 2 + 1])
        code.value = 0xffff & abs(common_makeup_codes[i * 2] << (16 - code.bits_used))
        code.c_color = both
        code.mask = 0xffff
        code.mask = 0xffff & abs(code.mask << (16 - code.bits_used))
        code.pixels = 0xffff & abs((i + 1) * 64 + 1728)
        codes[c] = code
        c += 1

    return codes


def load_black_codes() -> list:
    total_codes = (len(black_term_codes) + len(white_term_codes) + len(white_makeup_codes) + len(
        black_makeup_codes) + len(common_makeup_codes)) / 2
    codes = [HorizontalCode()] * math.ceil(total_codes)
    c = 0

    # black
    for i in range(0, math.ceil(len(black_term_codes) / 2)):
        code = HorizontalCode()
        code.bits_used = 0xff & abs(black_term_codes[i * 2 + 1])
        code.value = 0xffff & abs(black_term_codes[i * 2] << (16 - code.bits_used))
        code.c_color = black
        code.mask = 0xffff
        code.mask = 0xffff & abs(code.mask << (16 - code.bits_used))
        code.pixels = 0xffff & abs(i)
        code.terminating = True
        codes[c] = code
        c += 1

    # black makeup
    for i in range(0, math.ceil(len(black_makeup_codes) / 2)):
        code = HorizontalCode()
        code.bits_used = 0xff & abs(black_makeup_codes[i * 2 + 1])
        code.value = 0xffff & abs(black_makeup_codes[i * 2] << (16 - code.bits_used))
        code.c_color = black
        code.mask = 0xffff
        code.mask = 0xffff & abs(code.mask << (16 - code.bits_used))
        code.pixels = 0xffff & abs((i + 1) * 64)
        codes[c] = code
        c += 1

    # common make up
    for i in range(0, math.ceil(len(common_makeup_codes) / 2)):
        code = HorizontalCode()
        code.bits_used = 0xff & abs(common_makeup_codes[i * 2 + 1])
        code.value = 0xffff & abs(common_makeup_codes[i * 2] << (16 - code.bits_used))
        code.c_color = both
        code.mask = 0xffff
        code.mask = 0xffff & abs(code.mask << (16 - code.bits_used))
        code.pixels = 0xffff & abs((i + 1) * 64 + 1728)
        codes[c] = code
        c += 1

    return codes
