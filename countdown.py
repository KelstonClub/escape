NODE = "countdown"

import os, sys
import logging
logger = logging.getLogger(NODE)

LOGGING_FILEPATH = f"escape-{NODE}.log"
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
file_handler = logging.FileHandler(LOGGING_FILEPATH)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

import threading
import time

HERE = os.path.abspath(os.path.dirname(sys.argv[0]))
logger.info("HERE: %s", HERE)
logger.info("cwd: %s", os.getcwd())

logger.info("About to import vlc")
import vlc
logger.info("vlc imported as %r", vlc)

import networkzero as nw0
logger.info("nw0 imported as %s", nw0)

HEARTBEAT_ADDRESS = nw0.address()
HEARTBEAT_INTERVAL_S = 2.0

player = vlc.MediaPlayer(os.path.join(HERE, "background-sounds/countdown.mp4"))
logger.info("VLC Player %r", player)
player.set_fullscreen(True)
player.audio_set_volume(100)

def stop():
    player.stop()

def reset():
    logger.info("About to reset...")
    player.stop()
    player.play()
    #~ time.sleep(0.5)
    player.set_rate(1.0)
    #~ player.pause()
    logger.info("Reset complete")

def play():
    logger.info("About to play...")
    player.play()

def speed_up():
    logger.info("About to speed up")
    player.set_rate(1.5)

def pause():
    logger.info("About to pause")
    player.pause()

def handle_command(command):
    if command == "reset":
        reset()
    elif command == "stop":
        stop()
    elif command == "start":
        play()
    elif command == "speed_up":
        speed_up()
    elif command == "pause":
        pause()
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
    logger.info("About to reset")
    reset()
    logger.info("About to advertise")
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
    main(*sys.argv[1:])
