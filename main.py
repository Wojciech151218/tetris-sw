import argparse
import json
import time
from game_handler import GameHandler
from input import CombinedInput
from output import CombinedOutput


def load_config(path):
    with open(path, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


def start_server(port: int = 8000):
    import subprocess
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parent
    return subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port)],
        cwd=str(project_root),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main(run_type, ticks_per_fall, refresh_rate, height, width):

    if run_type == "dev":
        from console_input import ConsoleInput
        from console_output import ConsoleOutput
        controller = ConsoleInput()
        renderer = ConsoleOutput()
    elif run_type == "bbb-console":
        from button_input import ButtonInput
        from console_output import ConsoleOutput
        from csv_output import CsvOutput 
        from console_input_light import ConsoleInputLight

        controller = CombinedInput([ConsoleInput(),ButtonInput()])
        renderer = CombinedOutput([ConsoleOutput(), CsvOutput()])
    elif run_type == "bbb-web":
        from websocket_input import WebSocketInput
        from websocket_output import WebSocketOutput
        from button_input import ButtonInput
        from csv_output import CsvOutput
        server_process = start_server()
        controller =  CombinedInput([WebSocketInput(),ButtonInput()])
        renderer = CombinedOutput([WebSocketOutput(),CsvOutput()])
    elif run_type == "web":
        from websocket_input import WebSocketInput
        from websocket_output import WebSocketOutput

        server_process = start_server()
        controller =  WebSocketInput()
        renderer = WebSocketOutput()

    else:
        print("Invalid run type: " + run_type + " must be dev, bbb, bbb-console, bbb-web, or web ")
        return

    game_handler = GameHandler(
        input=controller,
        output=renderer,
        ticks_per_fall=ticks_per_fall,
        height=height,
        width=width,
    )
    print('game started ... ')
    while True:
        game_handler.handle_tick()
        time.sleep(refresh_rate)

if __name__ == "__main__":
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument("run_type", help="dev or bbb")
    base_parser.add_argument(
        "--config",
        default="config.json",
        help="Path to JSON config with defaults",
    )
    base_args, _ = base_parser.parse_known_args()

    config = load_config(base_args.config)
    ticks_per_fall = config.get("ticks_per_fall", 5)
    refresh_rate = config.get("refresh_rate", 0.1)
    height = config.get("height", 16)
    width = config.get("width", 12)

    parser = argparse.ArgumentParser(parents=[base_parser])
    parser.set_defaults(
        ticks_per_fall=ticks_per_fall,
        refresh_rate=refresh_rate,
        height=height,
        width=width,
    )
    parser.add_argument(
        "--ticks-per-fall",
        type=int,
        dest="ticks_per_fall",
        help="Ticks per fall",
    )
    parser.add_argument(
        "--refresh-rate",
        type=float,
        dest="refresh_rate",
        help="Seconds between ticks",
    )
    parser.add_argument("--height", type=int, help="Board height")
    parser.add_argument("--width", type=int, help="Board width")

    args = parser.parse_args()
    main(
        args.run_type,
        args.ticks_per_fall,
        args.refresh_rate,
        args.height,
        args.width,
    )