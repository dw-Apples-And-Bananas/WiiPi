from wiipi import WiiPi
import time
from zero_hid import Keyboard
keyboard = Keyboard()

class Wii(WiiPi):
    def __init__(self):
        super().__init__()
        self.update()

    def A_pressed(self):
        keyboard.type("A Pressed\n")
        super().A_pressed()
    def A_released(self):
        keyboard.type("A Released\n\n")
        super().A_released()

    def update(self):
        while True:
            super().update()

time.sleep(5)
Wii()
