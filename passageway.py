import os, sys
import time
import logging
logger = logging.getLogger("passageway")

import networkzero as nw0

def reset():
    logger.info("About to reset...")
    time.sleep(0.2)

def activate():
    logger.info("About to activate...")
    time.sleep(0.2)

def main():
    passageway = nw0.advertise("passageway")
    logger.info("Advertising passageway as %s", passageway)

    while True:
        logger.info("Waiting for command...")
        command = nw0.wait_for_message_from(passageway)
        logger.info("Received command %s", command)

        if command == "reset":
            reset()
        elif command == "activate":
            activate()
        else:
            raise RuntimeError("Unrecognised command: %s" % command)

if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])
