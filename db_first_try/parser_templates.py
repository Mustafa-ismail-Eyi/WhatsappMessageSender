#! python3
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from traceback import print_tb

def get_parser():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--command",
        "-c"
    )
    args = parser.parse_args()

    return args

get_parser()