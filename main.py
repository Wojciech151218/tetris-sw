import time

from blessed import Terminal

from console_input import ConsoleInput
from console_output import ConsoleOutput
from game_handler import GameHandler


def main():
    ticks_per_fall = 500
    refresh_rate = 0.001
    term = Terminal()
    controller = ConsoleInput(term=term)
    renderer = ConsoleOutput(term=term)
    game_handler = GameHandler(
        input=controller, 
        output=renderer, 
        ticks_per_fall=ticks_per_fall,
    )
    while True:
        game_handler.handle_tick()
        time.sleep(refresh_rate)

if __name__ == "__main__":
    main()