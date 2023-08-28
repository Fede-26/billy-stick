"""
Webrepl plugin

This plugin allows you to use the webrepl hosted on the esp.

"""
import st7735
from machine import Pin, SoftSPI
import uasyncio as asyncio
from lib.primitives.pushbutton import Pushbutton

tft = None
button = None
spi = SoftSPI(sck=Pin(39), mosi=Pin(40), miso=Pin(41))
spi.init(baudrate=10_000_000)

status = False
current_color = 0
colors = [
    {
        "lcd": st7735.WHITE,
        "led": bytes([0xFF, 0xFF, 0xFF, 0xFF])
    },
    {
        "lcd": st7735.RED,
        "led": bytes([0xFF, 0x00, 0x00, 0xFF])

    },
    {
        "lcd": st7735.GREEN,
        "led": bytes([0xFF, 0x00, 0xFF, 0x00])
    },
    {
        "lcd": st7735.BLUE,
        "led": bytes([0xFF, 0xFF, 0x00, 0x00])
    },
    {
        "lcd": st7735.YELLOW,
        "led": bytes([0xFF, 0x00, 0xFF, 0xFF])
    },
    {
        "lcd": st7735.MAGENTA,
        "led": bytes([0xFF, 0xFF, 0x00, 0xFF])
    },
    {
        "lcd": st7735.CYAN,
        "led": bytes([0xFF, 0xFF, 0xFF, 0x00])
    }
]

def changeColor():
    global current_color
    global status
    global colors
    print("Change color")
    if status:
        current_color = (current_color + 1) % len(colors)
        color = colors[current_color]
        tft.fill(color["lcd"])
        startFrame = bytes([0]*4)
        msg = color["led"]
        endFrame = bytes([0xFF]*4)
        spi.write(startFrame)
        spi.write(msg)
        spi.write(endFrame)

def toggleLed():
    global spi
    global status
    global current_color
    global colors
    print("Toggle led")

    startFrame = bytes([0]*4)
    endFrame = bytes([0xFF]*4)
    if status:
        msg = bytes([0x0c, 0x00, 0x00, 0x00])
        tft.fill(st7735.BLACK)
    else:
        msg = colors[current_color]["led"]
        tft.fill(colors[current_color]["lcd"])
    status = not status
    spi.write(startFrame)
    spi.write(msg)
    spi.write(endFrame)

async def amain(tft):
    global button
    button = Pushbutton(Pin(0, Pin.IN, Pin.PULL_UP), suppress=True, sense=1)
    button.release_func(changeColor)
    button.long_func(toggleLed)
    while True:
        await asyncio.sleep(1)

def main(xtft):
    global spi
    global tft
    tft = xtft
    tft.fill(st7735.BLACK)

    startFrame = bytes([0]*4)
    msg = bytes([0x0c, 0x00, 0x00, 0x00])
    endFrame = bytes([0xFF]*4)
    spi.write(startFrame)
    spi.write(msg)
    spi.write(endFrame)


    asyncio.run(amain(tft))
