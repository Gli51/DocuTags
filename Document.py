from cmu_112_graphics import *

class Document():
    def __init__(self, path, title, pages, doctags):
        self.path = path
        self.title = title
        self.pages = pages
        self.tags = doctags
        self.currPage = 0

    def addTag(self, newTag):
        pass

    def getTags(self):


    def rename(self, newName):
        pass

    def saveFile(self):
        """Writes changes to file I/O. Code taken from https://www.diderot.one/course/34/chapters/2604/"""
        with open(self.path, "wt") as f:  
            f.write(self.contents)
