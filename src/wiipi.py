import time
import cwiid

class WiiPi:
    def __init__(self):
        if not self.connect():
            quit()
       time.sleep(3)
        self.wii.rpt_mode = cwiid.RPT_BTN
        self.leds = [0,0,0,0]
        self.rumble()
        self.buttons = {
            "a": [self.BTN_A, 0],
            "b": [self.BTN_B, 0],
            "up": [self.BTN_UP, 0],
            "down": [self.BTN_DOWN, 0],
            "left": [self.BTN_LEFT, 0],
            "right": [self.BTN_RIGHT, 0],
            "plus": [self.BTN_PLUS, 0],
            "minus": [self.BTN_MINUS, 0],
            "home": [self.BTN_HOME, 0],
            "1": [self.BTN_1, 0],
            "2": [self.BTN_2, 0]
        }

    def update(self):
        btnState = self.wii.state["buttons"]
        """
        if btnState:
            for btn in self.buttons:
                if self.buttons[btn][0]() and self.buttons[btn][1] == 0:
                    self.button_pressed(btn)
        """
        
        if (btnState & cwiid.BTN_A) and self.buttons["a"][1] == 0:
            self.button_pressed("a")
        if (btnState & cwiid.BTN_B) and self.buttons["b"][1] == 0:
            self.button_pressed("b")
        """
        else:
            if self.buttons["a"][1] == 1:
                self.button_released("a")
            if self.buttons["b"][1] == 1:
                self.button_released("b")

            for btn in self.buttons:
                if self.buttons[btn][1] == 1:
                    self.button_released(btn)
        """

    def button_pressed(self, btn):
        self.buttons[btn][1] = 1
    def button_released(self, btn):
        self.buttons[btn][1] = 0

    def BTN_A(self): return cwiid.BTN_A
    def BTN_B(self): return cwiid.BTN_B
    def BTN_UP(self): return cwiid.BTN_UP
    def BTN_DOWN(self): return cwiid.BTN_DOWN
    def BTN_LEFT(self): return cwiid.BTN_LEFT
    def BTN_RIGHT(self): return cwiid.BTN_RIGHT
    def BTN_PLUS(self): return cwiid.BTN_PLUS
    def BTN_MINUS(self): return cwiid.BTN_MINUS
    def BTN_HOME(self): return cwiid.BTN_HOME
    def BTN_1(self): return cwiid.BTN_1
    def BTN_2(self): return cwiid.BTN_2
        
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
        attempts = 0
        while attempts <= 3:
            try:
                self.wii = cwiid.Wiimote()
                return True
            except RuntimeError:
                attempts += 1
        return False
