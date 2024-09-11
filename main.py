import random
from random import randint
from tkinter import *

import pandas
from pandas import read_csv
import time

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
flash_card_words = {}

# ---------------------------- CREATE NEW FLASH CARD ------------------------------- #
try:
    data = read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    flash_card_words = original_data.to_dict(orient="records")
else:
    flash_card_words = data.to_dict(orient="records")



def next_flash_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(flash_card_words)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card['French'], fill="black")
    canvas.itemconfig(canvas_img, image=canvas_bg_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card['English'], fill="white")
    canvas.itemconfig(canvas_img, image=new_image)

def is_known():
    flash_card_words.remove(current_card)
    next_flash_card()

    data = pandas.DataFrame(flash_card_words)
    data.to_csv("data/words_to_learn.csv", index= False)
    next_flash_card( )
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

flip_timer = window.after(3000, func=flip_card)

# Canvas
canvas = Canvas(width=800, height=526)
canvas_bg_img = PhotoImage(file="./images/card_front.png")
new_image = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=canvas_bg_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# button
button_right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=button_right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

button_wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=button_wrong_img, highlightthickness=0, command=flip_card)
wrong_button.grid(row=1, column=0)


next_flash_card()

window.mainloop()