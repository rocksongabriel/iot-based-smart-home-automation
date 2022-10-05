from machine import Pin, PWM

fan_pin = Pin(16, Pin.OUT)
fan_pwm = PWM(fan_pin)

def change_speed_of_fan(speed):
    if speed == 0:
        fan_pwm.duty(0)
        print(fan_pwm.duty()) # off 
    elif speed == 1:
        fan_pwm.duty(512)
        print(fan_pwm.duty()) # 50% 
    elif speed == 2:
        fan_pwm.duty(767)
        print(fan_pwm.duty()) # 75% 
    elif speed == 3:
        fan_pwm.duty(1023)
        print(fan_pwm.duty()) # full speed
