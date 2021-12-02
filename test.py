import glob
import json
import socket
import codecs
from tkinter.constants import W
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

def _load_numpy_image(filepath):
    obj_text = codecs.open(filepath, 'r', encoding="utf-8").read()
    b_new = json.loads(obj_text)
    return np.array(b_new["image_data"])

root = tk.Tk()
root.geometry("200x200")
canvas = tk.Canvas(root, width=100, height=100)
canvas.pack()

app_img_array = _load_numpy_image("test.json")
app_img = ImageTk.PhotoImage(master=root, image=Image.fromarray((app_img_array).astype(np.uint8)))
canvas.create_image(100, 100, anchor="nw", image=app_img)


root.mainloop()