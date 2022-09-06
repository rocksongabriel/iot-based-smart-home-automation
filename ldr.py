from machine import ADC, Pin


class LDR:
    
    def __init__(self, pin_number, atten=None):
        
        # Initialize ADC
        self.adc = ADC(Pin(pin_number))
        
    def read_raw(self):
        self.adc.read_uv()
        
    def value(self):
        return self.read_raw()
        
        

ldr1 = ADC(Pin(36))
ldr2 = ADC(Pin(13))
print(ldr1.read_uv()/1000)
print(ldr2.read_uv()/1000)

print(ldr1.read_u16())
print(ldr1.read_u16())