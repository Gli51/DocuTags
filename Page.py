class Page():
    def __init__(self, words, tags):
        """Initializes page class with contents and tags."""
        self.words = words
        self.internalTags = tags

    def getWordCount(self):

    def getCharCount(self):
        """Returns the number of characters (including spaces) on the page"""
        return len(self.words)

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

    def lines(self, PageWidth):
        """Returns list of words that appear on each line based off of a
        specified page width."""
        pass

    def 