NODE = "countdown"

import os, sys
import logging
logger = logging.getLogger(NODE)
import threading
import time

os.add_dll_directory(r"C:\Program Files\VideoLAN\VLC")
import vlc

import networkzero as nw0

HEARTBEAT_ADDRESS = nw0.address()
HEARTBEAT_INTERVAL_S = 2.0

player = vlc.MediaPlayer("background-sounds/countdown.mp4")
player.set_fullscreen(True)

def reset():
    logger.info("About to reset...")
    player.stop()

def play():
    logger.info("About to play...")
    player.play()

def speed_up():
    logger.info("About to speed up")
    player.set_rate(1.5)

def handle_command(command):
    if command == "reset":
        reset()
    elif command == "play":
        play()
    elif command == "speed_up":
        speed_up()
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
    countdown = nw0.advertise(NODE)
    logger.info("Advertising countdown as %s", countdown)
    #~ threading.Thread(target=send_heartbeat, daemon=True).start()

    while True:
        logger.info("Waiting for command...")
        command = nw0.wait_for_message_from(countdown)
        logger.info("Received command %s", command)

        try:
            handle_command(command)
        except:
            logger.exception("Error handling command")
            nw0.send_reply_to(countdown, False)
        else:
            nw0.send_reply_to(countdown, True)


if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])
