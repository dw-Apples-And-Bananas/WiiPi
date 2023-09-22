from wiipi import WiiPi
import time
from zero_hid import Keyboard
keyboard = Keyboard()

class Wii(WiiPi):
    def __init__(self):
        super().__init__()
        self.update()

    def button_pressed(self, btn):
        keyboard.type(f"{btn} Pressed\n")
        super().button_pressed()
    def button_released(self, btn):
        keyboard.type(f"{btn} Released\n\n")
        super().button_released()

    def update(self):
        while True:
            super().update()

time.sleep(5)
Wii()
