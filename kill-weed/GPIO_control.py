import Jetson.GPIO as GPIO
import time

valve1_pin=7
valve2_pin=12
valve3_pin=15
valve4_pin=33
valve5_pin=32

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


     
GPIO.output(valve1_pin, GPIO.LOW)
GPIO.output(valve2_pin, GPIO.LOW)
GPIO.output(valve3_pin, GPIO.LOW)
GPIO.output(valve4_pin, GPIO.LOW)
GPIO.output(valve5_pin, GPIO.LOW)

while(1):
    with open('bounding_box_info.txt') as f:
            i=1
            lines = f.readlines()   #list of lines in file
            for line in lines: #search every line
                if i==5:
                    solenoid_selection = line
                    print(line)
                    i=1
                else:
                     i=i+1
                

                #VALVE 1 ACTIVATION
            if solenoid_selection == 'valve1_pin':
                GPIO.output(valve1_pin, GPIO.HIGH)
                GPIO.output(valve2_pin, GPIO.LOW)
                GPIO.output(valve3_pin, GPIO.LOW)
                GPIO.output(valve4_pin, GPIO.LOW)
                GPIO.output(valve5_pin, GPIO.LOW)
                time.sleep(1)
                Output_low()
                time.sleep(3)
                #VALVE 2 ACTIVATION
            elif solenoid_selection == 'valve2_pin':
                GPIO.output(valve1_pin, GPIO.LOW)
                GPIO.output(valve2_pin, GPIO.HIGH)
                GPIO.output(valve3_pin, GPIO.LOW)
                GPIO.output(valve4_pin, GPIO.LOW)
                GPIO.output(valve5_pin, GPIO.LOW)
                time.sleep(1)
                Output_low()
                time.sleep(3)
                #VALVE 3 ACTIVATION
            elif solenoid_selection == 'valve3_pin':
                GPIO.output(valve1_pin, GPIO.LOW)
                GPIO.output(valve2_pin, GPIO.LOW)
                GPIO.output(valve3_pin, GPIO.HIGH)
                GPIO.output(valve4_pin, GPIO.LOW)
                GPIO.output(valve5_pin, GPIO.LOW)
                time.sleep(1)
                Output_low()
                time.sleep(3)
                #VALVE 4 ACTIVATION
            elif solenoid_selection == 'valve4_pin':
                GPIO.output(valve1_pin, GPIO.LOW)
                GPIO.output(valve2_pin, GPIO.LOW)
                GPIO.output(valve3_pin, GPIO.LOW)
                GPIO.output(valve4_pin, GPIO.HIGH)
                GPIO.output(valve5_pin, GPIO.LOW)
                time.sleep(1)
                Output_low()
                time.sleep(3)
                #VALVE 5 ACTIVATION
            elif solenoid_selection == 'valve5_pin':
                GPIO.output(valve1_pin, GPIO.LOW)
                GPIO.output(valve2_pin, GPIO.LOW)
                GPIO.output(valve3_pin, GPIO.LOW)
                GPIO.output(valve4_pin, GPIO.LOW)
                GPIO.output(valve5_pin, GPIO.HIGH)
                time.sleep(1)
                Output_low()
                time.sleep(3)
     
GPIO.cleanup()