from config.constants import INPUT_TEXT_COLOR


COLORS = {
    "black": "\033[1;30;40m",
    "red": "\033[1;31;40m",
    "green": "\033[1;32;40m",
    "yellow": "\033[1;33;40m",
    "blue": "\033[1;34;40m",
    "purple": "\033[1;35;40m",
    "cyan": "\033[1;36;40m",
    "white": "\033[1;37;40m",
    "black-bg": "\033[1;31;40m",
    "red-bg": "\033[1;31;41m",
    "green-bg": "\033[1;31;42m",
    "yellow-bg": "\033[1;31;43m",
    "blue-bg": "\033[1;31;44m",
    "purple-bg": "\033[1;31;45m",
    "cyan-bg": "\033[1;31;46m",
    "white-bg": "\033[1;31;47m",
}

NORMAL_TEXT = "\033[0;37;40m"
INPUT_TEXT = "\033[0;37;40m"

if INPUT_TEXT_COLOR in COLORS.keys():
    INPUT_TEXT = COLORS[INPUT_TEXT_COLOR]
