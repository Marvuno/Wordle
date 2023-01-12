import random
import pygame
import enchant
from tkinter import *
from tkinter import messagebox

pygame.mixer.init()
with open('custom_word_list.txt') as f:
    word_list = f.readlines()
    word = random.choice(word_list).split(',')[0]
with open('full_word_list.txt') as f2:
    guess_list = f2.readlines()
    guess_list = [x.split(',')[0] for x in guess_list]

# UI/UX with Tkinter

KEYBOARD_LAYOUT = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                   'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'Enter', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Clear']
alphabet = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
            'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
            'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
# Colour
BKGD = "#FFFFFF"
YELLOW = "#c9b458"
WHITE = "#FFFFFF"
GREEN = "#538d4e"
LIGHTGREY = "#d8d8d8"
GREY = "#939598"
DARKGREY = "#2A2A2A"
BLACK = "#212121"

d = enchant.Dict("en_US")
checklist = [''] * 5
guess_labels = []
keyboard_buttons = []
num, attempt = 0, 0


# Input letters
def key_input(letter):
    global num
    if len("".join(checklist)) == 5:
        pass
    else:
        guess_labels[num].config(text=letter)
        checklist[num % 5] = letter
        num += 1

    # Lock to 5-letter word
    if num >= ((attempt + 1) * 5):
        for i in range(28):
            if i != 20 and i != 27:
                keyboard_buttons[i].config(state=DISABLED)


# Enter
def validate_guess(checklist, word):
    global attempt
    result = False
    guess = "".join(checklist)
    if len(guess) == 5:
        if d.check(guess) or guess in guess_list:
            for i in range(5):
                if guess[i] == word[i]:
                    guess_labels[i + 5 * attempt].config(bg=GREEN, fg=WHITE)
                    alphabet[guess[i]] += 1000
                elif guess[i] in word:
                    guess_labels[i + 5 * attempt].config(bg=YELLOW, fg=WHITE)
                    alphabet[guess[i]] += 100
                else:
                    guess_labels[i + 5 * attempt].config(bg=GREY, fg=WHITE)
                    alphabet[guess[i]] += 1
            attempt += 1
            checklist[0:5] = [''] * 5
        else:
            messagebox.showwarning("Invalid", "This word is invalid!")
    else:
        messagebox.showwarning("Warning", "Please enter a 5-letter word.")

    # Lock to 5-letter word
    for i in range(28):
        keyboard_buttons[i].config(state=NORMAL)

    for btn in keyboard_buttons:
        if btn.cget("text") == "Enter" or btn.cget("text") == "Clear":
            continue
        elif alphabet[btn.cget("text")] >= 1000:
            btn.config(bg=GREEN, fg=WHITE)
        elif alphabet[btn.cget("text")] >= 100:
            btn.config(bg=YELLOW, fg=WHITE)
        elif alphabet[btn.cget("text")] >= 1:
            btn.config(bg=GREY, fg=WHITE)

    if guess == word:
        pygame.mixer.music.load("win.mp3")
        result = True
    elif attempt == 6:
        result = True
        pygame.mixer.music.load("lost.mp3")

    if result:
        print(word)
        for i in range(28):
            keyboard_buttons[i].config(state=DISABLED)
        pygame.mixer.music.play()
        window.bind('a', lambda event: None)
        window.bind('b', lambda event: None)
        window.bind('c', lambda event: None)
        window.bind('d', lambda event: None)
        window.bind('e', lambda event: None)
        window.bind('f', lambda event: None)
        window.bind('g', lambda event: None)
        window.bind('h', lambda event: None)
        window.bind('i', lambda event: None)
        window.bind('j', lambda event: None)
        window.bind('k', lambda event: None)
        window.bind('l', lambda event: None)
        window.bind('m', lambda event: None)
        window.bind('n', lambda event: None)
        window.bind('o', lambda event: None)
        window.bind('p', lambda event: None)
        window.bind('q', lambda event: None)
        window.bind('r', lambda event: None)
        window.bind('s', lambda event: None)
        window.bind('t', lambda event: None)
        window.bind('u', lambda event: None)
        window.bind('v', lambda event: None)
        window.bind('w', lambda event: None)
        window.bind('x', lambda event: None)
        window.bind('y', lambda event: None)
        window.bind('z', lambda event: None)
        window.bind('<Return>', lambda event: None)
        window.bind('<Delete>', lambda event: None)


# Clear
def clear(checklist):
    global num
    length = len("".join(checklist))
    checklist[0:5] = [''] * 5
    num -= length
    for i in range(length):
        guess_labels[num+i].config(text='')
    # Lock to 5-letter word
    for i in range(28):
        keyboard_buttons[i].config(state=NORMAL)


def GuessBox():
    box = Label(window, text="", fg=BLACK, bg=BKGD, font=("Verdana", 18, "bold"), borderwidth=4,
                relief="ridge", padx=15, pady=10, width=1)
    return box


def SpaceBox():
    box = Label(window, text="", bg=BKGD, font=("Verdana", 2), padx=1, pady=0)
    return box


def Keyboard():
    box = Button(window, text="", bg=LIGHTGREY, font=("Arial", 12, "bold"), padx=5, pady=0, width=1, height=2)
    return box


window = Tk()
window.title("Wordle")
window.config(padx=50, pady=50, bg=BKGD)

# Create Title
title = Label(window, text="WORDLE", fg=DARKGREY, bg=BKGD, font=("Arial", 48, "bold"))
title.grid(column=0, row=0, columnspan=10)

# Space in between
spacer_1 = Label(window, bg=BKGD).grid(column=0, row=1, columnspan=10)
spacer_2 = Label(window, bg=BKGD).grid(column=0, row=15, columnspan=10)

# Create guess box
column, row = 0, 2
for i in range(60):
    if row % 2 == 0:
        space_box = SpaceBox()
        space_box.grid(column=column * 2, row=row)
    else:
        guess_box = GuessBox()
        guess_box.grid(column=column * 2, row=row, columnspan=2)
        guess_labels.append(guess_box)

    if column == 4:
        row += 1
        column = 0
    else:
        column += 1

# Create keyboard
column, row = 0, 16
for i in range(28):
    button = Keyboard()
    button.config(text=KEYBOARD_LAYOUT[i])
    keyboard_buttons.append(button)
    if i == 20 or i == 27:
        button.config(width=4)
        button.grid(column=column, row=row, columnspan=2)
        column += 1
    else:
        button.grid(column=column, row=row)

    if column == 9:
        row += 1
        column = 0
    else:
        column += 1

# Keyboard buttons functions
keyboard_buttons[0].config(command=lambda: key_input('A'))
keyboard_buttons[1].config(command=lambda: key_input('B'))
keyboard_buttons[2].config(command=lambda: key_input('C'))
keyboard_buttons[3].config(command=lambda: key_input('D'))
keyboard_buttons[4].config(command=lambda: key_input('E'))
keyboard_buttons[5].config(command=lambda: key_input('F'))
keyboard_buttons[6].config(command=lambda: key_input('G'))
keyboard_buttons[7].config(command=lambda: key_input('H'))
keyboard_buttons[8].config(command=lambda: key_input('I'))
keyboard_buttons[9].config(command=lambda: key_input('J'))
keyboard_buttons[10].config(command=lambda: key_input('K'))
keyboard_buttons[11].config(command=lambda: key_input('L'))
keyboard_buttons[12].config(command=lambda: key_input('M'))
keyboard_buttons[13].config(command=lambda: key_input('N'))
keyboard_buttons[14].config(command=lambda: key_input('O'))
keyboard_buttons[15].config(command=lambda: key_input('P'))
keyboard_buttons[16].config(command=lambda: key_input('Q'))
keyboard_buttons[17].config(command=lambda: key_input('R'))
keyboard_buttons[18].config(command=lambda: key_input('S'))
keyboard_buttons[19].config(command=lambda: key_input('T'))
keyboard_buttons[20].config(command=lambda: validate_guess(checklist, word))  # Enter
keyboard_buttons[21].config(command=lambda: key_input('U'))
keyboard_buttons[22].config(command=lambda: key_input('V'))
keyboard_buttons[23].config(command=lambda: key_input('W'))
keyboard_buttons[24].config(command=lambda: key_input('X'))
keyboard_buttons[25].config(command=lambda: key_input('Y'))
keyboard_buttons[26].config(command=lambda: key_input('Z'))
keyboard_buttons[27].config(command=lambda: clear(checklist))  # Clear

# Support keyboard
window.bind('a', lambda event: key_input('A'))
window.bind('b', lambda event: key_input('B'))
window.bind('c', lambda event: key_input('C'))
window.bind('d', lambda event: key_input('D'))
window.bind('e', lambda event: key_input('E'))
window.bind('f', lambda event: key_input('F'))
window.bind('g', lambda event: key_input('G'))
window.bind('h', lambda event: key_input('H'))
window.bind('i', lambda event: key_input('I'))
window.bind('j', lambda event: key_input('J'))
window.bind('k', lambda event: key_input('K'))
window.bind('l', lambda event: key_input('L'))
window.bind('m', lambda event: key_input('M'))
window.bind('n', lambda event: key_input('N'))
window.bind('o', lambda event: key_input('O'))
window.bind('p', lambda event: key_input('P'))
window.bind('q', lambda event: key_input('Q'))
window.bind('r', lambda event: key_input('R'))
window.bind('s', lambda event: key_input('S'))
window.bind('t', lambda event: key_input('T'))
window.bind('u', lambda event: key_input('U'))
window.bind('v', lambda event: key_input('V'))
window.bind('w', lambda event: key_input('W'))
window.bind('x', lambda event: key_input('X'))
window.bind('y', lambda event: key_input('Y'))
window.bind('z', lambda event: key_input('Z'))
window.bind('<Return>', lambda event: validate_guess(checklist, word))
window.bind('<Delete>', lambda event: clear(checklist))

window.mainloop()
