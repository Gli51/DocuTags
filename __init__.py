#The main file, __init__.py
#This file runs the whole game by calling WritingApp, a modal app.

#CITATION: cmu_112_graphics package from https://www.diderot.one/course/34/chapters/2846/
from cmu_112_graphics import *
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
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
    
    #TODO: FINISH THIS
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
        self.pageWidth = 560
        self.pagePosX = int(self.width* (5/11))
        self.pageHeight = 790 - self.menuBotHeight - self.offsetY
        self.isWriting = True #only set isWriting to false when self.docSearch.isTyping is set to True
        self.docSearch = SearchBar(self, self.offsetX + 70, self.menuHeight//2)
        self.timer = 0
        self.errorMessage = None
        self.searchError = False

        #######################################################################
        #Grid Variables
        #######################################################################
        self.gridCols = 66
        self.gridRows = 40
        self.letterWidth = 8
        self.letterHeight = self.letterWidth * 2
        self.pageMarginX = self.pagePosX - self.pageWidth//2 + self.offsetX
        self.pageMarginY = self.menuHeight + self.offsetY*2

        #######################################################################
        #Cursor vars
        #######################################################################
        self.cursorRow = self.currDoc.pages[self.currDoc.currPage].words.count("\n")
        self.cursorCol = len(self.currDoc.pages[self.currDoc.currPage].words) % self.gridCols

    def closeEditor(self):
        """Onclick method for when the close button is clicked."""
        self.currDoc.updateTags() #TODO: this doesnt seem to be update the tags. if pages with tags are deleted
        #and that tag is not a doctag, then it should remove it from the document.
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
        self.typingSearch(event)
        self.typingWords(event)

    def typingSearch(self, event):
        if self.docSearch.isTyping == True:
            alphabet= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            numbers = "0123456789"
            symbols = "!@#$%^&*()'.,<>/?\|]}[{+_-=;:"
            if (event.key in alphabet or event.key in numbers or event.key in symbols
                or event.key == '"'):
                self.docSearch.searchInput += event.key
            if event.key == "Space":
                self.docSearch.searchInput += " "
            if event.key == "Backspace":
                if len(self.docSearch.searchInput) > 0:
                    self.docSearch.searchInput = self.docSearch.searchInput[:-1]
            if event.key == "Enter":
                    self.searchDocument()

    def typingWords(self, event):
        if self.isWriting == True and len(self.currDoc.pages) > 0:
            alphabet= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            numbers = "0123456789"
            symbols = "!@#$%^&*()'.,<>/?\|]}[{+_-=;:"
            if (event.key in alphabet or event.key in numbers or event.key in symbols
                or event.key == '"'):
                self.currDoc.pages[self.currDoc.currPage].words += event.key
                self.cursorCol += 1
                self.overflow()
                #set page contents equal to page contents[:i] + event.key + pagecontents[i:]
            if event.key == "Space":
                self.currDoc.pages[self.currDoc.currPage].words += " "
                self.cursorCol += 1
                self.overflow()
                #same as above excent replace event.key with " "
            if event.key == "Backspace":
                #TODO: need to consider the lines/rows too
                if len(self.currDoc.pages[self.currDoc.currPage].words) > 1:
                    if self.currDoc.pages[self.currDoc.currPage].words[self.cursorCol-1] == "\n":
                        self.cursorRow -= 1
                        #TODO: bug here because the line doesnt need to be filled. mod doesn't really work
                        self.cursorCol = (len(self.currDoc.pages[self.currDoc.currPage].words) -
                            self.currDoc.pages[self.currDoc.currPage].words.count("\n")) % self.gridCols
                        self.currDoc.pages[self.currDoc.currPage].words = self.currDoc.pages[self.currDoc.currPage].words[:-1]
                    else:
                        self.currDoc.pages[self.currDoc.currPage].words = self.currDoc.pages[self.currDoc.currPage].words[:-1]
                        self.cursorCol -= 1
            if event.key == "Enter":
                self.currDoc.pages[self.currDoc.currPage].words += "\n"
                self.cursorRow += 1
                self.cursorCol = 0
                #add a newline at cursor index
            if event.key == "Tab":
                #adds tab expanded to spaces
                for i in range(4): #Goes to new line if the tab would go off the canvas
                    if (len(self.currDoc.pages[self.currDoc.currPage].words) + i) % 66 == 0:
                        self.currDoc.pages[self.currDoc.currPage].words += "\n"
                        self.cursorRow += 1
                        self.cursorCol = 0
                        return
                self.currDoc.pages[self.currDoc.currPage].words += (" "*4)
                self.cursorCol += 4
                self.overflow()


    def overflow(self):
        #Ignores newlines when counting characters for overflow
        newlineCount = self.currDoc.pages[self.currDoc.currPage].words.count("\n")
        if (len(self.currDoc.pages[self.currDoc.currPage].words) - newlineCount) % 66 == 0:
            self.currDoc.pages[self.currDoc.currPage].words += "\n"
            self.cursorRow += 1
            self.cursorCol = 0

    def mousePressed(self, event):
        crow = (event.y-self.pageMarginY) // self.letterHeight
        ccol = (event.x-self.pageMarginX) // self.letterWidth
        if 0 <= crow < self.gridRows and 0 <= ccol < self.gridCols:
            #self.cursorRow = crow
            #self.cursorCol = ccol
            if self.docSearch.isTyping == True:
                self.docSearch.isTyping = False
                self.isWriting = True
            #set string line and string index here
    
    def updateCursor(self):
        self.cursorRow = self.currDoc.pages[self.currDoc.currPage].words.count("\n")
        self.cursorCol = len(self.currDoc.pages[self.currDoc.currPage].words) % self.gridCols

    ###############################################
    #Popups
    ###############################################

    def jumpToPopup(self):
        descrip = """Which page would you like to go to?"""
        answer = simpledialog.askstring("Jump to", descrip)
        if answer != None and answer.isdigit():
            if self.currDoc.jumpToPage(answer) == False:
                print("Page not in range")
    
    def deletePopup(self):
        if self.currDoc.currPage != None:
            descrip = """Are you sure you want to delete this page?\n
            Deleted pages cannot be recovered."""
            answer = messagebox.askyesno("WARNING", descrip)
            if answer != False:
                self.currDoc.deletePage()
                self.updateCursor()

    def addPageTagPopup(self):
        """Onclick method that opens popup when adding page tag"""
        currPage = self.currDoc.currPage
        if self.currDoc.currPage != None:
            descrip = """Add page tags\n
            (Separate tags by commas. Not case sensitive)"""
            answer = simpledialog.askstring("Add Page Tag", descrip)
            if answer != False:
                newTags = []
                for elem in answer.split(","):
                    elem = elem.strip()
                    newTags.append(elem)
                self.currDoc.pages[currPage].addPageTag(newTags)

    def delPageTagPopup(self):
        """Onclick method that opens popup when removing page tag"""
        currPage = self.currDoc.currPage
        if self.currDoc.currPage != None:
            descrip = """Delete page tags\n
            (Separate tags by commas. Not case sensitive)"""
            answer = simpledialog.askstring("WARNING", descrip)
            if answer != False:
                removedTags = []
                for elem in answer.split(","):
                    removedTags.append(elem.strip())
                self.currDoc.pages[currPage].delPageTag(removedTags)

    ###############################################
    #Tag Creation (For later)
    ###############################################

    #Highlight text (mouse pressed and mouse dragged)

    #tagText

    #clearTag

    ###############################################
    #Content searching stuff
    ###############################################

    def searchDocument(self):
        pageNum = []
        for i in range(len(self.currDoc.pages)):
            if self.docSearch.searchInput in self.currDoc.pages[i].words:
                pageNum.append(i)
        if len(pageNum) > 0:
            self.currDoc.currPage = pageNum[0]
        else:
            self.searchError = True

    #def nextMatch(self):
        #pass

    #lastMatch

    def timerFired(self):
        frequency = 3000
        self.timer += self.timerDelay
        if self.searchError == True and self.errorMessage == None:
            self.errorMessage = "Search input cannot be found in this document."
        if self.timer % frequency == 0:
            self.searchError = False
            self.errorMessage = None
                

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
        tagButtonWidth = 100

        canvas.create_rectangle(0, 0, self.width, self.menuHeight, fill= "white", width=0)
        self.docSearch.drawBox(canvas)
        drawButton(canvas, self.width - tagButtonWidth*2 - (buttonWidth//2 + self.offsetX*2), self.menuHeight//2, onClick=self.addPageTagPopup,text="Add page tag", w=tagButtonWidth)
        drawButton(canvas, self.width - tagButtonWidth - (buttonWidth//2 + self.offsetX), self.menuHeight//2, onClick=self.delPageTagPopup,text="Delete page tag", w=tagButtonWidth)
        drawButton(canvas, self.width - (buttonWidth//2 + self.offsetX), self.menuHeight//2, onClick=self.closeEditor, text="Close", w=buttonWidth)
        if self.errorMessage != None:
            canvas.create_text(self.width//2, self.menuHeight*(3/2), text= f"{self.errorMessage}", fill="Indian red")

    def drawBotMenu(self, canvas):
        buttonWidth = 80
        arrowWidth = 40
    
        canvas.create_rectangle(0, self.height - self.menuBotHeight, self.width, self.height, fill= "white", width=0)
        drawButton(canvas, self.width*(3/4), self.height - self.menuBotHeight//2, onClick = self.currDoc.addPage, text="+Page")
        drawButton(canvas, self.width*(3/4) + buttonWidth + self.offsetX, self.height - self.menuBotHeight//2, onClick = self.deletePopup, text="-Page")
        #draws page count / total
        canvas.create_text(self.pagePosX, self.height - self.menuBotHeight//2, text=f"Page {self.currDoc.currPageNum} / {len(self.currDoc.pages)}")
        drawButton(canvas, self.offsetX + buttonWidth//2, self.height - self.menuBotHeight//2, onClick=self.jumpToPopup, text="Jump to")
        #draws page flip buttons
        drawButton(canvas, self.offsetX*2 + buttonWidth + arrowWidth, self.height - self.menuBotHeight//2, onClick=self.currDoc.flipBackward, text="<-", w=arrowWidth)
        drawButton(canvas, self.offsetX*3 + buttonWidth + arrowWidth*2, self.height - self.menuBotHeight//2, onClick=self.currDoc.flipForward, text="->", w=arrowWidth)

    def drawSidebar(self, canvas):
        offsetY = 60

        self.currDoc.drawCurrTags(canvas, self.width*(9/10), self.menuHeight + offsetY)
    
    def drawTextGrid(self, canvas):
        for row in range(self.gridRows):
            for col in range(self.gridCols):
                x0 = col * self.letterWidth + self.pageMarginX
                y0 = row * self.letterHeight + self.pageMarginY
                x1 = x0 + self.letterWidth
                y1 = y0 + self.letterHeight
                canvas.create_rectangle(x0, y0, x1, y1, outline="light grey")
    
    def drawCursor(self, canvas):
        x0 = self.cursorCol * self.letterWidth + self.pageMarginX
        y0 = self.cursorRow * self.letterHeight + self.pageMarginY
        x1 = x0 + self.letterWidth
        y1 = y0 + self.letterHeight
        canvas.create_rectangle(x0, y0, x1, y1, fill= "cornflower blue", width=0)

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill= "light grey", width=0)
        self.currDoc.drawDocPage(canvas, self.pagePosX - self.pageWidth//2, self.menuHeight + self.offsetY, self.pagePosX + self.pageWidth//2,
            self.pageHeight)
        if len(self.currDoc.pages) > 0:
            self.drawCursor(canvas)
        self.currDoc.drawDocContents(canvas, self.pagePosX - self.pageWidth//2, self.menuHeight + self.offsetY, self.pagePosX + self.pageWidth//2,
            self.pageHeight)
        #self.drawTextGrid(canvas)
        self.drawTopMenu(canvas)
        self.drawBotMenu(canvas)
        self.drawSidebar(canvas)
        
        


class LibraryMode(Mode):
    def appStarted(self): 
        self.editmode = self.getMode("editor")
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
        self.showingTags = False
        self.dropdownOpen = False

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
        if 0 <= index < len(self.shownDocs) and 0<=row<self.rows and 0<=col<self.cols:
            if self.shownDocs[index] != self.selectedDocument:
                self.selectedDocument = self.shownDocs[index]
                print("click1")
            elif self.shownDocs[index] == self.selectedDocument:
                print("click2")
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
         # TODO: sth weird with this. list index out of range
        self.shownDocs = matchedDocs
        if matchedDocs != []:
            self.selectedDocument = self.shownDocs[0]
        else:
            self.selectedDocument = None
       

    def drawHighlight(self, canvas):
        selectedIndex = self.shownDocs.index(self.selectedDocument) #TODO: currently broken. selectedDocument should always be in shownDocs
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
            #TODO:create filepath
            #TODO:get timestamp
            new = Document(self, "filepath", answer, "0000")
            self.documents.append(new)
            #TODO: might be some issue with filters
            self.shownDocs = self.documents
            self.selectedDocument = new
            self.setActiveMode("editor")

    def delDocPopup(self):
        if len(self.documents) > 0:
            descrip = """Are you sure you want to delete this document?\n
            Deleted documents cannot be recovered."""
            answer = messagebox.askyesno("WARNING", descrip)
            if answer == True:
                #TODO: deletes the file located at the path of the currently selected document
                self.documents.remove(self.selectedDocument)
                if len(self.documents) == 0:
                    self.selectedDocument = None
                else:
                    self.selectedDocument = self.shownDocs[0]

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

    def showAllTags(self):
        if self.showingTags == False:
            self.showingTags = True
        else:
            self.showingTags = False

    def drawBotMenu(self, canvas):
        """Draws the lower menu that contains the options for the selected file"""
        buttonWidth = 80
        canvas.create_rectangle(0, self.height - self.menuBotHeight, self.width, self.height, fill= "white", width=0)
        if self.selectedDocument != None:
            drawButton(canvas, self.offsetX + buttonWidth//2, self.height - self.menuBotHeight//2, onClick = self.delDocPopup, text= "Delete")
            drawButton(canvas, self.width//4, self.height - self.menuBotHeight//2, onClick = self.renamePopup, text= "Rename")
            drawButton(canvas, self.width//4 + self.offsetX + buttonWidth, self.height - self.menuBotHeight//2, onClick = self.addTagPopup, text= "Add doctag")
            drawButton(canvas, self.width//4 + (self.offsetX + buttonWidth)*2, self.height - self.menuBotHeight//2, onClick = self.delTagPopup, text= "Delete tags")
            drawButton(canvas, self.width*(3/4), self.height - self.menuBotHeight//2, onClick=self.showAllTags, text= "Show All Tags", w = 100)



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


    #####################################
    #Editing functions
    #####################################

    def renamePopup(self):
        answer = simpledialog.askstring("Rename", "What would you like to rename the document?")
        if answer != None:
            self.selectedDocument.rename(answer)
            #TODO: write new title to file
    

    def addTagPopup(self):
        """Adds a doctag to the document. Not case sensitive."""

        descrip = """Add a general tag to your document.\n
        (Separate tags by commas. Not case sensitive)"""
        answer = simpledialog.askstring("Add doctags", descrip)
        if answer != None:
            newTags = []
            existingTags = []
            for tag in self.selectedDocument.tags:
                existingTags.append(tag.name)
            for elem in answer.split(","):
                if not (elem.lower() in existingTags):
                    newTags.append(elem.strip())
                else:
                    print("Doc already has this tag!") #TODO: maybe display this to user
            if newTags != []:
                self.selectedDocument.addDocTag(newTags)

    def delTagPopup(self):
        """Removes all instances of an inputted tag from the book, including its pages.
        Not case sensitive."""

        descrip = """WARNING: Will remove all instances of tag from the document\n
        (Separate tags by commas. Not case sensitive)"""

        answer = simpledialog.askstring("Remove tags", descrip)
        if answer != None:
            removedTags = []
            for elem in answer.split(","):
                removedTags.append(elem.strip())
            self.selectedDocument.delTag(removedTags)


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
        if self.showingTags == True:
            self.selectedDocument.drawAllTags(canvas)
        

def main():
    WritingApp(width=700, height=790)


if __name__ == "__main__":
    main()

