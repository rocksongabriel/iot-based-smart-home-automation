import time
from machine import Pin

# Instantiate the pins
internal_bulb = Pin(21, Pin.OUT)
led = Pin(2, Pin.OUT)


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
pir.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handle_motion_interrupt)

