import tkinter as tk
import random
import pickle
from collections import defaultdict
import sys
import time

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
    
def rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

ROWS = 6  # six rows of squares on display
BACK = 'black'   #background
FORE = 'white'   # foreground
OUTLINE ='dim gray'
SPACE = 7  # space between letter squares (pixels)
SQUARE = 60 # dimensions of square (pixels)
KEY_WIDTH = 40 # for keyboard
KEY_HEIGHT = 60
HEIGHT = 800 # canvas dimensions
WIDTH = 800
TOP_MARGIN = 100
BOTTOM_MARGIN = 50
GOOD = rgb(100, 200, 100)
CLOSE = rgb(200, 200, 100)
BAD = rgb(200, 100, 100)
UNKNOWN = 'LightGray'

class Wordle():
    def __init__(self, debug):
        self.debug = debug
        self.words = pickle.load(open('guesses5.set', 'rb'))
        self.answers = pickle.load(open('answers5.list', 'rb'))
        self.wordLength = 5
        self.maxGuesses = 6
        self.interval = 400
        root = self.root = tk.Tk()
        root.title("WORDLE")
        frame = self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        self.playFrame=tk.Frame(frame)
        self.canvas = MyCanvas(self.playFrame, width=WIDTH, height=HEIGHT, background = BACK)
        self.canvas.pack()
        self.controlFrame = tk.Frame(frame)
        self.controls = tk.Canvas(self.controlFrame, width=WIDTH, height=HEIGHT, background = BACK)
        self.controls.pack()
        self.drawCanvas()       
        self.drawControls()        
        self.playFrame.grid(row = 0, column = 0)
        self.controlFrame.grid(row = 0, column = 0)
        self.play()
        root.mainloop()        
        
    def drawCanvas(self):
        canvas = self.canvas
        self.squares = squares =  {}
        self.letters = letters = {}
        self.scrollTop = 0   # for scrolling guesses; index of top square displayed
        y = TOP_MARGIN
        leftMargin = WIDTH//2 - 2*(SQUARE+SPACE) - SQUARE//2
        for row in range(self.maxGuesses):
            x = leftMargin
            state = tk.NORMAL if row < ROWS else tk.HIDDEN
            for col in range(self.wordLength):
                squares[row,col] = canvas.create_rounded_rectangle(x, y, x+SQUARE, y+SQUARE,  
                                                                   outline = OUTLINE, state = state)
                letters[row, col] = canvas.create_text(x+SQUARE//2, y+SQUARE//2, font = ('Helvetica', '24', 'bold' ), 
                                                       justify=tk.CENTER,  text='', tag = f'L{row}{col}', state=state)
                x += SQUARE+SPACE
            y += SQUARE+SPACE 
            canvas.focus_set()
            canvas.bind('<KeyPress>', self.keyPressed)
            self.notice = canvas.create_text(WIDTH//2, TOP_MARGIN//2, justify=tk.CENTER, state=tk.HIDDEN,
                               text='', fill=FORE, font = ('Helvetica', 16))
            self.quitButton = tk.Button(canvas, bg='red', fg=FORE, activebackground='red', 
                                  activeforeground = FORE,
                                   text='Quit', font=('Helvetica', '24', 'bold'),
                                   command = self.root.destroy, height = 1, width = 6, relief= tk.FLAT)
            playButton = tk.Button(canvas, bg='green', fg=FORE,  activebackground='green', activeforeground = FORE,
                                   text='Play', font=('Helvetica', '24', 'bold'),
                                   command = self.play, height = 1, width = 6, relief = tk.FLAT)
            
            canvas.create_window(10, 10, window=playButton, state=tk.NORMAL, tags = 'button', anchor = tk.NW)
            canvas.create_window(WIDTH-10, 10, window = self.quitButton, state = tk.NORMAL, 
                                 tags='button', anchor = tk.NE)
            
            self.gear = tk.PhotoImage(file='gear.png')
            canvas.create_image(WIDTH-64, TOP_MARGIN, anchor=tk.NW, image=self.gear, tag ='gear')
            canvas.tag_bind('gear', '<ButtonRelease-1>', lambda e: self.controlFrame.tkraise())
            
        x = WIDTH//2    
        y = TOP_MARGIN + ROWS*(SQUARE+SPACE)
        canvas.create_text(x, y, text = 'Use \u2191 \u2193 to scroll', tag = 'scroll',
                                      font = ('Helvetica', 14), fill = FORE, anchor = tk.N)            
        self.makeQwerty()             
            
    def drawControls(self):        
        controls = self.controls
        x = WIDTH - 64
        y = TOP_MARGIN
        side = 24
        controls.create_rectangle(x, y, x+ side, y+side, outline= OUTLINE, fill=BACK, tag='done')
        controls.create_line(x, y, x+side, y+side, width=1, fill=FORE, tag='done' )
        controls.create_line(x+side, y, x, y+side, width=1, fill=FORE, tag='done' )
        controls.tag_bind('done', '<ButtonRelease-1>', lambda e: self.playFrame.tkraise())
        controls.create_text(WIDTH//2, TOP_MARGIN, anchor=tk.N, text="Settings", fill = FORE, font = ('Helvetica', 24))
        
    def enterPressed(self):
        canvas = self.canvas
        if self.letter != self.wordLength:
            return
        self.showGuess()
        word = ''
        g = self.guess
        for letter in range(self.wordLength):
            tag = f'L{g}{letter}'
            word += canvas.itemcget(tag, 'text')
        word = word.lower()
        if word not in self.words:
            msg = f'{word} not in word list'
            canvas.itemconfigure(self.notice, text=msg, state=tk.NORMAL)      
            return
        self.colorize(word)
        self.guess += 1
        if word == self.answer:
            self.celebrate()
        else:
            self.letter = 0
            if self.guess == self.maxGuesses:
                self.lose()
            
    def deletePressed(self):
        canvas = self.canvas
        if canvas.itemcget(self.notice, 'state') == tk.NORMAL:
            canvas.itemconfigure(self.notice, state=tk.HIDDEN)
        guess = self.guess
        letter = self.letter
        if letter == 0:
            return
        letter -= 1
        canvas.itemconfigure(f'L{guess}{letter}', text="")
        self.letter = letter
        
    def scrollDown(self, delta):
        # Scroll boxes down by delta lines (negative delta means scroll up)
        
        if delta == 0:
            return
        top = self.scrollTop
        bottom = top + ROWS -1
        squares = self.squares
        letters = self.letters
        canvas = self.canvas
        length = self.wordLength
        
        # Can't scroll down if current guess is in the window
        
        if delta > 0 and top <=  self.guess <= bottom:
            return
        
        # Can't scroll down if the game is over and the last
        # guess is in the window
        
        if delta > 0 and self.state != 'active':
            if top <= min(self.guess, self.maxGuesses - 1) <= bottom:
                return
            
        
        # Can't scroll up if already at the top
        if delta < 0 and top == 0:
            return
        
        ydelta = -delta * (SQUARE + SPACE)
        for row in range(self.maxGuesses):
            for col in range(length):
                canvas.itemconfigure(squares[row, col], state = tk.HIDDEN)
                canvas.itemconfigure(letters[row, col], state = tk.HIDDEN)
        for row in range(top+delta, top+delta+ROWS):
            for col in range(length):
                canvas.itemconfigure(squares[row, col], state = tk.NORMAL)
                canvas.itemconfigure(letters[row, col], state = tk.NORMAL) 
        for row in range(self.maxGuesses):
            for col in range(length):
                for widget in (squares[row, col], letters[row, col]):
                    canvas.move(widget, 0, ydelta)
                    
        self.scrollTop += delta
        
    def showGuess(self):
        if not self.scrollTop <= self.guess < self.scrollTop + ROWS:
            self.scrollDown(self.guess-(self.scrollTop+ROWS-1))        
            
    def alphaPressed(self, c):
        canvas = self.canvas
        if self.letter == self.wordLength:
            return
        self.showGuess()
        canvas.itemconfigure(f'L{self.guess}{self.letter}', text = c)
        self.letter += 1
        
    def keyPressed(self, event):
        key = event.keysym
        if key in ('Up', 'KP_Up'):
            self.scrollDown(-1)
            return
        elif key in ('Down', 'KP_Down'):
            self.scrollDown(1)
            return
        if self.state != 'active':
            if key not in 'PQpq':
                return
            if key.upper() == 'P':
                self.play()
                return
            if key.upper() == 'Q':
                self.quitButton.invoke()
        if not key.isalpha():
            return
        if key in ('Return', 'KP_Enter'):
            self.enterPressed()
        elif key in ('BackSpace', 'Delete'):
            self.deletePressed()
        if len(key) > 1:
            return
        self.alphaPressed(key.upper())
    
    def play(self):
        self.playFrame.tkraise()
        canvas = self.canvas
        letters = self.letters
        squares = self.squares
        self.start = time.time()
        self.answer = random.choice(self.answers)
        for q in self.qwerty.values():
            canvas.itemconfigure(q, fill=UNKNOWN)            
        if self.debug:
            print(f'answer is {self.answer}')
        self.guess = 0
        self.letter = 0
        canvas.itemconfigure(self.notice, text='', state=tk.HIDDEN) 
        canvas.itemconfigure('button', state=tk.HIDDEN)
        for row in range(self.maxGuesses):
            for col in range(self.wordLength):
                canvas.itemconfigure(letters[row, col] , text='', fill=FORE)
                canvas.itemconfigure(squares[row, col], fill='')
        self.state = 'active'
        
    def revealLetter(self, idx, letter, color):
        qwerty = self.qwerty
        canvas = self.canvas
        letters = self.letters
        squares = self.squares
        g = self.guess
        canvas.itemconfigure(letters[g, idx], text=letter.upper())
        canvas.itemconfigure(squares[g, idx], fill=color)
        current = canvas.itemcget(qwerty[letter], 'fill') 
        if color != CLOSE or current != GOOD:
            canvas.itemconfigure(qwerty[letter], fill = color)
        canvas.update()
        
    def colorize(self, word):
        canvas = self.canvas
        letters = self.letters
        used = defaultdict(int)
        colors = self.wordLength*[None]
        answer = self.answer
        correct = [i for i in range(self.wordLength) if word[i]==answer[i] ]
        g = self.guess
        for c in correct:
            colors[c] = GOOD 
            used[word[c]] += 1
        others = [i for i in range(self.wordLength) if i not in correct and word[i] in answer]
        available = {}
        for i in others:
            c = word[i]
            available[c] = max(answer.count(c) - used[c], 0)
        for i in others:
            c = word[i]
            if available[c] == 0:
                continue
            colors[i] = CLOSE
            available[c] -= 1
            
        for i in range(self.wordLength):
            if i not in correct + others:
                colors[i] = BAD
                
        #Aninmated coloring
        interval = self.interval
        for i in range(self.wordLength):
            canvas.itemconfigure(letters[g,i], text = '')
            canvas.update()

        for idx, letter in enumerate(word):
            color = colors[idx]
            canvas.after(interval, self.revealLetter(idx, letter, color))
                                
    def celebrate(self):
        canvas = self.canvas
        elapsed = int(time.time() -self.start)
        minutes = elapsed//60
        seconds = elapsed%60
        self.state = 'win'
        canvas.itemconfigure('button', state = tk.NORMAL)
        canvas.itemconfigure(self.notice, state=tk.NORMAL,
                             text = f'{self.guess+1} guesses\n{minutes} minutes {seconds} seconds')
        
    def lose(self):
        canvas = self.canvas
        elapsed = int(time.time() -self.start)
        minutes = elapsed//60
        seconds = elapsed%60
        self.state = 'lost'
        canvas.itemconfigure('button', state = tk.NORMAL)
        canvas.itemconfigure(self.notice,  state=tk.NORMAL,
                             text = f'Out of guesses.  Word is "{self.answer}"\n{minutes} minutes {seconds} seconds')     


    def newGame(self, event):
        self.play()
        
    def makeKey(self, char, row, col):
        canvas = self.canvas
        lengths = [7,9,10]
        length = lengths[row]
        y = HEIGHT - BOTTOM_MARGIN - (row +1) * KEY_HEIGHT - row * SPACE
        start = WIDTH//2 - (KEY_WIDTH + SPACE) * length//2
        x = start + col*(KEY_WIDTH+SPACE)
        key = canvas.create_rounded_rectangle(x, y, x+KEY_WIDTH, y+KEY_HEIGHT, fill=UNKNOWN, outline=OUTLINE, tags = 'key')
        letter = canvas.create_text(x+KEY_WIDTH//2, y+KEY_HEIGHT//2, text=char, font=('Helvetica', 24, 'bold'), fill = FORE)
        for c in (char.lower(), char.upper()):
            self.qwerty[c] = key
        handler = lambda entry: canvas.event_generate('<KeyPress>', keysym=char)
        for widget in (key, letter):
            canvas.tag_bind(widget, '<ButtonRelease-1>', handler)
    
    def makeQwerty(self):
        canvas = self.canvas
        self.qwerty = {}
        key = self.makeKey
        top = 'QWERTYUIOP'
        middle = 'ASDFGHJKL'
        bottom = 'ZXCVBNM'
        for col, char in enumerate(bottom):
            key(char, 0, col)        
        for col, char in enumerate(middle):
            key(char, 1, col)        
        for col, char in enumerate(top):
            key(char, 2, col)
        y = HEIGHT - BOTTOM_MARGIN - KEY_HEIGHT 
        x = WIDTH//2 - (KEY_WIDTH + SPACE) * 7 // 2
        x -= SPACE + 2*KEY_WIDTH
        key = canvas.create_rounded_rectangle(x, y, x+ 2* KEY_WIDTH, y+KEY_HEIGHT, fill=UNKNOWN, outline=OUTLINE)
        text = canvas.create_text(x+ KEY_WIDTH, y+ KEY_HEIGHT//2, text='Enter', fill=FORE, font=('Helvetica', 20, 'bold'))
        handler = lambda entry: canvas.event_generate('<KeyPress>', keysym='Return')
        for widget in (key, text):
            canvas.tag_bind(widget, '<ButtonRelease-1>', handler) 
        x+= 9*KEY_WIDTH + 8*SPACE
        key = canvas.create_rounded_rectangle(x, y, x+ 2* KEY_WIDTH, y+KEY_HEIGHT, fill=UNKNOWN)
        text = canvas.create_text(x+ KEY_WIDTH, y+ KEY_HEIGHT//2, text='Delete', fill=FORE, font=('Helvetica', 20, 'bold'))
        handler = lambda entry: canvas.event_generate('<KeyPress>', keysym='Delete')
        for widget in (key, text):
            canvas.tag_bind(widget, '<ButtonRelease-1>', handler)         

args = sys.argv

try:
    if args[1] in ('-d' '--debug'):
        Wordle(True)
except IndexError:
    Wordle(False)
