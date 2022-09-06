import _thread
import time

import BlynkLib as blynklib
from dht22 import read_temperature_and_humidity
from light_and_socket import switch_bulb, switch_socket
import machine
from machine import Pin
import utime
from wifi_config import connect_to_wifi

onboard_led = machine.Pin(2, machine.Pin.OUT)
pir = Pin(34, Pin.IN)

# PIR code
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

# Establish wifi connection
WIFI_SSID = "Movable Bot"
WIFI_PASSWORD = "22112001"

connection_status = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)[0]

if connection_status:

    # Establish connection with Blynk
    BLYNK_AUTH_TOKEN = "YKOfSGwfFR8SUxUiPQNSdxDOS8Hhk-ZD"
    blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN, server="blynk.cloud")


def write_temperature_and_humidity():
    temperature, humidity = read_temperature_and_humidity()

    T_VPIN = 33
    H_VPIN = 34

    blynk.virtual_write(T_VPIN, temperature)
    blynk.virtual_write(H_VPIN, humidity)

    print(f"Writing Temperature: {temperature}, Humidity: {humidity} to sever ...")


# Register connection handlers
@blynk.ON("connected")
def connected_handler(ping):
    # Sync the virtual pins when the the device connects
    blynk.sync_virtual(0, 1, 2)  # Sync virtual pins 0, 1, 2
    onboard_led.on()  # Turn LED on
    print(f"Connected to blynk server ... Ping: {ping}ms")


@blynk.ON("disconnected")
def disconnected_handler(ping):
    print(f"Disconnected from blynk server ... Ping: {ping}ms")


# Register handlers for the light and socket
@blynk.ON("V0")  # Virtual Pin 0
def inside_light_handler(value):
    value = int(value[0])
    print(f"Switching inside light {'on' if value == 1 else 'off' } ...")
    switch_bulb("inside", value)


@blynk.ON("V1")  # Virtual Pin 1
def outside_light_handler(value):
    value = int(value[0])
    print(f"Switching outside light {'on' if value == 1 else 'off' } ...")
    switch_bulb("outside", value)


@blynk.ON("V2")  # Virtual Pin 2
def socket_handler(value):
    value = int(value[0])
    print(f"Switching socket {'on' if value == 1 else 'off' } ...")
    switch_socket(value)


def runLoop():
    START_TIME_FOR_TEMP_UPLOAD = utime.ticks_ms()
    WAIT_TIME = 2000  # 2 seconds

    START_TIME_FOR_PIR = utime.ticks_ms()

    while True:

        now = utime.ticks_ms()

        # Send temperature and humidity data to blynk each 2 seconds
        if utime.ticks_diff(now, START_TIME_FOR_TEMP_UPLOAD) > WAIT_TIME:
            write_temperature_and_humidity()
            START_TIME_FOR_TEMP_UPLOAD = now

        # TODO: if the PIR detects motion, turn on the lights
        # If it detects motion again, turn off the lights
        # Turn internal lights on if motion is detected

        # if motion:
        #    switch_bulb("inside", 1)

        # Run the blynk instance
        blynk.run()


if __name__ == "__main__":
    runLoop()

    # Run the blynk in a different thread
    # _thread.stack_size(5*1024)
    # _thread.start_new_thread(runLoop(), ())
