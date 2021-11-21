import os, sys
import networkzero as nw0

def do_primary(target_state):
    raise NotImplementedError

def do_secondary(target_state):
    raise NotImplementedError

def main():
    stairway = nw0.advertise("stairway")
    (zone, state) = nw0.wait_for_message_from(stairway)

    if zone == "primary":
        do_primary(state)
    elif zone == "secondary":
        do_secondary(state)
    else:
        raise NotImplementedError

if __name__ == '__main__':
    main(*sys.argv[1:])
