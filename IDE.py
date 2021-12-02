import os
import json
import socket
import subprocess
import tkinter as tk
from tkinter import ttk
from listen import TweetThread
from iot_app import load_apps_from_directory, write_python_code
from iot_things import load_things_from_tweets
from iot_services import load_services_from_tweets
from iot_relationships import load_relationships_from_tweets
from tkinter.filedialog import asksaveasfilename, askopenfilename, askdirectory

#queue to hold tweet json's
tweet_list = []

#start the thread, it will place its output
# in this queue for us to consume
tweet_thread = TweetThread(tweet_list)
tweet_thread.start()

main_window = tk.Tk()
main_window.title('Group 16 IDE')
file_path = ''

# this is a stringvar type that is used by Tkinter
current_working_directory = os.getcwd()

def set_file_path(path):
    global file_path
    file_path = path

def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', tk.END)
        editor.insert('1.0', code)
        set_file_path(path)

def save():
    json_obj = {}
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    
    code = editor.get('1.0', tk.END)
        
    with open(path, 'r') as file:
        set_file_path(path)
        json_obj = json.loads(file.read())
        
    json_obj["recipe_code"] = code

    with open(path, "w") as file:
        json_obj = json.dump(json_obj, file)

def save_as():
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'w') as file:
        code = editor.get('1.0', tk.END)
        file.write(code)
        set_file_path(path)


def activate():
    if file_path == '':
        save_prompt = tk.Toplevel()
        text = tk.Label(save_prompt, text='Please save your code')
        text.pack()
        return
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    tk.code_output.insert(tk.END, output)
    tk.code_output.insert(tk.END,  error)

def stop():
  print("hi")

def delete():
  global file_path
  if os.path.exists(file_path):
    os.remove(file_path)
    editor.delete('1.0', tk.END)
    file_path = ''
  else:
    editor.delete('1.0', tk.END)
    print("The file does not exist")

#callbacks for buttons on the recipe window
def finalize_callback():
    global file_path

    editor_code = editor.get("1.0", tk.END)
    service_names = parse_service_names(editor_code)
    print(service_names)

    thing_ids = get_thing_ids(service_names)
    print(thing_ids)

    # app_code = f"""
    # t = {{ "Tweet Type" : "Service call", "Thing ID" : {thingId}, "Space ID" : "Team16Smartspace", "Service Name" : {serviceName}, "Service Inputs" : "(0)"
    #     }}
    # data = json.dumps(t, indent=2)
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # try: 
    #     s.connect(("192.168.137.160", 6668))
    #     s.send(data.encode())
    #     response = s.recv(1024).decode("utf-8")
    #     json_data = json.loads(response)
    #     print(json_data)
    # finally:
    #     s.close()"""
    #write_python_code(file_path, app_code)

def parse_service_names(code):

    retVal = []

    while "(" in code:
        startIndex = code.find('(')
        endIndex = code.find(')')
        token = code[startIndex + 1 :endIndex]
        retVal.append(token)
        code = code[endIndex + 1:]

    return retVal

def get_thing_ids(service_names):

    retVal = []

    for service_name in service_names:
        for tweet_dict in [x for x in tweet_list if x["Tweet Type"] == "Service"]:
            if tweet_dict["Name"] == service_name:
                retVal.append(tweet_dict["Thing ID"])
    
    return retVal


def clear_callback():
    editor.delete('1.0', tk.END)

#This function is called when the recipe option is selected from the overhead menu
def recipe():
    recipe_window = tk.Toplevel()
    recipe_window.title("Recipe Tab")
    recipe_window.geometry('500x500')
    
    #add finalize and clear button
    finalize_btn = tk.Button(recipe_window, text="finalize", command=finalize_callback)
    clear_btn = tk.Button(recipe_window, text="clear", command=clear_callback)
    
    text = tk.Label(recipe_window, text="This is the recipe tab")
    
    #pack them into the recipe_window window
    text.pack()
    finalize_btn.pack()
    clear_btn.pack()
            
def set_current_working_directory():
    chosen_directory = askdirectory()

    if chosen_directory == '' or chosen_directory == None:
        return

    global cwd_label
    cwd_label.configure(text=f"Current Directory: {chosen_directory}")

menu_bar = tk.Menu(main_window)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Upload', command=open_file)
file_menu.add_command(label='Activate', command=activate)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Stop', command=stop)
file_menu.add_command(label='Delete', command=delete)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='Application Manager', menu=file_menu)

run_bar = tk.Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=activate)
menu_bar.add_cascade(label='Run', menu=run_bar)

main_window.config(menu=menu_bar)

left_frame = ttk.Frame(main_window)
right_frame = ttk.Frame(main_window)

left_frame.pack(side=tk.LEFT, fill="both")
right_frame.pack(side=tk.LEFT, fill="both", expand=True)
tabControl = ttk.Notebook(left_frame, width=main_window.winfo_width())
things_tab = ttk.Frame(tabControl)
apps_tab = ttk.Frame(tabControl)
services_tab = ttk.Frame(tabControl)
relationships_tab = ttk.Frame(tabControl)
tabControl.add(apps_tab, text="Apps")
tabControl.add(services_tab, text="Services")
tabControl.add(things_tab, text="Things")
tabControl.add(relationships_tab, text="Relationships")
tabControl.pack(expand=True, fill="both")

recipe_label = ttk.Label(right_frame, text="Recipe")
recipe_label.pack()

editor = tk.Text(right_frame)
editor.pack(fill="both", expand=True)

editor_bottom_frame = ttk.Frame(right_frame)
finalize_btn = ttk.Button(editor_bottom_frame, text="finalize", command=finalize_callback)
clear_btn = ttk.Button(editor_bottom_frame, text="clear", command=clear_callback)
finalize_btn.pack(side=tk.LEFT, expand=True, fill="x")
clear_btn.pack(side=tk.LEFT, expand=True, fill="x")

editor_bottom_frame.pack(side=tk.BOTTOM, fill="x", expand=False)

#update the idle-tasks so that the wraplength will work
main_window.update_idletasks()

#apps_tab
cwd_label = tk.Label(apps_tab, text=f"Current Directory: {current_working_directory}", justify=tk.CENTER, wraplength=left_frame.winfo_width() - 40)
cwd_button =tk.Button(apps_tab, text="Change Directory", command=set_current_working_directory)
cwd_label.pack()
cwd_button.pack(side=tk.BOTTOM)

#place widgets for apps in the current directory into the apps tab
load_apps_from_directory(current_working_directory, apps_tab, editor, set_file_path)

#services tab
# load_thing_filter_selection_from_tweets(tweet_list, services_tab)
load_services_from_tweets(tweet_list, services_tab)

#things tab
load_things_from_tweets(tweet_list, things_tab)

#relationships tab
load_relationships_from_tweets(tweet_list, relationships_tab)

main_window.mainloop()