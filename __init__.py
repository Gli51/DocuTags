#The main file, __init__.py
#This file runs the whole game by calling WritingApp, a modal app.

#CITATION: cmu_112_graphics package from https://www.diderot.one/course/34/chapters/2846/
from cmu_112_graphics import *
import tkinter.simpledialog as sd
#CITATION: pickle from https://docs.python.org/3/library/pickle.html
import pickle
#CITATION: tkinter from https://docs.python.org/3/library/tkinter.html
#import tkinter as tk
from tkinter import *

from Document import *
from gui_functions import *
from Searchbar import *
from Dropdown import *
from Tag import *
from Page import *

class WritingApp(ModalApp):
    def appStarted(self):
        self.addMode(LibraryMode(name="library"))
        self.addMode(EditorMode(name="editor"))
        self.setActiveMode("library")
    
    
    def getDocs(self): #reads files in the library file directory and converts to Document.
        if not os.path.exists('documents'):
            os.makedirs('documents')
        for filename in os.listdir(): # get the directory
            if filename.endswith('txt'):
                f = open("save_dest.txt", "rb")
                document = pickle.load(f)
                f.close()
                """ with open(filename) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=';')
                        #set title
                        path = csv_reader[0]
                        title = csv_reader[1]
                        tags = []
                        for tag in csv_reader[2].split(","):
                            tags.append(tag)
                        make_timestamp = csv_reader[3]
                        edit_timestamp = csv_reader[4]
                        if csv_reader[5] != "":
                            for content in csv_reader[5].split("\P"): """
                                #add page object to list of pages
                        #if marked with pages, page words = the string after pages
                        #tags represented by {highlighted words here: tag1, tag2, tag3}

                        #add document to list of documents in library.

class EditorMode(Mode):
    def appStarted(self):
        self.libmode = self.getMode("library")
        self.currDoc = self.libmode.selectedDocument
        print(self.currDoc)
        self.menuHeight = self.height//14
        self.menuBotHeight = self.height//14
        self.offsetX = 14
        self.offsetY = 8
        self.titleSize = 11
        self.subtitleSize = 10
        self.pageWidth = 600

    def closeEditor(self):
        """Onclick method for when the close button is clicked."""
        self.setActiveMode("library")

    def modeActivated(self):
        self.appStarted()
    
    """ def create_widget(self, canvas):
        
        text=Text(canvas, height=100, width=100)
        text.grid() """


    ###############################################
    #Content management
    ###############################################

    #getCurrentPath (gets path of the edited document)

    #saveFile
        #(writeFile)
    
    def keyPressed(self, event):
            #if not typing in search bar:
            alphabet= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            numbers = "0123456789"
            symbols = "!@#$%^&*()'.,<>/?\|]}[{+_-=;:"
            if (event.key in alphabet or event.key in numbers or event.key in symbols
                or event.key == '"'):
                pass
                #set page contents equal to page contents[:i] + event.key + pagecontents[i:]
            if event.key == "Space":
                pass
                #same as above excent replace event.key with " "
            if event.key == "Backspace":
                pass
                #remove the string at the index of the cursor
            if event.key == "Enter":
                #add a newline at cursor index
                pass

    #overflow (need to keep track of page width)

    #mouse cursor

    ###############################################
    #Page management
    ###############################################

    #addPage(self)

    #delPage(self)

    #flipForward (go to next page)

    #flipBackward (go back a page)

    #jumpTo(self, page)

    #getCurrentPages

    ###############################################
    #Tag Creation
    ###############################################

    #Highlight text (mouse pressed and mouse dragged)

    #tagText

    #clearTag

    ###############################################
    #Content searching stuff
    ###############################################

    #searchDocument
        #get user input
        #look for matching string
        #jump to first instance

    #nextMatch

    #lastMatch

    ###############################################
    #Tag searching stuff
    ###############################################

    #findTag
        #get user input (dropdown menu click)
        #look through tagged content in document
        #if tag matches, jump to first instance
    
    #nextTag

    #lastTag

    ##############################################
    #Draw Menus
    ##############################################

    def drawTopMenu(self, canvas):
        buttonWidth = 60
        canvas.create_rectangle(0, 0, self.width, self.menuHeight, fill= "white", width=0)
        drawButton(canvas, self.width - (buttonWidth//2 + self.offsetX), self.menuHeight//2, onClick=self.closeEditor, text="Close", w=buttonWidth)

    def drawBotMenu(self, canvas):
        canvas.create_rectangle(0, self.height - self.menuBotHeight, self.width, self.height, fill= "white", width=0)
        drawButton(canvas, self.width*(3/4), self.height - self.menuBotHeight//2, onClick = self.currDoc.addPage, text="+Page")

    def drawSidebar(self, canvas):
        offsetY = 60
        self.currDoc.drawCurrTags(canvas, self.width*(9/10), self.menuHeight + offsetY)

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill= "light grey", width=0)
        self.drawTopMenu(canvas)
        self.drawBotMenu(canvas)
        self.drawSidebar(canvas)
        
        


class LibraryMode(Mode):
    def appStarted(self): 
        self.menuHeight = self.height//14
        self.menuBotHeight = self.height//16
        self.displayWidth = 300
        self.currTags = []
        self.rows = 4
        self.cols = 4
        self.libraryWidth = self.displayWidth * 2
        self.libraryHeight = self.height - self.menuBotHeight - self.menuHeight
        self.cellWidth = self.libraryWidth // self.cols
        self.cellHeight = self.libraryHeight // self.rows
        self.marginX = (self.width - self.libraryWidth)//2
        self.offsetX = 14
        self.offsetY = 8
        self.titleSize = 11
        self.subtitleSize = 10
        self.dividerX = 180
        self.highlightWidth = 14
        self.documents = []
        tag1 = Tag("short")
        tag2 = Tag("very long tag")
        tag3 = Tag("notes")
        page1 = Page(self, "abcdefg", [tag1, tag2])
        page2 = Page(self, "blahblah")
        doc1 = Document(self, "filepath1", "15-112: Fundamentals of Computer Science", "1141", [tag3], [page1, page2])
        doc2 = Document(self, "filepath2", "How People Work", "0127", [tag1, tag2], [page2])
        doc3 = Document(self, "filepath3", "Another Book", "0242", [tag3], [page2])
        self.documents.append(doc1)
        self.documents.append(doc2)
        self.documents.append(doc3)
        self.shownDocs = self.documents
        if len(self.documents) > 1:
            self.selectedDocument = self.documents[0]
        else:
            self.selectedDocument = None
        searchBoxWidth = 150
        self.topSearch = SearchBar(self, self.offsetX + searchBoxWidth//2, self.menuHeight - self.offsetY*2, searchBoxWidth)
        self.sortItems = ["Title", "Last edited", "Last created"]
        #TODO: get the function calls working correctly
        self.dropdown = SortDropdown(self, self.dividerX + searchBoxWidth, self.menuHeight*(1/3), self.sortItems)

    def mousePressed(self, event):
        """Handles the gui response to mouse presses."""
        if len(self.shownDocs) > 1:
            self.selectDoc(event)
        self.selectSearch(event)
        
    def selectDoc(self, event):
        """Selects documents in the grid based on mouse press coords. Launches editor
        on if selected document is clicked again."""
        row = (event.y - self.menuHeight)//self.cellHeight
        col = (event.x - (self.width//2 - self.displayWidth))//self.cellWidth
        index = col + row*self.cols
        if 0 <= index < len(self.documents) and 0<=row<self.rows and 0<=col<self.cols:
            if self.documents[index] != self.selectedDocument:
                self.selectedDocument = self.documents[index]
                print("click1")
            elif self.documents[index] == self.selectedDocument:
                print("click2")
                #TODO: open that selected document in editor
                self.setActiveMode("editor")

    def selectSearch(self, event):
        """Sets searchbar istyping to false if clicked not on the box."""
        if self.topSearch.isTyping == True:
            if not ((self.topSearch.cx - self.topSearch.boxWidth//2) <= event.x <= (self.topSearch.cx + self.topSearch.boxWidth//2) and
                (self.topSearch.cy - self.topSearch.boxHeight//2) <= event.y <= (self.topSearch.cy + self.topSearch.boxHeight//2)):
                self.topSearch.isTyping = False
    
    def keyPressed(self, event):
        if self.topSearch.isTyping == True:
            alphabet= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            numbers = "0123456789"
            symbols = "!@#$%^&*()'.,<>/?\|]}[{+_-=;:"
            if (event.key in alphabet or event.key in numbers or event.key in symbols
                or event.key == '"'):
                self.topSearch.searchInput += event.key
            if event.key == "Space":
                self.topSearch.searchInput += " "
            if event.key == "Backspace":
                self.topSearch.searchInput = self.topSearch.searchInput[:-1]
            if event.key == "Enter":
                self.searchMatch()
    
    def searchMatch(self):
        matchedDocs = []
        for doc in self.documents:
            if self.topSearch.searchInput.lower() in doc.title.lower():
                matchedDocs.append(doc)
        self.shownDocs = matchedDocs

    def drawHighlight(self, canvas):
        selectedIndex = self.documents.index(self.selectedDocument)
        row = selectedIndex // self.cols
        col = selectedIndex % self.rows
        cx = col * self.cellWidth + self.cellWidth//2 + (self.width//2-self.displayWidth)
        cy = row * self.cellHeight + self.cellHeight//2 + self.menuHeight
        highlightX = (self.libraryWidth//4 - self.highlightWidth) // 2
        highlightY = (self.libraryHeight//4 - self.highlightWidth) // 2
        canvas.create_rectangle(cx - highlightX, cy - highlightY, cx + highlightX,
            cy + highlightY, fill="cornflower blue", width=0)

    ###################################################
    #Document Creation/Deletion
    ###################################################

    def newDocPopup(self):
        answer = simpledialog.askstring("Create", "What would you like to name your document?")
        if answer != None:
            #create filepath
            #get timestamp
            new = Document(self, "filepath", answer, "0000")
            self.documents.append(new)
            self.selectedDocument = new
            self.setActiveMode("editor")

    #delDoc
        #deletes the file located at the path of the currently selected document

    ########################################
    #Menu bars
    ########################################
    
    def drawTopMenu(self, canvas):
        """Draws the top menu which contains the search bar, sort and filter options,
        and create new document button."""
        buttonWidth = 60

        canvas.create_rectangle(0, 0, self.width, self.menuHeight, fill= "white", width=0)
        canvas.create_text(self.offsetX, self.offsetY, anchor="nw", font=f"Arial {self.titleSize} normal", text="Search:")
        self.topSearch.drawBox(canvas)
        canvas.create_line(self.dividerX, self.offsetY, self.dividerX, self.menuHeight - self.offsetY, width=2, fill="light grey")
        canvas.create_text(self.dividerX + self.offsetX, self.offsetY, anchor = "nw", font=f"Arial {self.titleSize} normal", text="Sort by:")
        #sort dropdown
        self.dropdown.drawDDMenu(canvas)
        #filter text
        canvas.create_text(self.dividerX + self.offsetX, self.menuHeight - self.offsetY, anchor = "sw", font=f"Arial {self.titleSize} normal", text="Filter tag:")
        #TODO: filter display (max 4)
        #new doc button
        drawButton(canvas, self.width - (buttonWidth//2 + self.offsetX), self.menuHeight//2, onClick=self.newDocPopup, text="New Doc", w=buttonWidth)


    def drawBotMenu(self, canvas):
        """Draws the lower menu that contains the options for the selected file"""
        buttonWidth = 80
        canvas.create_rectangle(0, self.height - self.menuBotHeight, self.width, self.height, fill= "white", width=0)
        if self.selectedDocument != None:
            drawButton(canvas, self.width//4, self.height - self.menuBotHeight//2, onClick = self.renamePopup, text= "Rename")
            drawButton(canvas, self.width//4 + self.offsetX + buttonWidth, self.height - self.menuBotHeight//2, onClick = self.editTagPopup, text= "Edit Tags")
            #draw button for



    ########################################
    #Grid layout
    ########################################

    def drawGrid(self, canvas):
        for i in range(len(self.shownDocs)):
            row = i // self.cols
            col = i % self.rows
            cx = col * self.cellWidth + self.cellWidth//2 + (self.width//2-self.displayWidth)
            cy = row * self.cellHeight + self.cellHeight//2 + self.menuHeight
            #stuff for testing:
            #x0 = col * self.cellWidth + (self.width//2-self.displayWidth)
            #y0 = row * self.cellHeight + self.menuHeight
            #x1 = x0 + self.cellWidth
            #y1 = y0 + self.cellHeight
            #canvas.create_rectangle(x0,y0,x1,y1,outline="grey")
            #draw document[i] at center of cell
            self.shownDocs[i].drawThumbnail(canvas, cx, cy)

    #####################################################################################
    #TYPING CAN BE ITS OWN SEPARATE FUNCTION SINCE IT WILL BE REUSED IN MULTIPLE PLACES:
    #TEXT EDITOR, RENAME DOCUMENT, EDIT TAGS, SEARCH BAR INPUTS
    #####################################################################################

    #searchLibrary (will probably use a similar structure to searchDoc in the editor mode)

    #####################################
    #Editing functions
    #####################################

    def renamePopup(self):
        answer = simpledialog.askstring("Rename", "What would you like to rename the document?")
        if answer != None:
            self.selectedDocument.rename(answer)
            #TODO: write new title to file
    

    def editTagPopup(self):
        answer = simpledialog.askstring("Edit tags", "Separate tags by commas")
        if answer != None:
            newTags = []
            for elem in answer.split(","):
                newTags.append(elem) #TODO: replace this so it works with tag objects
                #newTag.append(Tag(elem))
            self.selectedDocument.editTag(newTags)

    #docTagDone (onclick method for when done button is clicked)

    ############################################
    #Sort
    ############################################
    #from operator import itemgetter, attrgetter

    #sort keys: title, time, tag
    #mutable/destructive sort which changes the indexes of the items in the list
        
    

    #def sortTag (sorts alphabetically by tag)

    #def sortRelevant (option only available when filtering by tag. sorts by occurences of filtered tags)

    
    ############################################
    #Filter
    ############################################

    #filterDoc
        #takes in a list of currently selected filter tags
        #doesn't render ones that don't have that tag

    #addFilterTag

    #removeFilterTag

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill= "light grey", width=0)
        #this is for testing purposes:
        #canvas.create_rectangle(self.width//2 - self.displayWidth, self.menuHeight, self.width//2 + self.displayWidth,
            #self.height - self.menuBotHeight, outline="grey")
        if self.selectedDocument != None and len(self.shownDocs) > 0:
            self.drawHighlight(canvas)
        self.drawGrid(canvas)
        self.drawTopMenu(canvas)
        self.drawBotMenu(canvas)
        

def main():
    WritingApp(width=700, height=790)


if __name__ == "__main__":
    main()

