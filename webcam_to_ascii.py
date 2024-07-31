from PIL import Image, ImageEnhance
from copy import deepcopy
import math
import os
import cv2
import pygame as pg

#ascii_brightness = "    .:-=+*#%@"
ascii_brightness = " _.,-=+:;cba!?0123456789$W#@N"
ascii_num = len(ascii_brightness)

color = True
background = False

reset = {"fore": "\033[0m",  "back": "\033[0m"}
color_dict = {
    "black":            {"fore": "30", "back": "40",  "rgb": (0, 0, 0)},
    "red":              {"fore": "31", "back": "41",  "rgb": (127, 0, 0)},
    "green":            {"fore": "32", "back": "42",  "rgb": (0, 127, 0)},
    "yellow":           {"fore": "33", "back": "43",  "rgb": (127, 127, 0)},
    "blue":             {"fore": "34", "back": "44",  "rgb": (0, 0, 127)},
    "magenta":          {"fore": "35", "back": "45",  "rgb": (127, 0, 127)},
    "cyan":             {"fore": "36", "back": "46",  "rgb": (0, 127, 127)},
    "white":            {"fore": "37", "back": "47",  "rgb": (127, 127, 127)},
    "bright_black":     {"fore": "90", "back": "100", "rgb": (85, 85, 85)},
    "bright_red":       {"fore": "91", "back": "101", "rgb": (255, 85, 85)},
    "bright_green":     {"fore": "92", "back": "102", "rgb": (85, 255, 85)},
    "bright_yellow":    {"fore": "93", "back": "103", "rgb": (255, 255, 85)},
    "bright_blue":      {"fore": "94", "back": "104", "rgb": (85, 85, 255)},
    "bright_magenta":   {"fore": "95", "back": "105", "rgb": (255, 85, 255)},
    "bright_cyan":      {"fore": "96", "back": "106", "rgb": (85, 255, 255)},
    "bright_white":     {"fore": "97", "back": "107", "rgb": (255, 255, 255)},
    }

all_rgb = []
for k, v in color_dict.items():
    all_rgb.append(v["rgb"])

dest_dim = (70, 50)

def to_ascii(img):
    img = img.resize(dest_dim)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)
    img_color = deepcopy(img)
    img = img.convert("L")
    ascii_result = []
    color_result = []
    for y in range(img.size[1]):
        temp = []
        if color:
            temp_color = []
        for x in range(img.size[0]):
            brightness = img.getpixel((x, y)) # 0 - 255
            color_pixel = img_color.getpixel((x, y))
            index = int((brightness / 255) * ascii_num - 1)
            if color:
                smallest_diff = 800
                for i, rgb in enumerate(all_rgb):
                    diff = math.sqrt((color_pixel[0] - rgb[0])**2 + (color_pixel[1] - rgb[1])**2 + (color_pixel[2] - rgb[2])**2)
                    if diff < smallest_diff:
                        smallest_diff = diff
                        color_key = list(color_dict.keys())[i]
                temp_color.append(color_dict[color_key]["rgb"])

            final_char = ascii_brightness[index]
            temp.append(final_char)
            
        ascii_result.append(temp)
        if color:
            color_result.append(temp_color)

    return ascii_result, color_result

CELL_SIZE = 15
pg.init()
screen = pg.display.set_mode((dest_dim[0]*CELL_SIZE, dest_dim[1]*CELL_SIZE))
clock = pg.time.Clock()
FPS = 30
font = pg.font.Font("C:/Windows/Fonts/consola.ttf", int(CELL_SIZE*1.3))
cap = cv2.VideoCapture(0)

running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    screen.fill(0)

    if cap.isOpened():
        success, frame = cap.read()
        if not success:
            cap.release()
            print("ERROR")
            exit()

        frame = cv2.flip(frame, 1)
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        ascii_result, color_result = to_ascii(img)

    for i, row in enumerate(ascii_result):
        for j, e in enumerate(row):
            color_pix = (255, 255, 255)
            if color:
                color_pix = color_result[i][j]
            if not background:
                rendered = font.render(ascii_result[i][j], True, color_pix)
                screen.blit(rendered, (j * CELL_SIZE, i * CELL_SIZE))
            else:
                pg.draw.rect(screen, color_pix, pg.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))


    pg.display.flip()
    clock.tick(FPS)

pg.quit()