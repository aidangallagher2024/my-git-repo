import Jetson.GPIO as GPIO
import time

ENCODER_A_PIN = 29  # GPIO pin for encoder A
ENCODER_B_PIN = 31   # GPIO pin for encoder B

position = 0
encoder_b_state = 0

def encoder_a_interrupt(channel):
    global position, encoder_b_state
    encoder_b_state = GPIO.input(ENCODER_B_PIN)
    if encoder_b_state:  # Clockwise rotation
        position += 1
    else:  # Counter-clockwise rotation
        position -= 1
    print(f"Position: {position}")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ENCODER_A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(ENCODER_A_PIN, GPIO.RISING, callback=encoder_a_interrupt, bouncetime=1)

try:
    print("Encoder initialized. Rotate the encoder to see changes in position.")
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting.")
