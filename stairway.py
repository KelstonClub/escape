import os, sys
import networkzero as nw0

def reset():
    raise NotImplementedError

def handle_primary(target_state):
    print("About to handle primary", target_state, "...")
    time.sleep(0.2)

def handle_secondary(target_state):
    print("About to handle secondary", target_state, "...")
    time.sleep(0.2)

def handle_message(message):
    (zone, state) = message

    if zone == "primary":
        handle_primary(state)
    elif zone == "secondary":
        handle_secondary(state)
    else:
        raise RuntimeError("Unrecognised message: %s" % message)

def main():
    stairway = nw0.advertise("stairway")

    while True:
        print("Waiting for message...")
        message = nw0.wait_for_message_from(stairway)
        if message == "reset":
            reset()
        else:
            handle_message(message)


if __name__ == '__main__':
    main(*sys.argv[1:])
