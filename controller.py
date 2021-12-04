import os, sys
import time
import logging
logger = logging.getLogger("controller")

import networkzero as nw0

def main():
    heartbeats = nw0.discover_group("heartbeat")
    for name, address in heartbeats:
        logger.info("Found heartbeat for %s at %s", name, address)

    while True:
        topic, info = nw0.wait_for_news_from(heartbeats)
        logger.info("Received heartbeat from %s", info)

if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])
