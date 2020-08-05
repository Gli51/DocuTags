#The Document class
#This file contains the methods and attributes of document objects.

from cmu_112_graphics import *
from gui_functions import *
from Page import *
from Tag import *

class Document(): #careful about timestamps, they may need to be strings to preserve zeroes.
    def __init__(self, app, path, title, make_timestamp, tags=[], pages=[]):
        """Takes in an app, path, title, tags, pages, and timestamp and initializes a document
        object."""
        self.app = app
        self.path = path
        self.title = title
        self.pages = pages
        self.doctags = tags
        self.tags = self.doctags
        self.currPage = None
        self.updatePages()
        self.updateTags()
        #This loads all the tags both internal and external to the document.
        #and sets current page if there are pages
        self.make_timestamp = make_timestamp
        self.edit_timestamp = None #TODO: write function to update this value
        self.docWidth = self.app.libraryWidth // 4 - 20
        self.docHeight = self.app.libraryHeight // 4 - 20
        self.thumbnailWidth = 16 #this is the number of characters that can fit on one line

        ###################################################################################
        #Variables for drawing tags
        ###################################################################################
        self.halfWidth = self.docWidth//2
        self.halfHeight = self.docHeight//2
        self.tagHeight = self.docHeight//12
        self.tagMargin = 4
        self.tagPaddingX = 6
        self.tagPaddingY = 2

    
    ##############################################################################
    #Magic Methods
    ##############################################################################
    def __repr__(self):
        return self.title

    ############################################################################
    #Editing methods + Pageflipping
    ############################################################################

    def addDocTag(self, newTags):
        """Adds tags to the list of tags."""
        for elem in newTags:
            #if tag already exists on another document, use the same color for the tag
            for document in self.app.documents:
                for tag in document.tags:
                    if tag.name == elem:
                        self.doctags.append(Tag(elem, tag.color))
                        return
            self.doctags.append(Tag(elem))
            self.updateTags()

    def delTag(self, tags):
        """Deletes all instances of that tag from the document, including pages."""
        for elem in tags:
            for doctag in self.doctags:
                if doctag.name == elem:
                    self.doctags.remove(doctag)
            for page in self.pages:
                for pagetag in page.tags:
                    if pagetag.name == elem:
                        page.tags.remove(pagetag)
            self.updateTags()


    def updateTags(self):
        """Method that updates the list of all tags in document. Called when
        doctags or pagetags/internal tags are edited."""
        self.tags = self.doctags
        if len(self.pages) > 0:
            for page in self.pages:
                if len(page.tags) > 0:
                    for tag in page.tags:
                        if tag not in self.doctags:
                            self.tags.append(tag)

    def updatePages(self):
        if len(self.pages) > 0:
            self.currPage = 0

    def getTags(self) -> list:
        """returns a list of tags."""
        return self.tags

    def rename(self, newName):
        self.title = newName
        #TODO: write to file

    def deletePage(self):
        """Takes in a pageIndex and removes it from the list of pages."""
        if len(self.pages) > self.currPage: # this should always be true
            self.pages.pop(self.currPage)
            return True
        else:
            return False
    
    def addPage(self):
        """Adds a new blank page at the index after the current page."""
        if len(self.pages) > 0:
            newPageIndex = self.currPage + 1
        else:
            newPageIndex = 0
        self.pages.insert(newPageIndex, Page(self))
        #switch pages to the newly created page
        self.currPage = newPageIndex
        print(self.currPage)
        print(str(self.pages))

    def flipForward(self):
        """flips to the next page if it is not the last page. returns true if successful"""
        if self.currPage < len(self.pages)-1:
            #flip page forward
            self.currPage += 1
            return True
        else: return False

    def flipBackward(self):
        """flips back a page if it is not the first page. returns true if successful"""
        if self.currPage != 0:
            #flip page backward
            self.currPage -= 1
            return True
        else: return False

    def jumpToPage(self, pageIndex: int):
        """Jumps to the page with a specified index."""
        self.currPage = pageIndex

    def saveFile(self): #TODO: Update this to write the timestamp and document contents properly
        """Writes changes to file I/O. Code taken from https://www.diderot.one/course/34/chapters/2604/"""
        with open(self.path, "wt") as f:  
            f.write(self.contents)

    def thumbnailWraparound(self) -> str:
        """Returns a string of words fit to a specified pageWidth where words
        are not split if they run off the page."""
        # convert to a list
        #join list with newlines between each element.
        pageWidth = self.thumbnailWidth
        words = []
        page = []
        wordGroup = ""
        for elem in self.title.split(' '):
            words.append(elem)
        for i in range(len(words)):
            if words[i] is not words[-1]: #if not last element
                if len(words[i]) < pageWidth:
                    wordGroup += words[i]
                if len(words[i]) == pageWidth:
                    page.append(wordGroup)
                    wordGroup = ""
                elif len(wordGroup + " " + words[i+1]) > pageWidth:
                    page.append(wordGroup)
                    wordGroup = ""
                else:
                    wordGroup += " "
            elif words[i] is words[-1]:# if is last element
                wordGroup += words[i]
                page.append(wordGroup)
        thumbnailText = '\n'.join(page)
        return thumbnailText
    
    ############################################################################
    #Drawing functions
    ############################################################################

    def drawThumbnail(self, canvas, cx:int, cy:int):
        """Draws a thumbnail of the document around the given center coordinates."""
        leftAnchor = cx - self.halfWidth + 12

        #draw rectangle
        canvas.create_rectangle(cx - self.halfWidth, cy - self.halfHeight, cx + self.halfWidth, cy + self.halfHeight, fill="white",
            width=0)
        #draw title text
        canvas.create_text(cx, cy - (self.halfHeight*(6/7)), anchor= "n", font= ("Courier New", 9, "normal"), 
            text= f"{self.thumbnailWraparound()}", fill="grey20")

        #draw tags
        #TODO: Clean up the variables in this code!
        for i in range(len(self.tags)):
            tagLength = len(self.tags[i].name)* 7 + self.tagPaddingX*2
            tagHeight = 14 + self.tagPaddingY
            row = i
            roundRectangle(canvas, leftAnchor, cy + row*(tagHeight + self.tagMargin),
                leftAnchor + tagLength, cy + tagHeight + row*(tagHeight + self.tagMargin), radius=6, fill=f"{self.tags[i].color}")
            #TODO: have this use the color and name of the tag object
            canvas.create_text(leftAnchor + self.tagPaddingX, cy + row*(tagHeight + self.tagMargin),
                anchor="nw", font=("Courier New", 8, "normal"), text=f"{self.tags[i].name}")

    def drawDocPage(self, canvas):
        pass
        #call page drawing function for the current page
        #if len(self.pages) > 0:
            #wordsToDraw = self.pages[self.currPage].words
            #create canvas object with wordsToDraw

    def drawCurrTags(self, canvas, cx:int, cy:int):
        leftAnchor = cx - self.halfWidth + 12
        labelOffsetY = 30

        canvas.create_text(cx, cy - labelOffsetY, text="Page Tags:")

        if self.currPage != None:
            currTags = self.pages[self.currPage].tags

            for i in range(len(currTags)):
                tagLength = len(currTags[i].name)* 7 + self.tagPaddingX*2
                tagHeight = 14 + self.tagPaddingY
                row = i
                roundRectangle(canvas, leftAnchor, cy + row*(tagHeight + self.tagMargin),
                    leftAnchor + tagLength, cy + tagHeight + row*(tagHeight + self.tagMargin), radius=6, fill=f"{currTags[i].color}")
                canvas.create_text(leftAnchor, cy + row*(tagHeight + self.tagMargin),
                    anchor="nw", font=("Courier New", 8, "normal"), text=f"{currTags[i].name}")

