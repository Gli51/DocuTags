from operator import attrgetter

class SortDropdown():
    def __init__(self, app, cx, cy, items:list):
        self.app = app
        self.cx = cx
        self.cy = cy
        self.boxWidth = 100
        self.boxHeight = 20
        self.items = items # length of this is the number of rows
        self.textOffset = 10
        self.menuText = "Dropdown v"

    def openMenu(self):
        """Onclick method that expands dropdown when first box is toggled"""
        if self.app.dropdownOpen == False:
           self.app.dropdownOpen = True
        else:
            self.app.dropdownOpen = False
    
    """ def chooseItem(self, text):
        self.selectedItem = text
        self.menuText = #some name of the selected item
        self.selecting = False """

    def drawItem(self, canvas, text, i):
        """Draws a cell given cell text, an index, and text color."""
        if text == "Title":
            sortFunc = self.sortTitle
        if text == "Last edited":
            sortFunc = self.sortEditTime
        if text == "Last created":
            sortFunc = self.sortMakeTime
        self.selecting = False

        cy = self.cy + self.boxHeight + self.boxHeight*i
        canvas.create_rectangle(self.cx - self.boxWidth//2, cy - self.boxHeight//2,
            self.cx + self.boxWidth//2, cy + self.boxHeight//2, fill="light grey", outline="white", width = 2, onClick=sortFunc)
        canvas.create_text(self.cx, cy, text=text)

    ############################################################################
    #Sorting functions
    ############################################################################
    
    def sortEditTime(self):
        self.app.shownDocs.sort(key=attrgetter('edit_timestamp', 'title'.lower()))
    
    def sortTitle(self):
        self.app.shownDocs.sort(key=attrgetter('title'.lower(), 'edit_timestamp'))#TODO: uppercase counts as first, should be case insensitive
    
    def sortMakeTime(self):
        self.app.shownDocs.sort(key=attrgetter('make_timestamp', 'title'.lower()))


    def drawDDMenu(self, canvas):
        canvas.create_rectangle(self.cx-self.boxWidth//2, self.cy - self.boxHeight//2,
            self.cx + self.boxWidth//2, self.cy + self.boxHeight//2, onClick=self.openMenu,
            fill="light grey", outline="white", width = 2)
        if self.app.dropdownOpen == True:
            for i in range(len(sorted(self.items))):
                self.drawItem(canvas, self.items[i], i)
        canvas.create_text(self.cx - self.boxWidth//2 + self.textOffset, self.cy, anchor="w", text=self.menuText, fill="grey")
