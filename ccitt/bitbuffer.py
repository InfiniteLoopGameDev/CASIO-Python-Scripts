class BitBuffer:
    def flush_bits(self, count):
        self.buffer = 0xffffffff & (self.buffer << count)
        self.empty_bits = 0xff & (self.empty_bits + count)
        self.try_fill_buffer()

    def peak_8(self):
        return 0xff & self.buffer >> 24, 0xff & (32 - self.empty_bits)

    def peak_32(self):
        return 0xffffffff & self.buffer, 0xff & (32 - self.empty_bits)

    def has_data(self) -> bool:
        return not (self.empty_bits == 32 and len(self.source) == 0)

    def try_fill_buffer(self):
        while self.empty_bits > 7:
            self.add_byte(self.source[0])
            self.source.pop(0)

    def __init__(self, source: bytes):
        self.empty_bits = 32
        self.buffer = 0
        self.source = list(source)
        del source
        self.try_fill_buffer()

    def add_byte(self, source: int):
        __pad_right = self.empty_bits - 8
        __zeroed = self.buffer >> (8 + __pad_right) << (8 + __pad_right)
        __temp_source = 0xffffffff & source
        self.buffer = 0xffffffff & (__zeroed | __temp_source << __pad_right)
        self.empty_bits = 0xff & (self.empty_bits - 8)
