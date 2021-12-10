import os, sys
import time
import logging
logger = logging.getLogger("controller")

import networkzero as nw0

def main():
    old_heartbeats = set()
    while True:
        #
        # Rescan for heartbeats in case new processes have come on line and/or
        # we've had to restart
        #
        heartbeats = set(nw0.discover_group("heartbeat"))
        for name, address in heartbeats - old_heartbeats:
            logger.info("Found new heartbeat for %s at %s", name, address)
        for name, address in old_heartbeats - heartbeats:
            logger.info("Dropping heartbeat for %s at %s", name, address)
        old_heartbeats = heartbeats

        topic, info = nw0.wait_for_news_from([address for name, address in heartbeats], wait_for_s=3.0)
        if topic is not None:
            logger.info("Received heartbeat on %s", topic)

if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])
