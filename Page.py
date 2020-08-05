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

    def lines(self):
        """Returns list of words that appear on each line based off of the page width."""
        pass

    def addPageTag(self, newTag:str):
        #newTag is just the name of the new tag
        self.tags.append(Tag(newTag))

    def delPageTag(self, tag:str):
        #deletes tag on page by tag name
        for tag in self.tags:
            if tag.name == tag:
                self.tags.remove(tag)