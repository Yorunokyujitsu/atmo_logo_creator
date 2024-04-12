import os
import re
import numpy as np
from PIL import Image

def process_splash_image():
    input_file_path = 'restore/boot_splash_screen_notext.inc'
    if not os.path.exists(input_file_path):
        return

    with open(input_file_path, 'r') as file:
        data = file.read()

    match_w = re.search(r'SplashScreenW\s*=\s*(\d+)', data)
    match_h = re.search(r'SplashScreenH\s*=\s*(\d+)', data)

    if not (match_w and match_h):
        exit(1)

    SplashScreenW = int(match_w.group(1))
    SplashScreenH = int(match_h.group(1))

    start_index = data.find('{')
    end_index = data.find('}')
    SplashScreen_data = data[start_index + 1:end_index]

    SplashScreen = [int(pixel.strip(), 0) for pixel in SplashScreen_data.split(',') if pixel.strip()]

    if len(SplashScreen) != SplashScreenW * SplashScreenH:
        exit(1)

    image_array = np.zeros((SplashScreenH, SplashScreenW, 4), dtype=np.uint8)

    for y in range(SplashScreenH):
        for x in range(SplashScreenW):
            pixel_value = SplashScreen[y * SplashScreenW + x]
            r = (pixel_value >> 16) & 0xFF
            g = (pixel_value >> 8) & 0xFF
            b = pixel_value & 0xFF
            a = (pixel_value >> 24) & 0xFF
            image_array[y, x] = [r, g, b, a]

    splash_image = Image.fromarray(image_array, 'RGBA')

    output_folder = "output/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    splash_output_file = "splash.png"
    splash_output_path = os.path.join(output_folder, splash_output_file)
    splash_image.save(splash_output_path)
    print("Image restoration successful:", splash_output_file)

def process_fatal_image():
    input_file_path = 'restore/fatal_ams_logo.inc'
    if not os.path.exists(input_file_path):
        return

    AtmosphereLogoWidth = 0
    AtmosphereLogoHeight = 0
    AtmosphereLogoData = []

    with open(input_file_path, "r", encoding='utf-8') as f:
        data_started = False
        for line in f:
            if data_started:
                if "}" in line:
                    break
                data_line = line.strip().split(",")
                for val in data_line:
                    if val.strip():
                        AtmosphereLogoData.append(int(val.strip(), 16))
            elif line.startswith("constexpr size_t AtmosphereLogoWidth"):
                AtmosphereLogoWidth = int(line.split("=")[1].strip().split(";")[0].strip(), 16)
            elif line.startswith("constexpr size_t AtmosphereLogoHeight"):
                AtmosphereLogoHeight = int(line.split("=")[1].strip().split(";")[0].strip(), 16)
            elif line.startswith("static constexpr u16 AtmosphereLogoData[]"):
                data_started = True

    fatal_image = Image.new("RGBA", (AtmosphereLogoWidth, AtmosphereLogoHeight))

    image_data_iter = iter(AtmosphereLogoData)
    for y in range(AtmosphereLogoHeight):
        for x in range(AtmosphereLogoWidth):
            try:
                pixel_value = next(image_data_iter)
            except StopIteration:
                break
            r = ((pixel_value >> 11) & 0x1F) << 3
            g = ((pixel_value >> 5) & 0x3F) << 2
            b = (pixel_value & 0x1F) << 3
            a = 255
            pixel_rgba = (r, g, b, a)
            fatal_image.putpixel((x, y), pixel_rgba)
        else:
            continue
        break

    output_folder = "output/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fatal_output_file = "fatal.png"
    fatal_output_path = os.path.join(output_folder, fatal_output_file)
    fatal_image.save(fatal_output_path)
    print("Image restoration successful:", fatal_output_file)

process_splash_image()
process_fatal_image()
