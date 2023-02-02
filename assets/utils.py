from enum import Enum
from json import load

colors = {
    'reset': '\033[0m ',
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'blue': '\033[34m',
    'yellow': '\033[93m',
}

def getTermColor(color):
    if (color == 1):
        output = colors['blue']

    elif(color == 2):
        output = colors['green']

    elif (color == 3):
        output = colors['red']
        
    elif (color == 4):
        output = colors['yellow']

    elif (color == 5):
        output = colors['reset']

    return output

def resolveUsage(usage):
    output = ""

    if usage == 0:
        output = 'Normal'

    elif usage == 1:
        output = 'Buy Two'

    elif usage == 2:
        output = 'Buy Four'

    elif usage == 3:
        output = 'Block'

    elif usage == 4:
        output = 'Color Change'

    elif usage == 5:
        output = 'Reverse'

    return output

class Color(Enum):
    WILD_CARD = 0
    BLUE = 1
    GREEN = 2
    RED = 3
    YELLOW = 4

class Usage(Enum):
    STANDART = 0
    BUY_TWO = 1
    BUY_FOUR = 2
    BLOCK = 3
    COLOR_CHANGE = 4
    REVERSE = 5




