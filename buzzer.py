from machine import Pin, PWM
import time

pin_23 = Pin(23, Pin.OUT)

buzzer = PWM(pin_23)
buzzer.freq(1047)
buzzer.duty(50)

time.sleep(5)

buzzer.duty(0)
buzzer.deinit()