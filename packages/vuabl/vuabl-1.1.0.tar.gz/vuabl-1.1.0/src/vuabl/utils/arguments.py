import vuabl.utils.version as version
from argparse import ArgumentParser


def get_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="vuabl", 
        description=f"Visualizer for Unity Addressables build layout ({version.get_version()})")

    parser.add_argument("path", nargs="?", type=str, help="Addressables build layout file path")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug functionality")
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    parser.add_argument("--address", type=str, default="127.0.0.1", help="app address")
    parser.add_argument("--port", type=int, default=8050, help="app port")
    parser.add_argument("--theme", type=str, default="dark", choices=["dark", "light"], help="app theme")
    parser.add_argument("-s", "--silent", action="store_true", help="disable automatic app opening in browser")

    return parser
