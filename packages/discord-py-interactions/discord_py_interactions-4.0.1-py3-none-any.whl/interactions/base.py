import logging
from typing import ClassVar

from colorama import Fore, Style, init

__version__ = "4.0.1"
__repo_url__ = "https://github.com/goverfl0w/discord-interactions"
__authors__ = {
    "current": [
        {"name": "James Walston<@goverfl0w>", "status": "Lead Developer"},
        {"name": "DeltaX<@DeltaXW>", "status": "Co-developer"},
    ],
    "old": [
        {"name": "Daniel Allen<@LordOfPolls>"},
        {"name": "eunwoo1104<@eunwoo1104>"},
    ],
}


class Data:
    """A class representing constants for the library."""

    LOGGER: ClassVar[int] = logging.WARNING


class CustomFormatter(logging.Formatter):
    """A class that allows for customized logged outputs from the library."""

    format: str = "%(levelname)s:%(name)s:(ln.%(lineno)d):%(message)s"
    formats: dict = {
        logging.DEBUG: Fore.CYAN + format + Fore.RESET,
        logging.INFO: Fore.GREEN + format + Fore.RESET,
        logging.WARNING: Fore.YELLOW + format + Fore.RESET,
        logging.ERROR: Fore.RED + format + Fore.RESET,
        logging.CRITICAL: Style.BRIGHT + Fore.RED + format + Fore.RESET + Style.NORMAL,
    }

    def __init__(self):
        super().__init__()
        init(autoreset=True)

    def format(self, record):
        log_format = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)
