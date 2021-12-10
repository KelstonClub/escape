import os, sys
import logging
logger = logging.getLogger("numpad")
import time

import RPi.GPIO as GPIO
import gpiozero

from pygame import mixer
mixer.init()
import networkzero as nw0

from relays import relay_ctrl

MUSIC_FOLDER = "/home/pi/escape/background-sounds"

music = { "base" : "general_soundtrack_knives_out.wav",
          "intense" : "intense_knives_out.wav"}

ambience = { "general" : "ambience.wav",
             "wind": "general_soundtrack_knives_out.wav",
             "mice": "mice.wav" }

keypad_solution = "A86#3"

class keypad_ctrl:
    L1 = 5
    L2 = 6
    L3 = 19
    L4 = 13

    C1 = 16
    C2 = 12
    C3 = 25
    C4 = 24

    lines = [ (L1, ["1","2","3","A"]),
              (L2, ["4","5","6","B"]),
              (L3, ["7","8","9","C"]),
              (L4, ["*","0","#","D"]) ]

    def __init__(self, solution):
        GPIO.setwarnings(False)
        # general initialization?
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)
        GPIO.setup(self.L3, GPIO.OUT)
        GPIO.setup(self.L4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.solution = solution
        self.current_code = ""
        self.start_time = time.time()
        self.last_char = ""

        self.valid_key_sound = mixer.Sound("beep.wav")
        self.valid_key_sound.set_volume(0.65)

        self.wrong_password_sound = mixer.Sound("wrong.wav")
        self.wrong_password_sound.set_volume(0.4)

        self.correct_password_sound = mixer.Sound("success.wav")
        self.correct_password_sound.set_volume(0.4)

    def readLine(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        char_pressed = ""
        if(GPIO.input(self.C1) == 1):
            char_pressed = characters[0]
        if(GPIO.input(self.C2) == 1):
            char_pressed = characters[1]
        if(GPIO.input(self.C3) == 1):
            char_pressed = characters[2]
        if(GPIO.input(self.C4) == 1):
            char_pressed = characters[3]

        GPIO.output(line, GPIO.LOW)
        return char_pressed

    def refresh_keypad(self):
        for i in range(4):
            new_char = self.readLine(self.lines[i][0], self.lines[i][1])
            if new_char:
                if self.last_char != new_char:
                    print("Valid character: {}".format(new_char))
                    self.valid_key_sound.play()
                    self.current_code += new_char
                    self.last_char = new_char
                    self.start_time = time.time()
                continue
        
        if len(self.current_code) == 5:
            if self.current_code == self.solution:
                self.correct_password_sound.play()
                self.current_code = ""
                time.sleep(1)
                return True
            else:
                self.wrong_password_sound.play()
                self.last_char = ""

            self.current_code = ""
        
        time.sleep(0.1)
        
        if (time.time() - self.start_time > 5) and len(self.current_code) > 0:
            self.wrong_password_sound.play()
            print("Doing a reset")
            self.current_code = ""
            self.last_char = ""

        return False


def set_athmosphere_phase1(relays, studio, passageway):
    play_music(music["base"])
    
    relays.switch_normal_light(True)
    relays.switch_black_light(True)
    relays.switch_keypad_lock(True)

    nw0.send_message_to(studio, ("primary", None))
    nw0.send_message_to(passageway, ("primary", None))

def set_athmosphere_phase2(relays, studio, passageway):
    play_music(music["intense"])
    relays.switch_normal_light(False)
    relays.switch_black_light(False)
    nw0.send_message_to(studio, ("secondary", None))
    nw0.send_message_to(passageway, ("secondary", None))
    
    time.sleep(1)
    relays.switch_keypad_lock(False)

def set_stable(relays):
    relays.switch_normal_light(True)
    relays.switch_black_light(True)
    relays.switch_keypad_lock(True)    

def reset(relays, studio , passageway):
    set_stable(relays)
    nw0.send_message_to(studio, ("reset", None))
    nw0.send_message_to(passageway, ("reset", None))
    time.sleep(0.2)

def handle_message(message):
    logger.info("About to handle message %s ...", message)
    time.sleep(0.2)

def wait_for_numpad():
    logger.info("About to wait for numpad...")
    while True:
        combo = input("Enter the combination:")
        if combo == "1234":
            return True
        else:
            time.sleep(0.2)

def unlock():
    logger.info("About to unlock...")
    time.sleep(0.2)

def play_ambience():
    mixer.Sound("/home/pi/escape/background-sounds/ambience.wav")

# stop the previous music and run this one
def play_music(music_track):
    mixer.music.load(os.path.join(MUSIC_FOLDER, music_track))
    mixer.music.set_volume(0.75)
    mixer.music.play()

def main():
    # initialize services
    numpad = nw0.advertise("numpad")

    logger.info("Looking for studio...")
    studio = nw0.discover("studio")
    logger.info("Found studio at %s", studio)

    logger.info("Looking for passageway...")
    passageway = nw0.discover("passageway")
    logger.info("Found passageway at %s", passageway)

    keypad = keypad_ctrl(keypad_solution)
    relays = relay_ctrl()
    set_athmosphere_phase1(relays, studio, passageway)

    try:
        while True:
            if keypad.refresh_keypad():
                break

        set_athmosphere_phase2(relays, studio, passageway)
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        reset(relays, studio, passageway)
        print("\nApplication stopped!")
        exit(0)

    while True:
        logger.info("Checking for message...")
        message = nw0.wait_for_message_from(numpad, wait_for_s=0)
        if message is not None:
            handle_message(message)

        #
        # if the numpad is keyed correctly, unlock the box
        #
        wait_for_numpad()
        unlock()

        logger.info("About to turn primary lights off..")
        #
        # Turn the main lights off
        #
        if nw0.send_message_to(studio, ("primary", "off")):
            play_success()
        else:
            play_error()

        logger.info("About to turn secondary lights on..")
        #
        # Turn the secondary lights on
        #
        if nw0.send_message_to(studio, ("secondary", "on")):
            play_success()
        else:
            play_error()

        logger.info("About to activate passageway..")
        #
        # Send a message to the passageway controller for it to
        # do its thing
        #
        if nw0.send_message_to(passageway, "activate"):
            play_success()
        else:
            play_error()

if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    main(*sys.argv[1:])
