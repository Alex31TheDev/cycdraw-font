import sys
from os import listdir, path

from PIL import Image, UnidentifiedImageError

import json

def get_images(dir_path):
    files = listdir(dir_path)

    for file in files:
        name, ext = path.splitext(file)

        if ext == ".png":
            image = None

            try:
                image = Image.open(file, "r")
            except UnidentifiedImageError:
                print("Image", file, "is invalid.")

            if image is not None:
                yield (name, image)

def get_char_json():
    charMap = dict()

    for (name, image) in get_images():
        rawPixels = list(image.getdata())

        pixels = [None] * (len(rawPixels) * 3)
        offset = 0

        for pixel in rawPixels:
            pixels[offset] = pixel[0]
            pixels[offset + 1] = pixel[1]
            pixels[offset + 2] = pixel[2]

            offset += 3

        charMap[name] = {
            "w": image.width,
            "h": image.height,
            "pixels": pixels
        }

    return json.dumps(charMap)

def main():
    if len(sys.argv) > 1:
        in_path = sys.argv[1]
    else:
        in_path = "./input"

    charJson = get_char_json()

    with open("out.json", "w") as file:
        file.write(charJson)
                
    return

if __name__ == "__main__":
    main()
