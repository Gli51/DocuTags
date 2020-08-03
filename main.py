from cmu_112_graphics import *

class WritingApp(ModalApp):
    def appStarted(self):
        self.addMode(LibraryMode(name="library"))
        self.addMode(EditorMode(name="editor"))
        self.setActiveMode("library")
    
    def readFile(self):
        """Returns the contents of the file at the path. Code taken from https://www.diderot.one/course/34/chapters/2604/"""
        with open(self.path, "rt") as f:
            return f.read()
    
    def getDocs(self): #reads files and makes them into Document objects which are then added to the library
        #for all files in specific path:
        #set title
        #set content and tags
        #if marked with pages, page words = the string after pages
        #if simply a string, automatically set the pages with defaults
        #tags represented by {highlighted words here: tag1, tag2, tag3}
        rawContents = self.readFile()
        pass

class EditorMode(Mode):
    def appStarted(self):
        pass
    #save function (writeFile)

class LibraryMode(Mode):
    def appStarted(self): 
        self.menuHeight = self.height//12
        self.menuBotHeight = self.height//14
        self.libraryWidth = 300
    #Load in/display Documents
    #Button to create document
    #select document. If selected document clicked again, open editor for that document.

    def createDoc(self):

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill= "light grey", width=0)
        canvas.create_rectangle(0, 0, self.width, self.menuHeight, fill= "white", width=0)
        canvas.create_rectangle(0, self.height - self.menuBotHeight, self.width, self.height, fill= "white", width=0)
        canvas.create_rectangle(self.width//2 - self.libraryWidth, self.menuHeight, self.width//2 + self.libraryWidth,
            self.height - self.menuBotHeight, outline="grey")
        

def main():
    WritingApp(width=700, height=800)
    testAll()


if __name__ == "__main__":
    main()

