# Micropython lib for driving the JGY-370 DC12V10RPM High Torque Worm Gear Box Motors with a TB6612FNG

from rp2 import StateMachine,asm_pio
from machine import Pin
from TB6612FNG import Motor
from time import sleep

@asm_pio(autopush=True,push_thresh=32)
def encoder():
    label("start")
    wait(0, pin, 0)         # Wait for CLK to go low
    jmp(pin, "WAIT_HIGH")   # if Data is low
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop1")
    label("nop1")
    mov(x, invert(x))
    label("WAIT_HIGH")      # else
    jmp(x_dec, "nop2")          # Decrement X
    label("nop2")
    wait(1, pin, 0)         # Wait for CLK to go high
    jmp(pin, "WAIT_LOW")    # if Data is low
    jmp(x_dec, "nop3")          # Decrement X
    label("nop3")    
    label("WAIT_LOW")       # else
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop4")
    label("nop4")
    mov(x, invert(x))
    wrap()

class Servo():

    def __init__(self,EncA,EncB,STBY,AIN1,AIN2,PWMA,Debug=False):
        self.sm1=StateMachine(1,encoder,freq=125_000_000,in_base=Pin(EncA),jmp_pin=Pin(EncB))
        self.sm1.active(1)
        self.motor=Motor(STBY=STBY,AIN1=AIN1,AIN2=AIN2,PWMA=PWMA)
        self.Debug=Debug

    def getpos(self):
        self.sm1.exec("in_(x,32)")
        # 6400 is for 10 RPM motor ... change this for other RPM
        return int(self.sm1.get()/(6400/360))

    def fwd(self,deg):
        self.zero=self.getpos()
        self.x=0
        self.motor.forward(65535)
        while self.x<deg-2:
            self.x=self.getpos()-self.zero
            if(self.Debug): print(self.x)
        self.motor.stop()
        self.motor.standby()
        if(self.Debug):
            for i in range(0,2): print(self.getpos()-self.zero)
        sleep(0.5)

    def bwd(self,deg):
        self.zero=self.getpos()
        self.x=0
        self.motor.backward(65535)
        while self.x<deg-2:
            self.x=self.zero-self.getpos()
            if(self.Debug): print(self.x)
        self.motor.stop()
        self.motor.standby()
        if(self.Debug):
            for i in range(0,2): print(self.zero-self.getpos())
        sleep(0.5)
