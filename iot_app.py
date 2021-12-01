import glob
import socket
import tkinter as tk
from tkinter import ttk

#returns list of files 
def load_apps_from_directory(filepath, master_widget):
    app_widgets = []

    json_files = [x[x.rfind("/") + 1:] for x in glob.glob(filepath + "/*") if x.endswith(".json")]
    
    for file_name in json_files:
        app_widgets.append(tk.Label(master_widget, text=file_name))
    
    for widget in app_widgets:
        widget.pack()

def save_app_to_file(filepath, app_string):
    pass

def load_app_from_file(filepath):
    pass