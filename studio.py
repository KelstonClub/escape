NODE = "studio"

class _DummyRelay:
    def on(self): pass
    def off(self): pass

import os, sys
import logging
logger = logging.getLogger(NODE)
import time

from relays import relay_ctrl

import networkzero as nw0

HEARTBEAT_ADDRESS = nw0.address()
HEARTBEAT_INTERVAL_S = 2.0

def reset(relays):
    relays.switch_relay(0, False)
    relays.switch_relay(1, False)
    pass

def handle_primary(relays, target_state):
    logger.info("About to handle primary %s", target_state)
    if target_state == "on":
        relay1.on()
        relay2.on()
    else:
        relay1.off()
        relay2.off()
    time.sleep(0.2)

def handle_secondary(relays, target_state):
    logger.info("About to handle secondary %s", target_state)
    if target_state == "on":
        relay3.on()
    else:
        relay3.off()
    time.sleep(0.2)

def handle_message(relays, message):
    logger.info("Handle message %s", message)

    if message == "reset":
        reset(relays)
        return

    (zone, state) = message
    if zone == "primary":
        relays.switch_relay(0, False)
        relays.switch_relay(1, False)
    elif zone == "secondary":
        relays.switch_relay(0, True)
        relays.switch_relay(1, True)
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
    # 2,22,25
    relays = relay_ctrl([4, 22])

    # 1: normal light
    #22 : black light

    #relays.switch_relay(0, False)
    #relays.switch_relay(1, False)
    #relays.switch_relay(1, True)
    #relays.switch_relay(3, True)
    #relays.switch_relay(4, True)

    #reset(relays)
    studio = nw0.advertise("studio")
    logger.info("Advertising studio as %s", studio)
    #~ threading.Thread(target=send_heartbeat, daemon=True).start()

    while True:
        logger.info("Waiting for message...")
        message = nw0.wait_for_message_from(studio)
        logger.info("Received command %s", message)

        try:
            print(message)
            handle_message(relays, message)
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
