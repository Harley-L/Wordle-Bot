from tkinter import *
import string
from WordleGrid import WordleGrid
from singleplayer import machine_guess

lastKey = None  # last key pressed
grid = None


# Description: Homepage of the Wordle
# x: width of window - int
# y: height of window - int
class HomePage(Frame):
    def __init__(self, x, y):
        super().__init__()
        self.initUI(x, y)

    def initUI(self, x, y):
        global grid
        upper_frame = Frame(self, relief=RAISED, borderwidth=1, bg='black')
        upper_frame.pack(fill=BOTH, expand=True)

        top_frame = Frame(upper_frame, relief=RAISED, borderwidth=1, bg='black', height=50)
        top_frame.pack(fill=X)
        title = Label(top_frame, text="WORDLE", font=('Ariel', 30, 'bold'), bg='black', fg='white')
        title.pack()

        helpicon_dir = "resources/help_icon.png"
        helpicon = PhotoImage(file=helpicon_dir)
        helpiconformat = helpicon.subsample(20, 20)
        help_panelicon = Label(top_frame, image=helpiconformat)
        help_panelicon.photo = helpiconformat

        help_button = Button(top_frame, text="Help", image=help_panelicon.photo, relief="flat", bg='black', border=1, bd=0,
                             highlightthickness=0, command=lambda: machine_guess(grid))
        help_button.place(x=400, y=5)

        restarticon_dir = "resources/restart_icon.png"
        restarticon = PhotoImage(file=restarticon_dir)
        restarticonformat = restarticon.subsample(27, 27)
        restart_panelicon = Label(top_frame, image=restarticonformat)
        restart_panelicon.photo = restarticonformat

        help_button = Button(top_frame, text="Restart", image=restart_panelicon.photo, relief="flat", bg='black', border=1, bd=0,
                             highlightthickness=0, command=lambda: grid.restart())
        help_button.place(x=440, y=5)

        guess_frame = Frame(upper_frame, relief=RAISED, borderwidth=1, bg='black')
        guess_frame.pack(fill=BOTH, expand=True)

        # Letter frame parameters
        relief_option = RAISED
        borderwidth_option = 1
        bg_option = 'black'
        height_option = 50
        width_option = 50
        padx_option = 2
        pady_option = 2
        edgey_option = 30
        edgex_option = x/2 - height_option*2.5 - 4*padx_option

        letter_frames = [[], [], [], [], []]

        for r in range(6):
            for c in range(5):
                letteri = Frame(guess_frame, relief=relief_option, borderwidth=borderwidth_option, bg=bg_option,
                      height=height_option, width=width_option)
                if r == 0 and c == 0:
                    letteri.grid(padx=(edgex_option, padx_option), pady=(edgey_option, pady_option), row=r, column=c)
                elif r == 0:
                    letteri.grid(padx=padx_option, pady=(edgey_option, pady_option), row=r, column=c)
                elif c == 0:
                    letteri.grid(padx=(edgex_option, padx_option), pady=pady_option, row=r, column=c)
                else:
                    letteri.grid(padx=padx_option, pady=pady_option, row=r, column=c)

                texti = Label(letteri, text='', font=('Ariel', 30, 'bold'), bg=bg_option, fg='white')
                texti.place(x=25, y=25, anchor='center')

                letter_frames[c].append((letteri, texti))

        keyboard_frame = Frame(self, relief=RAISED, borderwidth=1, bg='black', height=200)
        keyboard_frame.pack(fill=X, expand=True)
        top_keyboard_row_frame = Frame(keyboard_frame, relief=RAISED, borderwidth=1, bg='black', height=200/3)
        top_keyboard_row_frame.pack(fill=X, expand=True)
        middle_keyboard_row_frame = Frame(keyboard_frame, relief=RAISED, borderwidth=1, bg='black', height=200/3)
        middle_keyboard_row_frame.pack(fill=X, expand=True)
        bottom_keyboard_row_frame = Frame(keyboard_frame, relief=RAISED, borderwidth=1, bg='black', height=200/3)
        bottom_keyboard_row_frame.pack(fill=X, expand=True)

        keyboard = []
        key_top_row = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        key_middle_row = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
        key_bottom_row = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        # Letter frame parameters
        relief_option_l = RAISED
        borderwidth_option_l = 1
        bg_option_l = 'black'
        height_option_l = 40
        width_option_l = 40
        padx_option_l = 5
        pady_option_l = 5
        edgex_option_l_t = x/2 - height_option_l*5 - 9*padx_option_l
        edgex_option_l_m = x/2 - height_option_l*4.5 - 8*padx_option_l
        edgex_option_l_b = x/2 - height_option_l*3.5 - 6*padx_option_l
        font_size_option_l = 24

        for i, char in enumerate(key_top_row):
            letteri = Frame(top_keyboard_row_frame, relief=relief_option_l, borderwidth=borderwidth_option_l, bg=bg_option_l,
                    height=height_option_l, width=width_option_l)
            if i == 0:
                letteri.grid(padx=(edgex_option_l_t, padx_option_l), pady=pady_option_l, row=0, column=i)
            else:
                letteri.grid(padx=padx_option_l, pady=pady_option_l, row=0, column=i)
            texti = Label(letteri, text=char, font=('Ariel', font_size_option_l, 'bold'), bg='black', fg='white')
            texti.place(x=width_option_l/2, y=height_option_l/2, anchor='center')

            keyboard.append((letteri, texti))

        for i, char in enumerate(key_middle_row):
            letteri = Frame(middle_keyboard_row_frame, relief=relief_option_l, borderwidth=borderwidth_option_l, bg=bg_option_l,
                    height=height_option_l, width=width_option_l)
            if i == 0:
                letteri.grid(padx=(edgex_option_l_m, padx_option_l), pady=pady_option_l, row=1, column=i)
            else:
                letteri.grid(padx=padx_option_l, pady=pady_option_l, row=1, column=i)
            texti = Label(letteri, text=char, font=('Ariel', font_size_option_l, 'bold'), bg='black', fg='white')
            texti.place(x=width_option_l / 2, y=height_option_l / 2, anchor='center')

            keyboard.append((letteri, texti))

        for i, char in enumerate(key_bottom_row):
            letteri = Frame(bottom_keyboard_row_frame, relief=relief_option_l, borderwidth=borderwidth_option_l,
                            bg=bg_option_l,
                            height=height_option_l, width=width_option_l)
            if i == 0:
                letteri.grid(padx=(edgex_option_l_b, padx_option_l), pady=pady_option_l, row=2, column=i)
            else:
                letteri.grid(padx=padx_option_l, pady=pady_option_l, row=2, column=i)
            texti = Label(letteri, text=char, font=('Ariel', font_size_option_l, 'bold'), bg='black', fg='white')
            texti.place(x=width_option_l / 2, y=height_option_l / 2, anchor='center')

            keyboard.append((letteri, texti))

        grid = WordleGrid(letter_frames, keyboard)

        self.pack(fill=BOTH, expand=True)


# Description: Manages keystrokes
# event: type of keystroke - string
def key_in(event):
    global grid
    if event.keysym == event.char:
        grid.press_char(event.char.capitalize())
    elif event.keysym == 'Delete':
        grid.delete()
    elif event.keysym == 'BackSpace':
        grid.delete()
    elif event.keysym == 'Return':
        grid.enter()
    elif event.keysym == 'Enter':
        grid.enter()


# Description: Main function to initialize Tkinter window
if __name__ == "__main__":
    window = Tk()
    window.title("WORDLE 2.0")
    # Set size of the window to not change.
    windowx = 500
    windowy = 560
    window.geometry(f"{500}x{560}+400+50")
    window.minsize(windowx, windowy)
    window.maxsize(windowx, windowy)
    window.configure(bg='black')
    wordle = HomePage(windowx, windowy)

    ent = Entry(window)
    ent.bind_all('<Key>', key_in)
    ent.focus_set()

    window.mainloop()
