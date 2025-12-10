import time

from blessed import Terminal

from console_input import ConsoleInput
from console_output import ConsoleOutput
from game_handler import GameHandler
from csv_output import CsvOutput 
from button_input import ButtonInput
from input import CombinedInput
from output import CombinedOutput
def main():
    ticks_per_fall = 500
    refresh_rate = 0.001
    term = Terminal()
    controller = CombinedInput([ConsoleInput(term=term), ButtonInput()])
    renderer = CombinedOutput([ConsoleOutput(term=term), CsvOutput()])
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