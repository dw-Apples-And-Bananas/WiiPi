import time
import cwiid

class WiiPi:    
    def __init__(self):
        if not self.connect():
            quit()
        self.wii.rpt_mode = cwiid.RPT_BTN
        self._led = 0
        self.led = 4
        self.rumble()

    @property
    def led(self):
        return self._led
    @led.setter
    def led(self, value):
        self._led = value
        self.wii.led = self._led
    
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
