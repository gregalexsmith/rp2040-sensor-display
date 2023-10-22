import time

import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from oled import initialize_oled
from button import Button
from sensor import SCD30Sensor
from sensor_data import SensorDataManager
from sensor_view import SensorView
from constants import ACTIVE_TIMEOUT


def initialize_externals():
    # Setup I2C devices
    displayio.release_displays()
    i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    oled = initialize_oled(i2c)
    sensor = SCD30Sensor(i2c)
    # Setup buttons
    buttons = {
        'A': Button(board.D9),
        'B': Button(board.D6),
        'C': Button(board.D5)
    }
    return oled, sensor, buttons


class ModeManager:
    def __init__(self):
        self.modes = ['A', 'B', 'C']
        self.mode_idx = 0
        self.current_mode = self.modes[self.mode_idx]

    def next_mode(self):
        self.mode_idx = (self.mode_idx + 1) % len(self.modes)
        self.current_mode = self.modes[self.mode_idx]

    def set(self, mode):
        if mode in self.modes:
            self.current_mode = mode
            self.mode_idx = self.modes.index(mode)

    def get_current_mode(self):
        return self.current_mode


class ButtonManager:
    def __init__(self, buttons):
        self.buttons = buttons
        self.last_pressed = None

    def check_buttons(self):
        for button_name, button in self.buttons.items():
            if button.update():
                self.last_pressed = button_name
                return True
        return False

    def get_last_pressed(self):
        return self.last_pressed

    def reset_last_pressed(self):
        self.last_pressed = None


def main():
    oled, sensor, buttons = initialize_externals()
    sensor_view = SensorView(oled)
    data_manager = SensorDataManager(sensor)
    button_manager = ButtonManager(buttons)
    mode_manager = ModeManager()

    sleep_mode = False
    last_button_press = time.monotonic()

    while True:
        if button_manager.check_buttons():
            last_button_press = time.monotonic()
            pressed_button = button_manager.get_last_pressed()
            sleep_mode = False

            if pressed_button == 'A':
                mode_manager.next_mode()
            elif pressed_button in ['B', 'C']:
                mode_manager.set_mode(pressed_button)

            sensor_data = data_manager.get_data()
            current_mode = mode_manager.get_current_mode()
            sensor_view.update_display(current_mode, sensor_data)
            button_manager.reset_last_pressed()

        if not sleep_mode and time.monotonic() - last_button_press > ACTIVE_TIMEOUT:
            sensor_view.enter_sleep_mode()
            sleep_mode = True

        if data_manager.data_available():
            data_manager.fetch_and_update_data()
            if not sleep_mode:
                sensor_data = data_manager.get_data()
                current_mode = mode_manager.get_current_mode()
                sensor_view.update_display(current_mode, sensor_data)

        time.sleep(0.5)


main()
