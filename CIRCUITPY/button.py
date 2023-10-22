import board
import digitalio


class Button:
    def __init__(self, pin):
        self._button = digitalio.DigitalInOut(pin)
        self._button.direction = digitalio.Direction.INPUT
        self._button.pull = digitalio.Pull.UP
        self._last_state = self._button.value
        self._pressed = False

    def update(self):
        """Check the button state and update the internal state."""
        current_state = self._button.value
        if not current_state and self._last_state:
            self._pressed = True
        else:
            self._pressed = False
        self._last_state = current_state
        return self._pressed

    def is_pressed(self):
        """Return True if the button has been pressed."""
        return self._pressed
