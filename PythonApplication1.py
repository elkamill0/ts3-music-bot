import sys
import time
import vlc
import pafy
from pafy import backend_shared
import logging
import watchdog
import watchdog.observers
from watchdog.observers import Observer
import watchdog.events
from watchdog.events import LoggingEventHandler
import queue

global q
q = queue.Queue()
t=0
result = -1
is_playing = False

class Event(watchdog.events.LoggingEventHandler):
    def on_modified(self, event):

        x = []
        x = url1.split()
        command = x[2]
        
        if command == "play":
            url = x[3]
            split_url(url)
        elif command == "playlist":
            url = x[3]
            split_url1(url)
        elif command == "list":
            print(list(q.queue))
        else:
            return 0

def play(url):
    global is_playing
    is_playing = True
    video = pafy.new(url)
    best = video.getbestaudio()
    playurl = best.url
    global player
    player = vlc.MediaPlayer(playurl)
    player.set_mrl(playurl, ":no-video")
    player.play()
    
    global t
    t=0

    print("played!")
    dur = video.duration
    convert(dur)
    print(list(q.queue))
    
def convert(dur):
    (h, m, s) = dur.split(":")
    global result
    result = int(h) * 3600 + int(m) * 60 + int(s)
    print(result)
    
def nothing():
    return



def split_url(url):
    if "[URL]" not in url:
        print("no")
        queue_add()
        if is_playing == False:
                play(url)
        elif is_playing == True:
            q.put(url)
            #queue_add()
            play(url)
    elif "[URL]" in url:
        print("yes")
        url = url.replace("[URL]", "")
        url = url.replace("[/URL]", "")
        if len(url) == 43:
            if is_playing == False:
                play(url)
                print("the first option")
                q.put(url)
            elif is_playing == True:
                print("the second option")
                q.put(url)
                print(list(q.queue))
                #queue_add()
                play(url)

def queue_add():
    if q.empty() == True:
        print("nothing 1")
        nothing()
    else:
        if q.empty() == True:
            print("nothing 2")
            nothing()
        else:
            play(q.queue[0])
            print("play queue!")
            q.get()
            
filepath = "C:\\Users\\Kamil\\AppData\\Roaming\\TS3Client\\chats\\SmtkR2ZVVXZaZHgwdmdqMVlWeFBnSERtSmU4PQ=="
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = filepath
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            if result == t:
                print("stopped")
                is_playing = False
                
                result = -1
                t=0
                #queue_add()

            time.sleep(1)
            t = t + 1

            #print(t)
            #print("result: ", result)
            print("is_playing = ", is_playing)
            f = open("C:\\Users\\Kamil\\AppData\\Roaming\\TS3Client\\chats\\SmtkR2ZVVXZaZHgwdmdqMVlWeFBnSERtSmU4PQ==\\channel.txt", "r")
            for url1 in f:  
                pass
            f.close()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
