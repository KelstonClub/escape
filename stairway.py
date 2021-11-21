import os, sys
import networkzero as nw0

def reset():
    raise NotImplementedError

def do_primary(target_state):
    raise NotImplementedError

def do_secondary(target_state):
    raise NotImplementedError

def handle_message(message):
    (zone, state) = message

    if zone == "primary":
        do_primary(state)
    elif zone == "secondary":
        do_secondary(state)
    else:
        raise RuntimeError("Unrecognised message: %s" % message)

def main():
    stairway = nw0.advertise("stairway")

    while True:
        message = nw0.wait_for_message_from(stairway)
        if message == "reset":
            reset()
        else:
            handle_message(message)


if __name__ == '__main__':
    main(*sys.argv[1:])
