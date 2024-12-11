from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import Jetson.GPIO as GPIO
import time
import serial

valve1_pin=21
valve2_pin=22
valve3_pin=15
valve4_pin=33
valve5_pin=32

#encoder_input = GPIO.input(encoder_pin)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(valve1_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valve2_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valve3_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valve4_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valve5_pin, GPIO.OUT, initial=GPIO.LOW)

def Output_low():
    GPIO.output(valve1_pin, GPIO.LOW)
    GPIO.output(valve2_pin, GPIO.LOW)
    GPIO.output(valve3_pin, GPIO.LOW)
    GPIO.output(valve4_pin, GPIO.LOW)
    GPIO.output(valve5_pin, GPIO.LOW)

def Output_high(f):
    Output_low()
    GPIO.output(f, GPIO.HIGH)

serial_port = serial.Serial(
    port="/dev/ttyACM0",  #was ttyTHS1 but this serial port connects to the arduino over usb
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)


while True:        
    if serial_port.inWaiting() > 0:
        data = serial_port.read()
        print(data)
        
    
serial_port.close()