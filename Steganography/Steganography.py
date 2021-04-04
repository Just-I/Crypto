from PIL import Image, ImageDraw
from random import randint
import argparse


class Steganography:
    def __init__(self):
        pass

    def Encrypt(self, image, text, keys, new_name):
        draw = ImageDraw.Draw(image)
        pixels = image.load()
        check_pixel = set()
        for line in text:
            for symbol in line:
                bits = []
                number = ord(symbol)
                for i in range(8):
                    bits.append(number % 2)
                    number = number // 2
                for i in range(8):
                    key = (randint(1, image.size[0] - 20), randint(1, image.size[1] - 20))
                    while key in check_pixel:
                        key = (randint(1, image.size[0] - 20), randint(1, image.size[1] - 20))
                    check_pixel.add(key)
                    draw.point(key, (pixels[key][0], pixels[key][1], pixels[key][2] // 2 * 2 + bits[i]))
                    keys.write(str(key[0]) + " " + str(key[1]) + '\n')
        image.save(new_name, "PNG")

    def Decrypt(self, image, keys):
        pixels = image.load()
        i = 0
        c = 1
        number = 0
        text = ""
        for line in keys:
            key = line.split(' ')
            pixel = (int(key[0]), int(key[1]))
            bit = pixels[pixel][2] % 2
            number += bit * c
            c *= 2
            i += 1
            if i == 8:
                i = 0
                c = 1
                text += chr(number)
                number = 0
        return text
    
informer = argparse.ArgumentParser(description='Information for steganography.')

informer.add_argument('--action', type=str)
informer.add_argument('--img_path', type=str)
informer.add_argument('--text_path', type=str)
informer.add_argument('--key_path', type=str)
informer.add_argument('--new_name', type=str)

info = informer.parse_args()
f = Image.open(info.img_path)

steg = Steganography()

if info.action == "Encrypt":
    g = open(info.text_path, 'r')
    k = open(info.key_path, 'w')
    steg.Encrypt(f, g, k, info.new_name)
elif info.action == "Decrypt":
    g = open(info.text_path, 'w')
    k = open(info.key_path, 'r')
    text = steg.Decrypt(f, k)
    g.write(text)
f.close()
g.close()
k.close()
