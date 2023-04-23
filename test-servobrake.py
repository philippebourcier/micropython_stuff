
from time import sleep
import servobrake

servobrake=servobrake.Servo(PWMA=10,AIN2=11,AIN1=12,STBY=13,EncA=14,EncB=15,Debug=True)

servobrake.fwd(90)
sleep(1)
servobrake.bwd(90)

