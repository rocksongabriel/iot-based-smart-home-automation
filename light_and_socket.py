from machine import Pin
import time


inside_bulb = Pin(21, Pin.OUT)
outside_bulb = Pin(22, Pin.OUT)
socket = Pin(5, Pin.OUT)

def switch_bulb(location, mode):
    """
    location: `inside` or `outside`
    mode: 1 or 0
    """
    
    if location == 'inside':
        if mode == 1:
            inside_bulb.on()
        elif mode == 0:
            inside_bulb.off()
    elif location == 'outside':
        if mode == 1:
            outside_bulb.on()
        elif mode == 0:
            outside_bulb.off()


def switch_socket(mode):
    """
    mode: 1 or 0
    """
    
    if mode == 1:
        socket.on()
    elif mode == 0:
        socket.off()
        

