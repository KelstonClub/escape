import os, sys
import logging
logger = logging.getLogger("stairway")
import time

import networkzero as nw0

def reset():
    raise NotImplementedError

def handle_primary(target_state):
    logger.info("About to handle primary %s", target_state)
    time.sleep(0.2)

def handle_secondary(target_state):
    logger.info("About to handle secondary %s", target_state)
    time.sleep(0.2)

def handle_message(message):
    logger.info("Handle message %s", message)
    (zone, state) = message

    if zone == "primary":
        handle_primary(state)
    elif zone == "secondary":
        handle_secondary(state)
    else:
        raise RuntimeError("Unrecognised message: %s" % message)

def main():
    stairway = nw0.advertise("stairway")
    logger.info("Advertising stairway as %s", stairway)

    while True:
        logger.info("Waiting for message...")
        message = nw0.wait_for_message_from(stairway)
        logger.info("Received command %s", message)

        if message == "reset":
            reset()
        else:
            handle_message(message)

if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])
