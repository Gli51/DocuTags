#The main file, __init__.py
#This file runs the whole game by calling WritingApp, a modal app.

from cmu_112_graphics import *
import pickle
from Document import *

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
        pass

    #closeEditor

    ###############################################
    #Content management
    ###############################################

    #getCurrentPath (gets path of the edited document)

    #saveFile
        #(writeFile)
    
    #keyPressed(shift, numbers, symbols, letters, enter/return, backspace, tab)
        #need to check for line overflow

    #overflow (need to keep track of page width)

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
        self.documents = []
        doc1 = Document(self, "filepath", "15-112: Fundamentals of Computer Science", 1141, ["tag1", "tag2"], ["abcdefg", "qrstuv"])
        self.documents.append(doc1)

    #selectDoc
        #If selected document clicked again, open editor for that document.
        #if another doc is clicked, deselect current and select newly clicked.

        #will need a mousepressed

    #newDoc
        #opens panel where title and timestamp can be entered

    #newDocCancel (onclick method)
        #closes the panel opened by newDoc

    #newDocDone (onclick method)
        #creates a new file in the directory with the given name and timestamp from newDoc. starts blank, with no tags
        #opens the document in the editor

    #delDoc
        #deletes the file located at the path of the currently selected document

    ########################################
    #Menu bars
    ########################################
    
    def drawTopMenu(self, canvas):
        """Draws the top menu which contains the search bar, sort and filter options,
        and create new document button."""
        offsetX = 14
        offsetY = 8
        dividerX = 180
        titleSize = 11
        subtitleSize = 10

        canvas.create_rectangle(0, 0, self.width, self.menuHeight, fill= "white", width=0)
        canvas.create_text(offsetX, offsetY, anchor="nw", font=f"Arial {titleSize} normal", text="Search:")
        #search input
        #divider
        canvas.create_line(dividerX, offsetY, dividerX, self.menuHeight - offsetY, width=2, fill="light grey")
        #sort text
        canvas.create_text(dividerX + offsetX, offsetY, anchor = "nw", font=f"Arial {titleSize} normal", text="Sort by:")
        #sort dropdown
        #filter text
        canvas.create_text(dividerX + offsetX, self.menuHeight - offsetY, anchor = "sw", font=f"Arial {titleSize} normal", text="Filter tag:")
        #filter display (max 4)
        #new doc button

    def drawBotMenu(self, canvas):
        canvas.create_rectangle(0, self.height - self.menuBotHeight, self.width, self.height, fill= "white", width=0)


    ########################################
    #Grid layout
    ########################################

    def drawGrid(self, canvas):
        for i in range(len(self.documents)):
            row = i % self.rows
            col = i // self.rows
            cx = col * self.cellWidth + self.cellWidth//2 + (self.width//2-self.displayWidth)
            cy = row * self.cellHeight + self.cellHeight//2 + self.menuHeight
            #stuff for testing:
            #x0 = col * self.cellWidth + (self.width//2-self.displayWidth)
            #y0 = row * self.cellHeight + self.menuHeight
            #x1 = x0 + self.cellWidth
            #y1 = y0 + self.cellHeight
            #canvas.create_rectangle(x0,y0,x1,y1,outline="grey")
            #draw document[i] at center of cell
            self.documents[i].drawThumbnail(canvas, cx, cy)

    #####################################################################################
    #TYPING CAN BE ITS OWN SEPARATE FUNCTION SINCE IT WILL BE REUSED IN MULTIPLE PLACES:
    #TEXT EDITOR, RENAME DOCUMENT, EDIT TAGS, SEARCH BAR INPUTS
    #####################################################################################

    #searchLibrary (will probably use a similar structure to searchDoc in the editor mode)

    #####################################
    #Editing functions
    #####################################

    #renameDoc
        #enables panel which is drawn over the rest of the screen
        #takes in text input
        #if renameDone onclick fired while panel is open, writes new title to file
    
    #renameDone (onclick method for when done button is clicked)

    #editDocTag
        #enables panel
        #takes text input
        #if docTagDone onclick fired, writes new tags to file.

    #docTagDone (onclick method for when done button is clicked)

    ############################################
    #Sort
    ############################################
    #from operator import itemgetter, attrgetter

    #sort keys: title, time, tag
    #mutable/destructive sort which changes the indexes of the items in the list
        
    #def sortTime (sorts by time)
        #documents.sort(documents, key=attrgetter('timestamp', 'title'))
    
    #def sortTitle (sorts alphabetical order A-Z)
        #documents.sort(documents, key=attrgetter('title', 'timestamp'))

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
        canvas.create_rectangle(self.width//2 - self.displayWidth, self.menuHeight, self.width//2 + self.displayWidth,
            self.height - self.menuBotHeight, outline="grey")
        self.drawGrid(canvas)
        self.drawTopMenu(canvas)
        self.drawBotMenu(canvas)
        

def main():
    WritingApp(width=700, height=800)


if __name__ == "__main__":
    main()

