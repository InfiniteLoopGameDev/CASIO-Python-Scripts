import math

import modecodes as mode_enums


class ModeCode:
    bits_used = 0
    mask = 0
    value = 0
    type = 0

    def get_vertical_offset(self) -> int:
        if self.type == mode_enums.VERTICAL_ZERO:
            return 0
        elif self.type == mode_enums.VERTICAL_L1:
            return -1
        elif self.type == mode_enums.VERTICAL_R1:
            return 1
        elif self.type == mode_enums.VERTICAL_L2:
            return -2
        elif self.type == mode_enums.VERTICAL_R2:
            return 2
        elif self.type == mode_enums.VERTICAL_L3:
            return -3
        elif self.type == mode_enums.VERTICAL_R3:
            return 3
        else:
            return 0

    def matches(self, data: int) -> bool:
        return (0xff & abs(data)) & self.mask == self.value


mode_codes = [
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


def GetModes() -> list:
    modes = []
    for i in range(0, math.ceil(len(mode_codes) / 3)):
        code = ModeCode()
        code.bits_used = 0xff & abs(mode_codes[i*3+1])
        code.value = 0xff & abs(mode_codes[i*3] << (8 - code.bits_used))
        code.mask = 0xff
        code.mask = 0xff & abs(code.mask << (8 - code.bits_used))
        code.type = mode_codes[i*3+2]
        modes.append(code)

    return modes
