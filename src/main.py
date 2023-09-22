from wiipi import WiiPi
import time

wii = WiiPi()

while True:
  for i in range(5):
    wii.led = i
    time.sleep(1)
