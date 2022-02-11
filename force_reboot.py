#!/usr/bin/env python3
import codecs
import serial
import time
from switch import RelayCtrl

POWER_PIN = 3
VOL_DOWN_PIN = 2

# Test sequence
myrelay = RelayCtrl()

myrelay.open()

# Turn off all relays
myrelay.turnoff(0)
myrelay.turnoff(1)
myrelay.turnoff(VOL_DOWN_PIN)
myrelay.turnoff(POWER_PIN)

# Emulate power key press 16s to force shutdown device
myrelay.turnon(POWER_PIN)
myrelay.status()
time.sleep(16)
myrelay.turnoff(POWER_PIN)
myrelay.status()
time.sleep(0.5)
