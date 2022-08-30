from dht import DHT22
import time
from machine import Pin

sensor = DHT22(Pin(33))

# Read the temperature and humidity every 2 seconds
def read_temperature_and_humidity():
    try:
        sensor.measure()
    except OSError as e:
        print(e)
    else:
        global temperature
        global humidity
        temperature = sensor.temperature()
        humidity = sensor.humidity()
    return temperature, humidity


if __name__ == "__main__":
    START = time.ticks_ms()
    WAIT_INTERVAL = 2000
    
    while True:
        if time.ticks_ms() - START >= WAIT_INTERVAL:
            temperature, humidity = read_temperature_and_humidity()
            print(f'Temperature: {temperature}*C, Humidity: {humidity}%')
            START = time.ticks_ms()
            print(temperature)
    