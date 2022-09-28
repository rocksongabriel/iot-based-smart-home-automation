from machine import Pin, ADC
from time import sleep

thresholdValue = 400

ldr = ADC(Pin(36))
led = Pin(2, Pin.OUT)

ldr.atten(ADC.ATTN_11DB)

def read_ldr():
    ldr_value = ldr.read()
    return ldr_value
