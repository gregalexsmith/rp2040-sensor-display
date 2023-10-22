import board
import displayio
import adafruit_displayio_ssd1306


def initialize_oled(i2c):
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
    return adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
