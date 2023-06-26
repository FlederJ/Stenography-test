import png
import base64
import random

# generate a random small image for the message


def create_image(message):
    width = len(message) * 8
    height = len(message) * 8
    img = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(random.randrange(2) * 255)
        img.append(row)
    with open('original.png', 'wb') as f:
        w = png.Writer(width, height, greyscale=True)
        w.write(f, img)
    return img


PROMPT = """
Welcome to basic steganography. Please choose:

1. To encode a message into an image
2. To decode an image into a message
q. to exit
"""

ENDOFMESSAGE = "0100100101010101010101100100111101010010010001010011100101000111010101000101010101010110010101000101010100110000010001100100100001010010010100110100010100111101"


def encode_message_as_bytestring(message):
    b64 = message.encode("utf8")
    bytes_ = base64.encodebytes(b64)
    bytestring = "".join(["{:08b}".format(x) for x in bytes_])
    bytestring += ENDOFMESSAGE
    return bytestring


def get_pixels_from_image(fname):
    img = png.Reader(fname).read()
    pixels = img[2]
    return pixels


def encode_pixels_with_message(pixels, bytestring):
    '''modifies pixels to encode the contents from bytestring'''

    enc_pixels = []
    string_i = 0
    for row in pixels:
        enc_row = []
        for i, char in enumerate(row):
            if string_i >= len(bytestring):
                pixel = row[i]
            else:
                if row[i] % 2 != int(bytestring[string_i]):
                    if row[i] == 0:
                        pixel = 255
                    else:
                        pixel = row[i] - 255
                else:
                    pixel = row[i]
            enc_row.append(pixel)
            string_i += 1

        enc_pixels.append(enc_row)
    print(enc_pixels)
    return enc_pixels


def write_pixels_to_image(pixels, fname):
    png.from_array(pixels, 'L;16').save(fname)


def decode_pixels(pixels):
    bytestring = []
    for row in pixels:
        for c in row:
            bytestring.append(str(c % 2))
    bytestring = ''.join(bytestring)
    message = decode_message_from_bytestring(bytestring)
    return message


def decode_message_from_bytestring(bytestring):
    bytestring = bytestring.split(ENDOFMESSAGE)[0]
    message = int(bytestring, 2).to_bytes(len(bytestring) // 8,
                                          byteorder='big')
    message = base64.decodebytes(message).decode("utf8")
    return message


def main():
    print(PROMPT)
    user_inp = ""
    while user_inp not in ("1", "2", "q"):
        user_inp = input("Your choice: ")

    if user_inp == "1":
        #in_image = input("Please enter filename of existing PNG image: ")
        in_message = input("Please enter the message to encode: ")
        in_image = "original.png"
        img = create_image(in_message)
        #print(img)
        print("-ENCODING-")
        pixels = get_pixels_from_image(in_image)
        bytestring = encode_message_as_bytestring(in_message)
        epixels = encode_pixels_with_message(pixels, bytestring)
        print(pixels)
        write_pixels_to_image(epixels, in_image.replace(".png", "-enc.png"))
        print("[DONE] -ENCODING-")

    elif user_inp == "2":
        in_image = input(
            "Please enter the filename of an existing PNG image: ")
        print("-DECODING-")
        pixels = get_pixels_from_image(in_image)
        print(decode_pixels(pixels))
        print("[DONE] -DECODING-")


if __name__ == "__main__":
    main()
