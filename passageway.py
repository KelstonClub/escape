import os, sys
import networkzero as nw0

def do_primary(target_state):
    raise NotImplementedError

def do_secondary(target_state):
    raise NotImplementedError

def main():
    passageway = nw0.advertise("passageway")
    command = nw0.wait_for_message_from(passageway)

    if command == "activate":
        activate()
    else:
        raise NotImplementedError

if __name__ == '__main__':
    main(*sys.argv[1:])
