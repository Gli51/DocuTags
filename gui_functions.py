#This file contains functions for common GUI elements.

def drawButton(canvas, cx:int, cy:int, onClick, text:str, w = 80, h = 20):
    """Takes in center coordinates, width and height, an onclick function.
    and text and draws a button with those criteria."""  
    roundRectangle(canvas, cx-w/2, cy-h/2, cx+w/2, cy+h/2, radius=14, fill="lightgrey",  
                        onClick=onClick)  
    canvas.create_text(cx, cy, text=text)

def roundRectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
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


#def dropdownMenu(canvas, items)
    #would need scrolling functionality?
    #sort items alphabetically (A-Z)
    #if items is an empty list, draw a single blank rectangle
    #for i in range(len(items):
        #draw rectangle with coordinates multiplied by i
        #draw text in center of rectangle (cy multiplied by i, cx constant)

    #each of the rectangles might call an onclick? need to select items from dropdown somehow.