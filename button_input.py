from input import Input
from action import Action
import Adafruit_BBIO.GPIO as GPIO
import time
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


    def _wait_for_button_release(self, pin: str):
        if GPIO.input(pin) == GPIO.LOW:
            time.sleep(0.01)
            return GPIO.input(pin) == GPIO.LOW
        return False

    def get_action(self) -> Optional[Action]:
        # Read the button states (0 means pressed, 1 means not pressed due to pull-up)
        if self._wait_for_button_release(self.left_button_pin):
            return Action.MOVE_LEFT
        elif self._wait_for_button_release(self.right_button_pin):
            return Action.MOVE_RIGHT
        elif self._wait_for_button_release(self.rotate_button_pin):
            return Action.ROTATE_LEFT
        else:
            return None

