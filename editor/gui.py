
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import threading
import os
from PIL import Image, ImageTk
from conf import ASSETS_DIR
from tkinter import filedialog
from app import run

# Function for opening the
# file explorer window
fileName = None
dirName = None
window = Tk()


def browseDir():
    global dirName
    dirName = filedialog.askdirectory(initialdir="/",
                                      title="Select a Folder",
                                      )
    print(dirName)

    # Change label contents


def browseFiles():
    global fileName
    fileName = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Audio files",
                                                      "*.mp3"),
                                                     ("all files",
                                                      "*.*")))
    print(fileName)


def start_edit():
    print('Works')
    t1 = threading.Thread(target=run(dirName, fileName, bar))
    t1.start()
    # Change label contents

# Create the root window


# Set window title
window.title('AiRoll')

# Set window size
window.geometry("690x360")

window.resizable(0, 0)

# Set window background color
window.config(background="#871719")

# Create a File Explorer label

button_load_movies = Button(
    window,
    text="Load Movies",
    command=browseDir,
    bg='#871719',
    borderwidth=0,
    cursor='hand2')

button_select_audio = Button(
    window,
    text="Select Audio",
    command=browseFiles,
    bg='#871719',
    borderwidth=0,
    cursor='hand2')

button_action = Button(
    window,
    text="Action",
    command=lambda: threading.Thread(
        target=start_edit).start(),
    bg='#871719',
    borderwidth=0,
    cursor='hand2')


claps_img = Image.open(os.path.join(ASSETS_DIR, 'claps.png'))
claps_img = ImageTk.PhotoImage(claps_img)
claps_label = Label(image=claps_img)
claps_label.image = claps_img
claps_label.config(bg='#871719')

popcorn_img = Image.open(os.path.join(ASSETS_DIR, 'popcorn.png'))
popcorn_img = ImageTk.PhotoImage(popcorn_img)
popcorn_label = Label(image=popcorn_img)
popcorn_img.image = popcorn_img
popcorn_label.config(bg='#871719')

ticket_img = Image.open(os.path.join(ASSETS_DIR, 'ticket.png'))
ticket_img = ImageTk.PhotoImage(ticket_img)
ticket_label = Label(image=ticket_img)
ticket_img.image = popcorn_img
ticket_label.config(bg='#871719')

load_movies_img = PhotoImage(file=os.path.join(ASSETS_DIR, 'load_movies.png'))
button_load_movies.config(image=load_movies_img, activebackground='#871719')

select_audio_img = PhotoImage(
    file=os.path.join(
        ASSETS_DIR,
        'select_audio.png'))
button_select_audio.config(image=select_audio_img, activebackground='#871719')

action_img = PhotoImage(file=os.path.join(ASSETS_DIR, 'action.png'))
button_action.config(image=action_img, activebackground='#871719')


style = ttk.Style()
style.theme_use('default')
style.configure(
    "grey.Horizontal.TProgressbar",
    background='#FFF200',
    borderwidth=0)
bar = Progressbar(window, length=200, style='grey.Horizontal.TProgressbar')
bar['value'] = 0

# c1 = Checkbutton(text = "Proxy Mode", onvalue = 1, offvalue = 0, height=1, width = 20)
# c1.config(activebackground='#871719')

# c2 = Checkbutton(text = "RAM Mode", onvalue = 1, offvalue = 0, height=1, width = 20)
# c2.config(activebackground='#871719')

claps_label.grid(column=0, row=1)
popcorn_label.grid(column=1, row=1)
ticket_label.grid(column=2, row=1)

button_load_movies.grid(column=0, row=2)
button_select_audio.grid(column=1, row=2)
button_action.grid(column=2, row=2)
bar.grid(column=1, row=3)
# c1.grid(column=0, row = 4)
# c2.grid(column=1, row = 4)



# Let the window wait for any events
window.mainloop()
