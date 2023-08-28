"""
main.py

It displays a menu on the TFT screen and allows the user to select a plugin.
With a single button press in cycles through the menu items.
With a long button press it selects the current menu item.
"""

import st7735
import utils.tft_config as tft_config
import data.fonts.vga2_8x8 as font
import data.fonts.vga2_bold_16x32 as font_big
from machine import Pin
import uasyncio as asyncio
from lib.primitives.pushbutton import Pushbutton
import os

tft = tft_config.config(3)
current_page = -1
plugins = []
button = None

def calculatePage(number, total):
    # Char 0x07 -> Dot
    # Char 0x09 -> Empty dot
    pages = [0x07] * total
    pages[number - 1] = 0x09
    pages = bytes(pages)
    return str(pages, "utf-8")

def displayPage(text, subtext, number, total):
    # Clears the screen
    tft.fill(st7735.BLACK)

    # Displays the text (title)
    tft.text(
        font_big,
        text,
        tft.width() // 2 - len(text) // 2 * font_big.WIDTH,
        tft.height() // 2 - font_big.HEIGHT,
        st7735.WHITE,
        st7735.BLACK
    )

    # Displays the subtext (description)
    tft.text(
        font,
        subtext,
        tft.width() // 2 - len(subtext) // 2 * font.WIDTH,
        tft.height() // 2,
        st7735.WHITE,
        st7735.BLACK
    )

    # Displays the page number
    pages = calculatePage(number, total)
    tft.text(
        font,
        pages,
        tft.width() // 2 - len(pages) // 2 * font.WIDTH,
        tft.height() - font.HEIGHT,
        st7735.WHITE,
        st7735.BLACK
    )

def populatePlugins():
    global plugins
    plugins = []
    # plugins = [
    #     {
    #         "name": "Test",
    #         "description": "I'm a usb stick",
    #         "path" : "plugins.test.test"
    #     },
    #     {
    #         "name": "Torcia",
    #         "description": "Use the LED",
    #         "path" : "plugins.flashlight.flashlight"
    #     }
    # ]

    plugins_dir = "plugins"
    print("plugins:")
    for plugin in os.listdir(plugins_dir):
        real_path = plugins_dir + "/" + plugin + "/"
        print(real_path)
        import_path = "plugins." + plugin + "." + plugin
        with open(f"{plugins_dir}/{plugin}/description.txt") as f:
            description = f.read()
        plugins.append({
                        "name": plugin[0].upper() + plugin[1:],
                        "description": description ,
                        "path" : import_path
                        })

def drawPage():
    global plugins
    global current_page

    current_page += 1
    if current_page >= len(plugins):
        current_page = 0

    print("New page")
    displayPage(
            plugins[current_page]["name"],
            plugins[current_page]["description"],
            current_page + 1,
            len(plugins)
        )


def selectPlugin():
    print(f"Selected {plugins[current_page]['path']}")
    button.deinit()
    exec("import " + plugins[current_page]["path"] + " as plugin")
    plugin.main(tft)

async def amain():
    global button
    drawPage()
    print("Starting")
    pin = Pin(0, Pin.IN)
    button = Pushbutton(pin, suppress=True)
    button.debounce_ms(100)
    button.release_func(drawPage)
    button.long_func(selectPlugin)
    while True:
        await asyncio.sleep(1)

def main():

    tft.init(st7735.INITR_GREENTAB5)

    # tft.fill(st7735.BLACK)
    populatePlugins()

    asyncio.run(amain())

main()

