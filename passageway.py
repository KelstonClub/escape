import os, sys
import networkzero as nw0

def reset():
    raise NotImplementedError

def do_primary(target_state):
    raise NotImplementedError

def do_secondary(target_state):
    raise NotImplementedError

def main():
    passageway = nw0.advertise("passageway")

    while True:
        command = nw0.wait_for_message_from(passageway)

        if command == "reset":
            reset()
        elif command == "activate":
            activate()
        else:
            raise RuntimeError("Unrecognised command: %s" % command)

if __name__ == '__main__':
    main(*sys.argv[1:])
