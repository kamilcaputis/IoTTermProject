import tkinter as tk
from tkinter.constants import W

#takes as input a list of json dicts describing tweets and
#creates frame with the service name and pack it on the services tab
def load_services_from_tweets(tweet_list, master_widget):
    
    #erase the old frames first!!!
    for widget in master_widget.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    
    #only pack frames that are from a Thing ID that is selected in the selection box
    selection_box = None
    for widget in master_widget.winfo_children():
        if isinstance(widget, tk.Listbox):
            selection_box = widget
            break
    
    selected_services = [selection_box.get(x) for x in selection_box.curselection()]
    frames = []
    
    #print(f"size of tweet_list: {len(tweet_list)}")
    #print(tweet_list)

    for service_dict in [x for x in tweet_list if x["Tweet Type"] == "Service" and x["Thing ID"] in selected_services]:
        temp_frame = tk.Frame(master_widget)
        temp_label = tk.Label(temp_frame, text=service_dict["Name"] + " - " + service_dict["Thing ID"])
        temp_label.pack(side=tk.LEFT)
        frames.append(temp_frame)
        
    for frame in frames:
        frame.pack()
    
    master_widget.after(500, lambda: load_services_from_tweets(tweet_list, master_widget))

def load_thing_selection_filter_from_tweets(tweet_list, master_widget):
    
    selection_box = None

    for widget in master_widget.winfo_children():
        if isinstance(widget, tk.Listbox):
            selection_box = widget
    
    if selection_box == None:
        selection_box = tk.Listbox(master_widget, selectmode="multiple")
        selection_box.pack(padx=10, pady=10, fill="x", side=tk.TOP)
        
    thing_ids = set([x["Thing ID"] for x in tweet_list if x["Tweet Type"] == "Identity_Thing"])
    
    #get the entries in the selection_box
    entries_tuple = selection_box.get(0, selection_box.size() - 1 if selection_box.size() > 0 else None)
    
    for missing_entry in [thing_id for thing_id in thing_ids if not thing_id in entries_tuple]:
        selection_box.insert(tk.END, missing_entry)
        
    master_widget.after(5000, lambda: load_thing_selection_filter_from_tweets(tweet_list, master_widget))
        