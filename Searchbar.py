#This file contains the class for the search bar
#Search bar takes in and stores user input.

from cmu_112_graphics import *
from gui_functions import *

class SearchBar(object):
    def __init__(self, app, cx, cy, boxWidth = 140, boxHeight= 20):
        self.app = app
        self.cx = cx
        self.cy = cy
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        self.isTyping = False
        self.searchInput = ""
        self.textOffsetX = 20

    def onClick(self):
        if self.isTyping == False:
            self.isTyping = True
            print(self.isTyping)


    def drawBox(self, canvas):
        canvas.create_rectangle(self.cx - self.boxWidth//2, self.cy - self.boxHeight//2,
            self.cx + self.boxWidth//2, self.cy + self.boxHeight//2, fill="white", outline="light grey", 
            width=2, onClick=self.onClick)
        if self.isTyping == False and self.searchInput == "":
            canvas.create_text(self.textOffsetX, self.cy, anchor="w", fill= "light grey", text= "Search titles...")
        else:
            canvas.create_text(self.textOffsetX, self.cy, anchor="w", fill= "grey", text= f"{self.searchInput}")
            #draw cursor
            #render user input

