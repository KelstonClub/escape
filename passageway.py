import os, sys
import time
import networkzero as nw0

def reset():
    print("About to reset...")
    time.sleep(0.2)

def activate():
    print("About to activate...")
    time.sleep(0.2)

def main():
    passageway = nw0.advertise("passageway")

    while True:
        print("Waiting for command...")
        command = nw0.wait_for_message_from(passageway)

        if command == "reset":
            reset()
        elif command == "activate":
            activate()
        else:
            raise RuntimeError("Unrecognised command: %s" % command)

if __name__ == '__main__':
    main(*sys.argv[1:])
