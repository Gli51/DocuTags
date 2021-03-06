#The Document class
#This file contains the methods and attributes of document objects.

from cmu_112_graphics import *
from gui_functions import *
from Page import *
from Tag import *
import copy

class Document(): #careful about timestamps, they may need to be strings to preserve zeroes.
    def __init__(self, app, path, title, make_timestamp, edit_timestamp, tags=[], pages=[]):
        """Takes in an app, path, title, tags, pages, and timestamp and initializes a document
        object."""
        self.app = app
        self.path = path
        self.title = title
        self.pages = pages
        self.doctags = tags
        self.tags = []
        self.currPage = None
        self.currPageNum = None
        self.updatePages()
        self.updateTags()
        #This loads all the tags both internal and external to the document.
        #and sets current page if there are pages
        self.make_timestamp = make_timestamp
        self.edit_timestamp = edit_timestamp 
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
        contents = []
        for page in self.pages:
            contents.append(page.words)
        return str(contents)
            

    ############################################################################
    #Editing methods + Pageflipping
    ############################################################################

    def addDocTag(self, newTags):
        """Adds tags to the list of tags."""
        for elem in newTags:     
            self.doctags.append(Tag(elem.lower()))
        self.updateTags()
        self.saveFile()

    def delTag(self, tags):
        """Deletes all instances of that tag from the document, including pages."""
        for elem in tags:
            for doctag in self.doctags:
                if doctag.name == elem.lower():
                    self.doctags.remove(doctag)
            for page in self.pages:
                for pagetag in page.tags:
                    if pagetag.name == elem:
                        page.tags.remove(pagetag)
            self.updateTags()
            self.saveFile()


    def updateTags(self):
        """Method that updates the list of all tags in document. Called when
        doctags or pagetags/internal tags are edited."""
        self.tags = []
        for doctag in self.doctags:
            self.tags.append(doctag)
        if len(self.pages) > 0:
            for page in self.pages:
                if len(page.tags) > 0:
                    for tag in page.tags:
                        if tag not in self.doctags:
                            self.tags.append(tag)


    def updatePages(self):
        if len(self.pages) > 0:
            self.currPage = 0
            self.currPageNum = self.currPage + 1
        elif len(self.pages) == 0:
            self.currPage = None
            self.currPageNum = None

    def getTags(self) -> list:
        """returns a list of tags."""
        return self.tags

    def rename(self, newName):
        self.title = newName
        self.saveFile()

    def deletePage(self):
        """Takes in a pageIndex and removes it from the list of pages."""
        if len(self.pages) > self.currPageNum and len(self.pages) > 0 and self.currPageNum > 1 and self.currPage != None:
            self.pages.pop(self.currPage)
        elif self.currPage == 0 and len(self.pages) > 0:
            self.pages.pop(self.currPage)
            self.app.editmode.updateCursor()
            if len(self.pages) < 1:
                self.currPage = None
                self.currPageNum = None
    
    def addPage(self):
        """Adds a new blank page at the index after the current page."""
        if len(self.pages) > 0:
            newPageIndex = self.currPage + 1 #TODO: UPDATE THIS SO CREATING NEW PAGES GOES TO THE NEW PAGE
        else:
            newPageIndex = 0
        self.pages.insert(newPageIndex, Page(self.app, "", []))
        #switch pages to the newly created page
        #the page number should always be one greater than the list index
        self.currPage = newPageIndex
        self.currPageNum = self.currPage + 1
        self.app.editmode.updateCursor()

    def flipForward(self):
        """flips to the next page if it is not the last page. returns true if successful"""
        if self.currPage != None and self.currPage < len(self.pages)-1:
            #flip page forward
            self.currPage += 1
            self.currPageNum += 1
            self.app.editmode.updateCursor()
            return True
        else: return False

    def flipBackward(self):
        """flips back a page if it is not the first page. returns true if successful"""
        if self.currPage != None and self.currPage > 0:
            #flip page backward
            self.currPage -= 1
            self.currPageNum -= 1
            self.app.editmode.updateCursor()
            return True
        else: return False

    def jumpToPage(self, pageNum: str):
        """Jumps to the page with a specified index."""
        pageIndex = int(pageNum) -1
        if 0 <= pageIndex < len(self.pages):
            self.currPage = pageIndex
            self.currPageNum = self.currPage + 1
            self.app.editmode.updateCursor()
            return True
        return False

    def saveFile(self): 
        """Writes changes to file I/O."""
        pageWords = '<pwords>'.join(page.words for page in self.pages)
        pageTags = '<tname>'.join((",".join(tag.name for tag in page.tags)) for page in self.pages)
        filepath = os.path.join("docfiles", self.path)
        doctagStr = ",".join(tag.name for tag in self.doctags)
        file_str = (f"(/)Title: {self.title}\n(/)Doctags: {doctagStr}\n(/)Pages: {pageWords}\n(/)Pagetags: {pageTags}")
        f = open(filepath, "w")
        f.write(file_str)
        f.close()

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

        #draw the first three tags
        #TODO: Clean up the variables in this code!
        for i in range(len(self.tags[:3])):
            tagLength = len(self.tags[i].name)* 7 + self.tagPaddingX*2
            tagHeight = 14 + self.tagPaddingY
            row = i
            roundRectangle(canvas, leftAnchor, cy + row*(tagHeight + self.tagMargin),
                leftAnchor + tagLength, cy + tagHeight + row*(tagHeight + self.tagMargin), radius=6, fill=f"{self.tags[i].color}")
            canvas.create_text(leftAnchor + self.tagPaddingX, cy + row*(tagHeight + self.tagMargin),
                anchor="nw", font=("Courier New", 8, "normal"), text=f"{self.tags[i].name}")

    def drawDocPage(self, canvas, x0:int, y0:int, x1:int, y1:int):
        """Draws the current page given the coords for the top and left corner."""
        #call page drawing function for the current page
        if len(self.pages) > 0:
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", width=0)
            
    
    def drawDocContents(self, canvas, x0, y0, x1, y1):
        "Draws the words for the current page based off page size coords"
        if len(self.pages) > 0:
            wordsToDraw = self.pages[self.currPage].words
            canvas.create_text(self.app.editmode.pagePosX - self.app.editmode.pageWidth//2 + self.app.editmode.offsetX,
                self.app.editmode.menuHeight + self.app.editmode.offsetY*2, anchor="nw",
                font=("Courier New", 10, "normal"), text=f"{wordsToDraw}")

    def drawCurrTags(self, canvas, cx:int, cy:int):
        """Draws a column of the tags on the current page given location coords."""
        leftAnchor = cx - self.halfWidth + 12
        labelOffsetY = 30

        canvas.create_text(cx, cy - labelOffsetY, text="Page Tags:")

        if self.currPage != None and len(self.pages) > 0:
            if len(self.pages[self.currPage].tags) > 0: # if the length of the page tags is greater than 0
                currTags = self.pages[self.currPage].tags

                for i in range(len(currTags)):
                    tagLength = len(currTags[i].name)* 7 + self.tagPaddingX*2
                    tagHeight = 14 + self.tagPaddingY
                    row = i
                    roundRectangle(canvas, leftAnchor, cy + row*(tagHeight + self.tagMargin),
                        leftAnchor + tagLength, cy + tagHeight + row*(tagHeight + self.tagMargin), radius=6, fill=f"{currTags[i].color}")
                    canvas.create_text(leftAnchor, cy + row*(tagHeight + self.tagMargin),
                        anchor="nw", font=("Courier New", 8, "normal"), text=f"{currTags[i].name}")

    def drawAllTags(self, canvas):
        """Draws a column of all tags on the document."""
        #draw tag with its color
        cx = self.app.width*(3/4)
        cy = self.app.height - self.app.menuBotHeight//2
        leftAnchor = cx - self.halfWidth + 12
        buttonHalfHeight = 10

        if len(self.tags) > 0:
            numTags = len(self.tags)
            boxHeight = 20 * numTags
        
            #draw rectangular background, height dependent on length of tag list
            canvas.create_rectangle(cx - self.halfWidth, cy - boxHeight - buttonHalfHeight, cx + self.halfWidth, cy- buttonHalfHeight, fill="light grey",
                width=2, outline="white")

            #TODO: Clean up the variables in this code!
            for i in range(len(self.tags)):
                tagLength = len(self.tags[i].name)* 7 + self.tagPaddingX*2
                tagHeight = 14 + self.tagPaddingY
                row = i
                roundRectangle(canvas, leftAnchor, cy - tagHeight - row*(tagHeight + self.tagMargin) - buttonHalfHeight,
                    leftAnchor + tagLength, cy - row*(tagHeight + self.tagMargin) - buttonHalfHeight, radius=6, fill=f"{self.tags[i].color}")
                canvas.create_text(leftAnchor + self.tagPaddingX, cy - row*(tagHeight + self.tagMargin) - tagHeight - buttonHalfHeight,
                    anchor="nw", font=("Courier New", 8, "normal"), text=f"{self.tags[i].name}")

