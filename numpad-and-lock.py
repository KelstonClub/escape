import os, sys
from pygame import mixer
mixer.init()
import networkzero as nw0

def wait_for_numpad():
    raise NotImplementedError

def unlock():
    raise NotImplementedError

def play_success():
    mixer.Sound("success.wav").play()

def play_error():
    mixer.Sound("failure.wav").play()

def main():
    stairway = nw0.discover("stairway")
    passageway = nw0.discover("passageway")

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
