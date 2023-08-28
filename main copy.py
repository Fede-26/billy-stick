"""
main.py

It displays a menu on the TFT screen and allows the user to select a plugin.
With a single button press in cycles through the menu items.
With a long button press it selects the current menu item.
"""

import st7735
import utils.tft_config as tft_config
import data.fonts.vga2_8x8 as font

tft = tft_config.config(1)
curr_line = 0

def center(text):
    length = len(text)
    tft.text(
        font,
        text,
        tft.width() // 2 - length // 2 * font.WIDTH,
        tft.height() // 2 - font.HEIGHT,
        st7735.WHITE,
        st7735.RED)

def newLine(text):
    global curr_line
    lines = tft.width() // font.WIDTH
    x = 0
    y = curr_line * font.HEIGHT
    tft.text(
        font,
        text,
        x,
        y,
        st7735.WHITE,
        st7735.BLACK)

def main():
    global curr_line
#     tft.init(st7735.INITR_GREENTAB)
#     tft.init(st7735.INITR_REDTAB)
#     tft.init(st7735.INITR_BLACKTAB)
#     tft.init(st7735.INITR_GREENTAB2)
#     tft.init(st7735.INITR_GREENTAB3)
#     tft.init(st7735.INITR_GREENTAB4)
#     tft.init(st7735.INITR_GREENTAB5)
#     tft.init(st7735.INITB)
    tft.init(st7735.INITR_GREENTAB5)

    tft.fill(st7735.BLACK)

    newLine("Test")
    curr_line += 1
    newLine("I'm a usb stick")

main()

