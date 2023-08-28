"""
Display utilities
"""
import st7735

def writeLine(line, text, font, tft):
    lines = tft.width() // font.WIDTH
    x = 0
    y = line * font.HEIGHT
    tft.text(
        font,
        text,
        x,
        y,
        st7735.WHITE,
        st7735.BLACK)   