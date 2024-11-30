import Jetson.GPIO as GPIO
from encoder import Encoder
import time

OUT_A = 26
OUT_B = 24

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUT_A, GPIO.IN)
GPIO.setup(OUT_B, GPIO.IN)

def valueChanged(value):
    pass # Or do something useful with the value here!

e1 = Encoder(OUT_B, OUT_A, callback=valueChanged)

while(1):
    print(e1)
    time.sleep(1)