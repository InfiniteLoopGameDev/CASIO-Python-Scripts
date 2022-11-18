from casioplot import set_pixel

import ccittcodes, ccittmodes

# Whether decoded image should be inverted
reverse_color = True

# Static mode_code values
PASS = 1
HORIZONTAL = 2
VERTICAL_ZERO = 3
VERTICAL_R1 = 4
VERTICAL_R2 = 5
VERTICAL_R3 = 6
VERTICAL_L1 = 7
VERTICAL_L2 = 8
VERTICAL_L3 = 9
EXTENSION = 10

# Get codes from respective modules
horizontal_codes = ccittcodes.get_horizontal_codes()
mode_codes = ccittmodes.get_mode_codes()

# Defining global variables
source = []
lines = []
line_pos = (0, 0)
cur_color = 0xff
buffer = 0
empty_bits = 32


# Bit Buffer
def fill_buffer():
    global empty_bits, buffer
    while empty_bits > 7:
        __pad_right = empty_bits - 8
        __zeroed = buffer >> (8 + __pad_right) << (8 + __pad_right)
        buffer = 0xffffffff & (__zeroed | (0xffffffff & source[0]) << __pad_right)
        empty_bits = 0xff & (empty_bits - 8)
        source.pop(0)


def flush_bits(count: int):
    global buffer, empty_bits
    buffer = 0xffffffff & (buffer << count)
    empty_bits = 0xff & (empty_bits + count)
    fill_buffer()


def peak_8() -> (int, int):
    return 0xff & buffer >> 24, 0xff & (32 - empty_bits)


def peak_32() -> (int, int):
    return 0xffffffff & buffer, 0xff & (32 - empty_bits)


# Horizontal Codes
def find_match(data: int, is_white: bool) -> tuple[int, int, int, int, int]:
    data = 0xffff & abs(data >> 16)
    for i in horizontal_codes[not is_white]:
        if (0xffff & data) & i[1] == i[2]:
            return i


def decode_to_image(width: int, source_data: list):
    global line_pos
    global lines
    global cur_color
    global source
    source = source_data
    lines.append([0] * width)
