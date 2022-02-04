from singleplayer import choose_random_word
from Conditions import give_conditions
from tkinter import *


# Description: Template for popup window
# title: title text - string
# text: message text - string
def popup(title, text):
    # Initialize popup
    win = Toplevel()
    win.wm_title(title)
    winx = 400
    winy = 200
    win.minsize(winx, winy)
    win.maxsize(winx, winy)
    win.geometry(f"{winx}x{winy}+400+200")
    win.config(bg='black')

    # Title of the popup
    message = Label(win, text=text, font=('Ariel', 20), bg='black', fg='white')
    message.pack(side=TOP, pady=10)

    # Create canvas
    canvas = Canvas(win, width=winx, height=winy, bg='black', highlightthickness=0)
    canvas.pack(side=LEFT)

    # Exit button to close the popup window
    exitpop = Button(win, text="Okay", command=win.destroy, height=2, width=12)
    exitpop.place(x=(winx / 2) - 55, y=winy - 60)


# Description: Change a tile
# tiles: width of window - list of list of tupples(Frame, Label)
# x: row - int
# y: column - int
# char: character to change - char
# colour: colour of background to change - string
# font_colour: colour of font to change - string
def change_tile(tiles, x, y, char, colour='black', font_colour='white'):
    # colour options: green, yellow, and grey
    if colour == 'G':
        colour = '#538d4e'
    elif colour == 'Y':
        colour = '#b69f3c'
    elif colour == 'O':
        colour = '#3a3a3c'

    tiles[x][y][0].config(bg=colour)
    tiles[x][y][1].config(bg=colour, text=char, fg=font_colour)


# Description: Change a tile
# tiles: width of window - list of tupples(Frame, Label)
# x: index - int
# colour: colour of background to change - string
# font_colour: colour of font to change - string
def change_colour_tile(tiles, x, colour='black', font_colour='white'):
    # colour options: green, yellow, and grey
    if colour == 'G':
        colour = '#538d4e'
    elif colour == 'Y':
        colour = '#b69f3c'
    elif colour == 'O':
        colour = '#3a3a3c'

    tiles[x][0].config(bg=colour)
    tiles[x][1].config(bg=colour, fg=font_colour)


# Description: Wordle Game Class
class WordleGrid:
    def __init__(self, lf, alpha):
        self.letter_frames = lf
        self.col = 0
        self.row = 0
        self.word = ['', '', '', '', '']
        self.done = False
        self.solution, self.allowed_words = choose_random_word()
        self.guessed_chars = set()
        self.incorrect_placement = set()
        self.correct_placement = set()
        self.alpha = alpha
        self.past_words = []
        self.past_conditions = []
        self.hints = 0
        self.guesses = 0

    # Description: Type a character after pressing a key
    # char: char pressed - string
    def press_char(self, char):
        if not self.done and not self.col == 5:
            self.word[self.col] = char
            change_tile(self.letter_frames, self.col, self.row, char)
            self.col += 1

    # Description: Delete a character after pressing the delete key
    def delete(self):
        self.col -= 1
        self.word[self.col] = ''
        change_tile(self.letter_frames, self.col, self.row, '.', 'black', 'black')
        if self.col == -1:
            self.col = 0

    # Description: Register a word after entering characters to form a word
    def enter(self):
        if self.check_allowed():
            self.guess()
            self.word = ['', '', '', '', '']
            self.col = 0
            self.row += 1
            if self.row == 6 and self.past_conditions[-1] != ['G', 'G', 'G', 'G', 'G']:
                self.lose()

    # Description: Helper function to guess a word and perform the associated function
    def guess(self):
        for char in self.word:
            self.guessed_chars.add(char)
        cond = give_conditions("".join(self.word).lower(), "".join(self.solution).lower())

        self.past_words.append(self.word)
        self.past_conditions.append(cond)
        self.guesses += 1

        for i, colour in enumerate(cond):
            change_tile(self.letter_frames, i, self.row, self.word[i], colour)
            self.update_keyboard(colour, i)
        if cond == ['G', 'G', 'G', 'G', 'G']:
            self.win()

    # Description: If the machine guesses a word for you
    # given_word: given guessed word - string
    def helper_guess(self, given_word):
        self.word = given_word
        self.hints += 1
        self.col = 5
        for i, char in enumerate(self.word):
            change_tile(self.letter_frames, i, self.row, self.word[i], 'black')

    # Description: Check if a word is allowed to be guessed
    # Returns: word allowed to be guessed? - bool
    def check_allowed(self):
        if "".join(self.word).lower() not in self.allowed_words:
            for i in range(5):
                change_tile(self.letter_frames, i, self.row, self.word[i], 'red')
            for i in range(5):
                change_tile(self.letter_frames, i, self.row, '', 'black')
            self.word = ['', '', '', '', '']
            self.col = 0
            return False
        return True

    # Description: After guessing a word, what letters are used and what are their conditions
    # colour: condition colour - char
    # i: index of char in word - int
    def update_keyboard(self, colour, i):
        keyboard_order = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                          'Z', 'X', 'C', 'V', 'B', 'N', 'M']

        if colour == 'G':
            self.correct_placement.add(self.word[i])
        elif colour == 'Y':
            self.incorrect_placement.add(self.word[i])

        for i, key in enumerate(keyboard_order):
            if key in self.correct_placement:
                change_colour_tile(self.alpha, i, 'G')
            elif key in self.incorrect_placement:
                change_colour_tile(self.alpha, i, 'Y')
            elif key in self.guessed_chars:
                change_colour_tile(self.alpha, i, 'O')

    # Description: The user feedback if won
    def win(self):
        popup("You Win!", f"You Win!\nGuesses: {self.guesses}\nHints: {self.hints}")
        self.done = True

    # Description: The user feedback if lost
    def lose(self):
        popup("You Lose!", f"You Lose :(\nGuesses: {self.guesses}\nHints: {self.hints}")
        self.done = True

    # Description: Restart the Wordle by clearing the tiles and resetting instance variables
    def restart(self):
        for i, line in enumerate(self.letter_frames):
            for j, tile in enumerate(line):
                change_tile(self.letter_frames, i, j, '.', 'black', 'black')

        for i, tile in enumerate(self.alpha):
            change_colour_tile(self.alpha, i)

        self.col = 0
        self.row = 0
        self.word = ['', '', '', '', '']
        self.done = False
        self.solution, self.allowed_words = choose_random_word()
        self.guessed_chars = set()
        self.incorrect_placement = set()
        self.correct_placement = set()
        self.past_words = []
        self.past_conditions = []
        self.hints = 0
        self.guesses = 0
