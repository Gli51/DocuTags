from Tag import *

class Page():
    def __init__(self, app, words = "", tags = []):
        """Initializes page class with contents and tags."""
        self.app = app
        self.words = words
        self.tags = tags
        self.PageWidth = 30

    def getWordCount(self):
        """Returns the number of words on the page by counting the number
        of spaces and adding one."""
        return self.words.count(' ') + 1

    def getCharCount(self):
        """Returns the number of characters (including spaces) on the page"""
        return len(self.words)

    ###########################################################################
    #Magic Methods
    ###########################################################################
    def __repr__(self):
        return "page"

    def __add__(self, other):
        """Adds words to a page. If Page, adds the words on that Page to the words
        on the initial page"""
        if isinstance(other, str):
            return Page(self.words + other)
        if isinstance(other, Page):
            return Page(self.words + other.words)
        return "Can't add content of that type to Page"

    def __contains__(self, val):
        """Can find strings in the words on the page"""
        return val in self.words


    def addPageTag(self, newTags:str):
        #newTag is just the name of the new tag
        for elem in newTags:     
            self.tags.append(Tag(elem.lower()))
            self.app.editmode.currDoc.updateTags()

    def delPageTag(self, tags:str):
        #deletes tag on page by tag name
        for elem in tags:
            for pagetag in self.tags:
                if pagetag.name == elem.lower():
                    self.tags.remove(pagetag)
            #check if tag is on any other pages in document
            if len(self.app.editmode.currDoc.pages) > 0:
                count = 0
                for page in self.app.editmode.currDoc.pages:
                    for tag in page.tags:
                        if elem == tag.name:
                            count += 1
                if count < 2:
                    for tag in self.app.editmode.currDoc.tags:
                        if elem == tag.name:
                            self.app.editmode.currDoc.tags.remove(tag)
                self.app.editmode.currDoc.updateTags()