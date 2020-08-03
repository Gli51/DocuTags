from cmu_112_graphics import *
import random

class Tag():
    def __init__(self, name):
        self.name = name
        self.color = random.choice(["RoyalBlue1", "deep sky blue",
            "SpringGreen3", "peach puff", "brown1", "tan1", "MediumPurple3",
            "MediumOrchid1", "gold", "aquamarine2", "goldenrod1", "OliveDrab2", "IndianRed1"])

    #tags have a name and a color

    def changeColor(self, newColor: str):
        """Changes color to a hexcode of newColor."""
        self.color = newColor

    # function to draw tag???
