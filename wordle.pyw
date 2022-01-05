import tkinter as tk
import random
import pickle
from collections import defaultdict

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
FOREGROUND = 'white'
OUTLINE ='dim gray'
SPACE = 7  # space between letter squares (pixels)
SQUARE = 60 # dimensions of square (pixels)
HEIGHT = 800 # canvas dimensions
WIDTH = 800
TOP_MARGIN = 100
GOOD = 'green'
CLOSE = 'tan'
root = tk.Tk()
root.title("WORDLE")
canvas = MyCanvas(root, width=WIDTH, height=HEIGHT, background = BACKGROUND)
canvas.pack()

squares = {}
letters = {}
y = TOP_MARGIN
leftMargin = WIDTH//2 - 2*(SQUARE+SPACE) - SQUARE//2
for row in range(6):
    x = leftMargin
    for col in range(5):
        squares[row,col] = canvas.create_rounded_rectangle(x, y, x+SQUARE, y+SQUARE,  outline = OUTLINE)
        letters[row, col] = canvas.create_text(x+SQUARE//2, y+SQUARE//2, font = ('Helvetica', '24', 'bold' ), 
                                               justify=tk.CENTER,  text='', tag = f'L{row}{col}')
        x += SQUARE+SPACE
    y += SQUARE+SPACE
    
class Wordle():
    def __init__(self):
        self.words = pickle.load(open('guesses.set', 'rb'))
        self.answers = pickle.load(open('answers.list', 'rb'))
        canvas.focus_set()
        canvas.bind('<KeyPress>', self.keyPressed)
        self.unknown = canvas.create_text(400, TOP_MARGIN//2, justify=tk.CENTER, state=tk.HIDDEN,
                           text='', fill=FOREGROUND, font = ('Helvetica', 16))
        self.play()
        root.mainloop()        
        
    def enterPressed(self):
        if self.letter != 5:
            return
        word = ''
        g = self.guess
        for letter in range(5):
            tag = f'L{g}{letter}'
            word += canvas.itemcget(tag, 'text')
        word = word.lower()
        if word not in self.words:
            msg = f'{word} not in word list'
            canvas.itemconfigure(self.unknown, text=msg, state=tk.NORMAL)      
            return
        self.colorize(word)
        if word == self.answer:
            self.celebrate()
        self.guess += 1
        self.letter = 0
            
    def deletePressed(self):
        if canvas.itemcget(self.unknown, 'state') == tk.NORMAL:
            canvas.itemconfigure(self.unknown, state=tk.HIDDEN)
        guess = self.guess
        letter = self.letter
        if letter == 0:
            return
        letter -= 1
        canvas.itemconfigure(f'L{guess}{letter}', text="")
        self.letter = letter
            
    def alphaPressed(self, c):
        if self.letter == 5:
            return
        canvas.itemconfigure(f'L{self.guess}{self.letter}', text = c)
        self.letter += 1
        
    def keyPressed(self, event):
        key = event.keysym
        if not key.isalpha():
            return
        if key == 'Return':
            self.enterPressed()
        elif key in ('BackSpace', 'Delete'):
            self.deletePressed()
        if len(key) > 1:
            return
        self.alphaPressed(key.upper())
    
    def play(self):
        self.answer = random.choice(self.answers)
        print(f'answer is {self.answer}')
        self.guess = 0
        self.letter = 0
        canvas.itemconfigure(self.unknown, text='', state=tk.HIDDEN)    
        for row in range(6):
            for col in range(5):
                canvas.itemconfigure(letters[row, col] , text='', fill=FOREGROUND)
                canvas.itemconfigure(squares[row, col])
                    
    def colorize(self, word):
        used = defaultdict(int)
        answer = self.answer
        g = self.guess
        correct = [i for i in range(5) if word[i]==answer[i] ]
        for c in correct:
            canvas.itemconfigure(squares[g, c], fill= GOOD)
            used[word[c]] += 1
        others = [i for i in range(5) if i not in correct and word[i] in answer]
        available = {}
        for i in others:
            c = word[i]
            available[c] = max(answer.count(c) - used[c], 0)
        for i in others:
            c = word[i]
            if available[c] == 0:
                continue
            canvas.itemconfigure(squares[g, i], fill=CLOSE)
            available[c] -= 1
                                
    def celebrate(self):
        print('You win!')

wordle = Wordle()

