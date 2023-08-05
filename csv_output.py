from output import Output
from game import Game
from square import Square
import serial
import Adafruit_BBIO.UART as UART


class CsvOutput(Output):
    def __init__(self,uart = "UART1" , port ="/dev/ttyS1",baudrate=9600 ):
        UART.setup(uart)
        self.ser = serial.Serial(port = port, baudrate=baudrate)
        self.ser.close()
        self.ser.open() 

    def __del__(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()

    def render(self, game: Game):
        def get_csv_from_square(square: Square) -> str:
            return f"{square.x};{square.y};{square.color.value[0]}"

        squares = game.get_all_squares()

        csv = '\n'.join([get_csv_from_square(s) for s in squares]) + '\0'
        message = csv.encode('utf-8')
        print("sending {} squares: \n{}".format(csv.count('\n') + 1, csv))
        print(message)
        self.ser.write(message)





