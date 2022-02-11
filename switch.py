#!/usr/bin/env python3
import codecs
import serial
import time

# This is a sample code for http://www.chinalctech.com/cpzx/32.html

DEFAULT_DEVPATH="/dev/ttyUSB0"
DEFAULT_TIMEOUT=2

class RelayCtrl:
    def __init__(self, devpath=DEFAULT_DEVPATH, timeout=DEFAULT_TIMEOUT):
        self.devpath = devpath
        self.timeout = timeout
        self.ON_CMD= [b"A00101A2", b"A00201A3", b"A00301A4", b"A00401A5"]
        self.OFF_CMD=[b"A00100A1", b"A00200A2", b"A00300A3", b"A00400A4"]

    def open(self):
        self.s = serial.Serial(self.devpath, "9600", timeout=self.timeout)
        print("open " + self.s.name)

    def turnon(self, index):
        self.s.write(codecs.decode(self.ON_CMD[index], "hex"))
        time.sleep(0.1)

    def turnoff(self, index):
        self.s.write(codecs.decode(self.OFF_CMD[index], "hex"))
        time.sleep(0.1)

    def status(self):
        self.s.write(codecs.decode(b'FF','hex'))
        res=self.s.read(4)
        print(res)

    def close(self):
        self.s.close()

