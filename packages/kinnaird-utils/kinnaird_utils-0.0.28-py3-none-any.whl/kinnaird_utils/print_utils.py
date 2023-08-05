import re
import sys
import json
from decimal import Decimal
from colorama import Fore, Back

END = "\033[0m"
GREY = "\33[90m"


def print_red(string):
    print(f"{Fore.RED}{string}{END}")


def print_yellow(string):
    print(f"{Fore.YELLOW}{string}{END}")


def print_blue(string):
    print(f"{Fore.BLUE}{string}{END}")


def print_green(string):
    print(f"{Fore.GREEN}{string}{END}")


def print_grey(string):
    print(f"{GREY}{string}{END}")
    # Color code from here: https://stackoverflow.com/a/39452138


def print_grey_replace_output(string):
    sys.stdout.write(f"\r{GREY}{string}{END}")
    sys.stdout.flush()


def print_warning(message: str):
    print_red(r"""

     ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄  ▄  ▄ 
    ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░▌▐░▌▐░▌
    ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌ ▀▀▀▀█░█▀▀▀▀ ▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌▐░▌▐░▌
    ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌▐░▌    ▐░▌     ▐░▌     ▐░▌▐░▌    ▐░▌▐░▌          ▐░▌▐░▌▐░▌
    ▐░▌   ▄   ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▌   ▐░▌     ▐░▌     ▐░▌ ▐░▌   ▐░▌▐░▌ ▄▄▄▄▄▄▄▄ ▐░▌▐░▌▐░▌
    ▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌     ▐░▌     ▐░▌  ▐░▌  ▐░▌▐░▌▐░░░░░░░░▌▐░▌▐░▌▐░▌
    ▐░▌ ▐░▌░▌ ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀█░█▀▀ ▐░▌   ▐░▌ ▐░▌     ▐░▌     ▐░▌   ▐░▌ ▐░▌▐░▌ ▀▀▀▀▀▀█░▌▐░▌▐░▌▐░▌
    ▐░▌▐░▌ ▐░▌▐░▌▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌    ▐░▌▐░▌     ▐░▌     ▐░▌    ▐░▌▐░▌▐░▌       ▐░▌ ▀  ▀  ▀ 
    ▐░▌░▌   ▐░▐░▌▐░▌       ▐░▌▐░▌      ▐░▌ ▐░▌     ▐░▐░▌ ▄▄▄▄█░█▄▄▄▄ ▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄█░▌ ▄  ▄  ▄ 
    ▐░░▌     ▐░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌▐░▌▐░▌▐░▌
     ▀▀       ▀▀  ▀         ▀  ▀         ▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀  ▀  ▀ 
    """)
    print("\n")
    print_red("WARNING:")
    confirm = input(f"{message}. Are you sure you want to do that? [y/N]")
    if confirm.lower() == 'y':
        return True
    else:
        return False


class DecimalEncoder(json.JSONEncoder):
    """
    When you get the message 'errorMessage': 'Object of type Decimal is not JSON serializable', use this class.

    Usage:
        print(json.dumps(example_item, indent=4, cls=DecimalEncoder))

    Reference: https://www.tutorialfor.com/questions-318950.htm
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
