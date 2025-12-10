from output import Output
from game import Game
from square import Square
import serial
import UART


class CsvOutput(Output):
    def __init__(self,uart = "UART1" , port ="/dev/ttyS1",baudrate=9600 ):
        UART.setup(uart)
        self.ser = serial.Serial(port = port, baudrate=baudrate)
        self.ser.open() 

    def __del__(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()

    def render(self, game: Game):
        def get_csv_from_square(square: Square) -> str:
            return f"{square.x};{square.y};{square.color.value[0]}"

        saquares = game.get_all_squares()

        csv = '\n'.join([get_csv_from_square(s) for s in saquares]) + '\0'

        self.ser.write(csv)




