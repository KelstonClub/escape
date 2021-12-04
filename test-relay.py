from RPi import GPIO
def cleanup(*args): print("Cleanup in progress")
GPIO.cleanup = cleanup
import gpiozero

relay1 = gpiozero.OutputDevice(21, active_high=True, initial_value=False)
relay2 = gpiozero.OutputDevice(20, active_high=True, initial_value=False)
relay3 = gpiozero.OutputDevice(26, active_high=True, initial_value=False)

input("Press enter")

relays = [relay1, relay2, relay3]
for relay in relays:
    relay.on()