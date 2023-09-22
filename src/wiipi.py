import time
import cwiid
import os

class WiiPi:
    def __init__(self):
        if not self.connect():
            os.execl(sys.executable, sys.executable, *sys.argv)
        time.sleep(3)
        self.wii.rpt_mode = cwiid.RPT_BTN
        self.leds = [0,0,0,0]
        self.rumble()
        self.buttons = {
            "a": [cwiid.BTN_A, 0],
            "b": [cwiid.BTN_B, 0],
            "up": [cwiid.BTN_UP, 0],
            "down": [cwiid.BTN_DOWN, 0],
            "left": [cwiid.BTN_LEFT, 0],
            "right": [cwiid.BTN_RIGHT, 0],
            "plus": [cwiid.BTN_PLUS, 0],
            "minus": [cwiid.BTN_MINUS, 0],
            "home": [cwiid.BTN_HOME, 0],
            "1": [cwiid.BTN_1, 0],
            "2": [cwiid.BTN_2, 0]
        }

    def update(self):
        btnState = self.wii.state["buttons"]
        for btn in self.buttons:
            if (btnState & self.buttons[btn][0]):
                if self.buttons[btn][1] == 0:
                    self.button_pressed(btn)
            elif self.buttons[btn][1] == 1:
                self.button_released(btn)

    def button_pressed(self, btn):
        self.buttons[btn][1] = 1
    def button_released(self, btn):
        self.buttons[btn][1] = 0
        
    def led(self, leds:list[int]):
        ids = {
            [0,0,0,0]: 0,
            [1,0,0,0]: 1,
            [0,1,0,0]: 2,
            [1,1,0,0]: 3,
            [0,0,1,0]: 4,
            [1,0,1,0]: 5,
            [0,1,1,0]: 6,
            [1,1,1,0]: 7,
            [0,0,0,1]: 8,
            [1,0,0,1]: 9,
            [0,1,0,1]: 10,
            [1,1,0,1]: 11,
            [0,0,1,1]: 12,
            [1,0,1,1]: 13,
            [0,1,1,1]: 14,
            [1,1,1,1]: 15
        }
        wii.led = ids[leds]
        self.leds = leds
                                  
    def rumble(self, seconds:float=0.3):
        self.wii.rumble = 1
        time.sleep(seconds)
        self.wii.rumble = 0

    def connect(self):
        try:
            self.wii = cwiid.Wiimote()
            return True
        except RuntimeError:
            return False
