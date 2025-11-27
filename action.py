from enum import Enum
from timer import Timer
class Action(Enum):
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    ROTATE_LEFT = "rotate_left"
    ROTATE_RIGHT = "rotate_right"
    DROP = "drop"

    FALL = "fall"


class Tick():
    def __init__(self, action: Action , timer: Timer):
        self.timer = timer
        self.action = action

    def get_action(self):
        if not self.timer.increment():
            return self.action
        return Action.FALL

    def reset_timer(self):
        self.timer.reset()