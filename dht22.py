from dht import DHT22
import time
from machine import Pin


DHT22_GPIO_PIN = 33

sensor = DHT22(Pin(DHT22_GPIO_PIN, Pin.IN, Pin.PULL_UP))

# Read the temperature and humidity every 2 seconds
def read_temperature_and_humidity():
    try:
        sensor.measure()
    except OSError as e:
        print(f"Couldn't read dht22 sensor data: {e}")
    else:
        global temperature
        global humidity
        temperature = sensor.temperature()
        humidity = sensor.humidity()
    return temperature, humidity