import tkinter as tk

#takes as input a list of json dicts describing tweets
#and creates frame with the service name and pack it on the services tab
def load_relationships_from_tweets(tweet_list, master_widget):

    #erase everything on the master widget first!!
    for widget in master_widget.winfo_children():
        widget.destroy()

    frames = []

    for relationship_dict in [x for x in tweet_list if x["Tweet Type"] == "Relationship"]:
        temp_frame = tk.Frame(master_widget)
        temp_label = tk.Label(temp_frame, text=relationship_dict["Name"])
        temp_label.pack(size=tk.LEFT)
        frames.append(temp_frame)
        
    for frame in frames:
        frame.pack()
        
    master_widget.after(5000, lambda: load_relationships_from_tweets(tweet_list, master_widget))