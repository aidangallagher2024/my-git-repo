from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, cudaDrawLine, cudaFont
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

serial_arr = ["","","","",""]

net = detectNet(model="/home/group8/jetson-inference2/jetson-inference/python/training/detection/ssd/models/fake-plants/ssd-mobilenet.onnx", labels="/home/group8/jetson-inference2/jetson-inference/python/training/detection/ssd/models/fake-plants/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

camera = videoSource("/dev/video4")      # '/dev/video0' for V4L2
display = videoOutput("display://0") # 'my_video.mp4' for file

state = 0
count = 0
temp = 1
new_result = "0"

##  0 = communicate state   ##  1 = moving state  ##   2 = GPIO HIGH state   ##    3 = GPIO LOW state

time.sleep(3)   #give time for everything to initialize

while display.IsStreaming():
    img = camera.Capture()

    if img is None: # capture timeout
        continue

    detections = net.Detect(img)
    box_info=[]
    cudaDrawLine(img, (256, 0), (256, 720),(255,0,200,200), 2)
    cudaDrawLine(img, (512, 0), (512, 720),(255,0,200,200), 2)
    cudaDrawLine(img, (767, 0), (767, 720),(255,0,200,200), 2)
    cudaDrawLine(img, (1023, 0), (1023, 720),(255,0,200,200), 2)
    font = cudaFont()
    font.OverlayText(img, 1000, 100, f"{new_result} feet per second at spray time" )
    
    display.Render(img)
    
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    
    timestamp2 = time.time() # updating timestamp
    #print(timestamp2)       
    
    if state == 0:   

        if serial_port.inWaiting() > 0:
            data = serial_port.read()
            if data.decode() == '\n':
                temp = 1
            if temp == 1:
                if count < 5:
                    serial_arr[count] = data.decode()
                    count += 1
                    result = ""
                else:
                   # print(serial_arr[1:5])
                    count = 0
                    temp = 0
                    result = "".join(serial_arr)
                    new_result = result.replace('\n',"").replace("\r","")
                    print(new_result)
                    font.OverlayText(img, 1000, 100, f"{new_result} feet per second at spray time" )
                    state = 1
                
    

    if state == 1:
        for det in detections:
            #print(det.Center[1])
            #print(new_result)
            font.OverlayText(img, 1000, 100, f"{new_result} feet per second at spray time" )
            if float (new_result) > 0:    ##if encoder spinning
                box_info.append( (det.ClassID, det.Left, det.Right) )
                #print(box_info)
                #print(box_info[0])
                #print(box_info[0][0])
                #print(det.Center[1])
                #print(f"Confidence: {det.Confidence * 100.0:.1f}")
                if det.ClassID == 1 and det.Confidence*100.0 > 75: #while dandelion is in frame
                    if det.Center[1] > 500 and det.Center[1] < 600:
                        #VALVE 1 ACTIVATION
                        if det.Center[0] < 256:
                            s = valve1_pin
                            timestamp1 = time.time()
                            #print(f'Before: {timestamp1}')
                            state = 2 #program is now in GPIO HIGH state
                        #VALVE 2 ACTIVATION
                        elif det.Center[0]>=256 and det.Center[0]<512:
                            s = valve2_pin
                            timestamp1 = time.time()
                            #   print(f'Before: {timestamp1}')
                            state = 2 #program is now in GPIO HIGH state
                            #VALVE 3 ACTIVATION
                        elif det.Center[0]>=512 and det.Center[0]<767:
                            s = valve3_pin
                            timestamp1 = time.time()
                            # print(f'Before: {timestamp1}')
                            state = 2 #program is now in GPIO HIGH state
                            #VALVE 4 ACTIVATION
                        elif det.Center[0]>=767 and det.Center[0]<1023:
                            s = valve4_pin
                            timestamp1 = time.time()
                            # print(f'Before: {timestamp1}')
                            state = 2 #program is now in GPIO HIGH state
                        #VALVE 5 ACTIVATION
                        elif det.Center[0]> 1023:
                            s = valve5_pin
                            timestamp1 = time.time()
                            #print(f'Before: {timestamp1}')
                            state = 2 #program is now in GPIO HIGH state
            else:
                state = 1
                Output_low()
                font.OverlayText(img, 1000, 100, f"{new_result} feet per second at spray time" )
    elif state == 2:
        
        if timestamp2 - timestamp1 > (4/12)/float(new_result):
            Output_high(s)  #s carries the valve pin we want to activate
            font.OverlayText(img, 1000, 100, f"{new_result} feet per second at spray time" )
            state = 3   #send to GPIO_LOW state
        else:
            state = 2   #stay here until half a second passes

        
    elif state == 3:
        if timestamp2 - timestamp1 > ((4/12)/float(new_result)) + 0.25:  #quarter of a second after gpio has gone high
            #print('After')
            Output_low()    #keep outputting low until a couple second buffer goes by
            font.OverlayText(img, 1000, 100, f"{new_result} feet per second at spray time" )
            if timestamp2 - timestamp1 > ((4/12)/float(new_result)) + .375:
                state = 0   #set back to detect state
                
GPIO.cleanup()
serial_port.close()

