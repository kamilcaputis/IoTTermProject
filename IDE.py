import os
import json
import socket
import subprocess
from subprocess import check_output
import tkinter as tk
from tkinter import ttk
from listen import TweetThread
from iot_app import load_apps_from_directory, load_python_code_from_file, write_python_code
from iot_things import load_things_from_tweets
from iot_services import load_services_from_tweets, load_thing_selection_filter_from_tweets
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
        
    json_obj["recipe_code"] = code.strip()

    with open(path, "w") as file:
        json.dump(json_obj, file)

def save_as():
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'w') as file:
        code = editor.get('1.0', tk.END)
        file.write(code)
        set_file_path(path)


def activate():
    global file_path
    if file_path == '':
        save_prompt = tk.Toplevel()
        text = tk.Label(save_prompt, text='Please save your code')
        text.pack()
        return

    code = load_python_code_from_file(file_path)
    print(code)
    out = check_output(["python3", "-c", code])
    print(out)

    result_popup = tk.Toplevel(main_window)
    result_popup.geometry("500x500")

    result_popup.update_idletasks()

    result_text = tk.Label(master = result_popup, text = str(out).strip(), wraplength=result_popup.winfo_width() - 40)
    result_text.pack(side=tk.TOP)

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

    ti_sn_pairs = get_pairs(service_names)
    print(ti_sn_pairs)

    app_code = "import json\nimport socket\n"
    for pair in ti_sn_pairs:
        app_code += f"""t = {{ "Tweet Type" : "Service call", "Thing ID" : "{pair[0]}", "Space ID" : "Team16Smartspace", "Service Name" : "{pair[1]}", "Service Inputs" : "()"}}\ndata = json.dumps(t, indent=2)\ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\ntry:\n\ts.connect(("169.254.196.120", 6668))\n\ts.send(data.encode())\n\tresponse = s.recv(1024).decode("utf-8")\n\tjson_data = json.loads(response)\n\tprint(json_data)\nfinally:\n\ts.close()\n"""

    write_python_code(file_path, app_code)
    # clear_callback()
    # editor.insert("1.0", app_code)

def parse_service_names(code):

    retVal = []

    while "(" in code:
        startIndex = code.find('(')
        endIndex = code.find(')')
        token = code[startIndex + 1 :endIndex]
        retVal.append(token)
        code = code[endIndex + 1:]

    return retVal

def get_pairs(service_names):

    retVal = []

    for service_name in service_names:
        for tweet_dict in [x for x in tweet_list if x["Tweet Type"] == "Service"]:
            if tweet_dict["Name"] == service_name:
                retVal.append((tweet_dict["Thing ID"], service_name))
    
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
menu_bar.add_cascade(label='Application Manager', menu=file_menu)

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
filter_selection_label = tk.Label(services_tab, text="Filter By Thing ID", justify=tk.CENTER)
filter_selection_label.pack()
load_thing_selection_filter_from_tweets(tweet_list, services_tab)
service_list_label = tk.Label(services_tab, text="Service List:", justify=tk.CENTER)
service_list_label.pack()
load_services_from_tweets(tweet_list, services_tab, editor)

#things tab
load_things_from_tweets(tweet_list, things_tab)

#relationships tab
temp_frame = tk.Frame(relationships_tab)
temp_label = tk.Label(temp_frame, text="Temp Relationship")
temp_label.pack()
temp_frame.pack()
#load_relationships_from_tweets(tweet_list, relationships_tab)

# code_output = Text(master=recipe_tab, height=10)
# code_output.pack()

main_window.mainloop()
