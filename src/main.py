from wiipi import WiiPi
import time

class Wii(WiiPi):
    def __init__(self):
        super().__init__()
        self.update()

    def A_pressed(self):
        print("A Pressed")
        super().A_pressed()
    def A_released(self):
        print("A Released")
        super().A_released()

    def update(self):
        while True:
            super().update()

Wii()
