import json
import socket 
import struct
import threading

#threading subclass to continually run in background
#and place 
class TweetThread(threading.Thread):
    def __init__(self, tweet_list):
        threading.Thread.__init__(self)
        self.tweet_list = tweet_list

    #this is what the thread does when it starts
    #infinite loop, keeps putting json dicts of tweets
    #into the queue which will be consumed by the
    #main thread, this works because queues are thread-safe
    #in python
    def run(self):
        
        MCAST_GRP = '232.1.1.1'
        MCAST_PORT = 1235

        #setup socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        #set of the tweets that we have seen so if we get them again just ignore
        seen = set()

        while True:
            json_dat = {}
            dat = []
            try:
                dat = sock.recv(10240)
                
                if(dat in seen):
                    continue
                
                json_dat = json.loads(dat)
                self.tweet_list.append(json_dat)
                seen.add(dat)
                print("adding to tweeet list")
            except ValueError:
                print(":: Error! Invalid JSON. skipping tweet.......")

