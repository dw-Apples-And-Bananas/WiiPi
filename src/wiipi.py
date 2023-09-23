import time
import cwiid
import os, sys
import json
import threading

from zero_hid import Keyboard, KeyCodes
keyboard = Keyboard()

DIR = os.path.dirname(os.path.abspath(__file__))

class Button:
    def __init__(self, ID:int, value:int=0, holdtime:int=-1):
        self.ID = ID
        self.value = value
        self.holdtime = holdtime
        self.holding = True


class Remap:
    def __init__(self, wiipi):
        self.modifiers = ["gui", "control", "shift", "alt"]
        self.modifier = -1
        self.argnames = ["button", "action", "modifiers", "key"]
        self.args = {
            "button": "Hold/Tap Button On Wiimote",
            "action": None,
            "modifiers": "Cycle Modifiers With Left and Right Buttons",
            "key": "Cycle Keys With Left and Right Buttons"
        }
        self.arg = 0
        self.text = ""
        self.set(wiipi)

    def setup(self):
        self.text = json.dumps(self.args, indent=2)
        keyboard.type(self.text)
        self.pos = [self.text.count("\n"), len(self.text.split("\n")[-1])]
        self.position(0,0)
        self.select(0)

    def position(self, y, x):
        for i in range(self.pos[1]):
            keyboard.press([], KeyCodes.KEY_LEFT)
        vertical = self.pos[0] - y
        if vertical > 0:
            for i in range(vertical):
                keyboard.press([], KeyCodes.KEY_UP)
        elif vertical < 0:
            for i in range(vertical*-1):
                keyboard.press([], KeyCodes.KEY_DOWN)
        for i in range(x):
            keyboard.press([], KeyCodes.KEY_RIGHT)
        self.pos = [y, x]
        
    def select(self, y):
        x = self.text.split("\n")[y+1].find(self.args[self.argnames[y]])
        self.position(y+1,x)
    
    def back(self):
        if self.arg > 0:
            self.select(self.arg-1)
            
    def next(self):
        if self.arg < 2:
            self.select(self.arg+1)
    
    def released(self, btn):
        if self.arg == 0:
            self.args[0] = btn
            keyboard.type(self.args[0])
            self.pos[1] = len(self.args[0])
        elif self.arg == 1:
            if btn == "right":
                self.modifier += 1
                self.args[1] = self.modifiers[self.modifier]
                keyboard.type(self.args[1])
                self.pos[1] = len(self.args[1])
                self.select(1)

    def set(self, wiipi):
        self.configs = wiipi.configs
        self.configID = wiipi.config
        self.config = wiipi.config

    def write(self):
        self.configs[str(self.configID)] = self.config 
        with open(f"{DIR}/config.json", "w") as f:
            json.dump(self.configs, f, indent=2)

        
class WiiPi:
    def __init__(self):
        if not self.connect():
            os.execl(sys.executable, sys.executable, *sys.argv)
        for i in range(3):
            self.rumble(0.3)
            time.sleep(0.7)
        self.wii.rpt_mode = cwiid.RPT_BTN
        self.leds = "0000"
        self.blink = None
        self.blinktime = 0
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
        self.configID = 1
        self.load_configs()
        self.remapping = False
        self.remap = Remap(self)

    def load_configs(self):
        with open(f"{DIR}/configs.json") as f:
            self.configs = json.load(f)
        self.load_config(self.configID)

    def load_config(self, ID):
        if ID < 1:
            self.configID = 4
        elif ID > 4:
            self.configID = 1
        else:
            self.configID = ID
        self.config = self.configs[str(self.configID)]
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
                if self.buttons[btn].holdtime != -1 and time.time() - self.buttons[btn].holdtime > 1:
                    self.button_held(btn)
            if self.blink != None and time.time() - self.blinktime > 0.5:
                if self.leds == self.blink:
                    self.led("0000")
                else:
                    self.led(self.blink)
                self.blinktime = time.time()
            time.sleep(0.01)

    def button_pressed(self, btn):
        self.buttons[btn].value = 1
        self.buttons[btn].holdtime = time.time()
        
    def button_released(self, btn):
        if not self.remapping:
            if not self.buttons[btn].holding:
                if self.buttons["home"].holding:
                    if btn == "a":
                        self.blink = self.leds
                        self.remapping = True
                        self.remap.set(self)
                        self.remap.setup()
                    elif btn == "minus":
                        self.hiddenleds = self.leds
                        self.led("0000")
                    elif btn == "plus":
                        self.led(self.hiddenleds)
                    elif btn == "left":
                        self.load_config(self.configID-1)
                    elif btn == "right":
                        self.load_config(self.configID+1)
        elif not self.buttons[btn].holding and self.buttons["home"].holding:
            if btn == "a":
                self.led(self.blink)
                self.blink = None
                self.remapping = False
                self.remap.write()
                self.load_configs()
            elif btn == "b":
                self.remap.back()
        elif btn != "home":
            self.remap.released(btn)
        self.buttons[btn].value = 0
        self.buttons[btn].holdtime = -1
        self.buttons[btn].holding = False
        
    def button_held(self, btn):
        leds = self.leds
        self.led("1111")
        time.sleep(0.2)
        self.led("0000")
        time.sleep(0.1)
        self.led(leds)
        self.buttons[btn].holding = True
        self.buttons[btn].holdtime = -1
        
    def led(self, leds:str):
        ids = {
            "0000": 0,
            "1000": 1,
            "0100": 2,
            "1100": 3,
            "0010": 4,
            "1010": 5,
            "0110": 6,
            "1110": 7,
            "0001": 8,
            "1001": 9,
            "0101": 10,
            "1101": 11,
            "0011": 12,
            "1011": 13,
            "0111": 14,
            "1111": 15
        }
        self.wii.led = ids[leds]
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
