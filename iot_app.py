import glob
import json
import socket
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

#returns list of files 
def load_apps_from_directory(filepath, master_widget, editor, set_file_path):
    app_widgets = []

    json_files = [x for x in glob.glob(filepath + "/*") if x.endswith(".json")]
    
    for file_path in json_files:
        temp_frame = tk.Frame(master_widget)
        
        """
        #pack the image first
        app_img_array = _load_numpy_image(file_path)
        app_img = ImageTk.PhotoImage(image=Image.fromarray((app_img_array).astype(np.uint8)))
        
        canvas = tk.Canvas(temp_frame, width=50, height=50)
        canvas.pack(side=tk.LEFT)
        canvas.create_image(20, 20, anchor="nw", image=app_img)
        """
        
        temp_label = tk.Label(temp_frame, text=file_path[file_path.rfind("/") + 1:])
        temp_label.bind("<Button-1>", lambda e: _open_app(editor, file_path, set_file_path))
        temp_label.pack(side=tk.LEFT)
        app_widgets.append(temp_frame)
    
    for widget in app_widgets:
        widget.pack()
        
#replaces editor text, and sets the currently opened file to be this apps save file path.
def _open_app(editor, new_file_path, set_file_path):
    _replace_editor_text(editor, load_recipe_code_from_file(new_file_path))
    set_file_path(new_file_path)
    
#replaces the text in the editor with the given text
def _replace_editor_text(editor, text):
    editor.delete("1.0", tk.END)
    editor.insert("1.0", text)
        
#get numpy array from json file
def _load_numpy_image(filepath):
    img_data = np.array([])
    with open(filepath) as f:
        json_obj = json.load(f)
        img_data = np.fromstring(json_obj["image_data"], dtype=np.uint8)
    return img_data

def save_app_to_file(filepath, app_string):
    pass

#function that returns string of the code for the app that is in this JSON file
def load_python_code_from_file(filepath):
    with open(filepath, "r") as f:
        json_obj = json.load(f)
        code = json_obj["code"]
        return code

def load_recipe_code_from_file(filepath):
    with open(filepath, "r") as f:
        json_obj = json.load(f)
        return json_obj["recipe_code"]
    