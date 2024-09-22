from machine import Pin
from utime import sleep

# Initialize GPIO pin 8 as an output pin
pin = Pin(8, Pin.OUT)

print("LED starts flashing...")
while True:
    try:
        # Manually toggle the pin state
        pin.value(not pin.value())
        sleep(1)  # sleep 1sec
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")
