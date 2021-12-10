import RPi.GPIO as GPIO
import time

keypad_solution = "A86#3"

L1 = 5
L2 = 6
L3 = 19
L4 = 13

C1 = 16
C2 = 12
C3 = 25
C4 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    char_pressed = ""
    if(GPIO.input(C1) == 1):
        char_pressed = characters[0]
    if(GPIO.input(C2) == 1):
        char_pressed = characters[1]
    if(GPIO.input(C3) == 1):
        char_pressed = characters[2]
    if(GPIO.input(C4) == 1):
        char_pressed = characters[3]
    GPIO.output(line, GPIO.LOW)
    return char_pressed

current_code = ""
last_char = ""

lines = [ (L1, ["1","2","3","A"]),
          (L2, ["4","5","6","B"]),
          (L3, ["7","8","9","C"]),
          (L4, ["*","0","#","D"]) ]

start_time = time.time()
print(start_time)

try:
    while True:
        for i in range(4):
            new_char = readLine(lines[i][0], lines[i][1])
            if new_char:
                if last_char != new_char:
                    print("valid: {}".format(new_char))
                    current_code += new_char
                    last_char = new_char
                    start_time = time.time()
                continue
        
        if len(current_code) == 5:
            if current_code == keypad_solution:
                print("correct!")
            else:
                print("wrong!")

            current_code = ""
        
        time.sleep(0.1)
        
        print(len(current_code))
        if (time.time() - start_time > 5) and len(current_code) > 0:
            print(time.time() - start_time)
            print("reset")
            current_code = ""

except KeyboardInterrupt:
    print("\nApplication stopped!")

