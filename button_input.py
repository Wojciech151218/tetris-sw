from input import Input
from action import Action
import Adafruit_BBIO.GPIO as GPIO
from typing import Optional

class ButtonInput(Input):
    def __init__(self,left_pin: str = "P9_11", right_pin: str = "P9_12", rotate_pin: str = "P9_13"):
        # Initialize the GPIO pins for each button
        self.left_button_pin = left_pin   # GPIO_30
        self.right_button_pin = right_pin  # GPIO_60
        self.rotate_button_pin = rotate_pin # GPIO_31
        
        # Set up the buttons as inputs with pull-up resistors (default HIGH)
        GPIO.setup(self.left_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.right_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.rotate_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_action(self) -> Optional[Action]:
        # Read the button states (0 means pressed, 1 means not pressed due to pull-up)
        if GPIO.input(self.left_button_pin) == GPIO.LOW:
            return Action.MOVE_LEFT
        elif GPIO.input(self.right_button_pin) == GPIO.LOW:
            return Action.MOVE_RIGHT
        elif GPIO.input(self.rotate_button_pin) == GPIO.LOW:
            return Action.ROTATE_LEFT
        else:
            return None

