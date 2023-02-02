from assets.utils import *

class Card:
    def __init__(self, color, number, usage):
        self.color = color
        self.number = number
        self.usage = usage

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def getUsage(self):
        return self.usage

    def getNumber(self):
        return self.number

    def hasAction(self):
        if self.usage > 0:
            return True
        else:
            return False

    def __str__(self):
        color_str = Color(self.color).name.capitalize()
        usage_str = resolveUsage(self.usage)
        output = ""
        if(self.color > 0):
            terminal_color = getTermColor(self.color)
            white_color = getTermColor(5)
            # return f'Cor: {color_str}, Number: {self.number} Type: {usage_str}'
            output = f"{terminal_color}|{self.number}|{white_color}"
        else:
            output = f"|{self.number}|"

        return output