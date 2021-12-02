import tkinter as tk
from tkinter.constants import W

#takes as input a list of json dicts describing tweets and
#creates frame with the service name and pack it on the services tab
def load_services_from_tweets(tweet_list, master_widget):
    
    #erase the old frames first!!!
    for widget in master_widget.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    
    frames = []
    
    print(f"size of tweet_list: {len(tweet_list)}")
    print(tweet_list)

    for service_dict in [x for x in tweet_list if x["Tweet Type"] == "Service"]:
        temp_frame = tk.Frame(master_widget)
        temp_label = tk.Label(temp_frame, text=service_dict["Name"] + " - " + service_dict["Thing ID"])
        temp_label.pack(side=tk.LEFT)
        frames.append(temp_frame)
        
    for frame in frames:
        frame.pack()
    
    master_widget.after(5000, lambda: load_services_from_tweets(tweet_list, master_widget))
