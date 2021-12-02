import tkinter as tk

#takes as input a list of json dicts describing
def load_things_from_tweets(tweet_list, master_widget):
    
    #erase everything on the master widget first!!
    for widget in master_widget.winfo_children():
        widget.destroy()
    
    frames = []
    
    for thing_dict in [x for x in tweet_list if x["Tweet Type"] == "Identity_Thing"]:
        temp_frame = tk.Frame(master_widget)
        temp_label = tk.Label(temp_frame, text=thing_dict["Name"])
        temp_label.pack(side=tk.LEFT)
        frames.append(temp_frame)
        
    for frame in frames:
        frame.pack()
        
    master_widget.after(5000, lambda: load_things_from_tweets(tweet_list, master_widget))