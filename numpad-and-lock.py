import os, sys
import time

from pygame import mixer
mixer.init()
import networkzero as nw0

def reset():
    print("About to reset...")
    time.sleep(0.2)

def handle_message(message):
    print("About to handle message", message, "...")
    time.sleep(0.2)

def wait_for_numpad():
    print("About to wait for numpad...")
    time.sleep(0.2)

def unlock():
    print("About to unlock...")
    time.sleep(0.2)

def play_success():
    mixer.Sound("success.wav").play()

def play_error():
    mixer.Sound("failure.wav").play()

def main():
    numpad = nw0.advertise("numpad")
    stairway = nw0.discover("stairway")
    passageway = nw0.discover("passageway")

    while True:
        print("Checking for message...")
        message = nw0.wait_for_message_from(numpad, wait_for_s=0)
        if message is not None:
            handle_message(message)

        #
        # if the numpad is keyed correctly, unlock the box
        #
        wait_for_numpad()
        unlock()

        #
        # Turn the main lights off
        #
        if nw0.send_message_to(stairway, ("primary", "off")):
            play_success()
        else:
            play_error()

        #
        # Turn the secondary lights on
        #
        if nw0.send_message_to(stairway, ("secondary", "on")):
            play_success()
        else:
            play_error()

        #
        # Send a message to the passageway controller for it to
        # do its thing
        #
        if nw0.send_message_to(passageway, "activate"):
            play_success()
        else:
            play_error()


if __name__ == '__main__':
    main(*sys.argv[1:])
