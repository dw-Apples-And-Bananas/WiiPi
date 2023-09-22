import time
import cwiid
import os, sys
import json

DIR = os.path.dirname(os.path.abspath(__file__))

class Button:
    def __init__(self, ID:int, value:int=0, holdtime:int=-1):
        self.ID = ID
        self.value = value
        self.holdtime = holdtime

class WiiPi:
    def __init__(self):
        if not self.connect():
            os.execl(sys.executable, sys.executable, *sys.argv)
        for i in range(3):
            self.rumble(0.3)
            time.sleep(0.7)
        self.wii.rpt_mode = cwiid.RPT_BTN
        self.leds = [0,0,0,0]
        self.buttons = {
            "a": Button(cwiid.BTN_A),
            "b": Button(cwiid.BTN_B),
            "up": Button(cwiid.BTN_UP),
            "down": Button(cwiid.BTN_DOWN),
            "left": Button(cwiid.BTN_LEFT),
            "right": Button(cwiid.BTN_RIGHT),
            "plus": Button(cwiid.BTN_PLUS),
            "minus": Button(cwiid.BTN_MINUS),
            "home": Button(cwiid.BTN_HOME),
            "1": Button(cwiid.BTN_1),
            "2": Button(cwiid.BTN_2)
        }
        with open(f"{DIR}/configs.json") as f:
            self.configs = json.load(f)
        self.load_config(1)

    def load_config(ID):
        self.configID = ID
        self.config = self.configs[str(ID)]
        self.led(self.config["led"])

    def run(self):
        while True:
            btnState = self.wii.state["buttons"]
            for btn in self.buttons:
                if (btnState & self.buttons[btn].ID):
                    if self.buttons[btn].value == 0:
                        self.button_pressed(btn)
                elif self.buttons[btn].value == 1:
                    self.button_released(btn)
                elif self.buttons[btn].holdtime != -1 and time.time() - self.buttons[btn].holdtime > 1:
                    self.button_held(btn)
            time.sleep(0.01)

    def button_pressed(self, btn):
        self.buttons[btn].value = 1
        self.buttons[btn].holdtime = time.time()
        
    def button_released(self, btn):
        self.buttons[btn].value = 0
        self.buttons[btn].holdtime = -1
        
    def button_held(self, btn):
        self.buttons[btn].holdtime = -1
        
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


WiiPi().run()
