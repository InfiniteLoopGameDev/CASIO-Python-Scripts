class BitBuffer:
    def __init__(self, source: bytes):
        self.empty_bits = 32
        self.buffer = 0
        self.source = source
        self.source_pos = 0
        self.TryFillBuffer()

    def TryFillBuffer(self):
        while self.empty_bits > 7:
            if self.source_pos >= len(self.source):
                break
            self.AddByte(self.source[self.source_pos])
            self.source_pos += 1

    def AddByte(self, source: bytes):
        pad_right = self.empty_bits - 8
        zeroed = self.buffer >> (8 + pad_right) << (8 + pad_right)
        self.buffer = zeroed | (source << pad_right)
        self.empty_bits -= 8

    def Clear(self):
        self.buffer = 0
        self.empty_bits = 32
        self.source_pos = 0

    def HasData(self):
        return not ((0xff & (self.empty_bits)) == 32 and int(self.source_pos) >= len(self.source))

    def Peak32(self):
        return 0xffffffff & self.buffer, 0xff & (32 - self.empty_bits)

    def Peak16(self):
        return 0xffff & int((0xffffffff & self.buffer) >> 16), 0xff & (32 - self.empty_bits)

    def Peak8(self):
        return 0xff & int((0xffffffff & self.buffer) >> 24), 0xff & (32 - self.empty_bits)

    def FlushBits(self, count: int):
        self.buffer = 0xffffffff & (self.buffer << count)
        self.empty_bits += count
        self.TryFillBuffer()
