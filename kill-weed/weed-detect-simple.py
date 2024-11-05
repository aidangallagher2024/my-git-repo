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
import cv2
import time
led_pin = 7
seconds=1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)


net = detectNet(model="/home/group8/jetson-inference2/jetson-inference/python/training/detection/ssd/models/fake-plants/ssd-mobilenet.onnx", labels="/home/group8/jetson-inference2/jetson-inference/python/training/detection/ssd/models/fake-plants/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

camera = videoSource("/dev/video4")      # '/dev/video0' for V4L2
display = videoOutput("display://0") # 'my_video.mp4' for file
#display2 = videoOutput("/home/group8/jetson-inference/python/kill-weed/my_video.mp4") # 'my_video.mp4' for file

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
        if det.ClassID==1:
            GPIO.output(led_pin, GPIO.HIGH)
            print("led is on")
        else:
            GPIO.output(led_pin, GPIO.LOW)
            print("led is off")
GPIO.cleanup()
