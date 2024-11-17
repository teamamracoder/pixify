import random
from env_config import env


def generate_otp() -> int:
    """Generate 6 digit otp

    Keyword arguments:
    
    Return: return_description
    """
    return f"{random.randint(100000, 999999)}"


def is_debugging() -> bool:
    """Check debugging mode is on or not

    Keyword arguments:

    Return: boolean
    """
    return env("DEBUG")


def print_log(*msg) -> None:
    """This function will print the log message on console if debug mode is true

    Keyword arguments:
    messages -- log messages you want to print

    Return: None
    """
    if env("DEBUG"):
        print(*msg)
