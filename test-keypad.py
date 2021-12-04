import time

from gpiozero import InputDevice

L1 = InputDevice(21)
L2 = InputDevice(20)
L3 = InputDevice(16)
L4 = InputDevice(12)
L5 = InputDevice(26)
L6 = InputDevice(19)
L7 = InputDevice(13)
L8 = InputDevice(6)

lines = [L1, L2, L3, L4, L5, L6, L7, L8]

while True:
    print([i.is_active for i in lines])
    time.sleep(0.5)
