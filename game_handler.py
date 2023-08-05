from input import Input
from output import Output
from game import Game
from action import Tick
from timer import Timer
class GameHandler:
    def __init__(self,input: Input, output: Output,width =8 ,height = 32,ticks_per_fall=100):
        self.input = input
        self.game = Game(width=width, height=height)
        self.timer = Timer(ticks_per_fall)
        self.output = output
        self.ticks_per_fall = ticks_per_fall
        
    def handle_tick(self):
        action = self.input.get_action()
        tick = Tick(action, self.timer)
        self.game.perform_tick(tick)
        if self.game.is_game_over():
            self._reset_game()
            return
        self.output.render(self.game)

    def _reset_game(self):
        self.game = Game(width=8, height=16)
        self.timer = Timer(self.ticks_per_fall)