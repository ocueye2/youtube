import threading
from flask import render_template, Flask
import os
from mutagen import File
import pygame

app = Flask(__name__)

# Initialize global variables
music = ""
artist = ""

def musicscript():
    global music
    global artist
    pygame.mixer.init()
    music_folder = "E:\\stream scripts\\stream\\music"
    while True:
        songs = os.listdir(music_folder)
        for song in songs:
            path = os.path.join(music_folder, song)
            audio = File(path)
            if audio.tags:
                for tag, value in audio.tags.items():
                    if tag == "TIT2":
                        music = value.text[0] if isinstance(value.text, list) else value.text
                    elif tag == "TPE1":
                        artist = value.text[0] if isinstance(value.text, list) else value.text
            else:
                music = song
                artist = "Unknown Artist"
            print(f"Now playing: {music} by {artist}")
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

def web():
    app.run(port=8092)

@app.route("/")
def hello_world():
    return render_template('music.html', music=music, artist=artist)

# Create threads
mthred = threading.Thread(target=musicscript, )
webthred = threading.Thread(target=web, daemon=True)

# Start threads
mthred.start()
webthred.start()
