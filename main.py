import _thread
import time

import BlynkLib as blynklib
from dht22 import read_temperature_and_humidity
from light_and_socket import switch_bulb, switch_socket
import machine
from machine import Pin
import utime
from wifi_config import connect_to_wifi
from ldr import read_ldr
from fan import change_speed_of_fan

onboard_led = machine.Pin(2, machine.Pin.OUT)
pir = Pin(34, Pin.IN)

# PIR code
motion = False

override_ldr = 0
override_pir = 0
override_fan = 0

current_temperature = 0
current_humidity = 0



# Set interrupt on pir sensor
#pir.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handle_motion_interrupt)

# Establish wifi connection
WIFI_SSID = "Daasebre"
WIFI_PASSWORD = "Daasebre"

connection_status = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)[0]

if connection_status:

    # Establish connection with Blynk
    BLYNK_AUTH_TOKEN = "YKOfSGwfFR8SUxUiPQNSdxDOS8Hhk-ZD"
    blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN, server="blynk.cloud")

def change_indicator_status_on_dashboard(pin=None, value=None):
    # value: 0 or 1
    # pin: number of the virtual pin
    blynk.virtual_write(pin, value)

def write_temperature_and_humidity():
    temperature, humidity = read_temperature_and_humidity()
    global current_temperature
    global current_humidity
    
    current_temperature = temperature
    current_humidity = humidity

    T_VPIN = 33
    H_VPIN = 34

    blynk.virtual_write(T_VPIN, temperature)
    blynk.virtual_write(H_VPIN, humidity)

    print(f"Writing Temperature: {temperature}, Humidity: {humidity} to sever ...")


# Register connection handlers
@blynk.on("connected")
def connected_handler(ping):
    # Sync the virtual pins when the the device connects
    blynk.sync_virtual(0, 1, 2, 4, 9, 11)  # Sync virtual pins 0, 1, 2
    onboard_led.on()  # Turn LED on
    print(f"Connected to blynk server ... Ping: {ping}ms")


@blynk.on("disconnected")
def disconnected_handler(ping):
    print(f"Disconnected from blynk server ... Ping: {ping}ms")


# Register handlers for the light and socket
@blynk.on("V0")  # Virtual Pin 0
def inside_light_handler(value):
    value = int(value[0])
    if (value == 1 or value == 0 and override_pir == 1) or (override_pir == 1 and value == 1 or value == 0):
        print(f"MANUALLY Switching inside light {'on' if value == 1 else 'off' } ...")
        switch_bulb("inside", value)
        change_indicator_status_on_dashboard(5, value)


@blynk.on("V1")  # Virtual Pin 1
def outside_light_handler(value):
    value = int(value[0])
    
    if (value == 1 or value == 0 and override_ldr == 1 ) or (override_ldr == 1 and value == 1 or value == 0):
        print(f"MANUALLY Switching outside light {'on' if value == 1 else 'off' } ...")
        switch_bulb("outside", value)
        change_indicator_status_on_dashboard(6, value)


@blynk.on("V2")  # Virtual Pin 2
def socket_handler(value):
    value = int(value[0])
    print(f"MANUALLY Switching socket {'on' if value == 1 else 'off' } ...")
    switch_socket(value)
    change_indicator_status_on_dashboard(7, value)
    
@blynk.on("V9")
def fan_handler(value):
    value = int(value[0])
    if (override_fan == 1 and value in [0, 1, 2, 3]) or (value in [0, 1, 2, 3] and override_fan == 1):
        change_speed_of_fan(speed = value)


# Override the ldr value
@blynk.on("V4")
def override_ldr_handler(value):
    value = int(value[0])
    global override_ldr
    override_ldr = value
    change_indicator_status_on_dashboard(8, value)
    
@blynk.on("V10")
def override_pir_handler(value):
    value = int(value[0])
    global override_pir
    override_pir = value
    change_indicator_status_on_dashboard(10, value)
    
@blynk.on("V11")
def override_fan_handler(value):
    value = int(value[0])
    global override_fan
    override_fan = value
    
    
    
def runLoop():
    START_TIME_FOR_TEMP_UPLOAD = utime.ticks_ms()
    WAIT_TIME = 5000  # 5 seconds

    START_TIME_FOR_PIR = utime.ticks_ms()
    
    START_TIME_FOR_LDR = utime.ticks_ms()
    LDR_WAIT_TIME = 2000 # 2 seconds

    START_TIME_FOR_FAN_CONTROL = utime.ticks_ms()
    FAN_CONTROL_WAIT_TIME = 2000 # 2 seconds
    
    while True:

        now = utime.ticks_ms()

        # Send temperature and humidity data to blynk each 2 seconds
        if utime.ticks_diff(now, START_TIME_FOR_TEMP_UPLOAD) > WAIT_TIME:
            write_temperature_and_humidity()
            START_TIME_FOR_TEMP_UPLOAD = now
            
        # check ldr value and turn on external lights if it falls below threshold
        lightThreshold = 400
        
        if utime.ticks_diff(now, START_TIME_FOR_LDR) > LDR_WAIT_TIME:
            ldr_value = read_ldr()
            if ldr_value < lightThreshold and override_ldr == 0:
                switch_bulb("outside", 1)
                change_indicator_status_on_dashboard(1, 1) # turn the button on, on the interface
                change_indicator_status_on_dashboard(6, 1) # change outside light status
            elif ldr_value > lightThreshold and override_ldr == 0:
                switch_bulb("outside", 0)
                change_indicator_status_on_dashboard(1, 0) # turn the button off, on the interface
                change_indicator_status_on_dashboard(6, 0) # change outside light status
            
            START_TIME_FOR_LDR = now
                
        # AUTOMATIC CONTROL OF FAN
        if utime.ticks_diff(now, START_TIME_FOR_FAN_CONTROL) > FAN_CONTROL_WAIT_TIME:
            if override_fan == 0:
                if current_temperature <= 22.9:
                    change_speed_of_fan(speed=0)
                elif current_temperature >=23 or current_temperature <= 24.9:
                    change_speed_of_fan(speed=1)
                elif current_temperature >= 25 or current_temperature <= 27:
                    change_speed_of_fan(speed=2)
                elif current_temperature >= 27.1 and override_fan == 0:
                    change_speed_of_fan(speed=3)
                
            
            START_TIME_FOR_FAN_CONTROL = now

        # TODO: if the PIR detects motion, turn on the lights
        # If it detects motion again, turn off the lights
        # Turn internal lights on if motion is detected

        if motion and override_pir == 0:
            switch_bulb("inside", 1)
            change_indicator_status_on_dashboard(0, 1)
            change_indicator_status_on_dashboard(5, 1)
            

        # Run the blynk instance
        blynk.run()


if __name__ == "__main__":
    runLoop()

    # Run the blynk in a different thread
    # _thread.stack_size(5*1024)
    # _thread.start_new_thread(runLoop(), ())
