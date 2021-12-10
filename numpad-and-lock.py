NODE = "numpad"

class _DummyRelay:
    def on(self): pass
    def off(self): pass

import os, sys
import logging
logger = logging.getLogger("numpad")
import threading
import time
try:
    import gpiozero
except ImportError:
    logger.warn("Can't import gpiozero; probably not on RPi")
    relay1 = relay2 = relay3 = _DummyRelay()
else:
    relay1 = gpiozero.OutputDevice(21, active_high=True, initial_value=False)
    relay2 = gpiozero.OutputDevice(20, active_high=True, initial_value=False)
    relay3 = gpiozero.OutputDevice(26, active_high=True, initial_value=False)

from pygame import mixer
mixer.init()
import networkzero as nw0

def reset():
    logger.info("About to reset...")
    time.sleep(0.2)

def handle_message(message):
    logger.info("About to handle message %s ...", message)
    time.sleep(0.2)

def wait_for_numpad():
    logger.info("About to wait for numpad...")
    while True:
        combo = input("Enter the combination:")
        if combo == "1234":
            return True
        else:
            time.sleep(0.2)

def unlock():
    logger.info("About to unlock...")
    time.sleep(0.2)

def play_success():
    mixer.Sound("success.wav").play()

def play_error():
    mixer.Sound("failure.wav").play()

def send_heartbeat():
    while True:
        #
        # Advertise the heartbeat frequently to allow for beacon shutdowns
        #
        heartbeat = nw0.advertise("heartbeat/%s" % NODE, HEARTBEAT_ADDRESS)
        print("Sending heartbeat", NODE, "to", heartbeat)
        nw0.send_news_to(heartbeat, NODE)
        time.sleep(HEARTBEAT_INTERVAL_S)

def main():
    reset()
    numpad = nw0.advertise("numpad")
    logger.info("Advertising numpad as %s", numpad)
    #~ threading.Thread(target=send_heartbeat, daemon=True).start()
    logger.info("Looking for stairway...")
    stairway = nw0.discover("stairway")
    logger.info("Found stairway at %s", stairway)
    logger.info("Looking for passageway...")
    passageway = nw0.discover("passageway")
    logger.info("Found passageway at %s", passageway)

    while True:
        logger.info("Checking for message...")
        message = nw0.wait_for_message_from(numpad, wait_for_s=0)
        if message is not None:
            handle_message(message)

        #
        # if the numpad is keyed correctly, unlock the box
        #
        wait_for_numpad()
        unlock()

        logger.info("About to turn primary lights off..")
        #
        # Turn the main lights off
        #
        if nw0.send_message_to(stairway, ("primary", "off")):
            play_success()
        else:
            play_error()

        logger.info("About to turn secondary lights on..")
        #
        # Turn the secondary lights on
        #
        if nw0.send_message_to(stairway, ("secondary", "on")):
            play_success()
        else:
            play_error()

        logger.info("About to activate passageway..")
        #
        # Send a message to the passageway controller for it to
        # do its thing
        #
        if nw0.send_message_to(passageway, "activate"):
            play_success()
        else:
            play_error()

if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])
