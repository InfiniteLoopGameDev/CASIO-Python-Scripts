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
