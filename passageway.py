NODE = "passageway"

class _DummyRelay:
    def on(self): pass
    def off(self): pass

import os, sys
import logging
logger = logging.getLogger(NODE)
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

import networkzero as nw0

HEARTBEAT_ADDRESS = nw0.address()
HEARTBEAT_INTERVAL_S = 2.0


def reset():
    logger.info("About to reset...")
    time.sleep(0.2)

def activate():
    logger.info("About to activate...")
    time.sleep(0.2)

def handle_command(command):
    if command == "reset":
        reset()
    elif command == "activate":
        activate()
    else:
        raise RuntimeError("Unrecognised command: %s" % command)

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
    passageway = nw0.advertise(NODE)
    logger.info("Advertising passageway as %s", passageway)
    #~ threading.Thread(target=send_heartbeat, daemon=True).start()

    while True:
        logger.info("Waiting for command...")
        command = nw0.wait_for_message_from(passageway)
        logger.info("Received command %s", command)

        try:
            handle_command(command)
        except:
            logger.exception("Error handling command")
            nw0.send_reply_to(passageway, False)
        else:
            nw0.send_reply_to(passageway, True)


if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])
