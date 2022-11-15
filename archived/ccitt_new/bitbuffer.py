class BitBuffer:
    buffer = 0
    empty_bits = 0
    source = bytes()
    source_pos = 0

    def flush_bits(self, count):
        count = 0xff & abs(count)
        self.buffer = 0xffffffff & abs(self.buffer << count)
        self.empty_bits = 0xff & abs(self.empty_bits + count)
        self.try_fill_buffer()

    def peak_8(self):
        return 0xff & abs(self.buffer >> 24), 0xff & (32 - self.empty_bits)

    def peak_16(self):
        return 0xffff & abs(self.buffer >> 16), 0xff & (32 - self.empty_bits)

    def peak_32(self):
        return 0xffffffff & abs(self.buffer), 0xff & (32 - self.empty_bits)

    def has_data(self) -> bool:
        return not (self.empty_bits == 32 and int(self.source_pos) >= len(self.source))

    def clear(self):
        self.buffer = 0
        self.empty_bits = 32
        self.source_pos = 0

    def try_fill_buffer(self):
        while self.empty_bits > 7:
            if self.source_pos >= int(len(self.source)):
                break
            self.add_byte(self.source[self.source_pos])
            self.source_pos += 1

    def __init__(self, source: bytes):
        self.empty_bits = 32
        self.buffer = 0
        self.source = source
        self.source_pos = 0
        self.try_fill_buffer()

    def add_byte(self, source: bytes):
        __pad_right = self.empty_bits - 8
        __zeroed = self.buffer >> (8 + __pad_right) << (8 + __pad_right)
        __temp_source = 0xffffffff & abs(source)
        self.buffer = 0xffffffff & abs(__zeroed | __temp_source << __pad_right)
        self.empty_bits = 0xff & abs(self.empty_bits - 8)
