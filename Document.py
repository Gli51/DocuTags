#The Document class
#This file contains the methods and attributes of document objects.

from cmu_112_graphics import *

class Document():
    def __init__(self, app, path, title, make_timestamp, tags=[], pages=[]):
        """Takes in an app, path, title, tags, pages, and timestamp and initializes a document
        object."""
        self.app = app
        self.path = path
        self.title = title
        self.pages = pages
        self.tags = tags
        self.make_timestamp = make_timestamp
        self.edit_timestamp = None #TODO: write function to update this value
        self.currPage = 0
        self.docWidth = self.app.libraryWidth // 4 - 20
        self.docHeight = self.app.libraryHeight // 4 - 20
        self.thumbnailWidth = 18 #this is the number of characters that can fit on one line

    def addTag(self, newTag):
        """Adds a tag to the list of tags."""
        self.tags.append(newTag)

    def editTag(self, newTags):
        """Replaces the tags with a new list of tags"""
        self.tags = self.newTags

    def getTags(self) -> list:
        """returns a list of tags."""
        return self.tags

    def rename(self, newName):
        self.title = self.newName
        #write to file

    def deletePage(selft):
        """Takes in a pageIndex and removes it from the list of pages."""
        if len(self.pages) > self.currPage: # this should always be true
            self.pages.pop(self.currPage)
            return True
        else:
            return False
    
    def addPage(self):
        """Adds a new blank page at the index after the current page."""
        newPageIndex = self.currPage + 1
        self.pages.insert(newPageIndex, Page())

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

    def roundRectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """CITATION: from user SneakyTurtle on StackOverflow
        https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
        Draws a rounded rectangle with corners at (x1,y1) and x2,y2)."""
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        canvas.create_polygon(points, **kwargs, smooth=True)
    
    def drawThumbnail(self, canvas, cx:int, cy:int):
        """Draws a thumbnail of the document around the given center coordinates."""
        halfWidth = self.docWidth//2
        halfHeight = self.docHeight//2
        tagHeight = self.docHeight//12
        tagMargin = 4
        tagPaddingX = 6
        tagPaddingY = 2
        leftAnchor = cx - halfWidth + 12

        #draw rectangle
        canvas.create_rectangle(cx - halfWidth, cy - halfHeight, cx + halfWidth, cy + halfHeight, fill="white",
            width=0)
        #draw title text
        canvas.create_text(cx, cy - (halfHeight*(6/7)), anchor= "n", font= "Arial 10 normal", 
            text= f"{self.thumbnailWraparound()}", fill="grey20")

        #draw tags
        #TODO: Clean up the variables in this code!
        for i in range(len(self.tags)):
            tagLength = len(self.tags[i])* 6 + tagPaddingX*2
            tagHeight = 14 + tagPaddingY
            row = i
            self.roundRectangle(canvas, leftAnchor, cy + row*(tagHeight + tagMargin),
                leftAnchor + tagLength, cy + tagHeight + row*(tagHeight + tagMargin), radius=6, fill="gold")
            #TODO: have this use the color and name of the tag object
            canvas.create_text(leftAnchor + tagPaddingX, cy + row*(tagHeight//2 + tagMargin + tagPaddingY*2),
                anchor="nw", font="Arial 8 normal", text=f"{self.tags[i]}")

