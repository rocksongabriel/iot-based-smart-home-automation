import utime as time
from machine import Pin

from dht22 import read_temperature_and_humidity
from blynk import get_blynk

blynk = get_blynk()

T_VPIN = 33

@blynk.handle_event(f"read V{T_VPIN}")
def temperature_and_humidity_handler(vpin):
    
    # read the sensor dta
    temperature, humidity = read_temperature_and_humidity()
    print(temperature, humidity)
    

while True:
    blynk.run()