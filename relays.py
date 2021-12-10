import os, sys
import logging
logger = logging.getLogger("numpad")
import time

import RPi.GPIO as GPIO
import gpiozero

import networkzero as nw0

class relay_ctrl:
    relays_initialized = False
    keypad_lock = None
    black_light = None
    normal_light = None

    def __init__(self):
        self.init_relay_system()

    def init_relay_system(self):
        # loading GPIO and clean up
        def cleanup(*args): print("Cleanup of relay pins")
        GPIO.cleanup = cleanup

        # initilize relays
        # False: open
        self.keypad_lock = gpiozero.OutputDevice(21, active_high=True, initial_value=True)
        
        # False: on
        self.black_light = gpiozero.OutputDevice(20, active_high=True, initial_value=True)

        # True: on
        self.normal_light = gpiozero.OutputDevice(26, active_high=True, initial_value=True)

        self.relays_initialized = True

    def switch_keypad_lock(self, value):
        if value:
            self.keypad_lock.on()
        else:
            self.keypad_lock.off()

    def switch_black_light(self, value):
        if value:
            self.black_light.on()
        else:
            self.black_light.off()

    def switch_normal_light(self, value):
        if value:
            self.normal_light.on()
        else:
            self.normal_light.off()