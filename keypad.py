import RPi.GPIO as GPIO
import time

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

pin_code = "1234"
user_input = ""
current_key = None


def keypress_callback(channel):
    global current_key

    if current_key is None:
        current_key = channel


def setup_gpio():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(C1, GPIO.RISING, callback=keypress_callback)
    GPIO.add_event_detect(C2, GPIO.RISING, callback=keypress_callback)
    GPIO.add_event_detect(C3, GPIO.RISING, callback=keypress_callback)
    GPIO.add_event_detect(C4, GPIO.RISING, callback=keypress_callback)


def set_state(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)


def get_code():
    global user_input

    pressed = False
    GPIO.output(L3, GPIO.HIGH)
    GPIO.output(L3, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)

    if not pressed and GPIO.input(C4) == 1:
        if user_input == pin_code:
            print("yes")
        else:
            print("no")
        pressed = True

    GPIO.output(L3, GPIO.LOW)

    if pressed:
        user_input = ""

    return pressed


def readLine(line, characters):
    global user_input

    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        user_input += characters[0]
    if GPIO.input(C2) == 1:
        user_input += characters[1]
    if GPIO.input(C3) == 1:
        user_input += characters[2]
    if GPIO.input(C4) == 1:
        user_input += characters[3]

    GPIO.output(line, GPIO.LOW)


def main():
    global current_key

    try:
        while True:
            if current_key is None:
                set_state(GPIO.HIGH)
                if not GPIO.input(current_key):
                    current_key = None
                else:
                    time.slep(0.1)
            else:
                if not get_code():
                    readLine(L1, ["1", "2", "3", "A"])
                    readLine(L2, ["4", "5", "6", "B"])
                    readLine(L3, ["7", "8", "9", "C"])
                    readLine(L4, ["*", "0", "#", "D"])
                    time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nApplication stopped!")


if __name__ == "__main__":
    setup_gpio()
    main()
