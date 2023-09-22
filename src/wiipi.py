import time
import cwiid

class WiiPi:    
    class Buttons:
        a=0
        b=0
        up=0
        down=0
        left=0
        right=0
        minus=0
        plus=0
        home=0
        _1=0
        _2=0
    def __init__(self):
        if not self.connect():
            quit()
        self.wii.rpt_mode = cwiid.RPT_BTN
        self.leds = [0,0,0,0]
        self.rumble()
        self.buttons = self.Buttons

    def update(self):
        btnState = self.wii.state["buttons"]
        if btnState:
            if cwiid.BTN_A and self.buttons.a == 0:
                self.A_pressed()
            if cwiid.BTN_B and self.butons.b == 0:
                self.B_pressed()
            if cwiid.BTN_UP and self.buttons.up == 0:
                self.UP_pressed()
            if cwiid.BTN_DOWN and self.buttons.down == 0:
                self.DOWN_pressed()
            if cwiid.BTN_LEFT and self.buttons.left == 0:
                self.LEFT_pressed()
            if cwiid.BTN_RIGHT and self.buttons.right == 0:
                self.RIGHT_pressed()
            if cwiid.BTN_MINUS and self.buttons.minus == 0:
                self.MINUS_pressed()
            if cwiid.BTN_PLUS and self.buttons.plus == 0:
                self.PLUS_pressed()
            if cwiid.BTN_HOME and self.buttons.home == 0:
                self.HOME_pressed()
            if cwiid.BTN_1 and self.buttons._1 == 0:
                self._1_pressed()
            if cwiid.BTN_2 and self.buttons._2 == 0:
                self._2_pressed()
        else:
            if self.buttons.a == 1:
                self.A_released()
            if self.buttons.b == 1:
                self.B_released()
            if self.buttons.up == 1:
                self.UP_released()
            if self.buttons.down == 1:
                self.DOWN_released()
            if self.buttons.left == 1:
                self.LEFT_released()
            if self.buttons.right == 1:
                self.RIGHT_released()
            if self.buttons.minus == 1:
                self.MINUS_released()
            if self.buttons.plus == 1:
                self.PLUS_released()
            if self.buttons.home == 1:
                self.HOME_released()
            if self.buttons._1 == 1:
                self._1_released()
            if self.buttons._2 == 1:
                self._2_released()
            
    def A_pressed(self): self.buttons.a = 1
    def A_released(self): self.buttons.a = 0
    def B_pressed(self): self.buttons.b = 1 
    def B_released(self): self.buttons.b = 0
    def UP_pressed(self): self.buttons.up = 1 
    def UP_released(self): self.buttons.up = 0
    def DOWN_pressed(self): self.buttons.down = 1
    def DOWN_released(self): self.buttons.down = 0
    def LEFT_pressed(self): self.buttons.left = 1 
    def LEFT_released(self): self.buttons.left = 0
    def RIGHT_pressed(self): self.buttons.right = 1 
    def RIGHT_released(self): self.buttons.right = 0
    def MINUS_pressed(self): self.buttons.minus = 1 
    def MINUS_released(self): self.buttons.minus = 0
    def PLUS_pressed(self): self.buttons.plus = 1 
    def PLUS_released(self): self.buttons.plus = 0
    def HOME_pressed(self): self.buttons.home = 1
    def HOME_released(self): self.buttons.home = 0
    def _1_pressed(self): self.buttons._1 = 1 
    def _1_released(self): self.buttons._1 = 0
    def _2_pressed(self): self.buttons._2 = 1 
    def _2_released(self): self.buttons._2 = 0

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
