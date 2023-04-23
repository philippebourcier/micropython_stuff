# Micropython lib for driving the TB6612FNG on RP2 RP2040 Pico

from machine import Pin,PWM

class Motor():
    def __init__(self,STBY,AIN1,AIN2,PWMA):
        self.ain2 = Pin(AIN2, mode=Pin.OUT, pull=None)
        self.ain1 = Pin(AIN1, mode=Pin.OUT, pull=None)
        self.stby = Pin(STBY, mode=Pin.OUT, pull=None)
        # frequency 50 Hz
        self.apwm = PWM(Pin(PWMA))
        self.apwm.freq(50)
        self.stby.value(1)
        
    def forward(self,speed):
        self.stby.value(1)
        self.ain1.value(1)
        self.ain2.value(0)
        self.apwm.duty_u16(speed)
    
    def backward(self,speed):
        self.stby.value(1)
        self.ain1.value(0)
        self.ain2.value(1)
        self.apwm.duty_u16(speed)

    def brake(self):
        self.ain1.value(1)
        self.ain2.value(1)        
        self.apwm.duty_u16(0)
        
    def stop(self):
        self.ain1.value(0)
        self.ain2.value(0)        
        self.apwm.duty_u16(65535)
        
    def standby(self):
        self.ain1.value(0)
        self.ain2.value(0)
        self.apwm.duty_u16(65535)
        self.stby.value(0)
