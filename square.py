from enum import Enum
import random

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    PURPLE = "purple"
    ORANGE = "orange"
    PINK = "pink"
    BROWN = "brown"
    GRAY = "gray"
    BLACK = "black"
    WHITE = "white"
    
    @classmethod
    def get_random_color(cls):
        return random.choice(list(cls))

class Square:
    def __init__(self, color: Color = None ,x: int = 0, y: int = 0):
        self.color = color
        self.x = x
        self.y = y

    

    def get_color(self):
        return self.color

    
    

