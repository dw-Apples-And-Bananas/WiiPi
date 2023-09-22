import time
import cwiid

class WiiPi:    
    def __init__(self):
        if not self.connect():
            quit()
        self.wii.rpt_mode = cwiid.RPT_BTN
        self.leds = [0,0,0,0]
        self.rumble()

    def led(self, leds:list[int]):
        ids = {
            [0,0,0,0] = 0,
            [1,0,0,0] = 1,
            [0,1,0,0] = 2,
            [1,1,0,0] = 3,
            [0,0,1,0] = 4,
            [1,0,1,0] = 5,
            [0,1,1,0] = 6,
            [1,1,1,0] = 7,
            [0,0,0,1] = 8,
            [1,0,0,1] = 9,
            [0,1,0,1] = 10,
            [1,1,0,1] = 11,
            [0,0,1,1] = 12,
            [1,0,1,1] = 13,
            [0,1,1,1] = 14,
            [1,1,1,1] = 15
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
