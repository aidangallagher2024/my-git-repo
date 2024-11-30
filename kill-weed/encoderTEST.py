import Jetson.GPIO as gpiozero
from encoder import Encoder
import time
from gpiozero import Button
from signal import pause

ENCODER_A_PIN = 26  # Replace with your actual GPIO pin
ENCODER_B_PIN = 24  # Replace with your actual GPIO pin
"""""
GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUT_A, GPIO.IN)
GPIO.setup(OUT_B, GPIO.IN)
"""

position = 0
encoder_b_state = 0

encoder_a = Button(ENCODER_A_PIN, pull_up=True)
encoder_b = Button(ENCODER_B_PIN, pull_up=True)

def encoder_a_interrupt():
    global position, encoder_b_state
    # Read the state of the B channel
    encoder_b_state = encoder_b.is_pressed
    if encoder_b_state:  # Clockwise rotation
        position += 1
    else:  # Counter-clockwise rotation
        position -= 1
    print(f"Position: {position}")

encoder_a.when_pressed = encoder_a_interrupt

print("Encoder initialized. Rotate the encoder to see changes in position.")
pause()

"""""
def valueChanged(value):
    pass # Or do something useful with the value here!

e1 = Encoder(OUT_B, OUT_A, callback=valueChanged)

while(1):
    print(e1)
    time.sleep(1)
    """