from operator import attrgetter

class SortDropdown():
    def __init__(self, app, cx, cy, items:list):
        self.app = app
        self.cx = cx
        self.cy = cy
        self.boxWidth = 100
        self.boxHeight = 20
        self.selecting = False
        self.items = items # length of this is the number of rows
        self.textOffset = 10
        self.selectedItem = None

    def openMenu(self):
        """Onclick method that expands dropdown when first box is toggled"""
        if self.selecting == False:
           self.selecting = True
        else:
            self.selecting = False
    
    def chooseItem(self):
        """Onclick method that calls sort function corresponding to given text."""
        if text == "Title":
            self.sortTitle()
        if text == "Last edited":
            self.sortEditTime()
        if text == "Last created":
            self.sortMakeTime()
        self.selecting = False

    #each of the rectangles might call an onclick? need to select items from dropdown somehow.
    def drawItem(self, canvas, text, i):
        """Draws a cell given cell text, an index, and text color."""
        if text == "Title":
            sortFunc = self.sortTitle()
        if text == "Last edited":
            sortFunc = self.sortEditTime()
        if text == "Last created":
            sortFunc = self.sortMakeTime()
        self.selecting = False

        cy = self.cy + self.boxHeight + self.boxHeight*i
        canvas.create_rectangle(self.cx - self.boxWidth//2, cy - self.boxHeight//2,
            self.cx + self.boxWidth//2, cy + self.boxHeight//2, fill="light grey", outline="white", width = 2, onClick=sortFunc)
        canvas.create_text(self.cx, cy, text=text)

    def sortEditTime(self):
        self.app.shownDocs.sort(key=attrgetter('edit_timestamp', 'title'))
    
    def sortTitle(self):
        self.app.shownDocs.sort(key=attrgetter('title', 'edit_timestamp'))
    
    def sortMakeTime(self):
        self.app.shownDocs.sort(key=attrgetter('make_timestamp', 'title'))


    def drawDDMenu(self, canvas):
        canvas.create_rectangle(self.cx-self.boxWidth//2, self.cy - self.boxHeight//2,
            self.cx + self.boxWidth//2, self.cy + self.boxHeight//2, onClick=self.openMenu,
            fill="light grey", outline="white", width = 2)
        if self.selecting == True:
            for i in range(len(sorted(self.items))):
                self.drawItem(canvas, self.items[i], i)
        #if self.selected == True:
            #pass
            #create text with selected option
        #else:
        canvas.create_text(self.cx - self.boxWidth//2 + self.textOffset, self.cy, anchor="w", text="Select...", fill="grey")
