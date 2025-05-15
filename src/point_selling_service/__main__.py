import argparse
from .entrypoint import run_api

RUN_COMMAND = "run"

parser = argparse.ArgumentParser(description="Point Selling Service")
subparsers = parser.add_subparsers(dest="command")
run_parser = subparsers.add_parser(RUN_COMMAND, help="Run the application")


if __name__ == "__main__":
    args = parser.parse_args()
    match args.command:
        case "run":
            run_api()
        case _:
            parser.print_help()
