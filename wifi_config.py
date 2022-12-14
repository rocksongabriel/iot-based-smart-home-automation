import network
import time
from machine import Pin

onboard_led = Pin(2, Pin.OUT)


def connect_to_wifi(SSID, PASSWORD):
    wifi = network.WLAN(network.STA_IF)
    connected = False
    
    connection_timeout = 0
    
    # Refresh the connection
    wifi.active(False)
    wifi.active(True)
    
    # connect wifi
    wifi.connect(SSID, PASSWORD)
    
    print(f"Connecting to WiFi network '{SSID}'")
    onboard_led.on()
    time.sleep(2)
    onboard_led.off()
    # while the wifi has not connected, keep trying for 5 seconds
    while not wifi.isconnected() and connection_timeout < 10:
        connection_timeout += 1
        time.sleep(1)
        onboard_led.on()
        print(f'Retrying to connect to wifi... {connection_timeout}')
        time.sleep(1)
        onboard_led.off()
        
    # if the wifi gets connected, print the connection details
    if wifi.isconnected():
        connected = True
        print('Wifi has connected successfully ...')
        print(wifi.ifconfig())
    else:
        print('Connection Timeout !!!')
    
    # return True if the connection is successful
    return connected, wifi.ifconfig()
