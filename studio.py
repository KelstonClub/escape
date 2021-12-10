NODE = "studio"

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
    handle_primary("on")
    handle_secondary("off")

def handle_primary(target_state):
    logger.info("About to handle primary %s", target_state)
    if target_state == "on":
        relay1.on()
        relay2.on()
    else:
        relay1.off()
        relay2.off()
    time.sleep(0.2)

def handle_secondary(target_state):
    logger.info("About to handle secondary %s", target_state)
    if target_state == "on":
        relay3.on()
    else:
        relay3.off()
    time.sleep(0.2)

def handle_message(message):
    logger.info("Handle message %s", message)

    if message == "reset":
        reset()
        return

    (zone, state) = message
    if zone == "primary":
        handle_primary(state)
    elif zone == "secondary":
        handle_secondary(state)
    else:
        raise RuntimeError("Unrecognised message: %s" % message)

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
    studio = nw0.advertise("studio")
    logger.info("Advertising studio as %s", studio)
    #~ threading.Thread(target=send_heartbeat, daemon=True).start()

    while True:
        logger.info("Waiting for message...")
        message = nw0.wait_for_message_from(studio)
        logger.info("Received command %s", message)

        try:
            handle_message(message)
        except:
            logger.exception("Error handling message")
            nw0.send_reply_to(studio, False)
        else:
            nw0.send_reply_to(studio, True)

if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])