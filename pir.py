import time
from machine import Pin

# Detect motion when a person enters the room.
# Detect presence when someone is still in the room.

# Detect presence when a person enters the room.
"""
1. Use an interrupt to monitor the sensor.
2. Turn on the lights after the 
"""

# Instantiate the pins
internal_bulb = Pin(21, Pin.OUT)
led = Pin(2, Pin.OUT)
pir = Pin(34, Pin.IN)

motion = False

def handle_motion_interrupt(pin):
    global motion
    if pin.value():
        motion = True
    else:
        motion = False
    global interrupt_pin
    interrupt_pin = pin
    

# Set interrupt on pir sensor
pir.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=handle_motion_interrupt)


# Check for motion in room
while True:
    if motion:
        internal_bulb.on()
    else:
        internal_bulb.off()
        time.sleep(5)
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
