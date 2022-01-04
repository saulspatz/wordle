import tkinter as tk
import random
import pickle

class MyCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs )
        
    # adapted from https://pretagteam.com/question/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius = 10, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
          ]          
        return self.create_polygon(points, ** kwargs, smooth = True)

BACKGROUND = 'black'
OUTLINE ='dim gray'
SPACE = 7  # space between letter squares (pixels)
SQUARE = 60 # dimensions of square (pixels)
HEIGHT = 800 # canvas dimensions
WIDTH = 800
TOP_MARGIN = 100
root = tk.Tk()
root.title("WORDLE")
canvas = MyCanvas(root, width=WIDTH, height=HEIGHT, background = BACKGROUND)
canvas.pack()

squares = {}
y = TOP_MARGIN
for row in range(6):
    x = WIDTH//2 - 2*(SQUARE+SPACE) - SQUARE//2
    for col in range(5):
        squares[row,col] = canvas.create_rounded_rectangle(x, y, x+SQUARE, y+SQUARE, outline = OUTLINE, tag = 'square')
        x += SQUARE+SPACE
    y += SQUARE+SPACE
    
words = pickle.load(open('guesses.set', 'rb'))
answers = pickle.load(open('answers.set', 'rb'))
                    
    
def play():
    index = random.choice(range(len(answers)))
    
    
    
root.mainloop()
