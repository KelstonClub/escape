import os, sys
import logging
logger = logging.getLogger("stairway")
import time
import gpiozero

import networkzero as nw0

relay1 = gpiozero.OutputDevice(21, active_high=True, initial_value=False)
relay2 = gpiozero.OutputDevice(20, active_high=True, initial_value=False)
relay3 = gpiozero.OutputDevice(26, active_high=True, initial_value=False)

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

def main():
    reset()
    stairway = nw0.advertise("stairway")
    logger.info("Advertising stairway as %s", stairway)

    while True:
        logger.info("Waiting for message...")
        message = nw0.wait_for_message_from(stairway)
        logger.info("Received command %s", message)

        try:
            handle_message(message)
        except:
            logger.exception("Error handling message")
            nw0.send_reply_to(stairway, False)
        else:
            nw0.send_reply_to(stairway, True)

if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])
