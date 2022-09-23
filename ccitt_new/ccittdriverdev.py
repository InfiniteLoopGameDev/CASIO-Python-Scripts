import ccittdecoder
import ccittcodes

if __name__ == "__main__":
    file_data = open("../frame.bin", "rb").read()
    white = ccittcodes.load_white_codes()
    black = ccittcodes.load_black_codes()
    count = 0

    for i in white:
        print(i, [i.bits_used, i.mask, i.value, i.c_color, i.pixels, i.terminating])
        count += 1

    # decoder = ccittdecoder.CCITTDecoder(128, file_data)
    # img = decoder.decode()
    # print(img)