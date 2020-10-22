from tkinter import *
from conf import DATASET_DIR
from pathlib import Path
import face_recognition
from PIL import ImageTk, Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True




def get_all_Images():
    images_paths = []
    for path in Path(DATASET_DIR).rglob('*.png'):
        images_paths.append(path)
        print(path)
    return images_paths


IMAGES_PATHS = get_all_Images()
INDEX = 0
X_SUB = 5
Y_SUB = 5
root = Tk()
root.title("Progam do sortowania Materiału treningowego -  Szymon Ruciński")
my_img = ImageTk.PhotoImage(Image.open(IMAGES_PATHS[1]))
my_label = Label(image=my_img)
my_label.pack()
my_label.grid(row=0, column=0, columnspan=6)
left_icon = PhotoImage(file="D:\\Programowanie\\AI\\scrapFrames\\assets_filterFrame\\left.png") 
right_icon = PhotoImage(file="D:\Programowanie\\AI\\scrapFrames\\assets_filterFrame\\right.png")

l_icon =  left_icon.subsample(X_SUB,Y_SUB)
r_icon = right_icon.subsample(X_SUB,Y_SUB)

def forward():
    global my_label
    global button_forward
    global my_img
    global INDEX

    my_label.grid_forget()
    my_img = ImageTk.PhotoImage(Image.open(IMAGES_PATHS[INDEX]))
    my_label = Label(image=my_img)
    my_label.grid(row=0, column=0, columnspan=6)
    INDEX = INDEX + 1

    if INDEX == len(IMAGES_PATHS)-1:
        button_forward = Button(root, image=r_icon, state=DISABLED)
    print(INDEX)
    print(IMAGES_PATHS[INDEX])



def backward():
    global my_label
    global button_back
    global my_img
    global INDEX

    if INDEX > 0:
        my_label.grid_forget()
        my_img = ImageTk.PhotoImage(Image.open(IMAGES_PATHS[INDEX]))
        my_label = Label(image=my_img)
        my_label.grid(row=0, column=0, columnspan=6)
        INDEX = INDEX-1

    if INDEX == 0:
        button_back = Button(root, text="<--", state=DISABLED)
        my_label.grid(row=0, column=0, columnspan=6)
    print(INDEX)


button_forward = Button(root, image=r_icon, pady=25, command=lambda: forward())
button_back = Button(root, image=l_icon, pady=25, command=lambda: backward())
button_back.grid(row=1, column=2)
button_forward.grid(row=1, column=3)

button_wide = Button(root, text="1. Wide shot", width = 25, height = 2)
button_close_up = Button(root, text="2. Close-up", width = 25, height = 2)
button_ex_close_up = Button(root, text="3. Extreme close-up", width = 25, height = 2)
button_long_shot = Button(root, text="4. Long shot", width = 25, height = 2)

button_wide.grid(row=2,pady=5, column=2)
button_close_up.grid(row=3, pady=10, column=2)
button_long_shot.grid(row=3, pady=10, column=3)
button_ex_close_up.grid(row=2, pady=10, column=3)

root.mainloop()





