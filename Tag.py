from cmu_112_graphics import *
import random
import hashlib

class Tag():
    def __init__(self, name, color=None):
        self.name = name

        self.colorList = ["RoyalBlue1", "deep sky blue",
                "SpringGreen3", "peach puff", "brown1", "tan1", "MediumPurple3",
                "MediumOrchid1", "gold", "aquamarine2", "goldenrod1", "OliveDrab2", "IndianRed1"]
        if color == None:
            #CITATION: https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
            self.color = self.colorList[int(hashlib.sha1(self.name.encode('utf-8')).hexdigest(), 16) % (len(self.colorList))]
        else:
            self.color = color

    #tags have a name and a color

    def __repr__(self):
        return self.name

    def changeColor(self, newColor: str):
        """Changes color to a hexcode of newColor."""
        self.color = newColor

    # function to draw tag???
