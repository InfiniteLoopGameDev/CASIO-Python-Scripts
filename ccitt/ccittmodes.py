import modecodes


class modeCode:
    BitsUsed = 0
    Value = 0
    Mask = 0
    Type = 0

    def Matches(self, data: int):
        return data & self.Mask == self.Value

    def GetVerticalOffset(self):
        if self.Type == modecodes.VerticalZero:
            return 0
        elif self.Type == modecodes.VerticalL1:
            return -1
        elif self.Type == modecodes.VerticalR1:
            return 1
        elif self.Type == modecodes.VerticalL2:
            return -2
        elif self.Type == modecodes.VerticalR2:
            return 2
        elif self.Type == modecodes.VerticalL3:
            return -3
        elif self.Type == modecodes.VerticalR3:
            return 3
        else:
            return 0


modeCodes = [
    0x1, 4, 1,
    0x1, 3, 2,
    0x1, 1, 3,  # 1
    0x03, 3, 4,  # 011
    0x03, 6, 5,  # 0000 11
    0x03, 7, 6,  # 0000 011
    0x2, 3, 7,  # 010
    0x02, 6, 8,  # 0000 10
    0x02, 7, 9,  # 0000 010
    0x01, 7, 10,  # 0000 010
]


def getModes():
    modes = []
    for i in range(0, int(len(modeCodes) / 3)):
        modes.append(0)

    for i in range(0, int(len(modeCodes) / 3)):
        code = modeCode()
        code.BitsUsed = 0xff & (modeCodes[i * 3 + 1])
        code.Value = 0xff & (modeCodes[i * 3] << (8 - code.BitsUsed))
        code.Mask = 0xff
        code.Mask = 0xff & (code.Mask << (8 - code.BitsUsed))
        code.Type = 0xff & (modeCodes[i * 3 + 2])
        modes[i] = code
    return modes
