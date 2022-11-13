import argparse


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    # parser.add_argument('--till-hour', type=int, choices=range(24))
    # parser.add_argument('--daytime', choices=['day', 'evening'], default='day')
    return parser.parse_args()


CONSOLE_ARGUMENTS = get_console_arguments()
