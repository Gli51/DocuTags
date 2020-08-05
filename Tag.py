from cmu_112_graphics import *
import random

class Tag():
    def __init__(self, name, color=None):
        self.name = name

        #If tag does not have a specific color, chooses a random color.
        #TODO: make sure it keeps this color and doesn't rechoose the random colors
        #every time you open the app
        if color == None:
            self.color = random.choice(["RoyalBlue1", "deep sky blue",
                "SpringGreen3", "peach puff", "brown1", "tan1", "MediumPurple3",
                "MediumOrchid1", "gold", "aquamarine2", "goldenrod1", "OliveDrab2", "IndianRed1"])
        else:
            self.color = color

    #tags have a name and a color

    def __repr__(self):
        return self.name + self.color

    def changeColor(self, newColor: str):
        """Changes color to a hexcode of newColor."""
        self.color = newColor

    # function to draw tag???
