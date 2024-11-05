#!/usr/bin/env python3
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import Jetson.GPIO as GPIO

valve1_pin=7
valve2_pin=11
valve3_pin=15
valve4_pin=33
valve5_pin=32

GPIO.setmode(GPIO.BOARD)
GPIO.setup(valve1_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valve2_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valve3_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valve4_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valve5_pin, GPIO.OUT, initial=GPIO.LOW)

net = detectNet(model="/home/group8/jetson-inference2/jetson-inference/python/training/detection/ssd/models/fake-plants/ssd-mobilenet.onnx", labels="/home/group8/jetson-inference2/jetson-inference/python/training/detection/ssd/models/fake-plants/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

#net = detectNet(model="/jetson-inference/python/training/detection/ssd/models/fake-plants/ssd-mobilenet.onnx", labels="/jetson-inference/python/training/detection/ssd/models/fake-plants/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

#net = detectNet(model="/jetson-inference/python/training/detection/ssd/models/fake-plants/ssd-mobilenet.onnx", threshold=0.5)
camera = videoSource("/dev/video4")      # '/dev/video0' for V4L2
display = videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
    img = camera.Capture()

    if img is None: # capture timeout
        continue

    detections = net.Detect(img)
    box_info=[]
    
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    
    for det in detections:
        box_info.append( (det.ClassID, det.Left, det.Right) )
        print(box_info)
        print(box_info[0])
        print(box_info[0][0])
        print(det.Center[0])
        print(f"Confidence: {det.Confidence * 100.0:.1f}")
        if det.ClassID == 1 : #while dandelion is in frame
            
            #VALVE 1 ACTIVATION
            if det.Right < 256:
                GPIO.output(valve1_pin, GPIO.HIGH)
                GPIO.output(valve2_pin, GPIO.LOW)
                GPIO.output(valve3_pin, GPIO.LOW)
                GPIO.output(valve4_pin, GPIO.LOW)
                GPIO.output(valve5_pin, GPIO.LOW)
            #VALVE 2 ACTIVATION
            elif det.Right>=256 and det.Right<512:
                if det.Center[0]-det.Left < det.Right-det.Center[0]:
                    GPIO.output(valve1_pin, GPIO.LOW)
                    GPIO.output(valve2_pin, GPIO.HIGH)
                    GPIO.output(valve3_pin, GPIO.LOW)
                    GPIO.output(valve4_pin, GPIO.LOW)
                    GPIO.output(valve5_pin, GPIO.LOW)
                else:
                    GPIO.output(valve1_pin, GPIO.HIGH)
                    GPIO.output(valve2_pin, GPIO.LOW)
                    GPIO.output(valve3_pin, GPIO.LOW)
                    GPIO.output(valve4_pin, GPIO.LOW)
                    GPIO.output(valve5_pin, GPIO.LOW)
                #VALVE 3 ACTIVATION
            elif det.Right>=512 and det.Right<767:
                if det.Center[0]-det.Left < det.Right-det.Center[0]:
                    GPIO.output(valve1_pin, GPIO.LOW)
                    GPIO.output(valve2_pin, GPIO.LOW)
                    GPIO.output(valve3_pin, GPIO.HIGH)
                    GPIO.output(valve4_pin, GPIO.LOW)
                    GPIO.output(valve5_pin, GPIO.LOW)
                else:
                    GPIO.output(valve1_pin, GPIO.LOW)
                    GPIO.output(valve2_pin, GPIO.HIGH)
                    GPIO.output(valve3_pin, GPIO.LOW)
                    GPIO.output(valve4_pin, GPIO.LOW)
                    GPIO.output(valve5_pin, GPIO.LOW)
                #VALVE 4 ACTIVATION
            elif det.Right>=767 and det.Right<1023:
                if det.Center[0]-det.Left < det.Right-det.Center[0]:
                    GPIO.output(valve1_pin, GPIO.LOW)
                    GPIO.output(valve2_pin, GPIO.LOW)
                    GPIO.output(valve3_pin, GPIO.LOW)
                    GPIO.output(valve4_pin, GPIO.HIGH)
                    GPIO.output(valve5_pin, GPIO.LOW)
                else:
                    GPIO.output(valve1_pin, GPIO.LOW)
                    GPIO.output(valve2_pin, GPIO.LOW)
                    GPIO.output(valve3_pin, GPIO.HIGH)
                    GPIO.output(valve4_pin, GPIO.LOW)
                    GPIO.output(valve5_pin, GPIO.LOW)
            #VALVE 5 ACTIVATION
            elif det.Left > 1023:
                    GPIO.output(valve1_pin, GPIO.LOW)
                    GPIO.output(valve2_pin, GPIO.LOW)
                    GPIO.output(valve3_pin, GPIO.LOW)
                    GPIO.output(valve4_pin, GPIO.LOW)
                    GPIO.output(valve5_pin, GPIO.HIGH)
            else:
                    GPIO.output(valve1_pin, GPIO.LOW)
                    GPIO.output(valve2_pin, GPIO.LOW)
                    GPIO.output(valve3_pin, GPIO.LOW)
                    GPIO.output(valve4_pin, GPIO.HIGH)
                    GPIO.output(valve5_pin, GPIO.LOW)
            
GPIO.cleanup()

            
